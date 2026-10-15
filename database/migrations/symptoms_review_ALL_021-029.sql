-- symptoms_review_ALL_021-029.sql - all nine symptom review migrations in one file.
-- Safe even if you already ran 021: every part only adds what is missing.

-- 021_symptoms_review_01.sql  -  symptom review, session 01: 10 symptoms
-- Adds only: longer descriptions, extra causes, red flags, references and disease links.
-- Nothing is deleted or replaced. Safe to run twice (every insert is guarded).
-- A description is only extended if it is still the exported text (your own edits are kept).

begin;

-- ================================================ sym_abdominal_pain  (Abdominal pain)
update public.symptoms set description = 'Abdominal pain is pain felt anywhere between the chest and the groin, arising from abdominal organs, the abdominal wall or referred from outside the abdomen. Its location, character, timing and associated features guide the differential, and severity does not always reflect seriousness. Visceral pain is dull and poorly localised (epigastric for the stomach and duodenum, periumbilical for the small bowel and appendix, suprapubic for the colon), whereas pain from an inflamed parietal peritoneum is sharp and well localised; appendicitis classically starts periumbilically and migrates to the right lower quadrant. Causes outside the abdomen, such as myocardial infarction, lower-lobe pneumonia and diabetic ketoacidosis, must not be missed.', updated_at = now()
where id = 'sym_abdominal_pain' and description = 'Abdominal pain is pain felt anywhere between the chest and the groin, arising from abdominal organs, the abdominal wall or referred from outside the abdomen. Its location, character, timing and associated features guide the differential, and severity does not always reflect seriousness.';
update public.symptoms set tags = tags || array['acute abdomen']::text[]
where id = 'sym_abdominal_pain' and not (tags @> array['acute abdomen']::text[]);
update public.symptoms set source_attribution = source_attribution || '; StatPearls - Acute Abdomen'
where id = 'sym_abdominal_pain' and position('StatPearls - Acute Abdomen' in source_attribution) = 0;
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_abdominal_pain', 'Intestinal obstruction', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_abdominal_pain'), 0)
where exists (select 1 from public.symptoms where id = 'sym_abdominal_pain')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_abdominal_pain' and content = 'Intestinal obstruction');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_abdominal_pain', 'Acute pancreatitis', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_abdominal_pain'), 0)
where exists (select 1 from public.symptoms where id = 'sym_abdominal_pain')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_abdominal_pain' and content = 'Acute pancreatitis');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_abdominal_pain', 'Ectopic pregnancy and other gynecologic causes (ovarian torsion, pelvic inflammatory disease)', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_abdominal_pain'), 0)
where exists (select 1 from public.symptoms where id = 'sym_abdominal_pain')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_abdominal_pain' and content = 'Ectopic pregnancy and other gynecologic causes (ovarian torsion, pelvic inflammatory disease)');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_abdominal_pain', 'Mesenteric ischemia or abdominal aortic aneurysm (older adults)', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_abdominal_pain'), 0)
where exists (select 1 from public.symptoms where id = 'sym_abdominal_pain')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_abdominal_pain' and content = 'Mesenteric ischemia or abdominal aortic aneurysm (older adults)');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_abdominal_pain', 'Acute hepatitis', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_abdominal_pain'), 0)
where exists (select 1 from public.symptoms where id = 'sym_abdominal_pain')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_abdominal_pain' and content = 'Acute hepatitis');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_abdominal_pain', 'Causes outside the abdomen: myocardial infarction, lower-lobe pneumonia, diabetic ketoacidosis', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_abdominal_pain'), 0)
where exists (select 1 from public.symptoms where id = 'sym_abdominal_pain')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_abdominal_pain' and content = 'Causes outside the abdomen: myocardial infarction, lower-lobe pneumonia, diabetic ketoacidosis');
insert into public.symptom_red_flags (symptom_id, content, position)
select 'sym_abdominal_pain', 'Pain out of proportion to examination findings in an older adult (possible mesenteric ischemia)', coalesce((select max(position) + 1 from public.symptom_red_flags where symptom_id = 'sym_abdominal_pain'), 0)
where exists (select 1 from public.symptoms where id = 'sym_abdominal_pain')
  and not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_abdominal_pain' and content = 'Pain out of proportion to examination findings in an older adult (possible mesenteric ischemia)');
insert into public.symptom_red_flags (symptom_id, content, position)
select 'sym_abdominal_pain', 'Missed period or positive pregnancy test with pain, bleeding or fainting (possible ectopic pregnancy)', coalesce((select max(position) + 1 from public.symptom_red_flags where symptom_id = 'sym_abdominal_pain'), 0)
where exists (select 1 from public.symptoms where id = 'sym_abdominal_pain')
  and not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_abdominal_pain' and content = 'Missed period or positive pregnancy test with pain, bleeding or fainting (possible ectopic pregnancy)');
insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select 'sym_abdominal_pain', 'StatPearls - Acute Abdomen', 'Kopitnik NL, Kashyap S, Dominique E. Acute Abdomen. [Updated 2025 Feb 15]. In: StatPearls [Internet]. Treasure Island (FL): StatPearls Publishing.', 'https://www.ncbi.nlm.nih.gov/books/NBK459328/', false, coalesce((select max(position) + 1 from public.symptom_references where symptom_id = 'sym_abdominal_pain'), 0)
where exists (select 1 from public.symptoms where id = 'sym_abdominal_pain')
  and not exists (select 1 from public.symptom_references where symptom_id = 'sym_abdominal_pain' and url = 'https://www.ncbi.nlm.nih.gov/books/NBK459328/');
insert into public.disease_symptoms (disease_id, symptom_id, typical_intensity, is_primary, weight_multiplier)
select 'hepatitis_a', 'sym_abdominal_pain', 5::smallint, false, 0.6::numeric
where exists (select 1 from public.diseases where id = 'hepatitis_a')
  and exists (select 1 from public.symptoms where id = 'sym_abdominal_pain')
  and not exists (select 1 from public.disease_symptoms where disease_id = 'hepatitis_a' and symptom_id = 'sym_abdominal_pain');
insert into public.disease_symptoms (disease_id, symptom_id, typical_intensity, is_primary, weight_multiplier)
select 'urinary_tract_infection', 'sym_abdominal_pain', 4::smallint, false, 0.5::numeric
where exists (select 1 from public.diseases where id = 'urinary_tract_infection')
  and exists (select 1 from public.symptoms where id = 'sym_abdominal_pain')
  and not exists (select 1 from public.disease_symptoms where disease_id = 'urinary_tract_infection' and symptom_id = 'sym_abdominal_pain');

-- ================================================ sym_abdominal_swelling  (Abdominal swelling (distension or ascites))
update public.symptoms set description = 'Abdominal swelling is enlargement of the abdomen from gas, fluid, organ enlargement or masses. Ascites, free fluid in the peritoneal cavity, most often results from portal hypertension and low serum albumin in chronic liver disease, including the periportal fibrosis of chronic Schistosoma japonicum infection, and is suggested by shifting dullness and a fluid wave. The classic causes of a swollen abdomen are remembered as fluid, flatus, fat, fetus and feces. When ascites is tapped, a serum-ascites albumin gradient (SAAG) of 1.1 g/dL or more points to portal hypertension (cirrhosis, heart failure), while a lower gradient suggests peritoneal causes such as tuberculosis or malignancy.', updated_at = now()
where id = 'sym_abdominal_swelling' and description = 'Abdominal swelling is enlargement of the abdomen from gas, fluid, organ enlargement or masses. Ascites, free fluid in the peritoneal cavity, most often results from portal hypertension and low serum albumin in chronic liver disease, including the periportal fibrosis of chronic Schistosoma japonicum infection, and is suggested by shifting dullness and a fluid wave.';
update public.symptoms set tags = tags || array['paracentesis']::text[]
where id = 'sym_abdominal_swelling' and not (tags @> array['paracentesis']::text[]);
update public.symptoms set source_attribution = source_attribution || '; StatPearls - Ascites'
where id = 'sym_abdominal_swelling' and position('StatPearls - Ascites' in source_attribution) = 0;
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_abdominal_swelling', 'Peritoneal tuberculosis', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_abdominal_swelling'), 0)
where exists (select 1 from public.symptoms where id = 'sym_abdominal_swelling')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_abdominal_swelling' and content = 'Peritoneal tuberculosis');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_abdominal_swelling', 'Constipation and fecal loading', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_abdominal_swelling'), 0)
where exists (select 1 from public.symptoms where id = 'sym_abdominal_swelling')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_abdominal_swelling' and content = 'Constipation and fecal loading');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_abdominal_swelling', 'Pancreatic ascites after pancreatitis', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_abdominal_swelling'), 0)
where exists (select 1 from public.symptoms where id = 'sym_abdominal_swelling')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_abdominal_swelling' and content = 'Pancreatic ascites after pancreatitis');
insert into public.symptom_red_flags (symptom_id, content, position)
select 'sym_abdominal_swelling', 'Rapid increase in abdominal girth or new ascites in a patient with known liver disease', coalesce((select max(position) + 1 from public.symptom_red_flags where symptom_id = 'sym_abdominal_swelling'), 0)
where exists (select 1 from public.symptoms where id = 'sym_abdominal_swelling')
  and not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_abdominal_swelling' and content = 'Rapid increase in abdominal girth or new ascites in a patient with known liver disease');
insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select 'sym_abdominal_swelling', 'StatPearls - Ascites', 'Goosenberg E, Kudaravalli P, Samant H. Ascites. [Updated 2025 Nov 30]. In: StatPearls [Internet]. Treasure Island (FL): StatPearls Publishing.', 'https://www.ncbi.nlm.nih.gov/books/NBK470482/', false, coalesce((select max(position) + 1 from public.symptom_references where symptom_id = 'sym_abdominal_swelling'), 0)
where exists (select 1 from public.symptoms where id = 'sym_abdominal_swelling')
  and not exists (select 1 from public.symptom_references where symptom_id = 'sym_abdominal_swelling' and url = 'https://www.ncbi.nlm.nih.gov/books/NBK470482/');
insert into public.disease_symptoms (disease_id, symptom_id, typical_intensity, is_primary, weight_multiplier)
select 'heart_failure', 'sym_abdominal_swelling', 3::smallint, false, 0.5::numeric
where exists (select 1 from public.diseases where id = 'heart_failure')
  and exists (select 1 from public.symptoms where id = 'sym_abdominal_swelling')
  and not exists (select 1 from public.disease_symptoms where disease_id = 'heart_failure' and symptom_id = 'sym_abdominal_swelling');

-- ================================================ sym_regurgitation  (Acid regurgitation (sour fluid or food coming back up))
update public.symptoms set description = 'Effortless backflow of sour or bitter stomach contents into the throat or mouth, without the retching of vomiting. It is, with heartburn, one of the two typical symptoms of gastroesophageal reflux disease and is often worse after large meals, when bending over or when lying down. Unlike vomiting, it comes without nausea or forceful abdominal contraction. Regurgitation responds less well to acid-suppressing medicines than heartburn does, so persistent regurgitation on a proton pump inhibitor is a reason for further testing. In infants, effortless spitting up after feeds is common and usually physiological.', updated_at = now()
where id = 'sym_regurgitation' and description = 'Effortless backflow of sour or bitter stomach contents into the throat or mouth, without the retching of vomiting. It is, with heartburn, one of the two typical symptoms of gastroesophageal reflux disease and is often worse after large meals, when bending over or when lying down.';
update public.symptoms set tags = tags || array['infant reflux']::text[]
where id = 'sym_regurgitation' and not (tags @> array['infant reflux']::text[]);
update public.symptoms set source_attribution = source_attribution || '; ACG Clinical Guideline - GERD (2022)'
where id = 'sym_regurgitation' and position('ACG Clinical Guideline - GERD (2022)' in source_attribution) = 0;
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_regurgitation', 'Physiological reflux in infants', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_regurgitation'), 0)
where exists (select 1 from public.symptoms where id = 'sym_regurgitation')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_regurgitation' and content = 'Physiological reflux in infants');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_regurgitation', 'Esophageal stricture or Zenker''s diverticulum (undigested food, bad breath)', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_regurgitation'), 0)
where exists (select 1 from public.symptoms where id = 'sym_regurgitation')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_regurgitation' and content = 'Esophageal stricture or Zenker''s diverticulum (undigested food, bad breath)');
insert into public.symptom_red_flags (symptom_id, content, position)
select 'sym_regurgitation', 'Anemia or persistent vomiting', coalesce((select max(position) + 1 from public.symptom_red_flags where symptom_id = 'sym_regurgitation'), 0)
where exists (select 1 from public.symptoms where id = 'sym_regurgitation')
  and not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_regurgitation' and content = 'Anemia or persistent vomiting');
insert into public.symptom_red_flags (symptom_id, content, position)
select 'sym_regurgitation', 'Poor weight gain, forceful vomiting or feeding refusal in an infant', coalesce((select max(position) + 1 from public.symptom_red_flags where symptom_id = 'sym_regurgitation'), 0)
where exists (select 1 from public.symptoms where id = 'sym_regurgitation')
  and not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_regurgitation' and content = 'Poor weight gain, forceful vomiting or feeding refusal in an infant');
insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select 'sym_regurgitation', 'ACG Clinical Guideline - GERD (2022)', 'Katz PO, Dunbar KB, Schnoll-Sussman FH, Greer KB, Yadlapati R, Spechler SJ. ACG Clinical Guideline for the Diagnosis and Management of Gastroesophageal Reflux Disease. Am J Gastroenterol. 2022;117(1):27-56. doi:10.14309/ajg.0000000000001538', 'https://pubmed.ncbi.nlm.nih.gov/34807007/', false, coalesce((select max(position) + 1 from public.symptom_references where symptom_id = 'sym_regurgitation'), 0)
where exists (select 1 from public.symptoms where id = 'sym_regurgitation')
  and not exists (select 1 from public.symptom_references where symptom_id = 'sym_regurgitation' and url = 'https://pubmed.ncbi.nlm.nih.gov/34807007/');

-- ================================================ sym_agitation  (Agitation, anxiety or hallucinations)
update public.symptoms set description = 'Agitation is a state of excessive motor and mental restlessness with irritability or anxiety, which may be accompanied by hallucinations when perception is disturbed. It arises from psychiatric illness but also from delirium due to infection, metabolic disturbance, intoxication or withdrawal, and is a feature of furious rabies. Delirium is suggested when agitation begins suddenly, fluctuates through the day and comes with poor attention; its quiet, withdrawn (hypoactive) form is easily missed. In furious rabies, episodes of agitation, hallucinations and hydrophobia alternate with lucid intervals.', updated_at = now()
where id = 'sym_agitation' and description = 'Agitation is a state of excessive motor and mental restlessness with irritability or anxiety, which may be accompanied by hallucinations when perception is disturbed. It arises from psychiatric illness but also from delirium due to infection, metabolic disturbance, intoxication or withdrawal, and is a feature of furious rabies.';
update public.symptoms set tags = tags || array['agitation']::text[]
where id = 'sym_agitation' and not (tags @> array['agitation']::text[]);
update public.symptoms set source_attribution = source_attribution || '; Merck Manual Professional - Delirium'
where id = 'sym_agitation' and position('Merck Manual Professional - Delirium' in source_attribution) = 0;
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_agitation', 'Low blood sugar (hypoglycemia)', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_agitation'), 0)
where exists (select 1 from public.symptoms where id = 'sym_agitation')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_agitation' and content = 'Low blood sugar (hypoglycemia)');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_agitation', 'Head injury or stroke', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_agitation'), 0)
where exists (select 1 from public.symptoms where id = 'sym_agitation')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_agitation' and content = 'Head injury or stroke');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_agitation', 'Bacterial meningitis', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_agitation'), 0)
where exists (select 1 from public.symptoms where id = 'sym_agitation')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_agitation' and content = 'Bacterial meningitis');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_agitation', 'Liver failure (hepatic encephalopathy)', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_agitation'), 0)
where exists (select 1 from public.symptoms where id = 'sym_agitation')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_agitation' and content = 'Liver failure (hepatic encephalopathy)');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_agitation', 'Urinary retention, constipation or untreated pain in older adults', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_agitation'), 0)
where exists (select 1 from public.symptoms where id = 'sym_agitation')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_agitation' and content = 'Urinary retention, constipation or untreated pain in older adults');
insert into public.symptom_red_flags (symptom_id, content, position)
select 'sym_agitation', 'Sudden onset in an older adult (possible delirium)', coalesce((select max(position) + 1 from public.symptom_red_flags where symptom_id = 'sym_agitation'), 0)
where exists (select 1 from public.symptoms where id = 'sym_agitation')
  and not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_agitation' and content = 'Sudden onset in an older adult (possible delirium)');
