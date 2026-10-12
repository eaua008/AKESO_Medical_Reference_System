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
