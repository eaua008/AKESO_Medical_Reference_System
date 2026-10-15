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