insert into public.symptom_red_flags (symptom_id, content, position)
select 'sym_agitation', 'Headache, neck stiffness and fever (possible meningitis)', coalesce((select max(position) + 1 from public.symptom_red_flags where symptom_id = 'sym_agitation'), 0)
where exists (select 1 from public.symptoms where id = 'sym_agitation')
  and not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_agitation' and content = 'Headache, neck stiffness and fever (possible meningitis)');
insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select 'sym_agitation', 'Merck Manual Professional - Delirium', 'Huang J. Delirium. Merck Manual Professional Version. Rahway (NJ): Merck & Co.; reviewed Feb 2025.', 'https://www.merckmanuals.com/professional/neurologic-disorders/delirium-and-dementia/delirium', false, coalesce((select max(position) + 1 from public.symptom_references where symptom_id = 'sym_agitation'), 0)
where exists (select 1 from public.symptoms where id = 'sym_agitation')
  and not exists (select 1 from public.symptom_references where symptom_id = 'sym_agitation' and url = 'https://www.merckmanuals.com/professional/neurologic-disorders/delirium-and-dementia/delirium');
insert into public.disease_symptoms (disease_id, symptom_id, typical_intensity, is_primary, weight_multiplier)
select 'bacterial_meningitis', 'sym_agitation', 4::smallint, false, 0.6::numeric
where exists (select 1 from public.diseases where id = 'bacterial_meningitis')
  and exists (select 1 from public.symptoms where id = 'sym_agitation')
  and not exists (select 1 from public.disease_symptoms where disease_id = 'bacterial_meningitis' and symptom_id = 'sym_agitation');
insert into public.disease_symptoms (disease_id, symptom_id, typical_intensity, is_primary, weight_multiplier)
select 'typhoid_fever', 'sym_agitation', 2::smallint, false, 0.4::numeric
where exists (select 1 from public.diseases where id = 'typhoid_fever')
  and exists (select 1 from public.symptoms where id = 'sym_agitation')
  and not exists (select 1 from public.disease_symptoms where disease_id = 'typhoid_fever' and symptom_id = 'sym_agitation');

-- ================================================ sym_melena  (Black, tarry stools (melena))
update public.symptoms set description = 'Melena is the passage of black, sticky, tarry stools with a characteristic foul odour, produced when blood from the upper gastrointestinal tract is digested. It usually indicates bleeding from the esophagus, stomach or duodenum; iron and bismuth can blacken stools but do not make them tarry. About 100 to 200 mL of blood in the upper gastrointestinal tract is needed to turn the stool black and tarry, and melena can continue for several days after the bleeding has stopped. Patients are risk-stratified early (for example with the Glasgow-Blatchford score) to decide on admission and endoscopy.', updated_at = now()
where id = 'sym_melena' and description = 'Melena is the passage of black, sticky, tarry stools with a characteristic foul odour, produced when blood from the upper gastrointestinal tract is digested. It usually indicates bleeding from the esophagus, stomach or duodenum; iron and bismuth can blacken stools but do not make them tarry.';
update public.symptoms set tags = tags || array['GI bleeding']::text[]
where id = 'sym_melena' and not (tags @> array['GI bleeding']::text[]);
update public.symptoms set source_attribution = source_attribution || '; Merck Manual Professional - Overview of GI Bleeding; ACG Clinical Guideline - Upper GI and Ulcer Bleeding (2021)'
where id = 'sym_melena' and position('Merck Manual Professional - Overview of GI Bleeding' in source_attribution) = 0;
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_melena', 'Gastrointestinal bleeding in severe dengue', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_melena'), 0)
where exists (select 1 from public.symptoms where id = 'sym_melena')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_melena' and content = 'Gastrointestinal bleeding in severe dengue');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_melena', 'Intestinal bleeding in typhoid fever (usually in the third week)', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_melena'), 0)
where exists (select 1 from public.symptoms where id = 'sym_melena')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_melena' and content = 'Intestinal bleeding in typhoid fever (usually in the third week)');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_melena', 'Bleeding from the small bowel or right colon (less common)', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_melena'), 0)
where exists (select 1 from public.symptoms where id = 'sym_melena')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_melena' and content = 'Bleeding from the small bowel or right colon (less common)');
insert into public.symptom_red_flags (symptom_id, content, position)
select 'sym_melena', 'Jaundice, ascites or known liver disease (possible variceal bleeding)', coalesce((select max(position) + 1 from public.symptom_red_flags where symptom_id = 'sym_melena'), 0)
where exists (select 1 from public.symptoms where id = 'sym_melena')
  and not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_melena' and content = 'Jaundice, ascites or known liver disease (possible variceal bleeding)');
insert into public.symptom_red_flags (symptom_id, content, position)
select 'sym_melena', 'Black stools during dengue, especially around the time the fever settles', coalesce((select max(position) + 1 from public.symptom_red_flags where symptom_id = 'sym_melena'), 0)
where exists (select 1 from public.symptoms where id = 'sym_melena')
  and not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_melena' and content = 'Black stools during dengue, especially around the time the fever settles');
insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select 'sym_melena', 'Merck Manual Professional - Overview of GI Bleeding', 'Ansari P. Overview of Gastrointestinal Bleeding. Merck Manual Professional Version. Rahway (NJ): Merck & Co.; reviewed Jun 2025.', 'https://www.merckmanuals.com/professional/gastrointestinal-disorders/gastrointestinal-bleeding/overview-of-gastrointestinal-bleeding', false, coalesce((select max(position) + 1 from public.symptom_references where symptom_id = 'sym_melena'), 0)
where exists (select 1 from public.symptoms where id = 'sym_melena')
  and not exists (select 1 from public.symptom_references where symptom_id = 'sym_melena' and url = 'https://www.merckmanuals.com/professional/gastrointestinal-disorders/gastrointestinal-bleeding/overview-of-gastrointestinal-bleeding');
insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select 'sym_melena', 'ACG Clinical Guideline - Upper GI and Ulcer Bleeding (2021)', 'Laine L, Barkun AN, Saltzman JR, Martel M, Leontiadis GI. ACG Clinical Guideline: Upper Gastrointestinal and Ulcer Bleeding. Am J Gastroenterol. 2021;116(5):899-917. doi:10.14309/ajg.0000000000001245', 'https://pubmed.ncbi.nlm.nih.gov/33929377/', false, coalesce((select max(position) + 1 from public.symptom_references where symptom_id = 'sym_melena'), 0)
where exists (select 1 from public.symptoms where id = 'sym_melena')
  and not exists (select 1 from public.symptom_references where symptom_id = 'sym_melena' and url = 'https://pubmed.ncbi.nlm.nih.gov/33929377/');
insert into public.disease_symptoms (disease_id, symptom_id, typical_intensity, is_primary, weight_multiplier)
select 'dengue', 'sym_melena', 3::smallint, false, 0.6::numeric
where exists (select 1 from public.diseases where id = 'dengue')
  and exists (select 1 from public.symptoms where id = 'sym_melena')
  and not exists (select 1 from public.disease_symptoms where disease_id = 'dengue' and symptom_id = 'sym_melena');
insert into public.disease_symptoms (disease_id, symptom_id, typical_intensity, is_primary, weight_multiplier)
select 'typhoid_fever', 'sym_melena', 2::smallint, false, 0.5::numeric
where exists (select 1 from public.diseases where id = 'typhoid_fever')
  and exists (select 1 from public.symptoms where id = 'sym_melena')
  and not exists (select 1 from public.disease_symptoms where disease_id = 'typhoid_fever' and symptom_id = 'sym_melena');
insert into public.disease_symptoms (disease_id, symptom_id, typical_intensity, is_primary, weight_multiplier)
select 'schistosomiasis', 'sym_melena', 2::smallint, false, 0.5::numeric
where exists (select 1 from public.diseases where id = 'schistosomiasis')
  and exists (select 1 from public.symptoms where id = 'sym_melena')
  and not exists (select 1 from public.disease_symptoms where disease_id = 'schistosomiasis' and symptom_id = 'sym_melena');
insert into public.disease_symptoms (disease_id, symptom_id, typical_intensity, is_primary, weight_multiplier)
select 'hepatitis_b', 'sym_melena', 2::smallint, false, 0.4::numeric
where exists (select 1 from public.diseases where id = 'hepatitis_b')
  and exists (select 1 from public.symptoms where id = 'sym_melena')
  and not exists (select 1 from public.disease_symptoms where disease_id = 'hepatitis_b' and symptom_id = 'sym_melena');

-- ================================================ sym_vesicular_rash  (Blister-like rash (vesicles))
update public.symptoms set description = 'A vesicular rash consists of small (under about 1 cm), fluid-filled elevations of the skin. In varicella the vesicles appear in successive crops, starting on the face and trunk, so lesions at all stages from macules to crusts coexist; other patterns include grouped vesicles (herpes simplex), dermatomal vesicles (zoster) and hand-foot-mouth distributions (enterovirus). In unvaccinated people, varicella lesions progress quickly from macules to papules to vesicles before crusting; breakthrough varicella after vaccination is milder, usually with fewer than 50 lesions that are mostly papules. In scabies, small vesicles may appear at the ends of burrows, especially on the hands and wrists.', updated_at = now()
where id = 'sym_vesicular_rash' and description = 'A vesicular rash consists of small (under about 1 cm), fluid-filled elevations of the skin. In varicella the vesicles appear in successive crops, starting on the face and trunk, so lesions at all stages from macules to crusts coexist; other patterns include grouped vesicles (herpes simplex), dermatomal vesicles (zoster) and hand-foot-mouth distributions (enterovirus).';
update public.symptoms set tags = tags || array['herpesvirus']::text[]
where id = 'sym_vesicular_rash' and not (tags @> array['herpesvirus']::text[]);
update public.symptoms set source_attribution = source_attribution || '; CDC - Clinical Overview of Chickenpox (Varicella)'
where id = 'sym_vesicular_rash' and position('CDC - Clinical Overview of Chickenpox (Varicella)' in source_attribution) = 0;
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_vesicular_rash', 'Scabies (vesicles at the ends of burrows)', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_vesicular_rash'), 0)
where exists (select 1 from public.symptoms where id = 'sym_vesicular_rash')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_vesicular_rash' and content = 'Scabies (vesicles at the ends of burrows)');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_vesicular_rash', 'Insect bites (papular urticaria)', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_vesicular_rash'), 0)
where exists (select 1 from public.symptoms where id = 'sym_vesicular_rash')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_vesicular_rash' and content = 'Insect bites (papular urticaria)');
insert into public.symptom_red_flags (symptom_id, content, position)
select 'sym_vesicular_rash', 'Vesicles on the tip of the nose or around the eye (possible ophthalmic zoster)', coalesce((select max(position) + 1 from public.symptom_red_flags where symptom_id = 'sym_vesicular_rash'), 0)
where exists (select 1 from public.symptoms where id = 'sym_vesicular_rash')
  and not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_vesicular_rash' and content = 'Vesicles on the tip of the nose or around the eye (possible ophthalmic zoster)');
insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select 'sym_vesicular_rash', 'CDC - Clinical Overview of Chickenpox (Varicella)', 'Centers for Disease Control and Prevention. Clinical Overview of Chickenpox (Varicella). Atlanta (GA): CDC; reviewed 2024 Jul 15.', 'https://www.cdc.gov/chickenpox/hcp/clinical-overview/index.html', false, coalesce((select max(position) + 1 from public.symptom_references where symptom_id = 'sym_vesicular_rash'), 0)
where exists (select 1 from public.symptoms where id = 'sym_vesicular_rash')
  and not exists (select 1 from public.symptom_references where symptom_id = 'sym_vesicular_rash' and url = 'https://www.cdc.gov/chickenpox/hcp/clinical-overview/index.html');

-- ================================================ sym_bloody_stool  (Blood in stool (hematochezia))
update public.symptoms set description = 'Hematochezia is the passage of bright red or maroon blood per rectum, alone or mixed with stool. It usually indicates a colonic, rectal or anal source, although brisk upper gastrointestinal bleeding can also present this way; bloody diarrhea with fever suggests invasive infectious or inflammatory colitis. Streaks of bright blood on the toilet paper or on the surface of formed stool point to an anorectal source, whereas blood mixed into the stool or maroon stools suggest a source higher in the colon. In the tropics, bloody diarrhea (dysentery) is most often due to Shigella or Entamoeba histolytica, and intestinal bleeding is also a complication of typhoid fever and severe dengue.', updated_at = now()
where id = 'sym_bloody_stool' and description = 'Hematochezia is the passage of bright red or maroon blood per rectum, alone or mixed with stool. It usually indicates a colonic, rectal or anal source, although brisk upper gastrointestinal bleeding can also present this way; bloody diarrhea with fever suggests invasive infectious or inflammatory colitis.';
update public.symptoms set tags = tags || array['dysentery']::text[]
where id = 'sym_bloody_stool' and not (tags @> array['dysentery']::text[]);
update public.symptoms set source_attribution = source_attribution || '; ACG Guideline - Acute Lower GI Bleeding (2023); Merck Manual Professional - Overview of GI Bleeding'
where id = 'sym_bloody_stool' and position('ACG Guideline - Acute Lower GI Bleeding (2023)' in source_attribution) = 0;
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_bloody_stool', 'Typhoid fever (intestinal hemorrhage)', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_bloody_stool'), 0)
where exists (select 1 from public.symptoms where id = 'sym_bloody_stool')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_bloody_stool' and content = 'Typhoid fever (intestinal hemorrhage)');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_bloody_stool', 'Severe dengue with bleeding', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_bloody_stool'), 0)
where exists (select 1 from public.symptoms where id = 'sym_bloody_stool')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_bloody_stool' and content = 'Severe dengue with bleeding');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_bloody_stool', 'Meckel''s diverticulum (children)', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_bloody_stool'), 0)
where exists (select 1 from public.symptoms where id = 'sym_bloody_stool')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_bloody_stool' and content = 'Meckel''s diverticulum (children)');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_bloody_stool', 'Intussusception in infants (red currant jelly stools)', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_bloody_stool'), 0)
where exists (select 1 from public.symptoms where id = 'sym_bloody_stool')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_bloody_stool' and content = 'Intussusception in infants (red currant jelly stools)');
insert into public.symptom_red_flags (symptom_id, content, position)
select 'sym_bloody_stool', 'Bloody diarrhea in a child who then passes little urine or becomes pale (possible hemolytic uremic syndrome)', coalesce((select max(position) + 1 from public.symptom_red_flags where symptom_id = 'sym_bloody_stool'), 0)
where exists (select 1 from public.symptoms where id = 'sym_bloody_stool')
  and not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_bloody_stool' and content = 'Bloody diarrhea in a child who then passes little urine or becomes pale (possible hemolytic uremic syndrome)');
insert into public.symptom_red_flags (symptom_id, content, position)
select 'sym_bloody_stool', 'Bleeding during dengue or with a low platelet count', coalesce((select max(position) + 1 from public.symptom_red_flags where symptom_id = 'sym_bloody_stool'), 0)
where exists (select 1 from public.symptoms where id = 'sym_bloody_stool')
  and not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_bloody_stool' and content = 'Bleeding during dengue or with a low platelet count');
insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select 'sym_bloody_stool', 'ACG Guideline - Acute Lower GI Bleeding (2023)', 'Sengupta N, Feuerstein JD, Jairath V, et al. Management of Patients With Acute Lower Gastrointestinal Bleeding: An Updated ACG Guideline. Am J Gastroenterol. 2023;118(2):208-231.', 'https://pubmed.ncbi.nlm.nih.gov/36735555/', false, coalesce((select max(position) + 1 from public.symptom_references where symptom_id = 'sym_bloody_stool'), 0)
where exists (select 1 from public.symptoms where id = 'sym_bloody_stool')
  and not exists (select 1 from public.symptom_references where symptom_id = 'sym_bloody_stool' and url = 'https://pubmed.ncbi.nlm.nih.gov/36735555/');
insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select 'sym_bloody_stool', 'Merck Manual Professional - Overview of GI Bleeding', 'Ansari P. Overview of Gastrointestinal Bleeding. Merck Manual Professional Version. Rahway (NJ): Merck & Co.; reviewed Jun 2025.', 'https://www.merckmanuals.com/professional/gastrointestinal-disorders/gastrointestinal-bleeding/overview-of-gastrointestinal-bleeding', false, coalesce((select max(position) + 1 from public.symptom_references where symptom_id = 'sym_bloody_stool'), 0)
where exists (select 1 from public.symptoms where id = 'sym_bloody_stool')
  and not exists (select 1 from public.symptom_references where symptom_id = 'sym_bloody_stool' and url = 'https://www.merckmanuals.com/professional/gastrointestinal-disorders/gastrointestinal-bleeding/overview-of-gastrointestinal-bleeding');
