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