insert into public.disease_symptoms (disease_id, symptom_id, typical_intensity, is_primary, weight_multiplier)
select 'acute_gastroenteritis', 'sym_bloody_stool', 4::smallint, false, 0.6::numeric
where exists (select 1 from public.diseases where id = 'acute_gastroenteritis')
  and exists (select 1 from public.symptoms where id = 'sym_bloody_stool')
  and not exists (select 1 from public.disease_symptoms where disease_id = 'acute_gastroenteritis' and symptom_id = 'sym_bloody_stool');
insert into public.disease_symptoms (disease_id, symptom_id, typical_intensity, is_primary, weight_multiplier)
select 'typhoid_fever', 'sym_bloody_stool', 2::smallint, false, 0.5::numeric
where exists (select 1 from public.diseases where id = 'typhoid_fever')
  and exists (select 1 from public.symptoms where id = 'sym_bloody_stool')
  and not exists (select 1 from public.disease_symptoms where disease_id = 'typhoid_fever' and symptom_id = 'sym_bloody_stool');
insert into public.disease_symptoms (disease_id, symptom_id, typical_intensity, is_primary, weight_multiplier)
select 'dengue', 'sym_bloody_stool', 2::smallint, false, 0.5::numeric
where exists (select 1 from public.diseases where id = 'dengue')
  and exists (select 1 from public.symptoms where id = 'sym_bloody_stool')
  and not exists (select 1 from public.disease_symptoms where disease_id = 'dengue' and symptom_id = 'sym_bloody_stool');

-- ================================================ sym_hematuria  (Blood in urine (hematuria / cola-colored urine))
update public.symptoms set description = 'Red, pink or brown (cola- or tea-colored) urine caused by red blood cells, or blood found only on urine testing. Brown urine with red cell casts suggests bleeding from the glomeruli (glomerulonephritis); bright red urine with clots more often comes from the bladder or urinary tract. Red or brown urine is not always blood: beets, rifampicin, myoglobin and free hemoglobin can look the same, so a dipstick and urine microscopy are needed. Microscopic hematuria is 3 or more red blood cells per high-power field on a properly collected sample; dysmorphic red cells, red cell casts and protein in the urine favor a glomerular source.', updated_at = now()
where id = 'sym_hematuria' and description = 'Red, pink or brown (cola- or tea-colored) urine caused by red blood cells, or blood found only on urine testing. Brown urine with red cell casts suggests bleeding from the glomeruli (glomerulonephritis); bright red urine with clots more often comes from the bladder or urinary tract.';
update public.symptoms set tags = tags || array['urinalysis']::text[]
where id = 'sym_hematuria' and not (tags @> array['urinalysis']::text[]);
update public.symptoms set source_attribution = source_attribution || '; AUA/SUFU Guideline - Microhematuria'
where id = 'sym_hematuria' and position('AUA/SUFU Guideline - Microhematuria' in source_attribution) = 0;
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_hematuria', 'Leptospirosis (kidney involvement)', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_hematuria'), 0)
where exists (select 1 from public.symptoms where id = 'sym_hematuria')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_hematuria' and content = 'Leptospirosis (kidney involvement)');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_hematuria', 'Dengue with bleeding', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_hematuria'), 0)
where exists (select 1 from public.symptoms where id = 'sym_hematuria')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_hematuria' and content = 'Dengue with bleeding');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_hematuria', 'Enlarged prostate', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_hematuria'), 0)
where exists (select 1 from public.symptoms where id = 'sym_hematuria')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_hematuria' and content = 'Enlarged prostate');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_hematuria', 'Polycystic kidney disease', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_hematuria'), 0)
where exists (select 1 from public.symptoms where id = 'sym_hematuria')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_hematuria' and content = 'Polycystic kidney disease');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_hematuria', 'Sickle cell disease or trait', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_hematuria'), 0)
where exists (select 1 from public.symptoms where id = 'sym_hematuria')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_hematuria' and content = 'Sickle cell disease or trait');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_hematuria', 'Injury to the kidney or urinary tract', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_hematuria'), 0)
where exists (select 1 from public.symptoms where id = 'sym_hematuria')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_hematuria' and content = 'Injury to the kidney or urinary tract');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_hematuria', 'Muscle breakdown or hemolysis (dipstick positive without red cells)', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_hematuria'), 0)
where exists (select 1 from public.symptoms where id = 'sym_hematuria')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_hematuria' and content = 'Muscle breakdown or hemolysis (dipstick positive without red cells)');
insert into public.symptom_red_flags (symptom_id, content, position)
select 'sym_hematuria', 'Passing blood clots or being unable to pass urine', coalesce((select max(position) + 1 from public.symptom_red_flags where symptom_id = 'sym_hematuria'), 0)
where exists (select 1 from public.symptoms where id = 'sym_hematuria')
  and not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_hematuria' and content = 'Passing blood clots or being unable to pass urine');
insert into public.symptom_red_flags (symptom_id, content, position)
select 'sym_hematuria', 'Blood in the urine after an injury', coalesce((select max(position) + 1 from public.symptom_red_flags where symptom_id = 'sym_hematuria'), 0)
where exists (select 1 from public.symptoms where id = 'sym_hematuria')
  and not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_hematuria' and content = 'Blood in the urine after an injury');
insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select 'sym_hematuria', 'AUA/SUFU Guideline - Microhematuria', 'American Urological Association / Society of Urodynamics, Female Pelvic Medicine & Urogenital Reconstruction. Microhematuria: AUA/SUFU Guideline (2020; amended 2025).', 'https://www.auanet.org/guidelines-and-quality/guidelines/microhematuria', false, coalesce((select max(position) + 1 from public.symptom_references where symptom_id = 'sym_hematuria'), 0)
where exists (select 1 from public.symptoms where id = 'sym_hematuria')
  and not exists (select 1 from public.symptom_references where symptom_id = 'sym_hematuria' and url = 'https://www.auanet.org/guidelines-and-quality/guidelines/microhematuria');
insert into public.disease_symptoms (disease_id, symptom_id, typical_intensity, is_primary, weight_multiplier)
select 'urinary_tract_infection', 'sym_hematuria', 3::smallint, false, 0.6::numeric
where exists (select 1 from public.diseases where id = 'urinary_tract_infection')
  and exists (select 1 from public.symptoms where id = 'sym_hematuria')
  and not exists (select 1 from public.disease_symptoms where disease_id = 'urinary_tract_infection' and symptom_id = 'sym_hematuria');
insert into public.disease_symptoms (disease_id, symptom_id, typical_intensity, is_primary, weight_multiplier)
select 'leptospirosis', 'sym_hematuria', 2::smallint, false, 0.5::numeric
where exists (select 1 from public.diseases where id = 'leptospirosis')
  and exists (select 1 from public.symptoms where id = 'sym_hematuria')
  and not exists (select 1 from public.disease_symptoms where disease_id = 'leptospirosis' and symptom_id = 'sym_hematuria');
insert into public.disease_symptoms (disease_id, symptom_id, typical_intensity, is_primary, weight_multiplier)
select 'dengue', 'sym_hematuria', 2::smallint, false, 0.4::numeric
where exists (select 1 from public.diseases where id = 'dengue')
  and exists (select 1 from public.symptoms where id = 'sym_hematuria')
  and not exists (select 1 from public.disease_symptoms where disease_id = 'dengue' and symptom_id = 'sym_hematuria');

-- ================================================ sym_blurred_vision  (Blurred vision)
update public.symptoms set description = 'Blurred vision is loss of sharpness of vision and inability to see fine details. It may result from refractive errors, lens changes from high blood glucose, cataract, retinal or optic nerve disease, and neurological causes. Asking whether it came on suddenly or gradually, in one eye or both, with or without pain, and whether it improves with blinking or looking through a pinhole separates refractive and surface problems from retinal, optic nerve and brain causes. Sudden loss of vision is itself a red flag, because most causes are serious.', updated_at = now()
where id = 'sym_blurred_vision' and description = 'Blurred vision is loss of sharpness of vision and inability to see fine details. It may result from refractive errors, lens changes from high blood glucose, cataract, retinal or optic nerve disease, and neurological causes.';
update public.symptoms set tags = tags || array['ophthalmology']::text[]
where id = 'sym_blurred_vision' and not (tags @> array['ophthalmology']::text[]);
update public.symptoms set source_attribution = source_attribution || '; Merck Manual Professional - Acute Vision Loss'
where id = 'sym_blurred_vision' and position('Merck Manual Professional - Acute Vision Loss' in source_attribution) = 0;
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_blurred_vision', 'Dry eye and conjunctivitis', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_blurred_vision'), 0)
where exists (select 1 from public.symptoms where id = 'sym_blurred_vision')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_blurred_vision' and content = 'Dry eye and conjunctivitis');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_blurred_vision', 'Glaucoma, including acute angle-closure', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_blurred_vision'), 0)
where exists (select 1 from public.symptoms where id = 'sym_blurred_vision')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_blurred_vision' and content = 'Glaucoma, including acute angle-closure');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_blurred_vision', 'Retinal vein or artery occlusion', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_blurred_vision'), 0)
where exists (select 1 from public.symptoms where id = 'sym_blurred_vision')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_blurred_vision' and content = 'Retinal vein or artery occlusion');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_blurred_vision', 'Optic neuritis', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_blurred_vision'), 0)
where exists (select 1 from public.symptoms where id = 'sym_blurred_vision')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_blurred_vision' and content = 'Optic neuritis');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_blurred_vision', 'Thyroid eye disease', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_blurred_vision'), 0)
where exists (select 1 from public.symptoms where id = 'sym_blurred_vision')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_blurred_vision' and content = 'Thyroid eye disease');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_blurred_vision', 'Medication effects (e.g., anticholinergic drugs)', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_blurred_vision'), 0)
where exists (select 1 from public.symptoms where id = 'sym_blurred_vision')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_blurred_vision' and content = 'Medication effects (e.g., anticholinergic drugs)');
insert into public.symptom_red_flags (symptom_id, content, position)
select 'sym_blurred_vision', 'Halos around lights with a red, painful eye, headache and vomiting (possible acute angle-closure glaucoma)', coalesce((select max(position) + 1 from public.symptom_red_flags where symptom_id = 'sym_blurred_vision'), 0)
where exists (select 1 from public.symptoms where id = 'sym_blurred_vision')
  and not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_blurred_vision' and content = 'Halos around lights with a red, painful eye, headache and vomiting (possible acute angle-closure glaucoma)');
insert into public.symptom_red_flags (symptom_id, content, position)
select 'sym_blurred_vision', 'New floaters, flashes of light or a curtain over vision (possible retinal detachment)', coalesce((select max(position) + 1 from public.symptom_red_flags where symptom_id = 'sym_blurred_vision'), 0)
where exists (select 1 from public.symptoms where id = 'sym_blurred_vision')
  and not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_blurred_vision' and content = 'New floaters, flashes of light or a curtain over vision (possible retinal detachment)');
insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select 'sym_blurred_vision', 'Merck Manual Professional - Acute Vision Loss', 'Brady CJ. Acute Vision Loss. Merck Manual Professional Version. Rahway (NJ): Merck & Co.; reviewed Oct 2025.', 'https://www.merckmanuals.com/professional/eye-disorders/symptoms-of-ophthalmic-disorders/acute-vision-loss', false, coalesce((select max(position) + 1 from public.symptom_references where symptom_id = 'sym_blurred_vision'), 0)
where exists (select 1 from public.symptoms where id = 'sym_blurred_vision')
  and not exists (select 1 from public.symptom_references where symptom_id = 'sym_blurred_vision' and url = 'https://www.merckmanuals.com/professional/eye-disorders/symptoms-of-ophthalmic-disorders/acute-vision-loss');
insert into public.disease_symptoms (disease_id, symptom_id, typical_intensity, is_primary, weight_multiplier)
select 'graves_disease', 'sym_blurred_vision', 3::smallint, false, 0.5::numeric
where exists (select 1 from public.diseases where id = 'graves_disease')
  and exists (select 1 from public.symptoms where id = 'sym_blurred_vision')
  and not exists (select 1 from public.disease_symptoms where disease_id = 'graves_disease' and symptom_id = 'sym_blurred_vision');

-- ================================================ sym_orthopnea  (Breathlessness lying flat (orthopnea))
update public.symptoms set description = 'Orthopnea is breathlessness in the recumbent position that is relieved by sitting or standing, often quantified by the number of pillows needed to sleep. It is characteristic of left ventricular failure due to redistribution of fluid into the pulmonary circulation, and often occurs with paroxysmal nocturnal dyspnea. Breathlessness that wakes the patient one to two hours after falling asleep and is relieved by sitting up (paroxysmal nocturnal dyspnea) carries the same meaning. Orthopnea also occurs with pericardial effusion and with weakness of both diaphragms, where breathing worsens immediately on lying flat.', updated_at = now()
where id = 'sym_orthopnea' and description = 'Orthopnea is breathlessness in the recumbent position that is relieved by sitting or standing, often quantified by the number of pillows needed to sleep. It is characteristic of left ventricular failure due to redistribution of fluid into the pulmonary circulation, and often occurs with paroxysmal nocturnal dyspnea.';
update public.symptoms set tags = tags || array['paroxysmal nocturnal dyspnea']::text[]
where id = 'sym_orthopnea' and not (tags @> array['paroxysmal nocturnal dyspnea']::text[]);
update public.symptoms set source_attribution = source_attribution || '; Merck Manual Professional - Dyspnea; 2022 AHA/ACC/HFSA Heart Failure Guideline'
where id = 'sym_orthopnea' and position('Merck Manual Professional - Dyspnea' in source_attribution) = 0;
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_orthopnea', 'Pericardial effusion or tamponade', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_orthopnea'), 0)
where exists (select 1 from public.symptoms where id = 'sym_orthopnea')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_orthopnea' and content = 'Pericardial effusion or tamponade');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_orthopnea', 'Fluid overload in kidney disease or acute glomerulonephritis', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_orthopnea'), 0)
where exists (select 1 from public.symptoms where id = 'sym_orthopnea')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_orthopnea' and content = 'Fluid overload in kidney disease or acute glomerulonephritis');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_orthopnea', 'Rheumatic heart disease (mitral valve damage)', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_orthopnea'), 0)
where exists (select 1 from public.symptoms where id = 'sym_orthopnea')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_orthopnea' and content = 'Rheumatic heart disease (mitral valve damage)');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_orthopnea', 'Obesity', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_orthopnea'), 0)
where exists (select 1 from public.symptoms where id = 'sym_orthopnea')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_orthopnea' and content = 'Obesity');
insert into public.symptom_red_flags (symptom_id, content, position)
select 'sym_orthopnea', 'Rapid weight gain with worsening leg or abdominal swelling', coalesce((select max(position) + 1 from public.symptom_red_flags where symptom_id = 'sym_orthopnea'), 0)
where exists (select 1 from public.symptoms where id = 'sym_orthopnea')
  and not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_orthopnea' and content = 'Rapid weight gain with worsening leg or abdominal swelling');
insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select 'sym_orthopnea', 'Merck Manual Professional - Dyspnea', 'Dezube R. Dyspnea. Merck Manual Professional Version. Rahway (NJ): Merck & Co.; reviewed Nov 2025.', 'https://www.merckmanuals.com/professional/pulmonary-disorders/symptoms-of-pulmonary-disorders/dyspnea', false, coalesce((select max(position) + 1 from public.symptom_references where symptom_id = 'sym_orthopnea'), 0)
where exists (select 1 from public.symptoms where id = 'sym_orthopnea')
  and not exists (select 1 from public.symptom_references where symptom_id = 'sym_orthopnea' and url = 'https://www.merckmanuals.com/professional/pulmonary-disorders/symptoms-of-pulmonary-disorders/dyspnea');
insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select 'sym_orthopnea', '2022 AHA/ACC/HFSA Heart Failure Guideline', 'Heidenreich PA, Bozkurt B, Aguilar D, et al. 2022 AHA/ACC/HFSA Guideline for the Management of Heart Failure. J Am Coll Cardiol. 2022;79(17):e263-e421. doi:10.1016/j.jacc.2021.12.012', 'https://doi.org/10.1016/j.jacc.2021.12.012', false, coalesce((select max(position) + 1 from public.symptom_references where symptom_id = 'sym_orthopnea'), 0)
where exists (select 1 from public.symptoms where id = 'sym_orthopnea')
  and not exists (select 1 from public.symptom_references where symptom_id = 'sym_orthopnea' and url = 'https://doi.org/10.1016/j.jacc.2021.12.012');
insert into public.disease_symptoms (disease_id, symptom_id, typical_intensity, is_primary, weight_multiplier)
select 'rheumatic_fever', 'sym_orthopnea', 3::smallint, false, 0.6::numeric
where exists (select 1 from public.diseases where id = 'rheumatic_fever')
  and exists (select 1 from public.symptoms where id = 'sym_orthopnea')
  and not exists (select 1 from public.disease_symptoms where disease_id = 'rheumatic_fever' and symptom_id = 'sym_orthopnea');
insert into public.disease_symptoms (disease_id, symptom_id, typical_intensity, is_primary, weight_multiplier)
select 'post_strep_glomerulonephritis', 'sym_orthopnea', 3::smallint, false, 0.6::numeric
where exists (select 1 from public.diseases where id = 'post_strep_glomerulonephritis')
  and exists (select 1 from public.symptoms where id = 'sym_orthopnea')
  and not exists (select 1 from public.disease_symptoms where disease_id = 'post_strep_glomerulonephritis' and symptom_id = 'sym_orthopnea');
insert into public.disease_symptoms (disease_id, symptom_id, typical_intensity, is_primary, weight_multiplier)
select 'copd', 'sym_orthopnea', 2::smallint, false, 0.5::numeric
where exists (select 1 from public.diseases where id = 'copd')
  and exists (select 1 from public.symptoms where id = 'sym_orthopnea')
  and not exists (select 1 from public.disease_symptoms where disease_id = 'copd' and symptom_id = 'sym_orthopnea');
insert into public.disease_symptoms (disease_id, symptom_id, typical_intensity, is_primary, weight_multiplier)
select 'chronic_kidney_disease', 'sym_orthopnea', 2::smallint, false, 0.4::numeric
where exists (select 1 from public.diseases where id = 'chronic_kidney_disease')
  and exists (select 1 from public.symptoms where id = 'sym_orthopnea')
  and not exists (select 1 from public.disease_symptoms where disease_id = 'chronic_kidney_disease' and symptom_id = 'sym_orthopnea');

update public.content_version set version = version + 1, updated_at = now() where id = 1;

commit;

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

-- 025_symptoms_review_05.sql  -  symptom review, session 05: 10 symptoms
-- Adds only: longer descriptions, extra causes, red flags, references and disease links.
-- Nothing is deleted or replaced. Safe to run twice (every insert is guarded).
-- A description is only extended if it is still the exported text (your own edits are kept).

begin;

-- ================================================ sym_chorea  (Involuntary jerky movements (chorea))
update public.symptoms set description = 'Brief, irregular, purposeless movements that flow from one body part to another, often with clumsiness, facial grimacing and emotional lability. In children and adolescents the most common acquired cause is Sydenham chorea, a late manifestation of acute rheumatic fever that can appear months after the streptococcal infection. The movements mainly affect the face and the hands and feet and are often blended into semi-purposeful actions to disguise them. They arise from reduced inhibition in the basal ganglia; Huntington disease is the commonest degenerative cause, and Sydenham chorea is usually self-limited.', updated_at = now()
where id = 'sym_chorea' and description = 'Brief, irregular, purposeless movements that flow from one body part to another, often with clumsiness, facial grimacing and emotional lability. In children and adolescents the most common acquired cause is Sydenham chorea, a late manifestation of acute rheumatic fever that can appear months after the streptococcal infection.';
update public.symptoms set tags = tags || array['basal ganglia']::text[]
where id = 'sym_chorea' and not (tags @> array['basal ganglia']::text[]);
update public.symptoms set source_attribution = source_attribution || '; Merck Manual Professional - Chorea, Athetosis, and Hemiballismus'
where id = 'sym_chorea' and position('Merck Manual Professional - Chorea, Athetosis, and Hemiballismus' in source_attribution) = 0;
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_chorea', 'Phenytoin, cocaine, tricyclic antidepressants or oral contraceptives', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_chorea'), 0)
where exists (select 1 from public.symptoms where id = 'sym_chorea')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_chorea' and content = 'Phenytoin, cocaine, tricyclic antidepressants or oral contraceptives');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_chorea', 'Tardive dyskinesia after long-term antipsychotics', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_chorea'), 0)
where exists (select 1 from public.symptoms where id = 'sym_chorea')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_chorea' and content = 'Tardive dyskinesia after long-term antipsychotics');
insert into public.symptom_red_flags (symptom_id, content, position)
select 'sym_chorea', 'Family history of a similar movement disorder or early dementia (possible Huntington disease)', coalesce((select max(position) + 1 from public.symptom_red_flags where symptom_id = 'sym_chorea'), 0)
where exists (select 1 from public.symptoms where id = 'sym_chorea')
  and not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_chorea' and content = 'Family history of a similar movement disorder or early dementia (possible Huntington disease)');
insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select 'sym_chorea', 'Merck Manual Professional - Chorea, Athetosis, and Hemiballismus', 'Rajput A, Noyes E. Chorea, Athetosis, and Hemiballismus. Merck Manual Professional Version. Rahway (NJ): Merck & Co.; reviewed Mar 2026.', 'https://www.merckmanuals.com/professional/neurologic-disorders/movement-and-cerebellar-disorders/chorea-athetosis-and-hemiballismus', false, coalesce((select max(position) + 1 from public.symptom_references where symptom_id = 'sym_chorea'), 0)
where exists (select 1 from public.symptoms where id = 'sym_chorea')
  and not exists (select 1 from public.symptom_references where symptom_id = 'sym_chorea' and url = 'https://www.merckmanuals.com/professional/neurologic-disorders/movement-and-cerebellar-disorders/chorea-athetosis-and-hemiballismus');

-- ================================================ sym_pruritus  (Itching (pruritus))
update public.symptoms set description = 'Pruritus is an unpleasant skin sensation that provokes the desire to scratch. It may be localized, usually from primary skin disease, or generalized, when systemic causes such as cholestatic liver disease, chronic kidney disease, drug reactions or hematologic disorders are considered. It is most often due to skin disease such as dry skin, dermatitis or fungal infection. Prominent itching without any visible skin changes should raise suspicion of a systemic, drug or nerve-related cause.', updated_at = now()
where id = 'sym_pruritus' and description = 'Pruritus is an unpleasant skin sensation that provokes the desire to scratch. It may be localized, usually from primary skin disease, or generalized, when systemic causes such as cholestatic liver disease, chronic kidney disease, drug reactions or hematologic disorders are considered.';
update public.symptoms set tags = tags || array['xerosis']::text[]
where id = 'sym_pruritus' and not (tags @> array['xerosis']::text[]);
update public.symptoms set source_attribution = source_attribution || '; Merck Manual Professional - Itching'
where id = 'sym_pruritus' and position('Merck Manual Professional - Itching' in source_attribution) = 0;
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_pruritus', 'Dry skin (xerosis)', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_pruritus'), 0)
where exists (select 1 from public.symptoms where id = 'sym_pruritus')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_pruritus' and content = 'Dry skin (xerosis)');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_pruritus', 'Fungal skin infection', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_pruritus'), 0)
where exists (select 1 from public.symptoms where id = 'sym_pruritus')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_pruritus' and content = 'Fungal skin infection');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_pruritus', 'Opioids and IV contrast', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_pruritus'), 0)
where exists (select 1 from public.symptoms where id = 'sym_pruritus')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_pruritus' and content = 'Opioids and IV contrast');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_pruritus', 'Blood disorders such as lymphoma and polycythemia', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_pruritus'), 0)
where exists (select 1 from public.symptoms where id = 'sym_pruritus')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_pruritus' and content = 'Blood disorders such as lymphoma and polycythemia');
insert into public.symptom_red_flags (symptom_id, content, position)
select 'sym_pruritus', 'Itching with heavy urination and thirst', coalesce((select max(position) + 1 from public.symptom_red_flags where symptom_id = 'sym_pruritus'), 0)
where exists (select 1 from public.symptoms where id = 'sym_pruritus')
  and not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_pruritus' and content = 'Itching with heavy urination and thirst');
insert into public.symptom_red_flags (symptom_id, content, position)
select 'sym_pruritus', 'Itching with numbness, tingling or weakness in the limbs', coalesce((select max(position) + 1 from public.symptom_red_flags where symptom_id = 'sym_pruritus'), 0)
where exists (select 1 from public.symptoms where id = 'sym_pruritus')
  and not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_pruritus' and content = 'Itching with numbness, tingling or weakness in the limbs');
insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select 'sym_pruritus', 'Merck Manual Professional - Itching', 'Benedetti J. Itching. Merck Manual Professional Version. Rahway (NJ): Merck & Co.; reviewed Jan 2024 (updated Apr 2025).', 'https://www.merckmanuals.com/professional/dermatologic-disorders/approach-to-the-dermatologic-patient/itching', false, coalesce((select max(position) + 1 from public.symptom_references where symptom_id = 'sym_pruritus'), 0)
where exists (select 1 from public.symptoms where id = 'sym_pruritus')
  and not exists (select 1 from public.symptom_references where symptom_id = 'sym_pruritus' and url = 'https://www.merckmanuals.com/professional/dermatologic-disorders/approach-to-the-dermatologic-patient/itching');

-- ================================================ sym_jaundice  (Jaundice)
update public.symptoms set description = 'Jaundice is yellow discolouration of the skin, mucous membranes and sclerae caused by accumulation of bilirubin. Scleral icterus is best appreciated when serum bilirubin exceeds about 3 mg/dL, and causes are grouped as prehepatic, hepatic and posthepatic. It can be visible from a bilirubin of about 2 to 3 mg/dL (34 to 51 µmol/L). Very high aminotransferases (over 500 U/L) with alkaline phosphatase under three times normal suggest liver-cell injury, whereas lower aminotransferases with alkaline phosphatase over three times normal suggest cholestasis.', updated_at = now()
where id = 'sym_jaundice' and description = 'Jaundice is yellow discolouration of the skin, mucous membranes and sclerae caused by accumulation of bilirubin. Scleral icterus is best appreciated when serum bilirubin exceeds about 3 mg/dL, and causes are grouped as prehepatic, hepatic and posthepatic.';
update public.symptoms set tags = tags || array['cholestasis']::text[]
where id = 'sym_jaundice' and not (tags @> array['cholestasis']::text[]);
update public.symptoms set source_attribution = source_attribution || '; Merck Manual Professional - Jaundice'
where id = 'sym_jaundice' and position('Merck Manual Professional - Jaundice' in source_attribution) = 0;
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_jaundice', 'Autoimmune hepatitis', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_jaundice'), 0)
where exists (select 1 from public.symptoms where id = 'sym_jaundice')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_jaundice' and content = 'Autoimmune hepatitis');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_jaundice', 'Cancer of the pancreas or bile ducts', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_jaundice'), 0)
where exists (select 1 from public.symptoms where id = 'sym_jaundice')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_jaundice' and content = 'Cancer of the pancreas or bile ducts');
insert into public.symptom_red_flags (symptom_id, content, position)
select 'sym_jaundice', 'Vomiting blood or black stools', coalesce((select max(position) + 1 from public.symptom_red_flags where symptom_id = 'sym_jaundice'), 0)
where exists (select 1 from public.symptoms where id = 'sym_jaundice')
  and not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_jaundice' and content = 'Vomiting blood or black stools');
insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select 'sym_jaundice', 'Merck Manual Professional - Jaundice', 'Tholey D. Jaundice. Merck Manual Professional Version. Rahway (NJ): Merck & Co.; reviewed Aug 2025.', 'https://www.merckmanuals.com/professional/hepatic-and-biliary-disorders/approach-to-the-patient-with-liver-disease/jaundice', false, coalesce((select max(position) + 1 from public.symptom_references where symptom_id = 'sym_jaundice'), 0)
where exists (select 1 from public.symptoms where id = 'sym_jaundice')
  and not exists (select 1 from public.symptom_references where symptom_id = 'sym_jaundice' and url = 'https://www.merckmanuals.com/professional/hepatic-and-biliary-disorders/approach-to-the-patient-with-liver-disease/jaundice');

-- ================================================ sym_arthralgia  (Joint pain (arthralgia))
update public.symptoms set description = 'Arthralgia is pain in one or more joints without necessarily visible swelling or inflammation. It may arise from injury, degenerative or inflammatory arthritis, or as part of systemic infection such as dengue (''breakbone fever''). Sudden pain in many joints is usually from a viral or other infection, a flare of inflammatory disease or crystal arthritis; chronic pain in many joints in adults is usually rheumatoid arthritis, spondyloarthritis or osteoarthritis. Pain at rest and on starting to move suggests inflammation, while pain that worsens with use and eases with rest suggests a mechanical cause.', updated_at = now()
where id = 'sym_arthralgia' and description = 'Arthralgia is pain in one or more joints without necessarily visible swelling or inflammation. It may arise from injury, degenerative or inflammatory arthritis, or as part of systemic infection such as dengue (''breakbone fever'').';
update public.symptoms set tags = tags || array['polyarthralgia']::text[]
where id = 'sym_arthralgia' and not (tags @> array['polyarthralgia']::text[]);
update public.symptoms set source_attribution = source_attribution || '; Merck Manual Professional - Pain in Multiple Joints'
where id = 'sym_arthralgia' and position('Merck Manual Professional - Pain in Multiple Joints' in source_attribution) = 0;
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_arthralgia', 'Reactive arthritis after infection', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_arthralgia'), 0)
where exists (select 1 from public.symptoms where id = 'sym_arthralgia')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_arthralgia' and content = 'Reactive arthritis after infection');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_arthralgia', 'Systemic lupus erythematosus', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_arthralgia'), 0)
where exists (select 1 from public.symptoms where id = 'sym_arthralgia')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_arthralgia' and content = 'Systemic lupus erythematosus');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_arthralgia', 'Spondyloarthritis', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_arthralgia'), 0)
where exists (select 1 from public.symptoms where id = 'sym_arthralgia')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_arthralgia' and content = 'Spondyloarthritis');
insert into public.symptom_red_flags (symptom_id, content, position)
select 'sym_arthralgia', 'Joint pain with fever, rash, red eyes or weight loss', coalesce((select max(position) + 1 from public.symptom_red_flags where symptom_id = 'sym_arthralgia'), 0)
where exists (select 1 from public.symptoms where id = 'sym_arthralgia')
  and not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_arthralgia' and content = 'Joint pain with fever, rash, red eyes or weight loss');
insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select 'sym_arthralgia', 'Merck Manual Professional - Pain in Multiple Joints', 'Villa-Forte A. Pain in Multiple Joints. Merck Manual Professional Version. Rahway (NJ): Merck & Co.; reviewed Apr 2025.', 'https://www.merckmanuals.com/professional/musculoskeletal-and-connective-tissue-disorders/pain-in-and-around-joints/pain-in-multiple-joints', false, coalesce((select max(position) + 1 from public.symptom_references where symptom_id = 'sym_arthralgia'), 0)
where exists (select 1 from public.symptoms where id = 'sym_arthralgia')
  and not exists (select 1 from public.symptom_references where symptom_id = 'sym_arthralgia' and url = 'https://www.merckmanuals.com/professional/musculoskeletal-and-connective-tissue-disorders/pain-in-and-around-joints/pain-in-multiple-joints');

-- ================================================ sym_joint_swelling  (Joint swelling)
update public.symptoms set description = 'Joint swelling is enlargement of a joint from synovial fluid (effusion), synovial thickening or swelling of the surrounding soft tissues. It distinguishes true arthritis from arthralgia alone and is characterized by the number and pattern of joints involved, acuity and the presence of warmth or redness. Septic arthritis is the most dangerous cause at any age, so a new swollen joint with fluid needs joint aspiration (cell count, Gram stain, culture and crystal search). Finding crystals does not rule out infection, and a joint white cell count over 50,000/µL can occur in both.', updated_at = now()
where id = 'sym_joint_swelling' and description = 'Joint swelling is enlargement of a joint from synovial fluid (effusion), synovial thickening or swelling of the surrounding soft tissues. It distinguishes true arthritis from arthralgia alone and is characterized by the number and pattern of joints involved, acuity and the presence of warmth or redness.';
update public.symptoms set tags = tags || array['arthrocentesis']::text[]
where id = 'sym_joint_swelling' and not (tags @> array['arthrocentesis']::text[]);
update public.symptoms set source_attribution = source_attribution || '; Merck Manual Professional - Pain in and Around a Single Joint'
where id = 'sym_joint_swelling' and position('Merck Manual Professional - Pain in and Around a Single Joint' in source_attribution) = 0;
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_joint_swelling', 'Bleeding into the joint (hemarthrosis) on anticoagulants or with a bleeding disorder', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_joint_swelling'), 0)
where exists (select 1 from public.symptoms where id = 'sym_joint_swelling')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_joint_swelling' and content = 'Bleeding into the joint (hemarthrosis) on anticoagulants or with a bleeding disorder');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_joint_swelling', 'Lyme disease', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_joint_swelling'), 0)
where exists (select 1 from public.symptoms where id = 'sym_joint_swelling')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_joint_swelling' and content = 'Lyme disease');
insert into public.symptom_red_flags (symptom_id, content, position)
select 'sym_joint_swelling', 'Joint swelling in someone on anticoagulants or with a bleeding disorder', coalesce((select max(position) + 1 from public.symptom_red_flags where symptom_id = 'sym_joint_swelling'), 0)
where exists (select 1 from public.symptoms where id = 'sym_joint_swelling')
  and not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_joint_swelling' and content = 'Joint swelling in someone on anticoagulants or with a bleeding disorder');
insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select 'sym_joint_swelling', 'Merck Manual Professional - Pain in and Around a Single Joint', 'Villa-Forte A. Pain in and Around a Single Joint. Merck Manual Professional Version. Rahway (NJ): Merck & Co.; reviewed Apr 2025 (updated Jun 2025).', 'https://www.merckmanuals.com/professional/musculoskeletal-and-connective-tissue-disorders/pain-in-and-around-joints/pain-in-and-around-a-single-joint', false, coalesce((select max(position) + 1 from public.symptom_references where symptom_id = 'sym_joint_swelling'), 0)
where exists (select 1 from public.symptoms where id = 'sym_joint_swelling')
  and not exists (select 1 from public.symptom_references where symptom_id = 'sym_joint_swelling' and url = 'https://www.merckmanuals.com/professional/musculoskeletal-and-connective-tissue-disorders/pain-in-and-around-joints/pain-in-and-around-a-single-joint');

-- ================================================ sym_koplik_spots  (Koplik spots)
update public.symptoms set description = 'Koplik spots are small bluish-white spots, about 2-3 mm, on an erythematous base on the buccal mucosa opposite the molars, likened to ''grains of salt on a red background''. They typically appear about a day before the measles rash and fade as the rash develops. They are seen in about 70% of cases, usually opposite the first and second upper molars, and may persist for a day or two after the rash appears. They follow a prodrome of fever, cough, runny nose and conjunctivitis; the rash then spreads from the head down, and patients are contagious from 4 days before to 4 days after rash onset.', updated_at = now()
where id = 'sym_koplik_spots' and description = 'Koplik spots are small bluish-white spots, about 2-3 mm, on an erythematous base on the buccal mucosa opposite the molars, likened to ''grains of salt on a red background''. They typically appear about a day before the measles rash and fade as the rash develops.';
update public.symptoms set tags = tags || array['enanthem']::text[]
where id = 'sym_koplik_spots' and not (tags @> array['enanthem']::text[]);
update public.symptoms set source_attribution = source_attribution || '; Merck Manual Professional - Measles; CDC - Clinical Overview of Measles'
where id = 'sym_koplik_spots' and position('Merck Manual Professional - Measles' in source_attribution) = 0;
insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select 'sym_koplik_spots', 'Merck Manual Professional - Measles', 'de St. Maurice A. Measles. Merck Manual Professional Version. Rahway (NJ): Merck & Co.; reviewed Jun 2025 (updated Sep 2025).', 'https://www.merckmanuals.com/professional/pediatrics/common-viral-infections-in-infants-and-children/measles', false, coalesce((select max(position) + 1 from public.symptom_references where symptom_id = 'sym_koplik_spots'), 0)
where exists (select 1 from public.symptoms where id = 'sym_koplik_spots')
  and not exists (select 1 from public.symptom_references where symptom_id = 'sym_koplik_spots' and url = 'https://www.merckmanuals.com/professional/pediatrics/common-viral-infections-in-infants-and-children/measles');
insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select 'sym_koplik_spots', 'CDC - Clinical Overview of Measles', 'Centers for Disease Control and Prevention. Clinical Overview of Measles. Atlanta (GA): CDC; reviewed May 2025 (updated Aug 2026).', 'https://www.cdc.gov/measles/hcp/clinical-overview/index.html', false, coalesce((select max(position) + 1 from public.symptom_references where symptom_id = 'sym_koplik_spots'), 0)
where exists (select 1 from public.symptoms where id = 'sym_koplik_spots')
  and not exists (select 1 from public.symptom_references where symptom_id = 'sym_koplik_spots' and url = 'https://www.cdc.gov/measles/hcp/clinical-overview/index.html');

-- ================================================ sym_edema  (Leg swelling (edema))
update public.symptoms set description = 'Peripheral edema is abnormal buildup of fluid in the tissues of the feet, ankles and legs, typically pitting on pressure. Bilateral edema suggests systemic causes such as heart, kidney or liver disease or medicines, while unilateral swelling suggests local venous or lymphatic causes. Heart failure gives symmetrical, painless pitting edema in the lowest parts of the body, whereas a sudden, painful swelling of one leg suggests deep vein thrombosis and usually needs an ultrasound. Generalised edema mostly comes from heart, liver or kidney disease.', updated_at = now()
where id = 'sym_edema' and description = 'Peripheral edema is abnormal buildup of fluid in the tissues of the feet, ankles and legs, typically pitting on pressure. Bilateral edema suggests systemic causes such as heart, kidney or liver disease or medicines, while unilateral swelling suggests local venous or lymphatic causes.';
update public.symptoms set tags = tags || array['pitting']::text[]
where id = 'sym_edema' and not (tags @> array['pitting']::text[]);
update public.symptoms set source_attribution = source_attribution || '; Merck Manual Professional - Edema'
where id = 'sym_edema' and position('Merck Manual Professional - Edema' in source_attribution) = 0;
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_edema', 'Lymphatic obstruction (lymphedema)', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_edema'), 0)
where exists (select 1 from public.symptoms where id = 'sym_edema')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_edema' and content = 'Lymphatic obstruction (lymphedema)');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_edema', 'Cellulitis', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_edema'), 0)
where exists (select 1 from public.symptoms where id = 'sym_edema')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_edema' and content = 'Cellulitis');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_edema', 'Angioedema', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_edema'), 0)
where exists (select 1 from public.symptoms where id = 'sym_edema')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_edema' and content = 'Angioedema');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_edema', 'Low blood protein from malnutrition', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_edema'), 0)
where exists (select 1 from public.symptoms where id = 'sym_edema')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_edema' and content = 'Low blood protein from malnutrition');
insert into public.symptom_red_flags (symptom_id, content, position)
select 'sym_edema', 'Sudden onset of swelling', coalesce((select max(position) + 1 from public.symptom_red_flags where symptom_id = 'sym_edema'), 0)
where exists (select 1 from public.symptoms where id = 'sym_edema')
  and not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_edema' and content = 'Sudden onset of swelling');
insert into public.symptom_red_flags (symptom_id, content, position)
select 'sym_edema', 'Swelling of the face, lips or tongue', coalesce((select max(position) + 1 from public.symptom_red_flags where symptom_id = 'sym_edema'), 0)
where exists (select 1 from public.symptoms where id = 'sym_edema')
  and not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_edema' and content = 'Swelling of the face, lips or tongue');
insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select 'sym_edema', 'Merck Manual Professional - Edema', 'Thompson AD, Shea MJ. Edema. Merck Manual Professional Version. Rahway (NJ): Merck & Co.; reviewed Aug 2024 (updated Oct 2025).', 'https://www.merckmanuals.com/professional/cardiovascular-disorders/symptoms-of-cardiovascular-disorders/edema', false, coalesce((select max(position) + 1 from public.symptom_references where symptom_id = 'sym_edema'), 0)
where exists (select 1 from public.symptoms where id = 'sym_edema')
  and not exists (select 1 from public.symptom_references where symptom_id = 'sym_edema' and url = 'https://www.merckmanuals.com/professional/cardiovascular-disorders/symptoms-of-cardiovascular-disorders/edema');
insert into public.disease_symptoms (disease_id, symptom_id, typical_intensity, is_primary, weight_multiplier)
select 'hepatitis_b', 'sym_edema', 2::smallint, false, 0.3::numeric
where exists (select 1 from public.diseases where id = 'hepatitis_b')
  and exists (select 1 from public.symptoms where id = 'sym_edema')
  and not exists (select 1 from public.disease_symptoms where disease_id = 'hepatitis_b' and symptom_id = 'sym_edema');

-- ================================================ sym_anorexia  (Loss of appetite)
update public.symptoms set description = 'Loss of appetite is a reduced desire to eat; the medical term is anorexia (distinct from the eating disorder anorexia nervosa). It accompanies many acute infections as well as chronic, malignant, psychiatric and medicine-related conditions. Weight loss with a poor appetite most often comes from depression, cancer, medicine side effects or substance use, whereas weight loss despite a good appetite suggests hyperthyroidism, uncontrolled diabetes or malabsorption.', updated_at = now()
where id = 'sym_anorexia' and description = 'Loss of appetite is a reduced desire to eat; the medical term is anorexia (distinct from the eating disorder anorexia nervosa). It accompanies many acute infections as well as chronic, malignant, psychiatric and medicine-related conditions.';
update public.symptoms set tags = tags || array['weight loss']::text[]
where id = 'sym_anorexia' and not (tags @> array['weight loss']::text[]);
update public.symptoms set source_attribution = source_attribution || '; Merck Manual Professional - Involuntary Weight Loss'
where id = 'sym_anorexia' and position('Merck Manual Professional - Involuntary Weight Loss' in source_attribution) = 0;
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_anorexia', 'Substance use', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_anorexia'), 0)
where exists (select 1 from public.symptoms where id = 'sym_anorexia')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_anorexia' and content = 'Substance use');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_anorexia', 'Malaria', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_anorexia'), 0)
where exists (select 1 from public.symptoms where id = 'sym_anorexia')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_anorexia' and content = 'Malaria');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_anorexia', 'HIV infection', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_anorexia'), 0)
where exists (select 1 from public.symptoms where id = 'sym_anorexia')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_anorexia' and content = 'HIV infection');
insert into public.symptom_red_flags (symptom_id, content, position)
select 'sym_anorexia', 'Swollen lymph nodes, bone pain or coughing blood', coalesce((select max(position) + 1 from public.symptom_red_flags where symptom_id = 'sym_anorexia'), 0)
where exists (select 1 from public.symptoms where id = 'sym_anorexia')
  and not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_anorexia' and content = 'Swollen lymph nodes, bone pain or coughing blood');
insert into public.symptom_red_flags (symptom_id, content, position)
select 'sym_anorexia', 'Fear of weight gain in a young person (possible eating disorder)', coalesce((select max(position) + 1 from public.symptom_red_flags where symptom_id = 'sym_anorexia'), 0)
where exists (select 1 from public.symptoms where id = 'sym_anorexia')
  and not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_anorexia' and content = 'Fear of weight gain in a young person (possible eating disorder)');
insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select 'sym_anorexia', 'Merck Manual Professional - Involuntary Weight Loss', 'Wasserman MR. Involuntary Weight Loss. Merck Manual Professional Version. Rahway (NJ): Merck & Co.; reviewed Feb 2025 (updated Jan 2026).', 'https://www.merckmanuals.com/professional/special-subjects/nonspecific-symptoms/involuntary-weight-loss', false, coalesce((select max(position) + 1 from public.symptom_references where symptom_id = 'sym_anorexia'), 0)
where exists (select 1 from public.symptoms where id = 'sym_anorexia')
  and not exists (select 1 from public.symptom_references where symptom_id = 'sym_anorexia' and url = 'https://www.merckmanuals.com/professional/special-subjects/nonspecific-symptoms/involuntary-weight-loss');
insert into public.disease_symptoms (disease_id, symptom_id, typical_intensity, is_primary, weight_multiplier)
select 'malaria', 'sym_anorexia', 3::smallint, false, 0.4::numeric
where exists (select 1 from public.diseases where id = 'malaria')
  and exists (select 1 from public.symptoms where id = 'sym_anorexia')
  and not exists (select 1 from public.disease_symptoms where disease_id = 'malaria' and symptom_id = 'sym_anorexia');
insert into public.disease_symptoms (disease_id, symptom_id, typical_intensity, is_primary, weight_multiplier)
select 'hiv_infection', 'sym_anorexia', 3::smallint, false, 0.4::numeric
where exists (select 1 from public.diseases where id = 'hiv_infection')
  and exists (select 1 from public.symptoms where id = 'sym_anorexia')
  and not exists (select 1 from public.disease_symptoms where disease_id = 'hiv_infection' and symptom_id = 'sym_anorexia');

-- ================================================ sym_anosmia  (Loss of smell or taste)
update public.symptoms set description = 'Anosmia is partial or total loss of the sense of smell, and ageusia or dysgeusia refers to loss or distortion of taste; because flavour depends largely on smell, the two are often reported together. Sudden loss of smell is a recognised feature of viral upper respiratory infections, notably COVID-19. Most people with anosmia can still taste salty, sweet, sour and bitter but report a loss of taste because flavour depends on smell. Head injury is the main cause in young adults and Alzheimer disease in older adults, and smell loss persists after an upper respiratory infection in a minority of people.', updated_at = now()
where id = 'sym_anosmia' and description = 'Anosmia is partial or total loss of the sense of smell, and ageusia or dysgeusia refers to loss or distortion of taste; because flavour depends largely on smell, the two are often reported together. Sudden loss of smell is a recognised feature of viral upper respiratory infections, notably COVID-19.';
update public.symptoms set tags = tags || array['dysgeusia']::text[]
where id = 'sym_anosmia' and not (tags @> array['dysgeusia']::text[]);
update public.symptoms set source_attribution = source_attribution || '; Merck Manual Professional - Anosmia'
where id = 'sym_anosmia' and position('Merck Manual Professional - Anosmia' in source_attribution) = 0;
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_anosmia', 'Alzheimer disease (older adults)', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_anosmia'), 0)
where exists (select 1 from public.symptoms where id = 'sym_anosmia')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_anosmia' and content = 'Alzheimer disease (older adults)');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_anosmia', 'Medicines and toxins', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_anosmia'), 0)
where exists (select 1 from public.symptoms where id = 'sym_anosmia')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_anosmia' and content = 'Medicines and toxins');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_anosmia', 'Radiation or nasal surgery', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_anosmia'), 0)
where exists (select 1 from public.symptoms where id = 'sym_anosmia')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_anosmia' and content = 'Radiation or nasal surgery');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_anosmia', 'Influenza', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_anosmia'), 0)
where exists (select 1 from public.symptoms where id = 'sym_anosmia')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_anosmia' and content = 'Influenza');
insert into public.symptom_red_flags (symptom_id, content, position)
select 'sym_anosmia', 'Sudden loss of smell', coalesce((select max(position) + 1 from public.symptom_red_flags where symptom_id = 'sym_anosmia'), 0)
where exists (select 1 from public.symptoms where id = 'sym_anosmia')
  and not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_anosmia' and content = 'Sudden loss of smell');
insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select 'sym_anosmia', 'Merck Manual Professional - Anosmia', 'Fried MP. Anosmia. Merck Manual Professional Version. Rahway (NJ): Merck & Co.; reviewed Mar 2025 (updated Sep 2026).', 'https://www.merckmanuals.com/professional/ear-nose-and-throat-disorders/approach-to-the-patient-with-nasal-and-pharyngeal-symptoms/anosmia', false, coalesce((select max(position) + 1 from public.symptom_references where symptom_id = 'sym_anosmia'), 0)
where exists (select 1 from public.symptoms where id = 'sym_anosmia')
  and not exists (select 1 from public.symptom_references where symptom_id = 'sym_anosmia' and url = 'https://www.merckmanuals.com/professional/ear-nose-and-throat-disorders/approach-to-the-patient-with-nasal-and-pharyngeal-symptoms/anosmia');
insert into public.disease_symptoms (disease_id, symptom_id, typical_intensity, is_primary, weight_multiplier)
select 'influenza', 'sym_anosmia', 2::smallint, false, 0.3::numeric
where exists (select 1 from public.diseases where id = 'influenza')
  and exists (select 1 from public.symptoms where id = 'sym_anosmia')
  and not exists (select 1 from public.disease_symptoms where disease_id = 'influenza' and symptom_id = 'sym_anosmia');

-- ================================================ sym_bleeding  (Mucosal bleeding / petechiae (gum bleeding, nosebleed))
update public.symptoms set description = 'Mucocutaneous bleeding includes petechiae (pinpoint red dots from capillary bleeding), bruising, nosebleeds (epistaxis) and gum bleeding. In dengue, minor mucocutaneous bleeding may occur, and mucosal bleeding is listed as a warning sign of severe dengue; it also reflects thrombocytopenia or coagulation disorders. Bleeding into the skin and mucous membranes with petechiae suggests a platelet or blood-vessel problem, while deep bleeding into joints and muscles suggests a clotting-factor disorder. The first tests are a full blood count, blood smear, PT and aPTT.', updated_at = now()
where id = 'sym_bleeding' and description = 'Mucocutaneous bleeding includes petechiae (pinpoint red dots from capillary bleeding), bruising, nosebleeds (epistaxis) and gum bleeding. In dengue, minor mucocutaneous bleeding may occur, and mucosal bleeding is listed as a warning sign of severe dengue; it also reflects thrombocytopenia or coagulation disorders.';
update public.symptoms set tags = tags || array['thrombocytopenia']::text[]
where id = 'sym_bleeding' and not (tags @> array['thrombocytopenia']::text[]);
update public.symptoms set source_attribution = source_attribution || '; Merck Manual Professional - Excessive Bleeding'
where id = 'sym_bleeding' and position('Merck Manual Professional - Excessive Bleeding' in source_attribution) = 0;
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_bleeding', 'Disseminated intravascular coagulation (DIC) in sepsis', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_bleeding'), 0)
where exists (select 1 from public.symptoms where id = 'sym_bleeding')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_bleeding' and content = 'Disseminated intravascular coagulation (DIC) in sepsis');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_bleeding', 'Kidney failure (uremic platelet dysfunction)', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_bleeding'), 0)
where exists (select 1 from public.symptoms where id = 'sym_bleeding')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_bleeding' and content = 'Kidney failure (uremic platelet dysfunction)');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_bleeding', 'Von Willebrand disease', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_bleeding'), 0)
where exists (select 1 from public.symptoms where id = 'sym_bleeding')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_bleeding' and content = 'Von Willebrand disease');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_bleeding', 'NSAIDs and aspirin', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_bleeding'), 0)
where exists (select 1 from public.symptoms where id = 'sym_bleeding')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_bleeding' and content = 'NSAIDs and aspirin');
insert into public.symptom_red_flags (symptom_id, content, position)
select 'sym_bleeding', 'Bleeding in pregnancy', coalesce((select max(position) + 1 from public.symptom_red_flags where symptom_id = 'sym_bleeding'), 0)
where exists (select 1 from public.symptoms where id = 'sym_bleeding')
  and not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_bleeding' and content = 'Bleeding in pregnancy');
insert into public.symptom_red_flags (symptom_id, content, position)
select 'sym_bleeding', 'Bloody diarrhea with low platelets (possible hemolytic uremic syndrome)', coalesce((select max(position) + 1 from public.symptom_red_flags where symptom_id = 'sym_bleeding'), 0)
where exists (select 1 from public.symptoms where id = 'sym_bleeding')
  and not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_bleeding' and content = 'Bloody diarrhea with low platelets (possible hemolytic uremic syndrome)');
insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select 'sym_bleeding', 'Merck Manual Professional - Excessive Bleeding', 'Streiff MB. Excessive Bleeding. Merck Manual Professional Version. Rahway (NJ): Merck & Co.; reviewed Sep 2025.', 'https://www.merckmanuals.com/professional/hematology-and-oncology/hemostasis/excessive-bleeding', false, coalesce((select max(position) + 1 from public.symptom_references where symptom_id = 'sym_bleeding'), 0)
where exists (select 1 from public.symptoms where id = 'sym_bleeding')
  and not exists (select 1 from public.symptom_references where symptom_id = 'sym_bleeding' and url = 'https://www.merckmanuals.com/professional/hematology-and-oncology/hemostasis/excessive-bleeding');
insert into public.disease_symptoms (disease_id, symptom_id, typical_intensity, is_primary, weight_multiplier)
select 'leptospirosis', 'sym_bleeding', 3::smallint, false, 0.5::numeric
where exists (select 1 from public.diseases where id = 'leptospirosis')
  and exists (select 1 from public.symptoms where id = 'sym_bleeding')
  and not exists (select 1 from public.disease_symptoms where disease_id = 'leptospirosis' and symptom_id = 'sym_bleeding');
insert into public.disease_symptoms (disease_id, symptom_id, typical_intensity, is_primary, weight_multiplier)
select 'chronic_kidney_disease', 'sym_bleeding', 2::smallint, false, 0.3::numeric
where exists (select 1 from public.diseases where id = 'chronic_kidney_disease')
  and exists (select 1 from public.symptoms where id = 'sym_bleeding')
  and not exists (select 1 from public.disease_symptoms where disease_id = 'chronic_kidney_disease' and symptom_id = 'sym_bleeding');

update public.content_version set version = version + 1, updated_at = now() where id = 1;

commit;

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

-- 029_symptoms_review_09.sql  -  symptom review, session 09: 16 symptoms
-- Adds only: longer descriptions, extra causes, red flags, references and disease links.
-- Nothing is deleted or replaced. Safe to run twice (every insert is guarded).
-- A description is only extended if it is still the exported text (your own edits are kept).

begin;

-- ================================================ sym_koilonychia  (Spoon-shaped, brittle nails (koilonychia))
update public.symptoms set description = 'Thin, brittle nails that become flat and then concave, so that the nail can hold a drop of water (spoon nails). It is classically linked to chronic iron deficiency, and can be normal in infants or follow trauma and occupational exposure. It appears in severe iron deficiency together with pica, a smooth sore tongue and cracks at the mouth corners. Iron deficiency is mostly due to blood loss, so in men and women past menopause the bowel is checked for hidden bleeding, which can be the only sign of a gut cancer.', updated_at = now()
where id = 'sym_koilonychia' and description = 'Thin, brittle nails that become flat and then concave, so that the nail can hold a drop of water (spoon nails). It is classically linked to chronic iron deficiency, and can be normal in infants or follow trauma and occupational exposure.';
update public.symptoms set tags = tags || array['spoon nails']::text[]
where id = 'sym_koilonychia' and not (tags @> array['spoon nails']::text[]);
update public.symptoms set source_attribution = source_attribution || '; Merck Manual Professional - Iron Deficiency Anemia'
where id = 'sym_koilonychia' and position('Merck Manual Professional - Iron Deficiency Anemia' in source_attribution) = 0;
insert into public.symptom_red_flags (symptom_id, content, position)
select 'sym_koilonychia', 'Iron deficiency in a man or a woman past menopause (look for bowel bleeding)', coalesce((select max(position) + 1 from public.symptom_red_flags where symptom_id = 'sym_koilonychia'), 0)
where exists (select 1 from public.symptoms where id = 'sym_koilonychia')
  and not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_koilonychia' and content = 'Iron deficiency in a man or a woman past menopause (look for bowel bleeding)');
insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select 'sym_koilonychia', 'Merck Manual Professional - Iron Deficiency Anemia', 'Gerber GF. Iron Deficiency Anemia. Merck Manual Professional Version. Rahway (NJ): Merck & Co.; reviewed Mar 2025.', 'https://www.merckmanuals.com/professional/hematology-and-oncology/anemias-caused-by-deficient-erythropoiesis/iron-deficiency-anemia', false, coalesce((select max(position) + 1 from public.symptom_references where symptom_id = 'sym_koilonychia'), 0)
where exists (select 1 from public.symptoms where id = 'sym_koilonychia')
  and not exists (select 1 from public.symptom_references where symptom_id = 'sym_koilonychia' and url = 'https://www.merckmanuals.com/professional/hematology-and-oncology/anemias-caused-by-deficient-erythropoiesis/iron-deficiency-anemia');

-- ================================================ sym_neck_stiffness  (Stiff neck (neck stiffness))
update public.symptoms set description = 'Pain and resistance when bending the chin toward the chest, caused by irritation of the meninges. Together with fever and headache or confusion it is a classic sign of meningitis; Kernig and Brudzinski signs test the same irritation. Muscle strain and neck arthritis also cause stiffness, but usually without fever. Fever and neck stiffness may be missing in newborns, infants, older adults, people with weak immunity and heavy drinkers, so a lumbar puncture should be considered early. Bacterial meningitis is an emergency: antibiotics (with steroids) are given within 30 minutes, and brain imaging comes before the lumbar puncture only if there is papilledema or a focal deficit.', updated_at = now()
where id = 'sym_neck_stiffness' and description = 'Pain and resistance when bending the chin toward the chest, caused by irritation of the meninges. Together with fever and headache or confusion it is a classic sign of meningitis; Kernig and Brudzinski signs test the same irritation. Muscle strain and neck arthritis also cause stiffness, but usually without fever.';
update public.symptoms set tags = tags || array['lumbar puncture']::text[]
where id = 'sym_neck_stiffness' and not (tags @> array['lumbar puncture']::text[]);
update public.symptoms set source_attribution = source_attribution || '; Merck Manual Professional - Acute Bacterial Meningitis'
where id = 'sym_neck_stiffness' and position('Merck Manual Professional - Acute Bacterial Meningitis' in source_attribution) = 0;
insert into public.symptom_red_flags (symptom_id, content, position)
select 'sym_neck_stiffness', 'Fever with drowsiness in an infant or older adult, even without a stiff neck', coalesce((select max(position) + 1 from public.symptom_red_flags where symptom_id = 'sym_neck_stiffness'), 0)
where exists (select 1 from public.symptoms where id = 'sym_neck_stiffness')
  and not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_neck_stiffness' and content = 'Fever with drowsiness in an infant or older adult, even without a stiff neck');
insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select 'sym_neck_stiffness', 'Merck Manual Professional - Acute Bacterial Meningitis', 'Klein RS. Acute Bacterial Meningitis. Merck Manual Professional Version. Rahway (NJ): Merck & Co.; reviewed Sep 2026.', 'https://www.merckmanuals.com/professional/neurologic-disorders/meningitis/acute-bacterial-meningitis', false, coalesce((select max(position) + 1 from public.symptom_references where symptom_id = 'sym_neck_stiffness'), 0)
where exists (select 1 from public.symptoms where id = 'sym_neck_stiffness')
  and not exists (select 1 from public.symptom_references where symptom_id = 'sym_neck_stiffness' and url = 'https://www.merckmanuals.com/professional/neurologic-disorders/meningitis/acute-bacterial-meningitis');

-- ================================================ sym_podagra  (Sudden hot, red, swollen big-toe joint (podagra))
update public.symptoms set description = 'Acute inflammation of the joint at the base of the big toe (first metatarsophalangeal joint), with severe pain, swelling, redness and warmth that peak within 24 hours, often starting at night. It is the most typical first presentation of gout; septic arthritis must be considered if there is fever or the person is unwell. Common triggers are injury, surgery, infection, thiazide diuretics, starting urate-lowering drugs, purine-rich food and alcohol. Diagnosis is by finding needle-shaped, negatively birefringent urate crystals in joint fluid; the blood urate level is normal in at least 30% of people during a flare.', updated_at = now()
where id = 'sym_podagra' and description = 'Acute inflammation of the joint at the base of the big toe (first metatarsophalangeal joint), with severe pain, swelling, redness and warmth that peak within 24 hours, often starting at night. It is the most typical first presentation of gout; septic arthritis must be considered if there is fever or the person is unwell.';
update public.symptoms set tags = tags || array['urate crystals']::text[]
where id = 'sym_podagra' and not (tags @> array['urate crystals']::text[]);
update public.symptoms set source_attribution = source_attribution || '; Merck Manual Professional - Gout'
where id = 'sym_podagra' and position('Merck Manual Professional - Gout' in source_attribution) = 0;
insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select 'sym_podagra', 'Merck Manual Professional - Gout', 'Keller SF. Gout. Merck Manual Professional Version. Rahway (NJ): Merck & Co.; reviewed Jul 2025.', 'https://www.merckmanuals.com/professional/musculoskeletal-and-connective-tissue-disorders/crystal-induced-arthritides/gout', false, coalesce((select max(position) + 1 from public.symptom_references where symptom_id = 'sym_podagra'), 0)
where exists (select 1 from public.symptoms where id = 'sym_podagra')
  and not exists (select 1 from public.symptom_references where symptom_id = 'sym_podagra' and url = 'https://www.merckmanuals.com/professional/musculoskeletal-and-connective-tissue-disorders/crystal-induced-arthritides/gout');

-- ================================================ sym_suprapubic_pain  (Suprapubic pain)
update public.symptoms set description = 'Suprapubic pain is discomfort in the lower midline abdomen above the pubic bone, over the bladder. It is a typical feature of acute cystitis, and suprapubic tenderness may be found on examination. In cystitis it comes on suddenly with frequency, urgency and burning while passing small volumes. A positive nitrite test is highly specific for bacteria, and leukocyte esterase is fairly sensitive; dysuria with white cells but no bacteria suggests urethritis or an STI.', updated_at = now()
where id = 'sym_suprapubic_pain' and description = 'Suprapubic pain is discomfort in the lower midline abdomen above the pubic bone, over the bladder. It is a typical feature of acute cystitis, and suprapubic tenderness may be found on examination.';
update public.symptoms set tags = tags || array['cystitis']::text[]
where id = 'sym_suprapubic_pain' and not (tags @> array['cystitis']::text[]);
update public.symptoms set source_attribution = source_attribution || '; Merck Manual Professional - Bacterial Urinary Tract Infections'
where id = 'sym_suprapubic_pain' and position('Merck Manual Professional - Bacterial Urinary Tract Infections' in source_attribution) = 0;
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_suprapubic_pain', 'Prostatitis', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_suprapubic_pain'), 0)
where exists (select 1 from public.symptoms where id = 'sym_suprapubic_pain')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_suprapubic_pain' and content = 'Prostatitis');
insert into public.symptom_red_flags (symptom_id, content, position)
select 'sym_suprapubic_pain', 'Repeated infections, or symptoms in a man', coalesce((select max(position) + 1 from public.symptom_red_flags where symptom_id = 'sym_suprapubic_pain'), 0)
where exists (select 1 from public.symptoms where id = 'sym_suprapubic_pain')
  and not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_suprapubic_pain' and content = 'Repeated infections, or symptoms in a man');
insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select 'sym_suprapubic_pain', 'Merck Manual Professional - Bacterial Urinary Tract Infections', 'Imam TH. Bacterial Urinary Tract Infections. Merck Manual Professional Version. Rahway (NJ): Merck & Co.; reviewed Mar 2026.', 'https://www.merckmanuals.com/professional/infectious-diseases/urinary-tract-infections/bacterial-urinary-tract-infections', false, coalesce((select max(position) + 1 from public.symptom_references where symptom_id = 'sym_suprapubic_pain'), 0)
where exists (select 1 from public.symptoms where id = 'sym_suprapubic_pain')
  and not exists (select 1 from public.symptom_references where symptom_id = 'sym_suprapubic_pain' and url = 'https://www.merckmanuals.com/professional/infectious-diseases/urinary-tract-infections/bacterial-urinary-tract-infections');

-- ================================================ sym_diaphoresis  (Sweating (diaphoresis))
update public.symptoms set description = 'Diaphoresis is profuse sweating out of proportion to temperature or activity. It accompanies fever and its defervescence, and cold sweats occur with sympathetic activation in acute coronary syndrome, hypoglycemia, shock and pain. Generalised sweating can come from lymphoma or leukemia, tuberculosis, endocarditis, hyperthyroidism, low blood sugar, drugs, opioid withdrawal and menopause. Sweating that is mainly at night points to cancer or infection, and sweating on only one side suggests a nerve problem.', updated_at = now()
where id = 'sym_diaphoresis' and description = 'Diaphoresis is profuse sweating out of proportion to temperature or activity. It accompanies fever and its defervescence, and cold sweats occur with sympathetic activation in acute coronary syndrome, hypoglycemia, shock and pain.';
update public.symptoms set tags = tags || array['hyperhidrosis']::text[]
where id = 'sym_diaphoresis' and not (tags @> array['hyperhidrosis']::text[]);
update public.symptoms set source_attribution = source_attribution || '; Merck Manual Professional - Hyperhidrosis'
where id = 'sym_diaphoresis' and position('Merck Manual Professional - Hyperhidrosis' in source_attribution) = 0;
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_diaphoresis', 'Tuberculosis', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_diaphoresis'), 0)
where exists (select 1 from public.symptoms where id = 'sym_diaphoresis')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_diaphoresis' and content = 'Tuberculosis');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_diaphoresis', 'Lymphoma or leukemia', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_diaphoresis'), 0)
where exists (select 1 from public.symptoms where id = 'sym_diaphoresis')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_diaphoresis' and content = 'Lymphoma or leukemia');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_diaphoresis', 'Endocarditis', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_diaphoresis'), 0)
where exists (select 1 from public.symptoms where id = 'sym_diaphoresis')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_diaphoresis' and content = 'Endocarditis');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_diaphoresis', 'Opioid or alcohol withdrawal', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_diaphoresis'), 0)
where exists (select 1 from public.symptoms where id = 'sym_diaphoresis')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_diaphoresis' and content = 'Opioid or alcohol withdrawal');
insert into public.symptom_red_flags (symptom_id, content, position)
select 'sym_diaphoresis', 'Sweating on only one side of the body', coalesce((select max(position) + 1 from public.symptom_red_flags where symptom_id = 'sym_diaphoresis'), 0)
where exists (select 1 from public.symptoms where id = 'sym_diaphoresis')
  and not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_diaphoresis' and content = 'Sweating on only one side of the body');
insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select 'sym_diaphoresis', 'Merck Manual Professional - Hyperhidrosis', 'Das S. Hyperhidrosis. Merck Manual Professional Version. Rahway (NJ): Merck & Co.; reviewed Jun 2026.', 'https://www.merckmanuals.com/professional/dermatologic-disorders/sweating-disorders/hyperhidrosis', false, coalesce((select max(position) + 1 from public.symptom_references where symptom_id = 'sym_diaphoresis'), 0)
where exists (select 1 from public.symptoms where id = 'sym_diaphoresis')
  and not exists (select 1 from public.symptom_references where symptom_id = 'sym_diaphoresis' and url = 'https://www.merckmanuals.com/professional/dermatologic-disorders/sweating-disorders/hyperhidrosis');
insert into public.disease_symptoms (disease_id, symptom_id, typical_intensity, is_primary, weight_multiplier)
select 'tuberculosis', 'sym_diaphoresis', 2::smallint, false, 0.3::numeric
where exists (select 1 from public.diseases where id = 'tuberculosis')
  and exists (select 1 from public.symptoms where id = 'sym_diaphoresis')
  and not exists (select 1 from public.disease_symptoms where disease_id = 'tuberculosis' and symptom_id = 'sym_diaphoresis');

-- ================================================ sym_goiter  (Swelling at the front of the neck (goiter))
update public.symptoms set description = 'Enlargement of the thyroid gland, seen or felt as a swelling at the front of the neck that moves up on swallowing. It may be diffuse (Graves disease, iodine deficiency, thyroiditis) or nodular, and thyroid function can be high, normal or low. Iodine deficiency is the leading cause worldwide. Most goiters cause no symptoms, but large ones can cause swallowing difficulty, hoarseness or a feeling of fullness in the throat; assessment uses thyroid function tests, ultrasound, thyroid antibodies and sometimes an iodine uptake scan.', updated_at = now()
where id = 'sym_goiter' and description = 'Enlargement of the thyroid gland, seen or felt as a swelling at the front of the neck that moves up on swallowing. It may be diffuse (Graves disease, iodine deficiency, thyroiditis) or nodular, and thyroid function can be high, normal or low.';
update public.symptoms set tags = tags || array['iodine deficiency']::text[]
where id = 'sym_goiter' and not (tags @> array['iodine deficiency']::text[]);
update public.symptoms set source_attribution = source_attribution || '; Merck Manual Professional - Simple Nontoxic Goiter'
where id = 'sym_goiter' and position('Merck Manual Professional - Simple Nontoxic Goiter' in source_attribution) = 0;
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_goiter', 'Goitrogens in food (cassava, cruciferous vegetables)', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_goiter'), 0)
where exists (select 1 from public.symptoms where id = 'sym_goiter')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_goiter' and content = 'Goitrogens in food (cassava, cruciferous vegetables)');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_goiter', 'Amiodarone or lithium', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_goiter'), 0)
where exists (select 1 from public.symptoms where id = 'sym_goiter')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_goiter' and content = 'Amiodarone or lithium');
insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select 'sym_goiter', 'Merck Manual Professional - Simple Nontoxic Goiter', 'Boucai L. Simple Nontoxic Goiter. Merck Manual Professional Version. Rahway (NJ): Merck & Co.; reviewed Jan 2026.', 'https://www.merckmanuals.com/professional/endocrine-and-metabolic-disorders/thyroid-disorders/simple-nontoxic-goiter', false, coalesce((select max(position) + 1 from public.symptom_references where symptom_id = 'sym_goiter'), 0)
where exists (select 1 from public.symptoms where id = 'sym_goiter')
  and not exists (select 1 from public.symptom_references where symptom_id = 'sym_goiter' and url = 'https://www.merckmanuals.com/professional/endocrine-and-metabolic-disorders/thyroid-disorders/simple-nontoxic-goiter');

-- ================================================ sym_lymphadenopathy  (Swollen lymph nodes (lymphadenopathy))
update public.symptoms set description = 'Lymphadenopathy is enlargement of lymph nodes in size, consistency or number, localized to one region or generalized across two or more non-contiguous regions. Most is reactive to infection, but size, consistency, fixation, location (especially supraclavicular) and duration help separate benign from malignant or systemic causes. Nodes in one area for less than 2 weeks are usually from a local infection, while nodes in several areas suggest a systemic illness such as mononucleosis, lymphoma or lupus. Without red flags, nodes can be watched for up to 4 weeks; steroids should not be given empirically because they can mask lymphoma or leukemia.', updated_at = now()
where id = 'sym_lymphadenopathy' and description = 'Lymphadenopathy is enlargement of lymph nodes in size, consistency or number, localized to one region or generalized across two or more non-contiguous regions. Most is reactive to infection, but size, consistency, fixation, location (especially supraclavicular) and duration help separate benign from malignant or systemic causes.';
update public.symptoms set tags = tags || array['supraclavicular']::text[]
where id = 'sym_lymphadenopathy' and not (tags @> array['supraclavicular']::text[]);
update public.symptoms set source_attribution = source_attribution || '; Merck Manual Professional - Lymphadenopathy'
where id = 'sym_lymphadenopathy' and position('Merck Manual Professional - Lymphadenopathy' in source_attribution) = 0;
insert into public.symptom_red_flags (symptom_id, content, position)
select 'sym_lymphadenopathy', 'A node larger than 2 cm, or an enlarged spleen', coalesce((select max(position) + 1 from public.symptom_red_flags where symptom_id = 'sym_lymphadenopathy'), 0)
where exists (select 1 from public.symptoms where id = 'sym_lymphadenopathy')
  and not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_lymphadenopathy' and content = 'A node larger than 2 cm, or an enlarged spleen');
insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select 'sym_lymphadenopathy', 'Merck Manual Professional - Lymphadenopathy', 'Douketis JD. Lymphadenopathy. Merck Manual Professional Version. Rahway (NJ): Merck & Co.; reviewed Mar 2026.', 'https://www.merckmanuals.com/professional/cardiovascular-disorders/lymphatic-disorders/lymphadenopathy', false, coalesce((select max(position) + 1 from public.symptom_references where symptom_id = 'sym_lymphadenopathy'), 0)
where exists (select 1 from public.symptoms where id = 'sym_lymphadenopathy')
  and not exists (select 1 from public.symptom_references where symptom_id = 'sym_lymphadenopathy' and url = 'https://www.merckmanuals.com/professional/cardiovascular-disorders/lymphatic-disorders/lymphadenopathy');
insert into public.disease_symptoms (disease_id, symptom_id, typical_intensity, is_primary, weight_multiplier)
select 'tuberculosis', 'sym_lymphadenopathy', 3::smallint, false, 0.4::numeric
where exists (select 1 from public.diseases where id = 'tuberculosis')
  and exists (select 1 from public.symptoms where id = 'sym_lymphadenopathy')
  and not exists (select 1 from public.disease_symptoms where disease_id = 'tuberculosis' and symptom_id = 'sym_lymphadenopathy');

-- ================================================ sym_burrows  (Thin wavy lines between fingers or on wrists (burrows))
update public.symptoms set description = 'Short, thread-like, grey or skin-colored wavy lines a few millimetres long, made by the scabies mite tunneling in the top layer of skin. They are found mainly in the finger webs, wrists, elbows, belt line, genitals and, in infants, palms and soles, with intense itching that is worse at night. Itching usually starts 4 to 6 weeks after a first infestation (sooner on re-infestation), and the face is spared in adults. Scrapings from a burrow can show the mite under a microscope, though a negative result does not rule scabies out; dermoscopy shows a ''delta-wing jet'' sign.', updated_at = now()
where id = 'sym_burrows' and description = 'Short, thread-like, grey or skin-colored wavy lines a few millimetres long, made by the scabies mite tunneling in the top layer of skin. They are found mainly in the finger webs, wrists, elbows, belt line, genitals and, in infants, palms and soles, with intense itching that is worse at night.';
update public.symptoms set tags = tags || array['dermoscopy']::text[]
where id = 'sym_burrows' and not (tags @> array['dermoscopy']::text[]);
update public.symptoms set source_attribution = source_attribution || '; Merck Manual Professional - Scabies'
where id = 'sym_burrows' and position('Merck Manual Professional - Scabies' in source_attribution) = 0;
insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select 'sym_burrows', 'Merck Manual Professional - Scabies', 'Dinulos JGH. Scabies. Merck Manual Professional Version. Rahway (NJ): Merck & Co.; reviewed Nov 2025.', 'https://www.merckmanuals.com/professional/dermatologic-disorders/parasitic-skin-infections/scabies', false, coalesce((select max(position) + 1 from public.symptom_references where symptom_id = 'sym_burrows'), 0)
where exists (select 1 from public.symptoms where id = 'sym_burrows')
  and not exists (select 1 from public.symptom_references where symptom_id = 'sym_burrows' and url = 'https://www.merckmanuals.com/professional/dermatologic-disorders/parasitic-skin-infections/scabies');

-- ================================================ sym_weight_loss  (Unintentional weight loss)
update public.symptoms set description = 'Unintentional weight loss is a decrease in body weight that occurs without deliberate dieting or exercise. Clinically significant loss (commonly defined as more than 5% of body weight over 6-12 months) warrants evaluation for malignancy, chronic infection, endocrine and gastrointestinal disease. Weight loss despite a good appetite suggests hyperthyroidism, uncontrolled diabetes or malabsorption, while weight loss with a poor appetite suggests depression, cancer or medicines. Baseline tests usually include a chest X-ray, urinalysis, blood count, ESR or CRP, HIV test, chemistry and TSH.', updated_at = now()
where id = 'sym_weight_loss' and description = 'Unintentional weight loss is a decrease in body weight that occurs without deliberate dieting or exercise. Clinically significant loss (commonly defined as more than 5% of body weight over 6-12 months) warrants evaluation for malignancy, chronic infection, endocrine and gastrointestinal disease.';
update public.symptoms set tags = tags || array['cachexia']::text[]
where id = 'sym_weight_loss' and not (tags @> array['cachexia']::text[]);
update public.symptoms set source_attribution = source_attribution || '; Merck Manual Professional - Involuntary Weight Loss'
where id = 'sym_weight_loss' and position('Merck Manual Professional - Involuntary Weight Loss' in source_attribution) = 0;
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_weight_loss', 'Medicines', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_weight_loss'), 0)
where exists (select 1 from public.symptoms where id = 'sym_weight_loss')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_weight_loss' and content = 'Medicines');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_weight_loss', 'Substance use', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_weight_loss'), 0)
where exists (select 1 from public.symptoms where id = 'sym_weight_loss')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_weight_loss' and content = 'Substance use');
insert into public.symptom_red_flags (symptom_id, content, position)
select 'sym_weight_loss', 'Bone pain or swollen lymph nodes', coalesce((select max(position) + 1 from public.symptom_red_flags where symptom_id = 'sym_weight_loss'), 0)
where exists (select 1 from public.symptoms where id = 'sym_weight_loss')
  and not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_weight_loss' and content = 'Bone pain or swollen lymph nodes');
insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select 'sym_weight_loss', 'Merck Manual Professional - Involuntary Weight Loss', 'Wasserman MR. Involuntary Weight Loss. Merck Manual Professional Version. Rahway (NJ): Merck & Co.; reviewed Feb 2025.', 'https://www.merckmanuals.com/professional/special-subjects/nonspecific-symptoms/involuntary-weight-loss', false, coalesce((select max(position) + 1 from public.symptom_references where symptom_id = 'sym_weight_loss'), 0)
where exists (select 1 from public.symptoms where id = 'sym_weight_loss')
  and not exists (select 1 from public.symptom_references where symptom_id = 'sym_weight_loss' and url = 'https://www.merckmanuals.com/professional/special-subjects/nonspecific-symptoms/involuntary-weight-loss');

-- ================================================ sym_urinary_frequency  (Urinary frequency & urgency)
update public.symptoms set description = 'Urinary frequency is the need to urinate more often than usual, and urgency is a sudden, strong need to urinate. Together they are typical of bladder irritation from infection, but also occur with overactive bladder, prostatic enlargement, pregnancy and diabetes. Frequency means passing normal or small volumes often, unlike polyuria, where the total volume is over 3 L a day. Getting up at night with a weak stream suggests prostate enlargement.', updated_at = now()
where id = 'sym_urinary_frequency' and description = 'Urinary frequency is the need to urinate more often than usual, and urgency is a sudden, strong need to urinate. Together they are typical of bladder irritation from infection, but also occur with overactive bladder, prostatic enlargement, pregnancy and diabetes.';
update public.symptoms set tags = tags || array['overactive bladder']::text[]
where id = 'sym_urinary_frequency' and not (tags @> array['overactive bladder']::text[]);
update public.symptoms set source_attribution = source_attribution || '; Merck Manual Professional - Urinary Frequency'
where id = 'sym_urinary_frequency' and position('Merck Manual Professional - Urinary Frequency' in source_attribution) = 0;
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_urinary_frequency', 'Kidney or bladder stones', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_urinary_frequency'), 0)
where exists (select 1 from public.symptoms where id = 'sym_urinary_frequency')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_urinary_frequency' and content = 'Kidney or bladder stones');
insert into public.symptom_red_flags (symptom_id, content, position)
select 'sym_urinary_frequency', 'Leg weakness, numbness around the buttocks or loss of bladder control (possible spinal cord compression)', coalesce((select max(position) + 1 from public.symptom_red_flags where symptom_id = 'sym_urinary_frequency'), 0)
where exists (select 1 from public.symptoms where id = 'sym_urinary_frequency')
  and not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_urinary_frequency' and content = 'Leg weakness, numbness around the buttocks or loss of bladder control (possible spinal cord compression)');
insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select 'sym_urinary_frequency', 'Merck Manual Professional - Urinary Frequency', 'Maddukuri G. Urinary Frequency. Merck Manual Professional Version. Rahway (NJ): Merck & Co.; reviewed Sep 2024.', 'https://www.merckmanuals.com/professional/genitourinary-disorders/symptoms-of-genitourinary-disorders/urinary-frequency', false, coalesce((select max(position) + 1 from public.symptom_references where symptom_id = 'sym_urinary_frequency'), 0)
where exists (select 1 from public.symptoms where id = 'sym_urinary_frequency')
  and not exists (select 1 from public.symptom_references where symptom_id = 'sym_urinary_frequency' and url = 'https://www.merckmanuals.com/professional/genitourinary-disorders/symptoms-of-genitourinary-disorders/urinary-frequency');
insert into public.disease_symptoms (disease_id, symptom_id, typical_intensity, is_primary, weight_multiplier)
select 'type2_diabetes', 'sym_urinary_frequency', 3::smallint, false, 0.4::numeric
where exists (select 1 from public.diseases where id = 'type2_diabetes')
  and exists (select 1 from public.symptoms where id = 'sym_urinary_frequency')
  and not exists (select 1 from public.disease_symptoms where disease_id = 'type2_diabetes' and symptom_id = 'sym_urinary_frequency');

-- ================================================ sym_visual_aura  (Visual aura)
update public.symptoms set description = 'A visual aura is a transient, fully reversible visual disturbance that develops gradually over at least 5 minutes and lasts up to 60 minutes, often preceding migraine headache. It typically begins as a small area of vision loss or bright shimmering lines (scintillating scotoma) that expands across the visual field. About a quarter of people with migraine have aura, usually before the headache and sometimes without any headache. In older adults, aura without headache can be mistaken for a transient ischemic attack.', updated_at = now()
where id = 'sym_visual_aura' and description = 'A visual aura is a transient, fully reversible visual disturbance that develops gradually over at least 5 minutes and lasts up to 60 minutes, often preceding migraine headache. It typically begins as a small area of vision loss or bright shimmering lines (scintillating scotoma) that expands across the visual field.';
update public.symptoms set tags = tags || array['scintillating scotoma']::text[]
where id = 'sym_visual_aura' and not (tags @> array['scintillating scotoma']::text[]);
update public.symptoms set source_attribution = source_attribution || '; Merck Manual Professional - Migraine'
where id = 'sym_visual_aura' and position('Merck Manual Professional - Migraine' in source_attribution) = 0;
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_visual_aura', 'Arterial dissection or vasculitis (rare mimics)', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_visual_aura'), 0)
where exists (select 1 from public.symptoms where id = 'sym_visual_aura')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_visual_aura' and content = 'Arterial dissection or vasculitis (rare mimics)');
insert into public.symptom_red_flags (symptom_id, content, position)
select 'sym_visual_aura', 'Aura with no headache in an older adult (consider TIA)', coalesce((select max(position) + 1 from public.symptom_red_flags where symptom_id = 'sym_visual_aura'), 0)
where exists (select 1 from public.symptoms where id = 'sym_visual_aura')
  and not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_visual_aura' and content = 'Aura with no headache in an older adult (consider TIA)');
insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select 'sym_visual_aura', 'Merck Manual Professional - Migraine', 'Silberstein SD. Migraine. Merck Manual Professional Version. Rahway (NJ): Merck & Co.; reviewed Feb 2025.', 'https://www.merckmanuals.com/professional/neurologic-disorders/headache/migraine', false, coalesce((select max(position) + 1 from public.symptom_references where symptom_id = 'sym_visual_aura'), 0)
where exists (select 1 from public.symptoms where id = 'sym_visual_aura')
  and not exists (select 1 from public.symptom_references where symptom_id = 'sym_visual_aura' and url = 'https://www.merckmanuals.com/professional/neurologic-disorders/headache/migraine');

-- ================================================ sym_posttussive_vomiting  (Vomiting after coughing fits (post-tussive vomiting))
update public.symptoms set description = 'Post-tussive vomiting is vomiting provoked by a severe bout of coughing, caused by the rise in intrathoracic and intra-abdominal pressure and vagal stimulation during paroxysms. It is a characteristic feature of pertussis and should prompt consideration of that diagnosis whenever vomiting follows coughing. Pertussis runs over 6 to 10 weeks; infants under 6 months are at highest risk and may have choking or blue spells instead of a whoop. Pertussis should be suspected with a cough of 2 weeks or more plus a whoop, coughing fits or vomiting after coughing, and PCR is the preferred test.', updated_at = now()
where id = 'sym_posttussive_vomiting' and description = 'Post-tussive vomiting is vomiting provoked by a severe bout of coughing, caused by the rise in intrathoracic and intra-abdominal pressure and vagal stimulation during paroxysms. It is a characteristic feature of pertussis and should prompt consideration of that diagnosis whenever vomiting follows coughing.';
update public.symptoms set tags = tags || array['whooping cough']::text[]
where id = 'sym_posttussive_vomiting' and not (tags @> array['whooping cough']::text[]);
update public.symptoms set source_attribution = source_attribution || '; Merck Manual Professional - Pertussis'
where id = 'sym_posttussive_vomiting' and position('Merck Manual Professional - Pertussis' in source_attribution) = 0;
insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select 'sym_posttussive_vomiting', 'Merck Manual Professional - Pertussis', 'Bush LM, Vazquez-Pertejo MT. Pertussis. Merck Manual Professional Version. Rahway (NJ): Merck & Co.; reviewed Jun 2024.', 'https://www.merckmanuals.com/professional/infectious-diseases/gram-negative-bacilli/pertussis', false, coalesce((select max(position) + 1 from public.symptom_references where symptom_id = 'sym_posttussive_vomiting'), 0)
where exists (select 1 from public.symptoms where id = 'sym_posttussive_vomiting')
  and not exists (select 1 from public.symptom_references where symptom_id = 'sym_posttussive_vomiting' and url = 'https://www.merckmanuals.com/professional/infectious-diseases/gram-negative-bacilli/pertussis');

-- ================================================ sym_hematemesis  (Vomiting blood (hematemesis))
update public.symptoms set description = 'Hematemesis is vomiting of fresh blood, clots or dark ''coffee-ground'' material from the upper gastrointestinal tract. It indicates bleeding proximal to the ligament of Treitz and requires assessment for hemodynamic instability. Coffee-ground vomit suggests the bleeding has slowed or stopped, whereas bright red blood suggests active bleeding. Initial care is airway protection, large IV lines, fluids and transfusion as needed, an IV proton pump inhibitor and endoscopy.', updated_at = now()
where id = 'sym_hematemesis' and description = 'Hematemesis is vomiting of fresh blood, clots or dark ''coffee-ground'' material from the upper gastrointestinal tract. It indicates bleeding proximal to the ligament of Treitz and requires assessment for hemodynamic instability.';
update public.symptoms set tags = tags || array['coffee-ground']::text[]
where id = 'sym_hematemesis' and not (tags @> array['coffee-ground']::text[]);
update public.symptoms set source_attribution = source_attribution || '; Merck Manual Professional - Overview of Gastrointestinal Bleeding'
where id = 'sym_hematemesis' and position('Merck Manual Professional - Overview of Gastrointestinal Bleeding' in source_attribution) = 0;
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_hematemesis', 'Bleeding in severe dengue', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_hematemesis'), 0)
where exists (select 1 from public.symptoms where id = 'sym_hematemesis')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_hematemesis' and content = 'Bleeding in severe dengue');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_hematemesis', 'Swallowed blood from a nosebleed', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_hematemesis'), 0)
where exists (select 1 from public.symptoms where id = 'sym_hematemesis')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_hematemesis' and content = 'Swallowed blood from a nosebleed');
insert into public.symptom_red_flags (symptom_id, content, position)
select 'sym_hematemesis', 'Pale, sweaty skin', coalesce((select max(position) + 1 from public.symptom_red_flags where symptom_id = 'sym_hematemesis'), 0)
where exists (select 1 from public.symptoms where id = 'sym_hematemesis')
  and not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_hematemesis' and content = 'Pale, sweaty skin');
insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select 'sym_hematemesis', 'Merck Manual Professional - Overview of Gastrointestinal Bleeding', 'Ansari P. Overview of Gastrointestinal Bleeding. Merck Manual Professional Version. Rahway (NJ): Merck & Co.; reviewed Jun 2025.', 'https://www.merckmanuals.com/professional/gastrointestinal-disorders/gastrointestinal-bleeding/overview-of-gastrointestinal-bleeding', false, coalesce((select max(position) + 1 from public.symptom_references where symptom_id = 'sym_hematemesis'), 0)
where exists (select 1 from public.symptoms where id = 'sym_hematemesis')
  and not exists (select 1 from public.symptom_references where symptom_id = 'sym_hematemesis' and url = 'https://www.merckmanuals.com/professional/gastrointestinal-disorders/gastrointestinal-bleeding/overview-of-gastrointestinal-bleeding');
insert into public.disease_symptoms (disease_id, symptom_id, typical_intensity, is_primary, weight_multiplier)
select 'dengue', 'sym_hematemesis', 2::smallint, false, 0.4::numeric
where exists (select 1 from public.diseases where id = 'dengue')
  and exists (select 1 from public.symptoms where id = 'sym_hematemesis')
  and not exists (select 1 from public.disease_symptoms where disease_id = 'dengue' and symptom_id = 'sym_hematemesis');
insert into public.disease_symptoms (disease_id, symptom_id, typical_intensity, is_primary, weight_multiplier)
select 'hepatitis_b', 'sym_hematemesis', 2::smallint, false, 0.3::numeric
where exists (select 1 from public.diseases where id = 'hepatitis_b')
  and exists (select 1 from public.symptoms where id = 'sym_hematemesis')
  and not exists (select 1 from public.disease_symptoms where disease_id = 'hepatitis_b' and symptom_id = 'sym_hematemesis');

-- ================================================ sym_nocturia  (Waking at night to urinate (nocturia))
update public.symptoms set description = 'Waking from sleep one or more times to pass urine. Causes include high evening fluid or caffeine intake, bladder and prostate problems, diabetes (high urine volume), heart failure (fluid shifted at night) and chronic kidney disease, in which the kidneys lose the ability to concentrate urine. Comparing how much is drunk with how much is passed (and a 24-hour urine collection if unclear) separates high urine output from frequent small voids. Troublesome nocturia often improves by drinking less in the evening.', updated_at = now()
where id = 'sym_nocturia' and description = 'Waking from sleep one or more times to pass urine. Causes include high evening fluid or caffeine intake, bladder and prostate problems, diabetes (high urine volume), heart failure (fluid shifted at night) and chronic kidney disease, in which the kidneys lose the ability to concentrate urine.';
update public.symptoms set tags = tags || array['polyuria']::text[]
where id = 'sym_nocturia' and not (tags @> array['polyuria']::text[]);
update public.symptoms set source_attribution = source_attribution || '; Merck Manual Professional - Polyuria'
where id = 'sym_nocturia' and position('Merck Manual Professional - Polyuria' in source_attribution) = 0;
insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select 'sym_nocturia', 'Merck Manual Professional - Polyuria', 'Maddukuri G. Polyuria. Merck Manual Professional Version. Rahway (NJ): Merck & Co.; reviewed Sep 2024.', 'https://www.merckmanuals.com/professional/nephrology/symptoms-of-nephrologic-disorders/polyuria', false, coalesce((select max(position) + 1 from public.symptom_references where symptom_id = 'sym_nocturia'), 0)
where exists (select 1 from public.symptoms where id = 'sym_nocturia')
  and not exists (select 1 from public.symptom_references where symptom_id = 'sym_nocturia' and url = 'https://www.merckmanuals.com/professional/nephrology/symptoms-of-nephrologic-disorders/polyuria');
insert into public.disease_symptoms (disease_id, symptom_id, typical_intensity, is_primary, weight_multiplier)
select 'heart_failure', 'sym_nocturia', 2::smallint, false, 0.3::numeric
where exists (select 1 from public.diseases where id = 'heart_failure')
  and exists (select 1 from public.symptoms where id = 'sym_nocturia')
  and not exists (select 1 from public.disease_symptoms where disease_id = 'heart_failure' and symptom_id = 'sym_nocturia');
insert into public.disease_symptoms (disease_id, symptom_id, typical_intensity, is_primary, weight_multiplier)
select 'type2_diabetes', 'sym_nocturia', 2::smallint, false, 0.3::numeric
where exists (select 1 from public.diseases where id = 'type2_diabetes')
  and exists (select 1 from public.symptoms where id = 'sym_nocturia')
  and not exists (select 1 from public.disease_symptoms where disease_id = 'type2_diabetes' and symptom_id = 'sym_nocturia');

-- ================================================ sym_wheezing  (Wheezing)
update public.symptoms set description = 'Wheezing is a high-pitched, musical sound produced by airflow through narrowed or compressed airways, usually most prominent on expiration. It is characteristic of asthma and chronic obstructive pulmonary disease, but ''all that wheezes is not asthma''. Medicines such as beta-blockers, ACE inhibitors and NSAIDs can cause it, and in children bronchiolitis and inhaled foreign bodies are important. A wheeze that stays in one place suggests a tumor or foreign body, and noise on breathing in suggests stridor rather than wheeze.', updated_at = now()
where id = 'sym_wheezing' and description = 'Wheezing is a high-pitched, musical sound produced by airflow through narrowed or compressed airways, usually most prominent on expiration. It is characteristic of asthma and chronic obstructive pulmonary disease, but ''all that wheezes is not asthma''.';
update public.symptoms set tags = tags || array['stridor']::text[]
where id = 'sym_wheezing' and not (tags @> array['stridor']::text[]);
update public.symptoms set source_attribution = source_attribution || '; Merck Manual Professional - Wheezing'
where id = 'sym_wheezing' and position('Merck Manual Professional - Wheezing' in source_attribution) = 0;
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_wheezing', 'Medicines (beta-blockers, ACE inhibitors, NSAIDs)', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_wheezing'), 0)
where exists (select 1 from public.symptoms where id = 'sym_wheezing')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_wheezing' and content = 'Medicines (beta-blockers, ACE inhibitors, NSAIDs)');
insert into public.symptom_red_flags (symptom_id, content, position)
select 'sym_wheezing', 'Drowsiness or exhaustion during an asthma attack', coalesce((select max(position) + 1 from public.symptom_red_flags where symptom_id = 'sym_wheezing'), 0)
where exists (select 1 from public.symptoms where id = 'sym_wheezing')
  and not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_wheezing' and content = 'Drowsiness or exhaustion during an asthma attack');
insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select 'sym_wheezing', 'Merck Manual Professional - Wheezing', 'Dezube R. Wheezing. Merck Manual Professional Version. Rahway (NJ): Merck & Co.; reviewed Nov 2025.', 'https://www.merckmanuals.com/professional/pulmonary-disorders/symptoms-of-pulmonary-disorders/wheezing', false, coalesce((select max(position) + 1 from public.symptom_references where symptom_id = 'sym_wheezing'), 0)
where exists (select 1 from public.symptoms where id = 'sym_wheezing')
  and not exists (select 1 from public.symptom_references where symptom_id = 'sym_wheezing' and url = 'https://www.merckmanuals.com/professional/pulmonary-disorders/symptoms-of-pulmonary-disorders/wheezing');
insert into public.disease_symptoms (disease_id, symptom_id, typical_intensity, is_primary, weight_multiplier)
select 'heart_failure', 'sym_wheezing', 2::smallint, false, 0.3::numeric
where exists (select 1 from public.diseases where id = 'heart_failure')
  and exists (select 1 from public.symptoms where id = 'sym_wheezing')
  and not exists (select 1 from public.disease_symptoms where disease_id = 'heart_failure' and symptom_id = 'sym_wheezing');

-- ================================================ sym_oral_thrush  (White patches in the mouth (oral thrush))
update public.symptoms set description = 'Oral thrush is Candida overgrowth in the mouth, classically forming creamy white, curd-like plaques on the tongue, buccal mucosa and palate that can be wiped off to leave a red, sometimes bleeding surface. Outside infancy, denture use, antibiotics and inhaled or systemic corticosteroids, it suggests impaired cell-mediated immunity and is an important clinical marker of HIV infection. The diagnosis is usually clinical, and a KOH preparation of a scraping shows yeast and pseudohyphae. Treatment options include clotrimazole troches, nystatin suspension or oral fluconazole.', updated_at = now()
where id = 'sym_oral_thrush' and description = 'Oral thrush is Candida overgrowth in the mouth, classically forming creamy white, curd-like plaques on the tongue, buccal mucosa and palate that can be wiped off to leave a red, sometimes bleeding surface. Outside infancy, denture use, antibiotics and inhaled or systemic corticosteroids, it suggests impaired cell-mediated immunity and is an important clinical marker of HIV infection.';
update public.symptoms set tags = tags || array['candidiasis']::text[]
where id = 'sym_oral_thrush' and not (tags @> array['candidiasis']::text[]);
update public.symptoms set source_attribution = source_attribution || '; Merck Manual Professional - Candidiasis (Mucocutaneous)'
where id = 'sym_oral_thrush' and position('Merck Manual Professional - Candidiasis (Mucocutaneous)' in source_attribution) = 0;
insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select 'sym_oral_thrush', 'Merck Manual Professional - Candidiasis (Mucocutaneous)', 'Aaron DM. Candidiasis (Mucocutaneous). Merck Manual Professional Version. Rahway (NJ): Merck & Co.; reviewed Oct 2025.', 'https://www.merckmanuals.com/professional/dermatologic-disorders/fungal-skin-infections/candidiasis-mucocutaneous', false, coalesce((select max(position) + 1 from public.symptom_references where symptom_id = 'sym_oral_thrush'), 0)
where exists (select 1 from public.symptoms where id = 'sym_oral_thrush')
  and not exists (select 1 from public.symptom_references where symptom_id = 'sym_oral_thrush' and url = 'https://www.merckmanuals.com/professional/dermatologic-disorders/fungal-skin-infections/candidiasis-mucocutaneous');

update public.content_version set version = version + 1, updated_at = now() where id = 1;

commit;

