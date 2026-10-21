-- 053_body_parts_01.sql  -  body part descriptions, batch b01 (54 entries)
-- Needs 052_body_part_info.sql first. Adds draft rows only: a row that is already
-- reviewed or published, or that has not changed, is left alone, so this is safe
-- to run twice. Drafts are not shown in the app until they are published.

begin;

-- Heart  (22 FMA ids)
insert into public.body_part_info as b (key, kind, fma_ids, layer, system, display_name, aliases, summary_plain, function_plain, description, location, details, clinical, exam_tip, sources, status)
values ('group:fma_FMA7088_o',
    'group',
    array['FMA11359', 'FMA7238', 'FMA7239', 'FMA7240', 'FMA7242', 'FMA7243', 'FMA7247', 'FMA7249', 'FMA7250', 'FMA7252', 'FMA7253', 'FMA7254', 'FMA7260', 'FMA7261', 'FMA7262', 'FMA7264', 'FMA7265', 'FMA9291', 'FMA9457', 'FMA9465', 'FMA9466', 'FMA9531']::text[],
    'organ',
    'cardiovascular',
    'Heart',
    '{}'::text[],
    'The heart is a hollow, muscular organ about the size of a closed fist. It sits in the middle of the chest near the lungs, with most of it slightly to the left.',
    'It pumps blood all the time, sending blood to the lungs to pick up oxygen and then out to every part of the body.',
    'The heart is a four-chambered muscular pump. The thin-walled right and left atria receive blood from veins; the thick-walled right and left ventricles pump it out, the right side to the lungs and the left side to the body, and a wall of tissue (septum) separates the two sides. Four valves (tricuspid, mitral, pulmonary and aortic) keep blood moving one way. The wall has three layers (endocardium, myocardium, epicardium) inside the pericardial sac.',
    'In the center of the chest, close to the lungs, with about two-thirds of its mass to the left of the midline. It lies inside a protective, fluid-containing sac, the pericardium.',
    '{"functions": "Pumps about 5 liters of blood a minute in a normal adult. The right ventricle drives the pulmonary circuit to the lungs; the left ventricle drives the systemic circuit. The SA node in the right atrium starts each beat; the signal passes through the AV node to the ventricles.", "blood_supply": "The right and left coronary arteries, branches of the ascending aorta, supply the heart wall. Cardiac veins drain it, mostly into the coronary sinus, which opens into the right atrium.", "nerve_supply": "Heart rate is adjusted mainly by the cardiac center in the medulla oblongata, which has sympathetic and parasympathetic components; without nerve input the SA node fires about 70 to 80 times a minute."}'::jsonb,
    '[{"text": "Coronary artery disease, plaque buildup (atherosclerosis) in the coronary arteries, is the most common heart disease in the United States and can cause angina, heart attack and heart failure.", "disease_id": "acute_coronary_syndrome"}, {"text": "Heart failure means the heart cannot pump enough blood to meet the body''s needs.", "disease_id": "heart_failure"}, {"text": "Valve disease causes leaking (regurgitation) or narrowing (stenosis); aortic stenosis is a common type, and prolapse, most often of the mitral valve, a common cause of leaking."}, {"text": "Untreated strep throat can lead to rheumatic fever, which can damage the heart valves years later.", "disease_id": "rheumatic_fever"}, {"text": "Tetralogy of Fallot, the most common complex congenital heart defect, combines pulmonary stenosis, a ventricular septal defect, an overriding aorta and right ventricular hypertrophy."}]'::jsonb,
    'Valve closure makes the heart sounds: the atrioventricular valves close first (lub), then the aortic and pulmonary valves (dub). Abnormal heart sounds are called murmurs.',
    '[{"title": "Structure of the Heart - NCI SEER Training Modules", "url": "https://training.seer.cancer.gov/anatomy/cardiovascular/heart/structure.html", "licence": "Public domain"}, {"title": "Heart - NCI SEER Training Modules", "url": "https://training.seer.cancer.gov/anatomy/cardiovascular/heart/", "licence": "Public domain"}, {"title": "Physiology of the Heart - NCI SEER Training Modules", "url": "https://training.seer.cancer.gov/anatomy/cardiovascular/heart/physiology.html", "licence": "Public domain"}, {"title": "Circulatory Pathways - NCI SEER Training Modules", "url": "https://training.seer.cancer.gov/anatomy/cardiovascular/blood/pathways.html", "licence": "Public domain"}, {"title": "How the Heart Works: Heart Anatomy - NHLBI", "url": "https://www.nhlbi.nih.gov/health/heart/anatomy", "licence": "Public domain"}, {"title": "How the Heart Works: Blood Flow - NHLBI", "url": "https://www.nhlbi.nih.gov/health/heart/blood-flow", "licence": "Public domain"}, {"title": "How the Heart Works: How the Heart Beats - NHLBI", "url": "https://www.nhlbi.nih.gov/health/heart/heart-beats", "licence": "Public domain"}, {"title": "Coronary Artery Disease - MedlinePlus (NLM)", "url": "https://medlineplus.gov/coronaryarterydisease.html", "licence": "Public domain"}, {"title": "Heart Valve Diseases - MedlinePlus (NLM)", "url": "https://medlineplus.gov/heartvalvediseases.html", "licence": "Public domain"}, {"title": "Congenital Heart Defects: Types - NHLBI", "url": "https://www.nhlbi.nih.gov/health/congenital-heart-defects/types", "licence": "Public domain"}]'::jsonb,
    'draft')
on conflict (key) do update set
    kind = excluded.kind,
    fma_ids = excluded.fma_ids,
    layer = excluded.layer,
    system = excluded.system,
    display_name = excluded.display_name,
    aliases = excluded.aliases,
    summary_plain = excluded.summary_plain,
    function_plain = excluded.function_plain,
    description = excluded.description,
    location = excluded.location,
    details = excluded.details,
    clinical = excluded.clinical,
    exam_tip = excluded.exam_tip,
    sources = excluded.sources,
    updated_at = now()
where b.status = 'draft'
  and (b.kind, b.fma_ids, b.layer, b.system, b.display_name, b.aliases, b.summary_plain, b.function_plain, b.description, b.location, b.details, b.clinical, b.exam_tip, b.sources)
  is distinct from (excluded.kind, excluded.fma_ids, excluded.layer, excluded.system, excluded.display_name, excluded.aliases, excluded.summary_plain, excluded.function_plain, excluded.description, excluded.location, excluded.details, excluded.clinical, excluded.exam_tip, excluded.sources);

-- Trachea  (1 FMA ids)
insert into public.body_part_info as b (key, kind, fma_ids, layer, system, display_name, aliases, summary_plain, function_plain, description, location, details, clinical, exam_tip, sources, status)
values ('trachea',
    'part',
    array['FMA7394']::text[],
    'organ',
    'respiratory',
    'Trachea',
    array['windpipe']::text[],
    'The trachea, or windpipe, is the main air tube to the lungs. It runs down from the voice box in the neck into the chest.',
    'It carries air down to the lungs when you breathe in and carries used air back out when you breathe out.',
    'The trachea is the main airway leading to the lungs. Hyaline cartilage in its wall holds it open so it does not collapse, while its back wall is soft. It is lined with ciliated pseudostratified columnar epithelium; goblet cells make mucus that traps dust and germs, and cilia sweep the mucus upward to be swallowed or coughed out.',
    'In the neck and chest, continuing down from the larynx (voice box). The oesophagus lies directly behind it. At about the level of the fifth thoracic vertebra, in the mediastinum, it divides into the right and left main bronchi.',
    '{"functions": "Conducts air between the larynx and the main bronchi; its mucus and cilia trap and clear inhaled particles and microorganisms."}'::jsonb,
    '[{"text": "Trachea problems include narrowing (stenosis), inflammation and some inherited conditions."}, {"text": "A tracheostomy may help breathing in people with swallowing problems, blocked airways or poor coughing, and in critical care patients who need a breathing machine."}]'::jsonb,
    'Its soft back wall lets the oesophagus, which lies right behind it, expand when food is swallowed.',
    '[{"title": "Larynx & Trachea - NCI SEER Training Modules", "url": "https://training.seer.cancer.gov/anatomy/respiratory/passages/larynx.html", "licence": "Public domain"}, {"title": "Bronchi, Bronchial Tree, & Lungs - NCI SEER Training Modules", "url": "https://training.seer.cancer.gov/anatomy/respiratory/passages/bronchi.html", "licence": "Public domain"}, {"title": "Tracheal Disorders - MedlinePlus (NLM)", "url": "https://medlineplus.gov/trachealdisorders.html", "licence": "Public domain"}, {"title": "How the Lungs Work: What Breathing Does for the Body - NHLBI", "url": "https://www.nhlbi.nih.gov/health/lungs/breathing-benefits", "licence": "Public domain"}]'::jsonb,
    'draft')
on conflict (key) do update set
    kind = excluded.kind,
    fma_ids = excluded.fma_ids,
    layer = excluded.layer,
    system = excluded.system,
    display_name = excluded.display_name,
    aliases = excluded.aliases,
    summary_plain = excluded.summary_plain,
    function_plain = excluded.function_plain,
    description = excluded.description,
    location = excluded.location,
    details = excluded.details,
    clinical = excluded.clinical,
    exam_tip = excluded.exam_tip,
    sources = excluded.sources,
    updated_at = now()
where b.status = 'draft'
  and (b.kind, b.fma_ids, b.layer, b.system, b.display_name, b.aliases, b.summary_plain, b.function_plain, b.description, b.location, b.details, b.clinical, b.exam_tip, b.sources)
  is distinct from (excluded.kind, excluded.fma_ids, excluded.layer, excluded.system, excluded.display_name, excluded.aliases, excluded.summary_plain, excluded.function_plain, excluded.description, excluded.location, excluded.details, excluded.clinical, excluded.exam_tip, excluded.sources);

-- Bronchial tree  (22 FMA ids)
insert into public.body_part_info as b (key, kind, fma_ids, layer, system, display_name, aliases, summary_plain, function_plain, description, location, details, clinical, exam_tip, sources, status)
values ('group:airways',
    'group',
    array['FMA68211', 'FMA68212', 'FMA68213', 'FMA68214', 'FMA68215', 'FMA68216', 'FMA68218', 'FMA68220', 'FMA68221', 'FMA68222', 'FMA68223', 'FMA68225', 'FMA68226', 'FMA68227', 'FMA68228', 'FMA68230', 'FMA68231', 'FMA68232', 'FMA68233', 'FMA68321', 'FMA68418', 'FMA7396']::text[],
    'organ',
    'respiratory',
    'Bronchial tree',
    array['bronchial tubes', 'bronchi']::text[],
    'The bronchial tree is the set of branching air tubes inside the chest. It starts where the windpipe splits in two and keeps dividing into smaller tubes inside each lung.',
    'It carries air from the windpipe deep into the lungs, down to the tiny air sacs where oxygen enters the blood.',
    'The trachea divides into the right and left main (primary) bronchi, which have cartilage and a lining like the trachea. Inside the lungs they keep branching: each lobe gets its own lobar (secondary) bronchus, and the branches become smaller and smaller, ending as bronchioles and then alveoli. As the tubes narrow, cartilage in the wall decreases and smooth muscle increases.',
    'In the chest. The split of the trachea lies in the mediastinum at about the fifth thoracic vertebra; the bronchi enter each lung at the hilum on its medial side. The right lung has three lobes and the left lung two.',
    '{"functions": "Conducts air to and from the alveoli, where gas exchange happens. Cartilage rings help keep the larger tubes open.", "nerve_supply": "Autonomic: parasympathetic signals narrow the bronchial tubes; sympathetic signals widen them."}'::jsonb,
    '[{"text": "Inflammation of the bronchial tubes (bronchitis) is most often caused by cold and flu viruses and gives a cough with mucus, wheezing and chest tightness."}, {"text": "In asthma the airways become swollen and tight, causing wheezing, coughing, chest tightness and shortness of breath; attacks can be life-threatening.", "disease_id": "asthma"}]'::jsonb,
    'Cartilage fades out as the bronchi branch and is absent in the smallest bronchioles, while smooth muscle increases.',
    '[{"title": "Bronchi, Bronchial Tree, & Lungs - NCI SEER Training Modules", "url": "https://training.seer.cancer.gov/anatomy/respiratory/passages/bronchi.html", "licence": "Public domain"}, {"title": "How the Lungs Work: The Respiratory System - NHLBI", "url": "https://www.nhlbi.nih.gov/health/lungs/respiratory-system", "licence": "Public domain"}, {"title": "How the Lungs Work: How Your Body Controls Breathing - NHLBI", "url": "https://www.nhlbi.nih.gov/health/lungs/body-controls-breathing", "licence": "Public domain"}, {"title": "Acute Bronchitis - MedlinePlus (NLM)", "url": "https://medlineplus.gov/acutebronchitis.html", "licence": "Public domain"}, {"title": "Asthma - MedlinePlus (NLM)", "url": "https://medlineplus.gov/asthma.html", "licence": "Public domain"}]'::jsonb,
    'draft')
on conflict (key) do update set
    kind = excluded.kind,
    fma_ids = excluded.fma_ids,
    layer = excluded.layer,
    system = excluded.system,
    display_name = excluded.display_name,
    aliases = excluded.aliases,
    summary_plain = excluded.summary_plain,
    function_plain = excluded.function_plain,
    description = excluded.description,
    location = excluded.location,
    details = excluded.details,
    clinical = excluded.clinical,
    exam_tip = excluded.exam_tip,
    sources = excluded.sources,
    updated_at = now()
where b.status = 'draft'
  and (b.kind, b.fma_ids, b.layer, b.system, b.display_name, b.aliases, b.summary_plain, b.function_plain, b.description, b.location, b.details, b.clinical, b.exam_tip, b.sources)
  is distinct from (excluded.kind, excluded.fma_ids, excluded.layer, excluded.system, excluded.display_name, excluded.aliases, excluded.summary_plain, excluded.function_plain, excluded.description, excluded.location, excluded.details, excluded.clinical, excluded.exam_tip, excluded.sources);

-- Oesophagus  (1 FMA ids)
insert into public.body_part_info as b (key, kind, fma_ids, layer, system, display_name, aliases, summary_plain, function_plain, description, location, details, clinical, exam_tip, sources, status)
values ('esophagus',
    'part',
    array['FMA7131']::text[],
    'organ',
    'digestive',
    'Oesophagus',
    '{}'::text[],
    'The oesophagus is a muscular tube about 25 cm long that runs from the throat down through the chest to the stomach.',
    'It moves swallowed food and drink down to the stomach by waves of muscle squeezing, without digesting it.',
    'The oesophagus is a collapsible muscular tube linking the pharynx to the stomach. Its wall has a mucosa, submucosa, muscularis and an outer adventitia; it has no serosa. The muscle is striated in the upper third, mixed in the middle third and smooth in the lower third. Upper and lower oesophageal sphincters control food entering and leaving it.',
    'Begins at the lower end of the pharynx (about the sixth cervical vertebra, lower border of the cricoid cartilage), descends through the mediastinum behind the trachea and heart and in front of the vertebral column, then passes through the oesophageal hiatus of the diaphragm to join the stomach.',
    '{"functions": "Carries food from the pharynx to the stomach by peristalsis; glands in its lining make mucus that lubricates the passage. No digestive juices are added. The lower oesophageal sphincter relaxes to let food in and stays closed to stop stomach contents flowing back.", "lymph_drainage": "Cervical part: deep cervical (internal jugular), supraclavicular and paratracheal nodes. Upper and middle thoracic: tracheobronchial, carinal, hilar, posterior mediastinal and periesophageal nodes. Lower thoracic: left gastric, cardial and perigastric nodes.", "nerve_supply": "Swallowing becomes automatic once started: the brain signals the oesophageal muscles to begin peristalsis, helped by nerves in the gut wall."}'::jsonb,
    '[{"text": "GERD, where stomach acid flows back into the oesophagus, is its most common problem; it can happen when the muscle at the lower end is weak or relaxes at the wrong time.", "disease_id": "gerd"}, {"text": "Long-term GERD can inflame and scar the oesophagus and change its lining (Barrett''s oesophagus).", "disease_id": "gerd"}, {"text": "In achalasia the lower oesophageal muscle does not relax properly, causing trouble swallowing."}, {"text": "About half of oesophageal cancers arise in the lower third, 40% in the middle third and 10% in the upper third."}]'::jsonb,
    'The oesophagus has no serosa; its outer layer is adventitia, connective tissue that blends with nearby structures.',
    '[{"title": "Anatomy of the Esophagus - NCI SEER Training Modules", "url": "https://training.seer.cancer.gov/ugi/anatomy/esophagus.html", "licence": "Public domain"}, {"title": "Layers of the UGI Organs - NCI SEER Training Modules", "url": "https://training.seer.cancer.gov/ugi/anatomy/layers.html", "licence": "Public domain"}, {"title": "Regional Lymph Nodes - NCI SEER Training Modules", "url": "https://training.seer.cancer.gov/ugi/anatomy/lymph-nodes.html", "licence": "Public domain"}, {"title": "Pharynx & Esophagus - NCI SEER Training Modules", "url": "https://training.seer.cancer.gov/anatomy/digestive/regions/pharynx.html", "licence": "Public domain"}, {"title": "Your Digestive System & How It Works - NIDDK", "url": "https://www.niddk.nih.gov/health-information/digestive-diseases/digestive-system-how-it-works", "licence": "Public domain"}, {"title": "Esophagus Disorders - MedlinePlus (NLM)", "url": "https://medlineplus.gov/esophagusdisorders.html", "licence": "Public domain"}, {"title": "GERD - MedlinePlus (NLM)", "url": "https://medlineplus.gov/gerd.html", "licence": "Public domain"}]'::jsonb,
    'draft')
on conflict (key) do update set
    kind = excluded.kind,
    fma_ids = excluded.fma_ids,
    layer = excluded.layer,
    system = excluded.system,
    display_name = excluded.display_name,
    aliases = excluded.aliases,
    summary_plain = excluded.summary_plain,
    function_plain = excluded.function_plain,
    description = excluded.description,
    location = excluded.location,
    details = excluded.details,
    clinical = excluded.clinical,
    exam_tip = excluded.exam_tip,
    sources = excluded.sources,
    updated_at = now()
where b.status = 'draft'
  and (b.kind, b.fma_ids, b.layer, b.system, b.display_name, b.aliases, b.summary_plain, b.function_plain, b.description, b.location, b.details, b.clinical, b.exam_tip, b.sources)
  is distinct from (excluded.kind, excluded.fma_ids, excluded.layer, excluded.system, excluded.display_name, excluded.aliases, excluded.summary_plain, excluded.function_plain, excluded.description, excluded.location, excluded.details, excluded.clinical, excluded.exam_tip, excluded.sources);

-- Stomach  (1 FMA ids)
insert into public.body_part_info as b (key, kind, fma_ids, layer, system, display_name, aliases, summary_plain, function_plain, description, location, details, clinical, exam_tip, sources, status)
values ('stomach',
    'part',
    array['FMA7148']::text[],
    'organ',
    'digestive',
    'Stomach',
    '{}'::text[],
    'The stomach is a hollow, muscular organ in the upper left part of the belly, just under the diaphragm. It sits between the food pipe and the small intestine.',
    'It stores swallowed food, mixes it with acid and digestive juices, and slowly passes the mixture on to the small intestine.',
    'The stomach has four parts: the cardia around the opening from the oesophagus, the fundus above it, the central body and the lower pyloric antrum. Its lining has gastric glands with mucous, parietal, chief and endocrine cells; the endocrine cells release the hormone gastrin. Three smooth muscle layers (longitudinal, circular and oblique) churn food into chyme.',
    'In the upper abdomen, just below the diaphragm, mostly left of the midline and partly under the liver. The lesser curvature faces right and the greater curvature left. It joins the duodenum at the pylorus; the greater omentum links it to the transverse colon, spleen and diaphragm.',
    '{"functions": "Stores food, mixes it with acid and enzymes (protein digestion begins here) and empties chyme into the duodenum through the pyloric sphincter. Lining cells release hormones that control digestion and signal hunger or fullness. Gastric secretion has cephalic, gastric and intestinal phases.", "nerve_supply": "Enteric nerves in the stomach wall control muscle contractions and speed up or slow food movement and digestive juice production; secretion is also under neural and hormonal control.", "lymph_drainage": "Perigastric nodes along the lesser curvature (left gastric, cardial) and greater curvature (gastroepiploic, pyloric, gastroduodenal), splenic hilar and peripancreatic nodes, then celiac and hepatic nodes."}'::jsonb,
    '[{"text": "A peptic ulcer is a sore in the lining of the stomach or duodenum, most often caused by Helicobacter pylori infection or long-term NSAID use; burning stomach pain is the usual symptom.", "disease_id": "peptic_ulcer_disease"}, {"text": "A hiatal hernia is when the top of the stomach pushes up through the opening in the diaphragm, making acid reflux (GERD) more likely.", "disease_id": "gerd"}, {"text": "Indigestion and heartburn are common stomach problems; blood in the stool, severe belly pain or ongoing vomiting need medical attention."}]'::jsonb,
    'The stomach wall has three smooth muscle layers: outer longitudinal, middle circular and inner oblique.',
    '[{"title": "Anatomy of the Stomach - NCI SEER Training Modules", "url": "https://training.seer.cancer.gov/ugi/anatomy/stomach.html", "licence": "Public domain"}, {"title": "Stomach - NCI SEER Training Modules", "url": "https://training.seer.cancer.gov/anatomy/digestive/regions/stomach.html", "licence": "Public domain"}, {"title": "Layers of the UGI Organs - NCI SEER Training Modules", "url": "https://training.seer.cancer.gov/ugi/anatomy/layers.html", "licence": "Public domain"}, {"title": "Regional Lymph Nodes - NCI SEER Training Modules", "url": "https://training.seer.cancer.gov/ugi/anatomy/lymph-nodes.html", "licence": "Public domain"}, {"title": "Your Digestive System & How It Works - NIDDK", "url": "https://www.niddk.nih.gov/health-information/digestive-diseases/digestive-system-how-it-works", "licence": "Public domain"}, {"title": "Stomach Disorders - MedlinePlus (NLM)", "url": "https://medlineplus.gov/stomachdisorders.html", "licence": "Public domain"}, {"title": "Peptic Ulcer - MedlinePlus (NLM)", "url": "https://medlineplus.gov/pepticulcer.html", "licence": "Public domain"}, {"title": "Hiatal Hernia - MedlinePlus (NLM)", "url": "https://medlineplus.gov/hiatalhernia.html", "licence": "Public domain"}]'::jsonb,
    'draft')
on conflict (key) do update set
    kind = excluded.kind,
    fma_ids = excluded.fma_ids,
    layer = excluded.layer,
    system = excluded.system,
    display_name = excluded.display_name,
    aliases = excluded.aliases,
    summary_plain = excluded.summary_plain,
    function_plain = excluded.function_plain,
    description = excluded.description,
    location = excluded.location,
    details = excluded.details,
    clinical = excluded.clinical,
    exam_tip = excluded.exam_tip,
    sources = excluded.sources,
    updated_at = now()
where b.status = 'draft'
  and (b.kind, b.fma_ids, b.layer, b.system, b.display_name, b.aliases, b.summary_plain, b.function_plain, b.description, b.location, b.details, b.clinical, b.exam_tip, b.sources)
  is distinct from (excluded.kind, excluded.fma_ids, excluded.layer, excluded.system, excluded.display_name, excluded.aliases, excluded.summary_plain, excluded.function_plain, excluded.description, excluded.location, excluded.details, excluded.clinical, excluded.exam_tip, excluded.sources);

-- Liver  (19 FMA ids)
insert into public.body_part_info as b (key, kind, fma_ids, layer, system, display_name, aliases, summary_plain, function_plain, description, location, details, clinical, exam_tip, sources, status)
values ('group:fma_FMA7197_o',
    'group',
    array['FMA13365', 'FMA14669', 'FMA14670', 'FMA15739', 'FMA15741', 'FMA15742', 'FMA15743', 'FMA15744', 'FMA15745', 'FMA15746', 'FMA71867', 'FMA71868', 'FMA71869', 'FMA71870', 'FMA71885', 'FMA71886', 'FMA71887', 'FMA71888', 'FMA71889']::text[],
    'organ',
    'digestive',
    'Liver',
    '{}'::text[],
    'The liver is the largest organ inside the body. It sits in the upper right part of the belly, just under the diaphragm.',
    'It makes bile to help digest fat, stores and processes nutrients from food, and removes harmful substances from the blood.',
    'The liver is the largest gland in the body. On its surface it shows two large lobes, a larger right and a smaller left, plus two small lobes, the quadrate and caudate. Inside, it is built of lobules, where liver cells (hepatocytes) line blood channels called sinusoids that drain to a central vein. It makes bile, which leaves through the hepatic ducts.',
    'In the upper abdomen, mostly in the right hypochondriac and epigastric regions, directly beneath the diaphragm. The gallbladder is attached to its under (visceral) surface, and the hepatic artery, portal vein and bile ducts enter or leave at the porta hepatis.',
    '{"functions": "Makes bile and bile salts; makes plasma proteins; stores nutrients; metabolises carbohydrates, fats and proteins; detoxifies and excretes waste; filters blood, with phagocytic Kupffer cells lining the sinusoids.", "blood_supply": "Dual supply: the common hepatic artery (a branch of the celiac trunk from the abdominal aorta) brings oxygen-rich blood, and the hepatic portal vein brings nutrient-rich blood from the digestive tract, spleen, pancreas and gallbladder.", "lymph_drainage": "Regional nodes are the hepatic hilar nodes (hepatic and periportal nodes); lymphatic vessels pass through the porta hepatis."}'::jsonb,
    '[{"text": "Viruses (hepatitis A, B and C), drugs, toxins, heavy alcohol use, inherited conditions and cancer can all damage the liver; jaundice and abdominal or leg swelling are common signs."}, {"text": "Chronic hepatitis B can lead to cirrhosis, liver cancer and liver failure; vaccination is the best protection.", "disease_id": "hepatitis_b"}, {"text": "In cirrhosis, scar tissue permanently replaces healthy liver tissue; about 1 in 400 adults in the United States are estimated to have it."}, {"text": "Scarring slows portal blood flow, causing portal hypertension with ascites, oesophageal or gastric varices that can bleed, and hepatic encephalopathy."}, {"text": "Most people who develop liver cancer already have cirrhosis."}]'::jsonb,
    'The liver has a dual blood supply: oxygen-rich blood from the hepatic artery and nutrient-rich blood from the hepatic portal vein.',
    '[{"title": "Accessory Organs of the Digestive System - NCI SEER Training Modules", "url": "https://training.seer.cancer.gov/anatomy/digestive/regions/accessory.html", "licence": "Public domain"}, {"title": "Anatomy of the Liver & Gallbladder - NCI SEER Training Modules", "url": "https://training.seer.cancer.gov/biliary/anatomy/liver.html", "licence": "Public domain"}, {"title": "Regional Lymph Nodes (Biliary) - NCI SEER Training Modules", "url": "https://training.seer.cancer.gov/biliary/anatomy/lymph-nodes.html", "licence": "Public domain"}, {"title": "Your Digestive System & How It Works - NIDDK", "url": "https://www.niddk.nih.gov/health-information/digestive-diseases/digestive-system-how-it-works", "licence": "Public domain"}, {"title": "Liver Diseases - MedlinePlus (NLM)", "url": "https://medlineplus.gov/liverdiseases.html", "licence": "Public domain"}, {"title": "Hepatitis B - MedlinePlus (NLM)", "url": "https://medlineplus.gov/hepatitisb.html", "licence": "Public domain"}, {"title": "Definition & Facts for Cirrhosis - NIDDK", "url": "https://www.niddk.nih.gov/health-information/liver-disease/cirrhosis/definition-facts", "licence": "Public domain"}]'::jsonb,
    'draft')
on conflict (key) do update set
    kind = excluded.kind,
    fma_ids = excluded.fma_ids,
    layer = excluded.layer,
    system = excluded.system,
    display_name = excluded.display_name,
    aliases = excluded.aliases,
    summary_plain = excluded.summary_plain,
    function_plain = excluded.function_plain,
    description = excluded.description,
    location = excluded.location,
    details = excluded.details,
    clinical = excluded.clinical,
    exam_tip = excluded.exam_tip,
    sources = excluded.sources,
    updated_at = now()
where b.status = 'draft'
  and (b.kind, b.fma_ids, b.layer, b.system, b.display_name, b.aliases, b.summary_plain, b.function_plain, b.description, b.location, b.details, b.clinical, b.exam_tip, b.sources)
  is distinct from (excluded.kind, excluded.fma_ids, excluded.layer, excluded.system, excluded.display_name, excluded.aliases, excluded.summary_plain, excluded.function_plain, excluded.description, excluded.location, excluded.details, excluded.clinical, excluded.exam_tip, excluded.sources);

-- Gallbladder  (1 FMA ids)
insert into public.body_part_info as b (key, kind, fma_ids, layer, system, display_name, aliases, summary_plain, function_plain, description, location, details, clinical, exam_tip, sources, status)
values ('gallbladder',
    'part',
    array['FMA7202']::text[],
    'organ',
    'digestive',
    'Gallbladder',
    '{}'::text[],
    'The gallbladder is a small, pear-shaped pouch tucked under the liver in the upper right part of the belly.',
    'It stores bile made by the liver and squeezes it into the small intestine during a meal to help digest fat.',
    'The gallbladder is a pear-shaped sac on the under (visceral) surface of the liver. It has a fundus (the wide end), a body and a neck that narrows into the cystic duct. Its main job is to store bile, a yellow-green fluid of water, bile salts, bile pigments and cholesterol. Bile salts break fat into small droplets so it can be digested.',
    'Upper right abdomen, under the liver and attached to its visceral surface. The cystic duct joins the common hepatic duct to form the common bile duct, which carries bile to the duodenum.',
    '{"functions": "Stores bile between meals and releases it into the duodenum after eating. Its wall has a mucosa, lamina propria, smooth muscle and serosa; there is no serosa where it lies against the liver.", "blood_supply": "Its venous blood goes to the liver through the portal vein.", "lymph_drainage": "Regional nodes include the cystic duct, pericholedochal, hepatic hilar, periportal, periduodenal, peripancreatic, celiac and superior mesenteric nodes, and the node of the foramen of Winslow."}'::jsonb,
    '[{"text": "Gallstones are hard deposits, usually of cholesterol or bilirubin; they affect about 10 to 15 percent of people in the United States."}, {"text": "Most gallstones are ''silent'', but a stone blocking a bile duct causes sudden upper right abdominal pain (biliary colic)."}, {"text": "Gallstones can cause inflammation of the gallbladder, infection of the bile ducts or liver, and gallstone pancreatitis."}, {"text": "Removing the gallbladder (cholecystectomy) treats many gallbladder problems; people can live without it."}, {"text": "Gallbladder cancer is rare; about 70 percent of gallbladder tumours spread directly into the liver."}]'::jsonb,
    'The cystic duct from the gallbladder joins the common hepatic duct to form the common bile duct.',
    '[{"title": "Accessory Organs of the Digestive System - NCI SEER Training Modules", "url": "https://training.seer.cancer.gov/anatomy/digestive/regions/accessory.html", "licence": "Public domain"}, {"title": "Anatomy of the Liver & Gallbladder - NCI SEER Training Modules", "url": "https://training.seer.cancer.gov/biliary/anatomy/liver.html", "licence": "Public domain"}, {"title": "Regional Lymph Nodes (Biliary) - NCI SEER Training Modules", "url": "https://training.seer.cancer.gov/biliary/anatomy/lymph-nodes.html", "licence": "Public domain"}, {"title": "Gallbladder Diseases - MedlinePlus (NLM)", "url": "https://medlineplus.gov/gallbladderdiseases.html", "licence": "Public domain"}, {"title": "Definition & Facts for Gallstones - NIDDK", "url": "https://www.niddk.nih.gov/health-information/digestive-diseases/gallstones/definition-facts", "licence": "Public domain"}, {"title": "Your Digestive System & How It Works - NIDDK", "url": "https://www.niddk.nih.gov/health-information/digestive-diseases/digestive-system-how-it-works", "licence": "Public domain"}, {"title": "Definition & Facts for Cirrhosis - NIDDK", "url": "https://www.niddk.nih.gov/health-information/liver-disease/cirrhosis/definition-facts", "licence": "Public domain"}]'::jsonb,
    'draft')
on conflict (key) do update set
    kind = excluded.kind,
    fma_ids = excluded.fma_ids,
    layer = excluded.layer,
    system = excluded.system,
    display_name = excluded.display_name,
    aliases = excluded.aliases,
    summary_plain = excluded.summary_plain,
    function_plain = excluded.function_plain,
    description = excluded.description,
    location = excluded.location,
    details = excluded.details,
    clinical = excluded.clinical,
    exam_tip = excluded.exam_tip,
    sources = excluded.sources,
    updated_at = now()
where b.status = 'draft'
  and (b.kind, b.fma_ids, b.layer, b.system, b.display_name, b.aliases, b.summary_plain, b.function_plain, b.description, b.location, b.details, b.clinical, b.exam_tip, b.sources)
  is distinct from (excluded.kind, excluded.fma_ids, excluded.layer, excluded.system, excluded.display_name, excluded.aliases, excluded.summary_plain, excluded.function_plain, excluded.description, excluded.location, excluded.details, excluded.clinical, excluded.exam_tip, excluded.sources);

-- Pancreas  (1 FMA ids)
insert into public.body_part_info as b (key, kind, fma_ids, layer, system, display_name, aliases, summary_plain, function_plain, description, location, details, clinical, exam_tip, sources, status)
values ('pancreas',
    'part',
    array['FMA7198']::text[],
    'organ',
    'digestive',
    'Pancreas',
    '{}'::text[],
    'The pancreas is a long, soft gland that lies across the back of the belly, behind the stomach and in front of the spine.',
    'It makes digestive juices that break down food in the small intestine and hormones, such as insulin, that control blood sugar.',
    'The pancreas is a gland with two jobs. Its exocrine part, most of the gland, is made of acinar cells that release digestive enzymes (amylase, trypsin, peptidase, lipase) into ducts that reach the duodenum. Its endocrine part is the scattered pancreatic islets (islets of Langerhans), which release insulin and glucagon into the blood. It is divided into a head, body and tail.',
    'Across the posterior abdominal wall, behind the stomach, stretching from the duodenum to the spleen. The head lies to the right of the superior mesenteric vein, the body between that vein and the aorta, and the tail reaches the hilum of the spleen.',
    '{"functions": "Exocrine: digestive enzymes for carbohydrates, fats and proteins, carried by the main pancreatic duct (duct of Wirsung) into the duodenum; release is controlled by secretin and cholecystokinin. Endocrine: alpha cells release glucagon when blood glucose is low; beta cells release insulin when it is high.", "blood_supply": "Its venous blood goes to the liver through the portal vein.", "lymph_drainage": "Regional nodes include the peripancreatic, pancreaticoduodenal, pyloric, superior mesenteric, celiac (head), hepatic artery, splenic and splenic hilar (body and tail), retroperitoneal and lateral aortic nodes."}'::jsonb,
    '[{"text": "Pancreatitis is inflammation caused by the gland''s own digestive enzymes; gallstones and heavy alcohol use are major risk factors."}, {"text": "Acute pancreatitis starts suddenly and usually settles within days; chronic pancreatitis does not heal and causes lasting damage."}, {"text": "In type 2 diabetes the pancreas cannot release enough insulin in response to meals; in type 1 diabetes the immune system destroys the beta cells.", "disease_id": "type2_diabetes"}, {"text": "In cystic fibrosis, thick, sticky mucus can block the ducts of the pancreas."}, {"text": "The head of the pancreas is the most common site of pancreatic cancer."}]'::jsonb,
    'The pancreas is both an exocrine gland (digestive enzymes to the duodenum) and an endocrine gland (insulin and glucagon from the islets of Langerhans).',
    '[{"title": "Accessory Organs of the Digestive System - NCI SEER Training Modules", "url": "https://training.seer.cancer.gov/anatomy/digestive/regions/accessory.html", "licence": "Public domain"}, {"title": "Pancreas - Islets of Langerhans - NCI SEER Training Modules", "url": "https://training.seer.cancer.gov/anatomy/endocrine/glands/pancreas.html", "licence": "Public domain"}, {"title": "Anatomy of the Pancreas & Duodenum - NCI SEER Training Modules", "url": "https://training.seer.cancer.gov/biliary/anatomy/", "licence": "Public domain"}, {"title": "Regional Lymph Nodes (Biliary) - NCI SEER Training Modules", "url": "https://training.seer.cancer.gov/biliary/anatomy/lymph-nodes.html", "licence": "Public domain"}, {"title": "Pancreatic Diseases - MedlinePlus (NLM)", "url": "https://medlineplus.gov/pancreaticdiseases.html", "licence": "Public domain"}, {"title": "Definition & Facts for Pancreatitis - NIDDK", "url": "https://www.niddk.nih.gov/health-information/digestive-diseases/pancreatitis/definition-facts", "licence": "Public domain"}, {"title": "Your Digestive System & How It Works - NIDDK", "url": "https://www.niddk.nih.gov/health-information/digestive-diseases/digestive-system-how-it-works", "licence": "Public domain"}, {"title": "Definition & Facts for Cirrhosis - NIDDK", "url": "https://www.niddk.nih.gov/health-information/liver-disease/cirrhosis/definition-facts", "licence": "Public domain"}]'::jsonb,
    'draft')
on conflict (key) do update set
    kind = excluded.kind,
    fma_ids = excluded.fma_ids,
    layer = excluded.layer,
    system = excluded.system,
    display_name = excluded.display_name,
    aliases = excluded.aliases,
    summary_plain = excluded.summary_plain,
    function_plain = excluded.function_plain,
    description = excluded.description,
    location = excluded.location,
    details = excluded.details,
    clinical = excluded.clinical,
    exam_tip = excluded.exam_tip,
    sources = excluded.sources,
    updated_at = now()
where b.status = 'draft'
  and (b.kind, b.fma_ids, b.layer, b.system, b.display_name, b.aliases, b.summary_plain, b.function_plain, b.description, b.location, b.details, b.clinical, b.exam_tip, b.sources)
  is distinct from (excluded.kind, excluded.fma_ids, excluded.layer, excluded.system, excluded.display_name, excluded.aliases, excluded.summary_plain, excluded.function_plain, excluded.description, excluded.location, excluded.details, excluded.clinical, excluded.exam_tip, excluded.sources);

-- Spleen  (1 FMA ids)
insert into public.body_part_info as b (key, kind, fma_ids, layer, system, display_name, aliases, summary_plain, function_plain, description, location, details, clinical, exam_tip, sources, status)
values ('spleen',
    'part',
    array['FMA7196']::text[],
    'organ',
    'endocrine',
    'Spleen',
    '{}'::text[],
    'The spleen is a fist-sized organ in the upper left part of the belly, under the ribs and behind the stomach.',
    'It filters the blood, removes old red blood cells and helps the body fight infections.',
    'The spleen is the largest lymphatic organ in the body. It is wrapped in a connective tissue capsule that sends partitions inward. Its white pulp is lymphatic tissue, mostly lymphocytes gathered around arteries; its red pulp is blood-filled venous sinuses with cords of lymphocytes and macrophages. It filters blood much as lymph nodes filter lymph.',
    'In the upper left abdominal cavity, just beneath the diaphragm, under the ribs and behind (posterior to) the stomach. The tail of the pancreas reaches its hilum.',
    '{"functions": "Filters blood; lymphocytes attack blood-borne germs and macrophages engulf debris; removes old and damaged red blood cells (with the liver); stores blood that can be squeezed into the circulation after a haemorrhage; produces lymphocytes.", "blood_supply": "Blood enters through the splenic artery, is filtered in the sinuses and leaves through the splenic vein; this venous blood reaches the liver through the portal vein."}'::jsonb,
    '[{"text": "Some diseases cause the spleen to enlarge, and an enlarged spleen is more easily damaged or ruptured by injury."}, {"text": "A badly damaged spleen may be removed (splenectomy); people can live without it but lose some ability to fight infections."}, {"text": "An enlarged spleen is a physical finding in malaria; rarely, P. vivax malaria causes rupture of the spleen.", "disease_id": "malaria"}]'::jsonb,
    'The spleen is the largest lymphatic organ in the body.',
    '[{"title": "Spleen - NCI SEER Training Modules", "url": "https://training.seer.cancer.gov/anatomy/lymphatic/components/spleen.html", "licence": "Public domain"}, {"title": "Spleen Diseases - MedlinePlus (NLM)", "url": "https://medlineplus.gov/spleendiseases.html", "licence": "Public domain"}, {"title": "Anatomy of the Pancreas & Duodenum - NCI SEER Training Modules", "url": "https://training.seer.cancer.gov/biliary/anatomy/", "licence": "Public domain"}, {"title": "Definition & Facts for Cirrhosis - NIDDK", "url": "https://www.niddk.nih.gov/health-information/liver-disease/cirrhosis/definition-facts", "licence": "Public domain"}, {"title": "Clinical Features of Malaria - CDC", "url": "https://www.cdc.gov/malaria/hcp/clinical-features/index.html", "licence": "Public domain"}]'::jsonb,
    'draft')
on conflict (key) do update set
    kind = excluded.kind,
    fma_ids = excluded.fma_ids,
    layer = excluded.layer,
    system = excluded.system,
    display_name = excluded.display_name,
    aliases = excluded.aliases,
    summary_plain = excluded.summary_plain,
    function_plain = excluded.function_plain,
    description = excluded.description,
    location = excluded.location,
    details = excluded.details,
    clinical = excluded.clinical,
    exam_tip = excluded.exam_tip,
    sources = excluded.sources,
    updated_at = now()
where b.status = 'draft'
  and (b.kind, b.fma_ids, b.layer, b.system, b.display_name, b.aliases, b.summary_plain, b.function_plain, b.description, b.location, b.details, b.clinical, b.exam_tip, b.sources)
  is distinct from (excluded.kind, excluded.fma_ids, excluded.layer, excluded.system, excluded.display_name, excluded.aliases, excluded.summary_plain, excluded.function_plain, excluded.description, excluded.location, excluded.details, excluded.clinical, excluded.exam_tip, excluded.sources);

-- Small intestine  (8 FMA ids)
insert into public.body_part_info as b (key, kind, fma_ids, layer, system, display_name, aliases, summary_plain, function_plain, description, location, details, clinical, exam_tip, sources, status)
values ('group:small_intestine',
    'group',
    array['FMA14643', 'FMA14964', 'FMA14965', 'FMA14966', 'FMA16981', 'FMA16982', 'FMA16983', 'FMA7206']::text[],
    'organ',
    'digestive',
    'Small intestine',
    '{}'::text[],
    'The small intestine is a long, folded tube in the belly that connects the stomach to the large intestine.',
    'It finishes digesting food and absorbs most of its nutrients and water into the body.',
    'The small intestine runs from the pyloric sphincter of the stomach to the ileocecal valve. It has three parts: the duodenum (first), the jejunum (middle) and the ileum (last). Its own juices mix with bile and pancreatic juice to finish digesting proteins, carbohydrates and fats. Circular folds (plicae circulares), villi and microvilli greatly increase its absorbing surface.',
    'Coiled in the abdomen between the stomach and the large intestine. The duodenum receives bile and pancreatic juice through the ampulla of Vater; the ileum empties into the large intestine at the ileocecal valve.',
    '{"functions": "Completes digestion and absorbs nutrients and water. Mucosal cells secrete mucus and enzymes (peptidase, sucrase, maltase, lactase, lipase, enterokinase); endocrine cells release secretin and cholecystokinin.", "blood_supply": "Its venous blood goes to the liver through the portal vein.", "nerve_supply": "The enteric nervous system in its wall controls muscle contractions and secretion when food stretches the wall; the brain and spinal cord also influence digestion."}'::jsonb,
    '[{"text": "A peptic ulcer can form in the lining of the duodenum (duodenal ulcer), most often from H. pylori infection or NSAID use.", "disease_id": "peptic_ulcer_disease"}, {"text": "Celiac disease is an immune reaction to gluten that damages the small intestine and prevents nutrient absorption."}, {"text": "Other small intestine disorders include Crohn''s disease, infections, bleeding, intestinal obstruction and cancer."}]'::jsonb,
    'The small intestine is the longest part of the digestive system, about 20 feet (roughly 6 metres), folded many times to fit in the abdomen.',
    '[{"title": "Small & Large Intestine - NCI SEER Training Modules", "url": "https://training.seer.cancer.gov/anatomy/digestive/regions/intestine.html", "licence": "Public domain"}, {"title": "Small Intestine Disorders - MedlinePlus (NLM)", "url": "https://medlineplus.gov/smallintestinedisorders.html", "licence": "Public domain"}, {"title": "Your Digestive System & How It Works - NIDDK", "url": "https://www.niddk.nih.gov/health-information/digestive-diseases/digestive-system-how-it-works", "licence": "Public domain"}, {"title": "Anatomy of the Liver & Gallbladder - NCI SEER Training Modules", "url": "https://training.seer.cancer.gov/biliary/anatomy/liver.html", "licence": "Public domain"}, {"title": "Definition & Facts for Cirrhosis - NIDDK", "url": "https://www.niddk.nih.gov/health-information/liver-disease/cirrhosis/definition-facts", "licence": "Public domain"}, {"title": "Definition & Facts for Peptic Ulcers - NIDDK", "url": "https://www.niddk.nih.gov/health-information/digestive-diseases/peptic-ulcers-stomach-ulcers/definition-facts", "licence": "Public domain"}, {"title": "Definition & Facts for Celiac Disease - NIDDK", "url": "https://www.niddk.nih.gov/health-information/digestive-diseases/celiac-disease/definition-facts", "licence": "Public domain"}]'::jsonb,
    'draft')
on conflict (key) do update set
    kind = excluded.kind,
    fma_ids = excluded.fma_ids,
    layer = excluded.layer,
    system = excluded.system,
    display_name = excluded.display_name,
    aliases = excluded.aliases,
    summary_plain = excluded.summary_plain,
    function_plain = excluded.function_plain,
    description = excluded.description,
    location = excluded.location,
    details = excluded.details,
    clinical = excluded.clinical,
    exam_tip = excluded.exam_tip,
    sources = excluded.sources,
    updated_at = now()
where b.status = 'draft'
  and (b.kind, b.fma_ids, b.layer, b.system, b.display_name, b.aliases, b.summary_plain, b.function_plain, b.description, b.location, b.details, b.clinical, b.exam_tip, b.sources)
  is distinct from (excluded.kind, excluded.fma_ids, excluded.layer, excluded.system, excluded.display_name, excluded.aliases, excluded.summary_plain, excluded.function_plain, excluded.description, excluded.location, excluded.details, excluded.clinical, excluded.exam_tip, excluded.sources);

-- Large intestine  (11 FMA ids)
insert into public.body_part_info as b (key, kind, fma_ids, layer, system, display_name, aliases, summary_plain, function_plain, description, location, details, clinical, exam_tip, sources, status)
values ('group:large_intestine',
    'group',
    array['FMA11338', 'FMA14542', 'FMA14544', 'FMA14545', 'FMA14546', 'FMA14547', 'FMA14647', 'FMA15042', 'FMA15043', 'FMA15044', 'FMA16549']::text[],
    'organ',
    'digestive',
    'Large intestine',
    array['large bowel', 'colon']::text[],
    'The large intestine is the last part of the digestive tube. It is a wide tube in the belly that starts where the small intestine ends and finishes at the anus.',
    'It takes water out of leftover food, turns the waste into stool and stores it until a bowel movement.',
    'The large intestine runs from the ileocecal junction to the anus. Its parts are the cecum (with the appendix), the colon (ascending, transverse, descending and sigmoid) and the rectum, ending in the anal canal; the colon alone is about 150 cm long. It is wider than the small intestine, has no villi, and its outer muscle forms three bands, the teniae coli, which gather the wall into pouches (haustra).',
    'The cecum and ascending colon form the right colon; the hepatic flexure lies under the right lobe of the liver; the transverse colon lies at the front of the abdomen; the splenic flexure lies near the spleen and tail of the pancreas; the descending and sigmoid colon form the left colon; the rectum follows the curve of the sacrum.',
    '{"functions": "Absorbs water and electrolytes, turns liquid waste into stool, and stores stool in the rectum until it is passed. It makes no digestive enzymes; its bacteria break down leftover nutrients and make vitamin K.", "lymph_drainage": "To lymph nodes along the colon (pericolic, epicolic and mesenteric nodes) and along the major arteries that supply each segment; the colon''s mesentery holds about 100 to 150 lymph nodes."}'::jsonb,
    '[{"text": "Colorectal cancer starts in the colon or rectum; adenomatous polyps can turn into cancer, so screening (stool tests, colonoscopy) is recommended from age 45 in the United States."}, {"text": "Diverticulitis is inflammation or infection of small pouches in the colon wall."}, {"text": "Ulcerative colitis causes ulcers in the colon and rectum; long-standing colitis raises colorectal cancer risk."}, {"text": "Irritable bowel syndrome causes abdominal cramping and changes in bowel habit."}]'::jsonb,
    'The longitudinal muscle of the colon is limited to three bands, the teniae coli, whose pull forms the pouches called haustra.',
    '[{"title": "Small & Large Intestine - NCI SEER Training Modules", "url": "https://training.seer.cancer.gov/anatomy/digestive/regions/intestine.html", "licence": "Public domain"}, {"title": "Colorectal Anatomy - NCI SEER Training Modules", "url": "https://training.seer.cancer.gov/colorectal/anatomy/", "licence": "Public domain"}, {"title": "Colorectal Anatomy and ICD-O-3 - NCI SEER Training Modules", "url": "https://training.seer.cancer.gov/colorectal/anatomy/colorectal-anatomy-and-icdO3.html", "licence": "Public domain"}, {"title": "Colorectal Wall of Pathology - NCI SEER Training Modules", "url": "https://training.seer.cancer.gov/colorectal/anatomy/colorectal-wall-of-pathology.html", "licence": "Public domain"}, {"title": "EOD Regional Nodes - NCI SEER Training Modules", "url": "https://training.seer.cancer.gov/colorectal/staging/eod-regional-nodes.html", "licence": "Public domain"}, {"title": "Your Digestive System & How It Works - NIDDK", "url": "https://www.niddk.nih.gov/health-information/digestive-diseases/digestive-system-how-it-works", "licence": "Public domain"}, {"title": "Colonic Diseases - MedlinePlus (NLM)", "url": "https://medlineplus.gov/colonicdiseases.html", "licence": "Public domain"}, {"title": "Colorectal Cancer - MedlinePlus (NLM)", "url": "https://medlineplus.gov/colorectalcancer.html", "licence": "Public domain"}]'::jsonb,
    'draft')
on conflict (key) do update set
    kind = excluded.kind,
    fma_ids = excluded.fma_ids,
    layer = excluded.layer,
    system = excluded.system,
    display_name = excluded.display_name,
    aliases = excluded.aliases,
    summary_plain = excluded.summary_plain,
    function_plain = excluded.function_plain,
    description = excluded.description,
    location = excluded.location,
    details = excluded.details,
    clinical = excluded.clinical,
    exam_tip = excluded.exam_tip,
    sources = excluded.sources,
    updated_at = now()
where b.status = 'draft'
  and (b.kind, b.fma_ids, b.layer, b.system, b.display_name, b.aliases, b.summary_plain, b.function_plain, b.description, b.location, b.details, b.clinical, b.exam_tip, b.sources)
  is distinct from (excluded.kind, excluded.fma_ids, excluded.layer, excluded.system, excluded.display_name, excluded.aliases, excluded.summary_plain, excluded.function_plain, excluded.description, excluded.location, excluded.details, excluded.clinical, excluded.exam_tip, excluded.sources);

-- Appendix  (1 FMA ids)
insert into public.body_part_info as b (key, kind, fma_ids, layer, system, display_name, aliases, summary_plain, function_plain, description, location, details, clinical, exam_tip, sources, status)
values ('appendix',
    'part',
    array['FMA14542']::text[],
    'organ',
    'digestive',
    'Appendix',
    '{}'::text[],
    'The appendix is a small, finger-shaped pouch attached to the start of the large intestine, in the lower right part of the belly.',
    'It has no known function.',
    'The appendix (vermiform appendix) is a narrow, worm-like pouch that branches off the cecum, the first part of the large intestine. It counts as part of the large intestine along with the cecum, colon and rectum. It has no known function, but it can become blocked and inflamed.',
    'In the lower right area of the abdomen, hanging from the lower part of the cecum, near where the small intestine (ileum) empties into the large intestine at the ileocecal valve.',
    '{"functions": "No known function."}'::jsonb,
    '[{"text": "Inflammation of the appendix (appendicitis) is a medical emergency and is the most common cause of sudden abdominal pain needing surgery in the United States.", "disease_id": "acute_appendicitis"}, {"text": "Appendicitis is usually caused by a blockage inside the appendix, such as hardened stool or a growth.", "disease_id": "acute_appendicitis"}, {"text": "Pain often starts near the navel and moves lower and to the right; treatment almost always means removing the appendix.", "disease_id": "acute_appendicitis"}, {"text": "If untreated, the appendix can burst, causing peritonitis (a serious abdominal infection) or an appendiceal abscess.", "disease_id": "acute_appendicitis"}]'::jsonb,
    'About 5 to 9 out of every 100 people get appendicitis at some point, most often in their teens and 20s.',
    '[{"title": "Appendicitis - MedlinePlus (NLM)", "url": "https://medlineplus.gov/appendicitis.html", "licence": "Public domain"}, {"title": "Definition & Facts for Appendicitis - NIDDK", "url": "https://www.niddk.nih.gov/health-information/digestive-diseases/appendicitis/definition-facts", "licence": "Public domain"}, {"title": "Symptoms & Causes of Appendicitis - NIDDK", "url": "https://www.niddk.nih.gov/health-information/digestive-diseases/appendicitis/symptoms-causes", "licence": "Public domain"}, {"title": "Your Digestive System & How It Works - NIDDK", "url": "https://www.niddk.nih.gov/health-information/digestive-diseases/digestive-system-how-it-works", "licence": "Public domain"}, {"title": "Colorectal Anatomy and ICD-O-3 - NCI SEER Training Modules", "url": "https://training.seer.cancer.gov/colorectal/anatomy/colorectal-anatomy-and-icdO3.html", "licence": "Public domain"}, {"title": "Small & Large Intestine - NCI SEER Training Modules", "url": "https://training.seer.cancer.gov/anatomy/digestive/regions/intestine.html", "licence": "Public domain"}]'::jsonb,
    'draft')
on conflict (key) do update set
    kind = excluded.kind,
    fma_ids = excluded.fma_ids,
    layer = excluded.layer,
    system = excluded.system,
    display_name = excluded.display_name,
    aliases = excluded.aliases,
    summary_plain = excluded.summary_plain,
    function_plain = excluded.function_plain,
    description = excluded.description,
    location = excluded.location,
    details = excluded.details,
    clinical = excluded.clinical,
    exam_tip = excluded.exam_tip,
    sources = excluded.sources,
    updated_at = now()
where b.status = 'draft'
  and (b.kind, b.fma_ids, b.layer, b.system, b.display_name, b.aliases, b.summary_plain, b.function_plain, b.description, b.location, b.details, b.clinical, b.exam_tip, b.sources)
  is distinct from (excluded.kind, excluded.fma_ids, excluded.layer, excluded.system, excluded.display_name, excluded.aliases, excluded.summary_plain, excluded.function_plain, excluded.description, excluded.location, excluded.details, excluded.clinical, excluded.exam_tip, excluded.sources);

-- Kidney  (2 FMA ids)
insert into public.body_part_info as b (key, kind, fma_ids, layer, system, display_name, aliases, summary_plain, function_plain, description, location, details, clinical, exam_tip, sources, status)
values ('kidney',
    'part',
    array['FMA7204', 'FMA7205']::text[],
    'organ',
    'urinary',
    'Kidney',
    '{}'::text[],
    'The kidneys are two bean-shaped organs, each about the size of a fist. They sit at the back of the belly, just below the ribs, one on each side of the spine.',
    'They clean the blood by taking out wastes and extra water, which leave the body as urine.',
    'The kidneys are the main organs of the urinary system. Each adult kidney is roughly 12 cm long, 6 cm wide and 3 cm thick, with an indented medial border, the hilum. Inside, an outer cortex surrounds a medulla made of renal pyramids; urine drains through minor and major calyces into the renal pelvis and on into the ureter. Each kidney holds about a million nephrons, the filtering units.',
    'On the posterior abdominal wall, behind the peritoneum (retroperitoneal), between the 12th thoracic and 3rd lumbar vertebrae, partly shielded by the lower ribs. The right kidney usually sits a little lower than the left because the liver pushes it down.',
    '{"functions": "Filter the blood and remove wastes, extra fluid and acid in urine; balance water, sodium, potassium, calcium and phosphorus; make hormones that help control blood pressure, stimulate red blood cell production and support bone health. The juxtaglomerular apparatus secretes renin.", "blood_supply": "The renal artery enters at the hilum and branches down to the nephrons; each glomerulus receives an afferent arteriole and is drained by an efferent arteriole. Filtered blood leaves through the renal vein at the hilum."}'::jsonb,
    '[{"text": "Chronic kidney disease slowly damages the nephrons over years; diabetes and high blood pressure are its most common causes, and many people have no symptoms until it is advanced.", "disease_id": "chronic_kidney_disease"}, {"text": "Kidney failure is treated with dialysis or a kidney transplant.", "disease_id": "chronic_kidney_disease"}, {"text": "Kidney stones are solid masses formed from substances in urine; a stuck stone can block urine flow and cause severe back or side pain and blood in the urine."}, {"text": "A urinary tract infection can reach the kidney (pyelonephritis); pain in the back or side below the ribs and fever are possible symptoms.", "disease_id": "urinary_tract_infection"}]'::jsonb,
    'The right kidney usually lies slightly lower than the left, because the liver displaces it downward.',
    '[{"title": "Kidneys - NCI SEER Training Modules", "url": "https://training.seer.cancer.gov/anatomy/urinary/components/kidney.html", "licence": "Public domain"}, {"title": "Your Kidneys & How They Work - NIDDK", "url": "https://www.niddk.nih.gov/health-information/kidney-disease/kidneys-how-they-work", "licence": "Public domain"}, {"title": "Your Urinary Tract & How It Works - NIDDK", "url": "https://www.niddk.nih.gov/health-information/urologic-diseases/urinary-tract-how-it-works", "licence": "Public domain"}, {"title": "Kidney Diseases - MedlinePlus (NLM)", "url": "https://medlineplus.gov/kidneydiseases.html", "licence": "Public domain"}, {"title": "Chronic Kidney Disease - MedlinePlus (NLM)", "url": "https://medlineplus.gov/chronickidneydisease.html", "licence": "Public domain"}, {"title": "Kidney Stones - MedlinePlus (NLM)", "url": "https://medlineplus.gov/kidneystones.html", "licence": "Public domain"}, {"title": "Urinary Tract Infections - MedlinePlus (NLM)", "url": "https://medlineplus.gov/urinarytractinfections.html", "licence": "Public domain"}]'::jsonb,
    'draft')
on conflict (key) do update set
    kind = excluded.kind,
    fma_ids = excluded.fma_ids,
    layer = excluded.layer,
    system = excluded.system,
    display_name = excluded.display_name,
    aliases = excluded.aliases,
    summary_plain = excluded.summary_plain,
    function_plain = excluded.function_plain,
    description = excluded.description,
    location = excluded.location,
    details = excluded.details,
    clinical = excluded.clinical,
    exam_tip = excluded.exam_tip,
    sources = excluded.sources,
    updated_at = now()
where b.status = 'draft'
  and (b.kind, b.fma_ids, b.layer, b.system, b.display_name, b.aliases, b.summary_plain, b.function_plain, b.description, b.location, b.details, b.clinical, b.exam_tip, b.sources)
  is distinct from (excluded.kind, excluded.fma_ids, excluded.layer, excluded.system, excluded.display_name, excluded.aliases, excluded.summary_plain, excluded.function_plain, excluded.description, excluded.location, excluded.details, excluded.clinical, excluded.exam_tip, excluded.sources);

-- Urinary bladder  (1 FMA ids)
insert into public.body_part_info as b (key, kind, fma_ids, layer, system, display_name, aliases, summary_plain, function_plain, description, location, details, clinical, exam_tip, sources, status)
values ('urinary bladder',
    'part',
    array['FMA15900']::text[],
    'organ',
    'urinary',
    'Urinary bladder',
    array['bladder']::text[],
    'The bladder is a hollow, balloon-shaped bag of muscle low in the belly, in the pelvis between the hip bones.',
    'It stores urine from the kidneys and then squeezes to push it out of the body.',
    'The urinary bladder is a muscular reservoir that stores urine until it is passed. Its size and shape change with how full it is. Its wall has a mucosa of transitional epithelium that folds into rugae when empty, a submucosa, and smooth muscle called the detrusor, whose contraction empties the bladder. The trigone on its floor lies between the two ureter openings and the urethral opening.',
    'In the pelvic cavity, behind the pubic symphysis and below the parietal peritoneum, which covers only its upper surface. The two ureters enter it from the kidneys, and the urethra leaves from the apex of the trigone on its floor.',
    '{"functions": "Stores urine, holding about 1.5 to 2 cups in an adult, and expels it when the detrusor contracts. Flaps over the ureter openings stop urine flowing back up to the kidneys. Internal and external sphincters keep urine in until urination."}'::jsonb,
    '[{"text": "Cystitis is inflammation of the bladder, often caused by infection; urinary tract infections are far more common in women than in men.", "disease_id": "urinary_tract_infection"}, {"text": "Bladder infection can cause painful or burning urination, a frequent urge to urinate and pressure in the lower belly; it is treated with antibiotics.", "disease_id": "urinary_tract_infection"}, {"text": "Bladder cancer forms in the bladder lining; smoking and workplace chemicals are risk factors, and blood in the urine is a key symptom. It is the sixth most common cancer in the United States."}, {"text": "Urinary incontinence (loss of bladder control) and overactive bladder are common bladder problems."}, {"text": "Cystoscopy uses a scope to look at the inside of the bladder wall."}]'::jsonb,
    'The trigone is a triangle on the bladder floor: the two ureter openings form its base and the urethral opening is its apex.',
    '[{"title": "Urinary Bladder - NCI SEER Training Modules", "url": "https://training.seer.cancer.gov/anatomy/urinary/components/bladder.html", "licence": "Public domain"}, {"title": "Your Urinary Tract & How It Works - NIDDK", "url": "https://www.niddk.nih.gov/health-information/urologic-diseases/urinary-tract-how-it-works", "licence": "Public domain"}, {"title": "Bladder Diseases - MedlinePlus (NLM)", "url": "https://medlineplus.gov/bladderdiseases.html", "licence": "Public domain"}, {"title": "Urinary Tract Infections - MedlinePlus (NLM)", "url": "https://medlineplus.gov/urinarytractinfections.html", "licence": "Public domain"}, {"title": "Bladder Cancer - MedlinePlus (NLM)", "url": "https://medlineplus.gov/bladdercancer.html", "licence": "Public domain"}]'::jsonb,
    'draft')
on conflict (key) do update set
    kind = excluded.kind,
    fma_ids = excluded.fma_ids,
    layer = excluded.layer,
    system = excluded.system,
    display_name = excluded.display_name,
    aliases = excluded.aliases,
    summary_plain = excluded.summary_plain,
    function_plain = excluded.function_plain,
    description = excluded.description,
    location = excluded.location,
    details = excluded.details,
    clinical = excluded.clinical,
    exam_tip = excluded.exam_tip,
    sources = excluded.sources,
    updated_at = now()
where b.status = 'draft'
  and (b.kind, b.fma_ids, b.layer, b.system, b.display_name, b.aliases, b.summary_plain, b.function_plain, b.description, b.location, b.details, b.clinical, b.exam_tip, b.sources)
  is distinct from (excluded.kind, excluded.fma_ids, excluded.layer, excluded.system, excluded.display_name, excluded.aliases, excluded.summary_plain, excluded.function_plain, excluded.description, excluded.location, excluded.details, excluded.clinical, excluded.exam_tip, excluded.sources);

-- Brain  (52 FMA ids)
insert into public.body_part_info as b (key, kind, fma_ids, layer, system, display_name, aliases, summary_plain, function_plain, description, location, details, clinical, exam_tip, sources, status)
values ('group:fma_FMA50801_o',
    'group',
    array['FMA241998', 'FMA61815', 'FMA61998', 'FMA62008', 'FMA62032', 'FMA62033', 'FMA62327', 'FMA67942', 'FMA67944', 'FMA72653', 'FMA72654', 'FMA72655', 'FMA72656', 'FMA72657', 'FMA72658', 'FMA72661', 'FMA72662', 'FMA72665', 'FMA72666', 'FMA72667', 'FMA72668', 'FMA72669', 'FMA72670', 'FMA72671', 'FMA72672', 'FMA72685', 'FMA72686', 'FMA72687', 'FMA72688', 'FMA72689', 'FMA72690', 'FMA72705', 'FMA72706', 'FMA72713', 'FMA72714', 'FMA72717', 'FMA72718', 'FMA72906', 'FMA72907', 'FMA72975', 'FMA72976', 'FMA72977', 'FMA72978', 'FMA73422', 'FMA73423', 'FMA73434', 'FMA73435', 'FMA78449', 'FMA78450', 'FMA78454', 'FMA78467', 'FMA78469']::text[],
    'organ',
    'nervous',
    'Brain',
    '{}'::text[],
    'The brain is the body''s control center. It sits inside the skull and joins the spinal cord at a large opening in the base of the skull.',
    'It controls thinking, memory, speech and movement, and helps run many of the body''s organs.',
    'The brain and spinal cord form the central nervous system. The cerebrum, the largest part, is split into right and left hemispheres joined by the corpus callosum; each has frontal, parietal, occipital and temporal lobes plus the deep insula. The diencephalon (thalamus, hypothalamus, epithalamus) lies centrally. The brainstem (midbrain, pons, medulla oblongata) links it to the spinal cord, and the cerebellum is the second largest part.',
    'In the cranial cavity of the skull. It is continuous with the spinal cord at the foramen magnum. A fold of dura, the tentorium, separates the cerebrum above from the cerebellum and brainstem below. It is wrapped by three meninges: dura mater, arachnoid and pia mater.',
    '{"functions": "Controls thought, memory, speech and movement and helps regulate many organs. The thalamus relays sensory signals (except smell) to the cerebral cortex; the hypothalamus helps keep homeostasis by regulating visceral activities; all ascending and descending tracts pass through the medulla oblongata."}'::jsonb,
    '[{"text": "A stroke is a loss of blood flow to part of the brain; brain cells start dying within minutes. About 80% of strokes are ischemic (a clot blocks a vessel).", "disease_id": "ischemic_stroke"}, {"text": "A hemorrhagic stroke happens when a blood vessel breaks and bleeds into the brain."}, {"text": "Meningitis is inflammation of the meninges; bacterial meningitis is rare but can be deadly and can cause hearing loss or brain damage.", "disease_id": "bacterial_meningitis"}, {"text": "Brain tumors are named supratentorial when in the cerebral lobes and infratentorial when in the cerebellum or brainstem."}, {"text": "Degenerative diseases such as Alzheimer''s and Parkinson''s disease, encephalitis and traumatic brain injury are other important brain disorders."}]'::jsonb,
    'The cerebrum is the largest part of the brain and the cerebellum the second largest; the thalamus makes up about 80 percent of the diencephalon.',
    '[{"title": "Central Nervous System - NCI SEER Training Modules", "url": "https://training.seer.cancer.gov/anatomy/nervous/organization/cns.html", "licence": "Public domain"}, {"title": "Brain Diseases - MedlinePlus (NLM)", "url": "https://medlineplus.gov/braindiseases.html", "licence": "Public domain"}, {"title": "Stroke - MedlinePlus (NLM)", "url": "https://medlineplus.gov/stroke.html", "licence": "Public domain"}, {"title": "Meningitis - MedlinePlus (NLM)", "url": "https://medlineplus.gov/meningitis.html", "licence": "Public domain"}, {"title": "Tentorium - NCI SEER Training Modules", "url": "https://training.seer.cancer.gov/cns/cns-anatomy/tentorium.html", "licence": "Public domain"}, {"title": "Brain and Spine Tumor Anatomy - National Cancer Institute", "url": "https://www.cancer.gov/rare-brain-spine-tumor/tumors/anatomy", "licence": "Public domain"}, {"title": "The Nervous System - NCI SEER Training Modules", "url": "https://training.seer.cancer.gov/cns/nervous-system/", "licence": "Public domain"}]'::jsonb,
    'draft')
on conflict (key) do update set
    kind = excluded.kind,
    fma_ids = excluded.fma_ids,
    layer = excluded.layer,
    system = excluded.system,
    display_name = excluded.display_name,
    aliases = excluded.aliases,
    summary_plain = excluded.summary_plain,
    function_plain = excluded.function_plain,
    description = excluded.description,
    location = excluded.location,
    details = excluded.details,
    clinical = excluded.clinical,
    exam_tip = excluded.exam_tip,
    sources = excluded.sources,
    updated_at = now()
where b.status = 'draft'
  and (b.kind, b.fma_ids, b.layer, b.system, b.display_name, b.aliases, b.summary_plain, b.function_plain, b.description, b.location, b.details, b.clinical, b.exam_tip, b.sources)
  is distinct from (excluded.kind, excluded.fma_ids, excluded.layer, excluded.system, excluded.display_name, excluded.aliases, excluded.summary_plain, excluded.function_plain, excluded.description, excluded.location, excluded.details, excluded.clinical, excluded.exam_tip, excluded.sources);

-- Cerebellum  (1 FMA ids)
insert into public.body_part_info as b (key, kind, fma_ids, layer, system, display_name, aliases, summary_plain, function_plain, description, location, details, clinical, exam_tip, sources, status)
values ('cerebellum',
    'part',
    array['FMA67944']::text[],
    'organ',
    'nervous',
    'Cerebellum',
    '{}'::text[],
    'The cerebellum is a part of the brain at the lower back of the head, tucked under the back of the main brain (cerebrum).',
    'It controls coordination and balance, for example when you play the piano or hit a tennis ball.',
    'The cerebellum is the second largest part of the brain. It lies below the occipital lobes of the cerebrum and is joined to the rest of the central nervous system by three paired bundles of myelinated fibers, the cerebellar peduncles. It controls coordination and balance.',
    'At the back of the cranial cavity, in the posterior cranial fossa, which also holds the pons and medulla oblongata. It lies below the occipital lobes and below the tentorium, the dural fold that separates it from the cerebrum.',
    '{"functions": "Coordination and balance."}'::jsonb,
    '[{"text": "Ataxias, a loss of muscle control in the arms and legs, are a key sign of cerebellar disorders."}, {"text": "Other cerebellar disorders include cancer, genetic disorders and degeneration, in which brain cells waste away; some have no cure but treatment may ease symptoms."}, {"text": "Tumors of the cerebellum or brainstem are called infratentorial tumors."}]'::jsonb,
    'The cerebellum sits in the posterior cranial fossa, which Gray''s Anatomy calls the largest and deepest of the three cranial fossae.',
    '[{"title": "Central Nervous System - NCI SEER Training Modules", "url": "https://training.seer.cancer.gov/anatomy/nervous/organization/cns.html", "licence": "Public domain"}, {"title": "Cerebellar Disorders - MedlinePlus (NLM)", "url": "https://medlineplus.gov/cerebellardisorders.html", "licence": "Public domain"}, {"title": "Tentorium - NCI SEER Training Modules", "url": "https://training.seer.cancer.gov/cns/cns-anatomy/tentorium.html", "licence": "Public domain"}, {"title": "Brain and Spine Tumor Anatomy - National Cancer Institute", "url": "https://www.cancer.gov/rare-brain-spine-tumor/tumors/anatomy", "licence": "Public domain"}, {"title": "Gray''s Anatomy of the Human Body, 20th ed. (1918), skull (interior of the base) - PubAnnotation GrayAnatomy doc 47", "url": "https://pubannotation.org/docs/sourcedb/GrayAnatomy/sourceid/47", "licence": "Public domain"}]'::jsonb,
    'draft')
on conflict (key) do update set
    kind = excluded.kind,
    fma_ids = excluded.fma_ids,
    layer = excluded.layer,
    system = excluded.system,
    display_name = excluded.display_name,
    aliases = excluded.aliases,
    summary_plain = excluded.summary_plain,
    function_plain = excluded.function_plain,
    description = excluded.description,
    location = excluded.location,
    details = excluded.details,
    clinical = excluded.clinical,
    exam_tip = excluded.exam_tip,
    sources = excluded.sources,
    updated_at = now()
where b.status = 'draft'
  and (b.kind, b.fma_ids, b.layer, b.system, b.display_name, b.aliases, b.summary_plain, b.function_plain, b.description, b.location, b.details, b.clinical, b.exam_tip, b.sources)
  is distinct from (excluded.kind, excluded.fma_ids, excluded.layer, excluded.system, excluded.display_name, excluded.aliases, excluded.summary_plain, excluded.function_plain, excluded.description, excluded.location, excluded.details, excluded.clinical, excluded.exam_tip, excluded.sources);

-- Pituitary gland  (1 FMA ids)
insert into public.body_part_info as b (key, kind, fma_ids, layer, system, display_name, aliases, summary_plain, function_plain, description, location, details, clinical, exam_tip, sources, status)
values ('pituitary gland',
    'part',
    array['FMA13889']::text[],
    'organ',
    'endocrine',
    'Pituitary gland',
    array['hypophysis', 'master gland']::text[],
    'The pituitary gland is a pea-sized gland at the base of the brain, just above the back of the nose.',
    'It makes hormones that control growth and tell many other glands, such as the thyroid and adrenal glands, how much hormone to make.',
    'The pituitary gland (hypophysis) is a small endocrine gland, about 1 cm across, hanging from the hypothalamus by a stalk, the infundibulum. Its anterior lobe (adenohypophysis) is controlled by releasing hormones from the hypothalamus; its posterior lobe (neurohypophysis) is controlled by nerve signals. Because it regulates other glands, it is often called the master gland.',
    'In the sella turcica, a hollow in the sphenoid bone at the base of the skull, where it is almost surrounded by bone. It lies below the hypothalamus of the brain, to which the infundibulum attaches it.',
    '{"functions": "Anterior lobe: growth hormone, thyroid-stimulating hormone, adrenocorticotropic hormone (ACTH, which drives cortisol release), the gonadotropins LH and FSH, and prolactin. Posterior lobe: antidiuretic hormone, which makes the kidneys keep water, and oxytocin, which contracts the uterus and ejects milk.", "nerve_supply": "The posterior lobe is controlled by nerve stimulation from the hypothalamus, which is connected to it through the infundibulum."}'::jsonb,
    '[{"text": "Pituitary tumors are the most common cause of pituitary disorders; most are benign adenomas, and very few are malignant."}, {"text": "Many pituitary tumors make excess hormone and can cause conditions such as Cushing''s syndrome or hyperthyroidism; headaches and vision problems can also occur."}, {"text": "Pituitary disorders often mean too much or too little of one hormone, for example acromegaly, hyperprolactinemia or hypopituitarism."}, {"text": "Surgery to remove a pituitary tumor can be done through the nose or upper lip, since the gland lies just above the sphenoid bone."}]'::jsonb,
    'The pituitary sits in the sella turcica of the sphenoid bone and is linked to the hypothalamus by the infundibulum.',
    '[{"title": "Pituitary Gland - NCI SEER Training Modules", "url": "https://training.seer.cancer.gov/anatomy/endocrine/glands/pituitary.html", "licence": "Public domain"}, {"title": "Pituitary Disorders - MedlinePlus (NLM)", "url": "https://medlineplus.gov/pituitarydisorders.html", "licence": "Public domain"}, {"title": "Pituitary Tumors - MedlinePlus (NLM)", "url": "https://medlineplus.gov/pituitarytumors.html", "licence": "Public domain"}, {"title": "What Are Pituitary Tumors? - National Cancer Institute", "url": "https://www.cancer.gov/types/pituitary/what-are-pituitary-tumors", "licence": "Public domain"}, {"title": "Pituitary Tumors Treatment (PDQ) Patient Version - National Cancer Institute", "url": "https://www.cancer.gov/types/pituitary/patient/pituitary-treatment-pdq", "licence": "Public domain"}]'::jsonb,
    'draft')
on conflict (key) do update set
    kind = excluded.kind,
    fma_ids = excluded.fma_ids,
    layer = excluded.layer,
    system = excluded.system,
    display_name = excluded.display_name,
    aliases = excluded.aliases,
    summary_plain = excluded.summary_plain,
    function_plain = excluded.function_plain,
    description = excluded.description,
    location = excluded.location,
    details = excluded.details,
    clinical = excluded.clinical,
    exam_tip = excluded.exam_tip,
    sources = excluded.sources,
    updated_at = now()
where b.status = 'draft'
  and (b.kind, b.fma_ids, b.layer, b.system, b.display_name, b.aliases, b.summary_plain, b.function_plain, b.description, b.location, b.details, b.clinical, b.exam_tip, b.sources)
  is distinct from (excluded.kind, excluded.fma_ids, excluded.layer, excluded.system, excluded.display_name, excluded.aliases, excluded.summary_plain, excluded.function_plain, excluded.description, excluded.location, excluded.details, excluded.clinical, excluded.exam_tip, excluded.sources);

-- Eyeball  (20 FMA ids)
insert into public.body_part_info as b (key, kind, fma_ids, layer, system, display_name, aliases, summary_plain, function_plain, description, location, details, clinical, exam_tip, sources, status)
values ('group:eye_ball',
    'group',
    array['FMA58081', 'FMA58082', 'FMA58236', 'FMA58237', 'FMA58239', 'FMA58240', 'FMA58242', 'FMA58243', 'FMA58271', 'FMA58272', 'FMA58299', 'FMA58300', 'FMA58483', 'FMA58484', 'FMA58607', 'FMA58608', 'FMA58828', 'FMA58829', 'FMA58839', 'FMA58840']::text[],
    'organ',
    'nervous',
    'Eyeball',
    '{}'::text[],
    'The eyeball is the round organ of sight that sits in the eye socket of the skull. Light enters at the front and is sensed at the back.',
    'It focuses light onto the light-sensitive retina, which turns it into signals that the optic nerve carries to the brain.',
    'The eyeball has three layers: the white sclera outside, the middle uvea (iris, ciliary body and choroid), and the light-sensitive retina at the back. At the front, the clear dome-shaped cornea and the lens behind it focus light onto the retina; the colored iris controls how much light enters through the pupil. Gel called vitreous fills the eye.',
    'In the orbit, a four-sided, pyramid-shaped cavity of the skull. The optic nerve links the retina at the back of the eye to the brain, passing through the optic foramen at the apex of the orbit.',
    '{"functions": "Cornea bends and focuses light and protects the eye from germs and dust; iris controls light entering the pupil; lens works with the cornea to focus light on the retina; retinal photoreceptors turn light into electrical signals; the macula, the center of the retina, gives fine detail."}'::jsonb,
    '[{"text": "Cataract is clouding of the lens, mostly from aging; surgery replaces the cloudy lens with an artificial intraocular lens."}, {"text": "Glaucoma is a group of diseases that damage the optic nerve, usually as fluid pressure inside the eye slowly rises; vision loss starts in side vision."}, {"text": "Retinal detachment, in which the retina pulls away from the back of the eye, is a medical emergency."}, {"text": "Diabetic retinopathy is damage to the small blood vessels of the retina caused by diabetes."}, {"text": "Refractive errors are the most common vision problems."}]'::jsonb,
    'The cornea and lens together focus light on the retina; with age, strands in the vitreous gel clump and cast shadows on the retina, seen as floaters.',
    '[{"title": "How the Eyes Work - National Eye Institute", "url": "https://www.nei.nih.gov/learn-about-eye-health/healthy-vision/how-eyes-work", "licence": "Public domain"}, {"title": "Uveitis - National Eye Institute", "url": "https://www.nei.nih.gov/learn-about-eye-health/eye-conditions-and-diseases/uveitis", "licence": "Public domain"}, {"title": "Floaters - National Eye Institute", "url": "https://www.nei.nih.gov/learn-about-eye-health/eye-conditions-and-diseases/floaters", "licence": "Public domain"}, {"title": "Corneal Disorders - MedlinePlus (NLM)", "url": "https://medlineplus.gov/cornealdisorders.html", "licence": "Public domain"}, {"title": "Retinal Disorders - MedlinePlus (NLM)", "url": "https://medlineplus.gov/retinaldisorders.html", "licence": "Public domain"}, {"title": "Cataract - MedlinePlus (NLM)", "url": "https://medlineplus.gov/cataract.html", "licence": "Public domain"}, {"title": "Glaucoma - MedlinePlus (NLM)", "url": "https://medlineplus.gov/glaucoma.html", "licence": "Public domain"}, {"title": "Eye Diseases - MedlinePlus (NLM)", "url": "https://medlineplus.gov/eyediseases.html", "licence": "Public domain"}, {"title": "Glaucoma - National Eye Institute", "url": "https://www.nei.nih.gov/learn-about-eye-health/eye-conditions-and-diseases/glaucoma", "licence": "Public domain"}, {"title": "Optic Nerve Disorders - MedlinePlus (NLM)", "url": "https://medlineplus.gov/opticnervedisorders.html", "licence": "Public domain"}, {"title": "Gray''s Anatomy of the Human Body, 20th ed. (1918), the skull as a whole - PubAnnotation GrayAnatomy doc 46", "url": "https://pubannotation.org/docs/sourcedb/GrayAnatomy/sourceid/46", "licence": "Public domain"}, {"title": "Gray''s Anatomy of the Human Body, 20th ed. (1918), skull (interior of the base) - PubAnnotation GrayAnatomy doc 47", "url": "https://pubannotation.org/docs/sourcedb/GrayAnatomy/sourceid/47", "licence": "Public domain"}]'::jsonb,
    'draft')
on conflict (key) do update set
    kind = excluded.kind,
    fma_ids = excluded.fma_ids,
    layer = excluded.layer,
    system = excluded.system,
    display_name = excluded.display_name,
    aliases = excluded.aliases,
    summary_plain = excluded.summary_plain,
    function_plain = excluded.function_plain,
    description = excluded.description,
    location = excluded.location,
    details = excluded.details,
    clinical = excluded.clinical,
    exam_tip = excluded.exam_tip,
    sources = excluded.sources,
    updated_at = now()
where b.status = 'draft'
  and (b.kind, b.fma_ids, b.layer, b.system, b.display_name, b.aliases, b.summary_plain, b.function_plain, b.description, b.location, b.details, b.clinical, b.exam_tip, b.sources)
  is distinct from (excluded.kind, excluded.fma_ids, excluded.layer, excluded.system, excluded.display_name, excluded.aliases, excluded.summary_plain, excluded.function_plain, excluded.description, excluded.location, excluded.details, excluded.clinical, excluded.exam_tip, excluded.sources);

-- Skull  (22 FMA ids)
insert into public.body_part_info as b (key, kind, fma_ids, layer, system, display_name, aliases, summary_plain, function_plain, description, location, details, clinical, exam_tip, sources, status)
values ('group:skull',
    'group',
    array['FMA52734', 'FMA52735', 'FMA52736', 'FMA52738', 'FMA52739', 'FMA52740', 'FMA52748', 'FMA52788', 'FMA52789', 'FMA52892', 'FMA52893', 'FMA53645', 'FMA53646', 'FMA53647', 'FMA53648', 'FMA53649', 'FMA53650', 'FMA53655', 'FMA53656', 'FMA54737', 'FMA54738', 'FMA9710']::text[],
    'bone',
    'musculoskeletal',
    'Skull',
    '{}'::text[],
    'The skull is the bony framework of the head. It is made of the cranium, which surrounds the brain, and the bones of the face.',
    'It is hard and protects the brain, and it forms the eye sockets, nose and jaws.',
    'The skull has the cranium above and behind and the face below and in front. The 8 cranial bones are the paired parietal and temporal bones and the single frontal, occipital, ethmoid and sphenoid bones. The 14 facial bones are the paired maxillae, zygomatic, nasal, palatine, lacrimal and inferior nasal conchae, plus the mandible and vomer. Most of its bones meet at fixed joints called sutures.',
    'Forms the head. The brain sits in the cranial cavity and joins the spinal cord through the foramen magnum in the occipital bone. The orbits and nasal cavity open on the front of the face.',
    '{"type": "flat", "joints": "Sutures: coronal (frontal with parietals), sagittal (between parietals), lambdoid (parietals with occipital), squamosal (temporal with parietal). Temporomandibular joints on each side connect the lower jaw (mandible) to the skull.", "landmarks": "Foramen magnum; anterior, middle and posterior cranial fossae; sella turcica holding the pituitary; optic foramen; orbits; zygomatic arch; mastoid process; temporal fossa; bregma and lambda, marking the anterior and posterior fontanelles of the fetal skull."}'::jsonb,
    '[{"text": "A closed head injury does not break through the skull; in an open (penetrating) injury an object pierces the skull and enters the brain."}, {"text": "Skull fractures are among the more severe head injuries, along with concussion and traumatic brain injury."}, {"text": "Temporomandibular disorders, over 30 conditions of the jaw joint and chewing muscles, cause jaw pain, stiffness and trouble chewing."}]'::jsonb,
    'The anterior fontanelle, the largest, is not fully closed until about the middle of the second year; the posterior fontanelle closes within a month or two after birth.',
    '[{"title": "Axial Skeleton - NCI SEER Training Modules", "url": "https://training.seer.cancer.gov/anatomy/skeletal/divisions/axial.html", "licence": "Public domain"}, {"title": "Classification of Bones - NCI SEER Training Modules", "url": "https://training.seer.cancer.gov/anatomy/skeletal/classification.html", "licence": "Public domain"}, {"title": "Gray''s Anatomy of the Human Body, 20th ed. (1918), the skull as a whole - PubAnnotation GrayAnatomy doc 46", "url": "https://pubannotation.org/docs/sourcedb/GrayAnatomy/sourceid/46", "licence": "Public domain"}, {"title": "Gray''s Anatomy of the Human Body, 20th ed. (1918), skull (interior of the base) - PubAnnotation GrayAnatomy doc 47", "url": "https://pubannotation.org/docs/sourcedb/GrayAnatomy/sourceid/47", "licence": "Public domain"}, {"title": "Head Injuries - MedlinePlus (NLM)", "url": "https://medlineplus.gov/headinjuries.html", "licence": "Public domain"}, {"title": "Temporomandibular Joint Dysfunction - MedlinePlus (NLM)", "url": "https://medlineplus.gov/temporomandibularjointdysfunction.html", "licence": "Public domain"}, {"title": "Central Nervous System - NCI SEER Training Modules", "url": "https://training.seer.cancer.gov/anatomy/nervous/organization/cns.html", "licence": "Public domain"}]'::jsonb,
    'draft')
on conflict (key) do update set
    kind = excluded.kind,
    fma_ids = excluded.fma_ids,
    layer = excluded.layer,
    system = excluded.system,
    display_name = excluded.display_name,
    aliases = excluded.aliases,
    summary_plain = excluded.summary_plain,
    function_plain = excluded.function_plain,
    description = excluded.description,
    location = excluded.location,
    details = excluded.details,
    clinical = excluded.clinical,
    exam_tip = excluded.exam_tip,
    sources = excluded.sources,
    updated_at = now()
where b.status = 'draft'
  and (b.kind, b.fma_ids, b.layer, b.system, b.display_name, b.aliases, b.summary_plain, b.function_plain, b.description, b.location, b.details, b.clinical, b.exam_tip, b.sources)
  is distinct from (excluded.kind, excluded.fma_ids, excluded.layer, excluded.system, excluded.display_name, excluded.aliases, excluded.summary_plain, excluded.function_plain, excluded.description, excluded.location, excluded.details, excluded.clinical, excluded.exam_tip, excluded.sources);

-- Mandible  (1 FMA ids)
insert into public.body_part_info as b (key, kind, fma_ids, layer, system, display_name, aliases, summary_plain, function_plain, description, location, details, clinical, exam_tip, sources, status)
values ('mandible',
    'part',
    array['FMA52748']::text[],
    'bone',
    'musculoskeletal',
    'Mandible',
    array['lower jaw']::text[],
    'The mandible is the lower jaw bone. It is the largest and strongest bone of the face and holds the lower teeth.',
    'It holds the lower teeth and moves at the two jaw joints just in front of the ears, so the mouth can open, close and chew.',
    'The mandible is the largest and strongest bone of the face. It has a curved, horseshoe-shaped body in front and two upright rami behind. The upper (alveolar) border of the body carries sockets for the 16 lower teeth. The two halves of the bone meet in the midline at the symphysis, which fuses during the first year of life.',
    'Forms the lower part of the face and the chin. At the back, each ramus rises to meet the temporal bone of the skull at the temporomandibular joint, which can be felt just in front of the ear when the mouth opens.',
    '{"joints": "Temporomandibular joint on each side: the condyle meets the temporal bone, with an articular disc between them. The lower teeth sit in sockets along the alveolar border.", "landmarks": "Symphysis and mental protuberance; mental foramen below the second premolar (mental nerve and vessels); mylohyoid line; ramus with mandibular foramen (inferior alveolar nerve and vessels) and lingula; angle; coronoid process; condylar process with head and neck; mandibular notch."}'::jsonb,
    '[{"text": "Temporomandibular disorders (TMDs) are over 30 conditions causing pain and poor function in the jaw joint and chewing muscles; they affect about 5% of adults in the United States."}, {"text": "TMDs are about twice as common in women as in men; clicking or popping of the jaw joint without pain is common and normal."}, {"text": "After the teeth are lost, the alveolar part of the mandible is absorbed, so the bone shrinks and the mental foramen comes to lie close to its upper border."}]'::jsonb,
    'The angle of the mandible changes with age: about 175 degrees at birth, about 110 to 120 degrees in adults, and back to about 140 degrees in old age.',
    '[{"title": "Gray''s Anatomy of the Human Body, 20th ed. (1918), The Mandible (Inferior Maxillary Bone) - PubAnnotation GrayAnatomy doc 44", "url": "https://pubannotation.org/docs/sourcedb/GrayAnatomy/sourceid/44", "licence": "Public domain"}, {"title": "TMD (Temporomandibular Disorders) - NIDCR", "url": "https://www.nidcr.nih.gov/health-info/tmd", "licence": "Public domain"}]'::jsonb,
    'draft')
on conflict (key) do update set
    kind = excluded.kind,
    fma_ids = excluded.fma_ids,
    layer = excluded.layer,
    system = excluded.system,
    display_name = excluded.display_name,
    aliases = excluded.aliases,
    summary_plain = excluded.summary_plain,
    function_plain = excluded.function_plain,
    description = excluded.description,
    location = excluded.location,
    details = excluded.details,
    clinical = excluded.clinical,
    exam_tip = excluded.exam_tip,
    sources = excluded.sources,
    updated_at = now()
where b.status = 'draft'
  and (b.kind, b.fma_ids, b.layer, b.system, b.display_name, b.aliases, b.summary_plain, b.function_plain, b.description, b.location, b.details, b.clinical, b.exam_tip, b.sources)
  is distinct from (excluded.kind, excluded.fma_ids, excluded.layer, excluded.system, excluded.display_name, excluded.aliases, excluded.summary_plain, excluded.function_plain, excluded.description, excluded.location, excluded.details, excluded.clinical, excluded.exam_tip, excluded.sources);

-- Vertebral column  (48 FMA ids)
insert into public.body_part_info as b (key, kind, fma_ids, layer, system, display_name, aliases, summary_plain, function_plain, description, location, details, clinical, exam_tip, sources, status)
values ('group:spine',
    'group',
    array['FMA10014', 'FMA10037', 'FMA10059', 'FMA10081', 'FMA10458', 'FMA12519', 'FMA12520', 'FMA12521', 'FMA12522', 'FMA12523', 'FMA12524', 'FMA12525', 'FMA13072', 'FMA13073', 'FMA13074', 'FMA13075', 'FMA13076', 'FMA13495', 'FMA13500', 'FMA13501', 'FMA13502', 'FMA13503', 'FMA13504', 'FMA13505', 'FMA13506', 'FMA13507', 'FMA13508', 'FMA13896', 'FMA13897', 'FMA13898', 'FMA13899', 'FMA13900', 'FMA16033', 'FMA16034', 'FMA16035', 'FMA16036', 'FMA16037', 'FMA16202', 'FMA25058', 'FMA25511', 'FMA9165', 'FMA9187', 'FMA9209', 'FMA9248', 'FMA9922', 'FMA9945', 'FMA9968', 'FMA9991']::text[],
    'bone',
    'musculoskeletal',
    'Vertebral column',
    array['spine', 'backbone']::text[],
    'The vertebral column, or backbone, is the chain of bones running down the middle of the back, from the base of the skull to the back of the pelvis.',
    'It holds up the head and body so you can stand and bend, and it protects the spinal cord that runs inside it.',
    'The vertebral column is a flexible column of 33 vertebrae: 7 cervical, 12 thoracic, 5 lumbar, 5 sacral and 4 coccygeal. The upper 24 stay separate and movable; in adults the sacral vertebrae fuse into the sacrum and the coccygeal ones into the coccyx. Soft disks with a jelly-like centre lie between the vertebrae and cushion them. A typical vertebra has a body in front and a vertebral arch behind, enclosing the vertebral foramen.',
    'In the midline of the back of the neck and trunk, from the base of the skull down to the coccyx. The thoracic part forms the back wall of the chest, and the sacrum sits at the back of the pelvis, wedged between the two hip bones.',
    '{"type": "irregular (the vertebrae)", "joints": "Supports the skull at its top; the ribs attach to the thoracic vertebrae; the fifth lumbar vertebra meets the sacrum at the sacrovertebral (lumbosacral) joint; the sacrum joins the coccyx below and a hip bone on each side.", "landmarks": "Typical vertebra: body, and a vertebral arch of two pedicles and two laminae carrying seven processes (one spinous, two transverse, four articular). Seen from the side there are four curves: cervical and lumbar convex forward, thoracic concave forward, pelvic concave downward and forward."}'::jsonb,
    '[{"text": "Scoliosis is a sideways S- or C-shaped curve of the spine; the most common (idiopathic) type usually starts at age 11 or older and is more frequent in girls."}, {"text": "A herniated disk is a ruptured disk whose jelly-like centre leaks out and irritates nearby nerves, causing back pain or sciatica."}, {"text": "Age-related changes such as spinal stenosis and herniated disks can press on the spinal cord or nerves and cause pain."}, {"text": "Incomplete fusion of the vertebral laminae (spina bifida) is most common in the lumbosacral region; the spinal membranes, and sometimes the cord, may protrude through the gap."}]'::jsonb,
    'The thoracic and pelvic curves are primary curves, present before birth; the cervical and lumbar curves are secondary, appearing as the child holds up its head, sits and walks.',
    '[{"title": "Gray''s Anatomy of the Human Body, 20th ed. (1918), The Vertebral Column - PubAnnotation GrayAnatomy doc 19", "url": "https://pubannotation.org/docs/sourcedb/GrayAnatomy/sourceid/19", "licence": "Public domain"}, {"title": "Gray''s Anatomy of the Human Body, 20th ed. (1918), General Characteristics of the Vertebrae - PubAnnotation GrayAnatomy doc 20", "url": "https://pubannotation.org/docs/sourcedb/GrayAnatomy/sourceid/20", "licence": "Public domain"}, {"title": "Gray''s Anatomy of the Human Body, 20th ed. (1918), The Sacrum and Coccyx - PubAnnotation GrayAnatomy doc 24", "url": "https://pubannotation.org/docs/sourcedb/GrayAnatomy/sourceid/24", "licence": "Public domain"}, {"title": "Gray''s Anatomy of the Human Body, 20th ed. (1918), The Vertebral Column as a Whole - PubAnnotation GrayAnatomy doc 25", "url": "https://pubannotation.org/docs/sourcedb/GrayAnatomy/sourceid/25", "licence": "Public domain"}, {"title": "Gray''s Anatomy of the Human Body, 20th ed. (1918), The Thorax - PubAnnotation GrayAnatomy doc 26", "url": "https://pubannotation.org/docs/sourcedb/GrayAnatomy/sourceid/26", "licence": "Public domain"}, {"title": "Gray''s Anatomy of the Human Body, 20th ed. (1918), The Skull - PubAnnotation GrayAnatomy doc 30", "url": "https://pubannotation.org/docs/sourcedb/GrayAnatomy/sourceid/30", "licence": "Public domain"}, {"title": "Classification of Bones - NCI SEER Training Modules", "url": "https://training.seer.cancer.gov/anatomy/skeletal/classification.html", "licence": "Public domain"}, {"title": "Spine Injuries and Disorders - MedlinePlus (NLM)", "url": "https://medlineplus.gov/spineinjuriesanddisorders.html", "licence": "Public domain"}, {"title": "Herniated Disk - MedlinePlus (NLM)", "url": "https://medlineplus.gov/herniateddisk.html", "licence": "Public domain"}, {"title": "Scoliosis - NIAMS", "url": "https://www.niams.nih.gov/health-topics/scoliosis", "licence": "Public domain"}]'::jsonb,
    'draft')
on conflict (key) do update set
    kind = excluded.kind,
    fma_ids = excluded.fma_ids,
    layer = excluded.layer,
    system = excluded.system,
    display_name = excluded.display_name,
    aliases = excluded.aliases,
    summary_plain = excluded.summary_plain,
    function_plain = excluded.function_plain,
    description = excluded.description,
    location = excluded.location,
    details = excluded.details,
    clinical = excluded.clinical,
    exam_tip = excluded.exam_tip,
    sources = excluded.sources,
    updated_at = now()
where b.status = 'draft'
  and (b.kind, b.fma_ids, b.layer, b.system, b.display_name, b.aliases, b.summary_plain, b.function_plain, b.description, b.location, b.details, b.clinical, b.exam_tip, b.sources)
  is distinct from (excluded.kind, excluded.fma_ids, excluded.layer, excluded.system, excluded.display_name, excluded.aliases, excluded.summary_plain, excluded.function_plain, excluded.description, excluded.location, excluded.details, excluded.clinical, excluded.exam_tip, excluded.sources);

-- Rib cage  (41 FMA ids)
insert into public.body_part_info as b (key, kind, fma_ids, layer, system, display_name, aliases, summary_plain, function_plain, description, location, details, clinical, exam_tip, sources, status)
values ('group:ribcage',
    'group',
    array['FMA7486', 'FMA7487', 'FMA7488', 'FMA7857', 'FMA7875', 'FMA7882', 'FMA7886', 'FMA7909', 'FMA7913', 'FMA7957', 'FMA7976', 'FMA7987', 'FMA8005', 'FMA8012', 'FMA8031', 'FMA8039', 'FMA8058', 'FMA8066', 'FMA8070', 'FMA8093', 'FMA8112', 'FMA8148', 'FMA8167', 'FMA8175', 'FMA8194', 'FMA8202', 'FMA8221', 'FMA8229', 'FMA8248', 'FMA8256', 'FMA8275', 'FMA8283', 'FMA8310', 'FMA8364', 'FMA8391', 'FMA8445', 'FMA8472', 'FMA8531', 'FMA8532', 'FMA8533', 'FMA8534']::text[],
    'bone',
    'musculoskeletal',
    'Rib cage',
    array['thoracic cage']::text[],
    'The rib cage is the cage of bone and cartilage around the chest. It is made of the breastbone in front, the ribs around the sides and the spine behind.',
    'It protects the heart and lungs, and its springy cartilages let the chest wall stretch and spring back when you breathe.',
    'The skeleton of the thorax is a cone-shaped cage of bone and cartilage, narrow above and broad below. Its front wall is the sternum and costal cartilages, its sides are the 12 pairs of ribs with 11 intercostal spaces between them, and its back wall is the 12 thoracic vertebrae. Ribs 1-7 are true ribs reaching the sternum by their own cartilage; ribs 8-10 join the cartilage above; ribs 11-12 are floating ribs.',
    'Encloses the chest between the neck and the abdomen. Its upper opening is bounded by the first thoracic vertebra, the first ribs and the top of the sternum; its lower opening is closed by the diaphragm, which forms the floor of the thorax.',
    '{"type": "flat (the sternum is a long, flat bone); the costal cartilages are hyaline cartilage", "joints": "Behind, the ribs join the thoracic vertebrae. In front, the costal cartilages of ribs 1-7 join the sternum and those of ribs 8-10 join the cartilage above. The manubrium also joins both clavicles.", "landmarks": "Sternum: manubrium with jugular notch, body with notches for costal cartilages 2-7, xiphoid process; sternal angle between manubrium and body. Typical rib: head, neck, tubercle, shaft with angle and costal groove for intercostal vessels and nerve. First rib: most curved, usually shortest, with scalene tubercle."}'::jsonb,
    '[{"text": "Broken ribs are a chest injury, usually from car accidents, falls or sports; some chest injuries can be life-threatening because of the important organs inside."}, {"text": "Costochondritis, slipping rib syndrome and pectus excavatum are other disorders of the ribs and chest wall."}]'::jsonb,
    'The sternal angle, the ridge where the manubrium meets the body of the sternum, is a useful surface landmark.',
    '[{"title": "Gray''s Anatomy of the Human Body, 20th ed. (1918), The Thorax - PubAnnotation GrayAnatomy doc 26", "url": "https://pubannotation.org/docs/sourcedb/GrayAnatomy/sourceid/26", "licence": "Public domain"}, {"title": "Gray''s Anatomy of the Human Body, 20th ed. (1918), The Sternum (Breast Bone) - PubAnnotation GrayAnatomy doc 27", "url": "https://pubannotation.org/docs/sourcedb/GrayAnatomy/sourceid/27", "licence": "Public domain"}, {"title": "Gray''s Anatomy of the Human Body, 20th ed. (1918), The Ribs - PubAnnotation GrayAnatomy doc 28", "url": "https://pubannotation.org/docs/sourcedb/GrayAnatomy/sourceid/28", "licence": "Public domain"}, {"title": "Gray''s Anatomy of the Human Body, 20th ed. (1918), The Costal Cartilages - PubAnnotation GrayAnatomy doc 29", "url": "https://pubannotation.org/docs/sourcedb/GrayAnatomy/sourceid/29", "licence": "Public domain"}, {"title": "Axial Skeleton - NCI SEER Training Modules", "url": "https://training.seer.cancer.gov/anatomy/skeletal/divisions/axial.html", "licence": "Public domain"}, {"title": "Chest Injuries and Disorders - MedlinePlus (NLM)", "url": "https://medlineplus.gov/chestinjuriesanddisorders.html", "licence": "Public domain"}]'::jsonb,
    'draft')
on conflict (key) do update set
    kind = excluded.kind,
    fma_ids = excluded.fma_ids,
    layer = excluded.layer,
    system = excluded.system,
    display_name = excluded.display_name,
    aliases = excluded.aliases,
    summary_plain = excluded.summary_plain,
    function_plain = excluded.function_plain,
    description = excluded.description,
    location = excluded.location,
    details = excluded.details,
    clinical = excluded.clinical,
    exam_tip = excluded.exam_tip,
    sources = excluded.sources,
    updated_at = now()
where b.status = 'draft'
  and (b.kind, b.fma_ids, b.layer, b.system, b.display_name, b.aliases, b.summary_plain, b.function_plain, b.description, b.location, b.details, b.clinical, b.exam_tip, b.sources)
  is distinct from (excluded.kind, excluded.fma_ids, excluded.layer, excluded.system, excluded.display_name, excluded.aliases, excluded.summary_plain, excluded.function_plain, excluded.description, excluded.location, excluded.details, excluded.clinical, excluded.exam_tip, excluded.sources);

-- Clavicle  (2 FMA ids)
insert into public.body_part_info as b (key, kind, fma_ids, layer, system, display_name, aliases, summary_plain, function_plain, description, location, details, clinical, exam_tip, sources, status)
values ('clavicle',
    'part',
    array['FMA13322', 'FMA13323']::text[],
    'bone',
    'musculoskeletal',
    'Clavicle',
    array['collarbone', 'collar bone']::text[],
    'The clavicle is the collarbone. It is a long bone with a gentle double curve that lies across the top of the chest, from the breastbone to the shoulder.',
    'It links the breastbone to the shoulder blade, forming the front of the shoulder girdle, and gives attachment to muscles of the neck, chest and shoulder.',
    'The clavicle is a long bone lying almost horizontally at the upper front of the chest, just above the first rib. It has a double curve, somewhat like an italic letter f. Its medial two-thirds are rounded, while its lateral third is flattened from above downward. It forms the front part of the shoulder girdle, with the scapula forming the back.',
    'At the upper front of the chest, just above the first rib. Its medial (sternal) end meets the manubrium of the sternum and its lateral (acromial) end meets the acromion of the scapula at the top of the shoulder. Much of it lies just under the skin.',
    '{"type": "long", "joints": "Sternoclavicular joint: the sternal end meets the manubrium of the sternum through an articular disc and also touches the first costal cartilage. Acromioclavicular joint: the acromial end meets the acromion of the scapula.", "landmarks": "Sternal end; acromial end with a small oval facet; conoid tubercle and trapezoid line on the underside of the lateral third (for the conoid and trapezoid ligaments); costal tuberosity for the costoclavicular ligament; subclavian groove for the subclavius muscle."}'::jsonb,
    '[]'::jsonb,
    'The clavicle starts to ossify earlier than any other bone in the body, from two centres that appear in the fifth or sixth week of fetal life.',
    '[{"title": "Gray''s Anatomy of the Human Body, 20th ed. (1918), The Clavicle (Collar Bone) - PubAnnotation GrayAnatomy doc 49", "url": "https://pubannotation.org/docs/sourcedb/GrayAnatomy/sourceid/49", "licence": "Public domain"}, {"title": "Shoulder Injuries and Disorders - MedlinePlus (NLM)", "url": "https://medlineplus.gov/shoulderinjuriesanddisorders.html", "licence": "Public domain"}]'::jsonb,
    'draft')
on conflict (key) do update set
    kind = excluded.kind,
    fma_ids = excluded.fma_ids,
    layer = excluded.layer,
    system = excluded.system,
    display_name = excluded.display_name,
    aliases = excluded.aliases,
    summary_plain = excluded.summary_plain,
    function_plain = excluded.function_plain,
    description = excluded.description,
    location = excluded.location,
    details = excluded.details,
    clinical = excluded.clinical,
    exam_tip = excluded.exam_tip,
    sources = excluded.sources,
    updated_at = now()
where b.status = 'draft'
  and (b.kind, b.fma_ids, b.layer, b.system, b.display_name, b.aliases, b.summary_plain, b.function_plain, b.description, b.location, b.details, b.clinical, b.exam_tip, b.sources)
  is distinct from (excluded.kind, excluded.fma_ids, excluded.layer, excluded.system, excluded.display_name, excluded.aliases, excluded.summary_plain, excluded.function_plain, excluded.description, excluded.location, excluded.details, excluded.clinical, excluded.exam_tip, excluded.sources);

-- Scapula  (2 FMA ids)
insert into public.body_part_info as b (key, kind, fma_ids, layer, system, display_name, aliases, summary_plain, function_plain, description, location, details, clinical, exam_tip, sources, status)
values ('scapula',
    'part',
    array['FMA13395', 'FMA13396']::text[],
    'bone',
    'musculoskeletal',
    'Scapula',
    array['shoulder blade']::text[],
    'The scapula is the shoulder blade, a flat, triangular bone at the back of the shoulder.',
    'It forms the socket of the shoulder joint and anchors many of the muscles of the shoulder and arm.',
    'The scapula forms the back part of the shoulder girdle. It is a flat, triangular bone with two surfaces (costal and dorsal), three borders (superior, lateral and medial) and three angles (superior, inferior and lateral). A prominent spine crosses the back surface and ends as the acromion, the summit of the shoulder; the lateral angle carries the shallow glenoid cavity.',
    'At the back of the upper chest wall, its front (costal) surface facing the thorax. Its lateral angle lies at the shoulder, where the glenoid cavity meets the humerus and the acromion meets the clavicle.',
    '{"type": "flat", "joints": "Shoulder (glenohumeral) joint: the glenoid cavity meets the head of the humerus. Acromioclavicular joint: a small oval facet on the acromion meets the acromial end of the clavicle.", "landmarks": "Subscapular fossa on the front; spine dividing the back into supraspinous and infraspinous fossae; acromion; coracoid process; glenoid cavity with supraglenoid and infraglenoid tubercles; suprascapular notch on the superior border for the suprascapular nerve."}'::jsonb,
    '[{"text": "The shoulder is the most movable joint in the body but is unstable because the head of the humerus is larger than its socket; problems include dislocations, separations, fractures and torn rotator cuffs."}]'::jsonb,
    'The spine of the scapula ends as the acromion, which forms the summit of the shoulder and overhangs the glenoid cavity.',
    '[{"title": "Gray''s Anatomy of the Human Body, 20th ed. (1918), The Scapula (Shoulder Blade) - PubAnnotation GrayAnatomy doc 50", "url": "https://pubannotation.org/docs/sourcedb/GrayAnatomy/sourceid/50", "licence": "Public domain"}, {"title": "Shoulder Injuries and Disorders - MedlinePlus (NLM)", "url": "https://medlineplus.gov/shoulderinjuriesanddisorders.html", "licence": "Public domain"}]'::jsonb,
    'draft')
on conflict (key) do update set
    kind = excluded.kind,
    fma_ids = excluded.fma_ids,
    layer = excluded.layer,
    system = excluded.system,
    display_name = excluded.display_name,
    aliases = excluded.aliases,
    summary_plain = excluded.summary_plain,
    function_plain = excluded.function_plain,
    description = excluded.description,
    location = excluded.location,
    details = excluded.details,
    clinical = excluded.clinical,
    exam_tip = excluded.exam_tip,
    sources = excluded.sources,
    updated_at = now()
where b.status = 'draft'
  and (b.kind, b.fma_ids, b.layer, b.system, b.display_name, b.aliases, b.summary_plain, b.function_plain, b.description, b.location, b.details, b.clinical, b.exam_tip, b.sources)
  is distinct from (excluded.kind, excluded.fma_ids, excluded.layer, excluded.system, excluded.display_name, excluded.aliases, excluded.summary_plain, excluded.function_plain, excluded.description, excluded.location, excluded.details, excluded.clinical, excluded.exam_tip, excluded.sources);

-- Humerus  (2 FMA ids)
insert into public.body_part_info as b (key, kind, fma_ids, layer, system, display_name, aliases, summary_plain, function_plain, description, location, details, clinical, exam_tip, sources, status)
values ('humerus',
    'part',
    array['FMA23130', 'FMA23131']::text[],
    'bone',
    'musculoskeletal',
    'Humerus',
    array['arm bone', 'upper arm bone']::text[],
    'The humerus is the upper arm bone. It runs from the shoulder down to the elbow and is the longest and largest bone of the arm.',
    'It links the shoulder to the elbow, forms part of both joints and gives muscles of the shoulder, arm and forearm a place to attach.',
    'The humerus is a long bone with a shaft and two ends. Its upper end has a rounded head, the anatomical and surgical necks and the greater and lesser tubercles, with the intertubercular groove between them. Its lower end widens into the capitulum and trochlea, which meet the forearm bones, with an epicondyle on each side.',
    'In the upper arm, between the shoulder and the elbow. The head meets the glenoid cavity of the scapula above; the lower end meets the radius and ulna at the elbow. The radial nerve runs in a shallow spiral groove on the shaft.',
    '{"type": "long", "joints": "Shoulder joint: the head meets the glenoid cavity of the scapula. Elbow joint: the capitulum meets the head of the radius and the trochlea meets the trochlear notch of the ulna.", "landmarks": "Head; anatomical and surgical necks; greater and lesser tubercles; intertubercular (bicipital) groove for the long head of biceps; deltoid tuberosity; radial groove for the radial nerve; capitulum; trochlea; medial and lateral epicondyles; coronoid, radial and olecranon fossae."}'::jsonb,
    '[{"text": "The surgical neck, just below the tubercles, is a frequent site of fracture; fracture of the anatomical neck is rare."}, {"text": "Tennis elbow (lateral epicondylitis) is overuse damage of the tendons on the outer elbow, where the common extensor tendon attaches to the lateral epicondyle."}, {"text": "Golfer''s elbow (medial epicondylitis) is tendinitis on the inner elbow, the side of the medial epicondyle and the common flexor tendon, from repeated wrist use or gripping."}, {"text": "The ulnar nerve runs in a groove behind the medial epicondyle."}]'::jsonb,
    'Gray''s Anatomy calls the humerus the longest and largest bone of the upper limb.',
    '[{"title": "Gray''s Anatomy of the Human Body, 20th ed. (1918), The Humerus (Arm Bone) - PubAnnotation GrayAnatomy doc 51", "url": "https://pubannotation.org/docs/sourcedb/GrayAnatomy/sourceid/51", "licence": "Public domain"}, {"title": "Gray''s Anatomy of the Human Body, 20th ed. (1918), General classification of bones - PubAnnotation GrayAnatomy doc 17", "url": "https://pubannotation.org/docs/sourcedb/GrayAnatomy/sourceid/17", "licence": "Public domain"}, {"title": "Classification of Bones - NCI SEER Training Modules", "url": "https://training.seer.cancer.gov/anatomy/skeletal/classification.html", "licence": "Public domain"}, {"title": "Arm Injuries and Disorders - MedlinePlus (NLM)", "url": "https://medlineplus.gov/arminjuriesanddisorders.html", "licence": "Public domain"}, {"title": "Shoulder Injuries and Disorders - MedlinePlus (NLM)", "url": "https://medlineplus.gov/shoulderinjuriesanddisorders.html", "licence": "Public domain"}, {"title": "Sports Injuries - NIAMS", "url": "https://www.niams.nih.gov/health-topics/sports-injuries", "licence": "Public domain"}]'::jsonb,
    'draft')
on conflict (key) do update set
    kind = excluded.kind,
    fma_ids = excluded.fma_ids,
    layer = excluded.layer,
    system = excluded.system,
    display_name = excluded.display_name,
    aliases = excluded.aliases,
    summary_plain = excluded.summary_plain,
    function_plain = excluded.function_plain,
    description = excluded.description,
    location = excluded.location,
    details = excluded.details,
    clinical = excluded.clinical,
    exam_tip = excluded.exam_tip,
    sources = excluded.sources,
    updated_at = now()
where b.status = 'draft'
  and (b.kind, b.fma_ids, b.layer, b.system, b.display_name, b.aliases, b.summary_plain, b.function_plain, b.description, b.location, b.details, b.clinical, b.exam_tip, b.sources)
  is distinct from (excluded.kind, excluded.fma_ids, excluded.layer, excluded.system, excluded.display_name, excluded.aliases, excluded.summary_plain, excluded.function_plain, excluded.description, excluded.location, excluded.details, excluded.clinical, excluded.exam_tip, excluded.sources);

-- Radius  (2 FMA ids)
insert into public.body_part_info as b (key, kind, fma_ids, layer, system, display_name, aliases, summary_plain, function_plain, description, location, details, clinical, exam_tip, sources, status)
values ('radius',
    'part',
    array['FMA23464', 'FMA23465']::text[],
    'bone',
    'musculoskeletal',
    'Radius',
    '{}'::text[],
    'The radius is one of the two forearm bones. It lies on the outer side of the forearm, next to the ulna, and runs from the elbow to the wrist.',
    'It joins the elbow above and forms the main bony part of the wrist joint below, and it gives the biceps and several forearm muscles a place to attach.',
    'The radius is a long, slightly curved bone with a shaft and two ends. Its upper end is a short cylindrical head on a narrow neck, with the radial tuberosity below for the biceps brachii tendon. Its lower end is broad, with a styloid process on the outer side and a concave surface that meets the wrist bones.',
    'On the lateral side of the forearm, alongside the longer and larger ulna. It is narrow above at the elbow and widens below at the wrist; an interosseous membrane joins its shaft to the ulna.',
    '{"type": "long", "joints": "Elbow: the head meets the capitulum of the humerus and the radial notch of the ulna. Wrist joint: the lower end meets the scaphoid and lunate. Distal radioulnar joint: the ulnar notch meets the head of the ulna.", "landmarks": "Head with a shallow cup (fovea); neck; radial tuberosity for the biceps brachii tendon; interosseous crest for the interosseous membrane; ulnar notch; carpal articular surface; styloid process on the lateral side."}'::jsonb,
    '[{"text": "The wrist, where the radius meets the carpal bones, can be fractured or sprained; falling on an outstretched hand during sports such as skating is one cause."}]'::jsonb,
    'The biceps brachii tendon inserts on the rough back part of the radial tuberosity, just below the neck of the radius.',
    '[{"title": "Gray''s Anatomy of the Human Body, 20th ed. (1918), The Radius - PubAnnotation GrayAnatomy doc 53", "url": "https://pubannotation.org/docs/sourcedb/GrayAnatomy/sourceid/53", "licence": "Public domain"}, {"title": "Gray''s Anatomy of the Human Body, 20th ed. (1918), General classification of bones - PubAnnotation GrayAnatomy doc 17", "url": "https://pubannotation.org/docs/sourcedb/GrayAnatomy/sourceid/17", "licence": "Public domain"}, {"title": "Arm Injuries and Disorders - MedlinePlus (NLM)", "url": "https://medlineplus.gov/arminjuriesanddisorders.html", "licence": "Public domain"}, {"title": "Wrist Injuries and Disorders - MedlinePlus (NLM)", "url": "https://medlineplus.gov/wristinjuriesanddisorders.html", "licence": "Public domain"}]'::jsonb,
    'draft')
on conflict (key) do update set
    kind = excluded.kind,
    fma_ids = excluded.fma_ids,
    layer = excluded.layer,
    system = excluded.system,
    display_name = excluded.display_name,
    aliases = excluded.aliases,
    summary_plain = excluded.summary_plain,
    function_plain = excluded.function_plain,
    description = excluded.description,
    location = excluded.location,
    details = excluded.details,
    clinical = excluded.clinical,
    exam_tip = excluded.exam_tip,
    sources = excluded.sources,
    updated_at = now()
where b.status = 'draft'
  and (b.kind, b.fma_ids, b.layer, b.system, b.display_name, b.aliases, b.summary_plain, b.function_plain, b.description, b.location, b.details, b.clinical, b.exam_tip, b.sources)
  is distinct from (excluded.kind, excluded.fma_ids, excluded.layer, excluded.system, excluded.display_name, excluded.aliases, excluded.summary_plain, excluded.function_plain, excluded.description, excluded.location, excluded.details, excluded.clinical, excluded.exam_tip, excluded.sources);

-- Ulna  (2 FMA ids)
insert into public.body_part_info as b (key, kind, fma_ids, layer, system, display_name, aliases, summary_plain, function_plain, description, location, details, clinical, exam_tip, sources, status)
values ('ulna',
    'part',
    array['FMA23467', 'FMA23468']::text[],
    'bone',
    'musculoskeletal',
    'Ulna',
    array['elbow bone']::text[],
    'The ulna is one of the two forearm bones. It lies on the inner side of the forearm, next to the radius, and its curved top (the olecranon) lies just under the skin at the back of the elbow.',
    'It forms the elbow joint with the upper arm bone and gives many forearm muscles, including the triceps and brachialis, a place to attach.',
    'The ulna is a long bone that is large and strong at the top and thin at the bottom. Its upper end has the olecranon and the coronoid process, which together form the trochlear notch that grips the humerus. Its small lower end has a rounded head and a styloid process, and is kept off the wrist joint by an articular disc.',
    'On the medial side of the forearm, parallel to the radius, from the elbow to the wrist. The back of the olecranon lies just under the skin at the elbow.',
    '{"type": "long", "joints": "Elbow: the trochlear notch meets the trochlea of the humerus. Proximal radioulnar joint: the radial notch meets the head of the radius. Distal radioulnar joint: the head of the ulna fits the ulnar notch of the radius.", "landmarks": "Olecranon (triceps brachii insertion); coronoid process; trochlear notch; radial notch; ulnar tuberosity (part of brachialis insertion); interosseous crest; head; styloid process."}'::jsonb,
    '[{"text": "Repeated throwing can tear the ulnar collateral ligament on the inner elbow, which attaches to the coronoid process and olecranon of the ulna."}, {"text": "Elbow problems include fractures, dislocations, bursitis and arthritis; the back of the olecranon lies under the skin, covered by a bursa."}]'::jsonb,
    'The lower end of the ulna does not take part in the wrist joint: a triangular articular disc lies between it and the wrist bones.',
    '[{"title": "Gray''s Anatomy of the Human Body, 20th ed. (1918), The Ulna (Elbow Bone) - PubAnnotation GrayAnatomy doc 52", "url": "https://pubannotation.org/docs/sourcedb/GrayAnatomy/sourceid/52", "licence": "Public domain"}, {"title": "Gray''s Anatomy of the Human Body, 20th ed. (1918), General classification of bones - PubAnnotation GrayAnatomy doc 17", "url": "https://pubannotation.org/docs/sourcedb/GrayAnatomy/sourceid/17", "licence": "Public domain"}, {"title": "Gray''s Anatomy of the Human Body, 20th ed. (1918), The Radius - PubAnnotation GrayAnatomy doc 53", "url": "https://pubannotation.org/docs/sourcedb/GrayAnatomy/sourceid/53", "licence": "Public domain"}, {"title": "Elbow Injuries and Disorders - MedlinePlus (NLM)", "url": "https://medlineplus.gov/elbowinjuriesanddisorders.html", "licence": "Public domain"}, {"title": "Sports Injuries - NIAMS", "url": "https://www.niams.nih.gov/health-topics/sports-injuries", "licence": "Public domain"}]'::jsonb,
    'draft')
on conflict (key) do update set
    kind = excluded.kind,
    fma_ids = excluded.fma_ids,
    layer = excluded.layer,
    system = excluded.system,
    display_name = excluded.display_name,
    aliases = excluded.aliases,
    summary_plain = excluded.summary_plain,
    function_plain = excluded.function_plain,
    description = excluded.description,
    location = excluded.location,
    details = excluded.details,
    clinical = excluded.clinical,
    exam_tip = excluded.exam_tip,
    sources = excluded.sources,
    updated_at = now()
where b.status = 'draft'
  and (b.kind, b.fma_ids, b.layer, b.system, b.display_name, b.aliases, b.summary_plain, b.function_plain, b.description, b.location, b.details, b.clinical, b.exam_tip, b.sources)
  is distinct from (excluded.kind, excluded.fma_ids, excluded.layer, excluded.system, excluded.display_name, excluded.aliases, excluded.summary_plain, excluded.function_plain, excluded.description, excluded.location, excluded.details, excluded.clinical, excluded.exam_tip, excluded.sources);

-- Hip bone  (2 FMA ids)
insert into public.body_part_info as b (key, kind, fma_ids, layer, system, display_name, aliases, summary_plain, function_plain, description, location, details, clinical, exam_tip, sources, status)
values ('hip bone',
    'part',
    array['FMA16586', 'FMA16587']::text[],
    'bone',
    'musculoskeletal',
    'Hip bone',
    array['innominate bone', 'coxal bone']::text[],
    'The hip bone is the large, flat bone on each side of the pelvis. The two hip bones meet at the front and join the sacrum at the back.',
    'It holds the socket for the thigh bone at the hip joint and forms the side and front walls of the pelvis.',
    'The hip bone (os coxae) is a large, flattened, irregular bone, narrow in the middle and wide above and below. It is made of three parts, the ilium, ischium and pubis, which are separate in children and fused in adults. They meet at the acetabulum, the deep cup that holds the head of the femur.',
    'In the pelvis, one on each side. The two hip bones meet at the front in the midline (pubic symphysis) and join the sacrum at the back, forming the sides and front wall of the pelvic cavity. The femur hangs from the acetabulum below.',
    '{"type": "flat", "joints": "Hip joint: the acetabulum holds the head of the femur. Sacroiliac joint: the auricular surface of the ilium meets the sacrum. Pubic symphysis: the pubis meets the other hip bone through a fibrocartilage disc.", "landmarks": "Iliac crest; anterior and posterior superior and inferior iliac spines; auricular surface; greater and lesser sciatic notches, separated by the ischial spine; ischial tuberosity; pubic tubercle; acetabulum; obturator foramen, oval in males and more triangular in females."}'::jsonb,
    '[{"text": "In hip dysplasia the femoral head fits loosely in the socket, which can lead to dislocation; it is usually present at birth."}, {"text": "Osteoarthritis of the hip joint causes pain and less movement and is common in older adults; treatment may include hip replacement."}]'::jsonb,
    'The acetabulum is shared by all three parts: the ischium gives a little over two-fifths, the ilium a little under two-fifths and the pubis about one-fifth.',
    '[{"title": "Gray''s Anatomy of the Human Body, 20th ed. (1918), The Hip Bone (Os Coxae; Innominate Bone) - PubAnnotation GrayAnatomy doc 57", "url": "https://pubannotation.org/docs/sourcedb/GrayAnatomy/sourceid/57", "licence": "Public domain"}, {"title": "Gray''s Anatomy of the Human Body, 20th ed. (1918), General classification of bones - PubAnnotation GrayAnatomy doc 17", "url": "https://pubannotation.org/docs/sourcedb/GrayAnatomy/sourceid/17", "licence": "Public domain"}, {"title": "Appendicular Skeleton - NCI SEER Training Modules", "url": "https://training.seer.cancer.gov/anatomy/skeletal/divisions/appendicular.html", "licence": "Public domain"}, {"title": "Hip Injuries and Disorders - MedlinePlus (NLM)", "url": "https://medlineplus.gov/hipinjuriesanddisorders.html", "licence": "Public domain"}]'::jsonb,
    'draft')
on conflict (key) do update set
    kind = excluded.kind,
    fma_ids = excluded.fma_ids,
    layer = excluded.layer,
    system = excluded.system,
    display_name = excluded.display_name,
    aliases = excluded.aliases,
    summary_plain = excluded.summary_plain,
    function_plain = excluded.function_plain,
    description = excluded.description,
    location = excluded.location,
    details = excluded.details,
    clinical = excluded.clinical,
    exam_tip = excluded.exam_tip,
    sources = excluded.sources,
    updated_at = now()
where b.status = 'draft'
  and (b.kind, b.fma_ids, b.layer, b.system, b.display_name, b.aliases, b.summary_plain, b.function_plain, b.description, b.location, b.details, b.clinical, b.exam_tip, b.sources)
  is distinct from (excluded.kind, excluded.fma_ids, excluded.layer, excluded.system, excluded.display_name, excluded.aliases, excluded.summary_plain, excluded.function_plain, excluded.description, excluded.location, excluded.details, excluded.clinical, excluded.exam_tip, excluded.sources);

-- Femur  (2 FMA ids)
insert into public.body_part_info as b (key, kind, fma_ids, layer, system, display_name, aliases, summary_plain, function_plain, description, location, details, clinical, exam_tip, sources, status)
values ('femur',
    'part',
    array['FMA24474', 'FMA24475']::text[],
    'bone',
    'musculoskeletal',
    'Femur',
    array['thigh bone']::text[],
    'The femur is the thigh bone. It runs down the thigh from the hip to the knee and is the longest and strongest bone in the body.',
    'It carries the body''s weight from the hip down to the shin bone and forms part of both the hip and the knee joints.',
    'The femur is a long bone with a nearly cylindrical shaft and two expanded ends. Its upper end has a rounded head, a neck and the greater and lesser trochanters; its lower end has the medial and lateral condyles. Body weight passes from the acetabulum through the femur to the tibia.',
    'In the thigh, between the pelvis above and the knee below. When standing it is not vertical: the shaft slants downward and medially, so the two femurs come closer together near the knees.',
    '{"type": "long", "joints": "Hip joint: the head fits into the socket (acetabulum) of the hip bone, a ball-and-socket joint. Knee joint: the condyles meet the condyles of the tibia and the menisci, and the patellar surface meets the patella.", "landmarks": "Head with a small pit (fovea) for the ligamentum teres; neck; greater and lesser trochanters; linea aspera, a long ridge on the back of the shaft; medial and lateral condyles with epicondyles; intercondylar fossa; patellar surface. The neck meets the shaft at about 125 degrees in adults (wider in infancy)."}'::jsonb,
    '[{"text": "Fractures of the hip can follow falls, sports or overuse; osteoporosis of the hip makes the bones weak and easy to break and is common in older people."}]'::jsonb,
    'Gray''s Anatomy calls the femur the longest and strongest bone in the skeleton.',
    '[{"title": "Gray''s Anatomy of the Human Body, 20th ed. (1918), The Femur (Thigh Bone) - PubAnnotation GrayAnatomy doc 59", "url": "https://pubannotation.org/docs/sourcedb/GrayAnatomy/sourceid/59", "licence": "Public domain"}, {"title": "Classification of Bones - NCI SEER Training Modules", "url": "https://training.seer.cancer.gov/anatomy/skeletal/classification.html", "licence": "Public domain"}, {"title": "Hip Injuries and Disorders - MedlinePlus (NLM)", "url": "https://medlineplus.gov/hipinjuriesanddisorders.html", "licence": "Public domain"}]'::jsonb,
    'draft')
on conflict (key) do update set
    kind = excluded.kind,
    fma_ids = excluded.fma_ids,
    layer = excluded.layer,
    system = excluded.system,
    display_name = excluded.display_name,
    aliases = excluded.aliases,
    summary_plain = excluded.summary_plain,
    function_plain = excluded.function_plain,
    description = excluded.description,
    location = excluded.location,
    details = excluded.details,
    clinical = excluded.clinical,
    exam_tip = excluded.exam_tip,
    sources = excluded.sources,
    updated_at = now()
where b.status = 'draft'
  and (b.kind, b.fma_ids, b.layer, b.system, b.display_name, b.aliases, b.summary_plain, b.function_plain, b.description, b.location, b.details, b.clinical, b.exam_tip, b.sources)
  is distinct from (excluded.kind, excluded.fma_ids, excluded.layer, excluded.system, excluded.display_name, excluded.aliases, excluded.summary_plain, excluded.function_plain, excluded.description, excluded.location, excluded.details, excluded.clinical, excluded.exam_tip, excluded.sources);

-- Patella  (2 FMA ids)
insert into public.body_part_info as b (key, kind, fma_ids, layer, system, display_name, aliases, summary_plain, function_plain, description, location, details, clinical, exam_tip, sources, status)
values ('patella',
    'part',
    array['FMA24486', 'FMA24487']::text[],
    'bone',
    'musculoskeletal',
    'Patella',
    array['kneecap', 'knee cap']::text[],
    'The patella is the kneecap. It is a flat, triangular bone at the front of the knee, sitting in a groove on the end of the thigh bone.',
    'It shields the front of the knee and gives the big thigh muscle (quadriceps) better leverage.',
    'The patella is a flat, triangular bone usually counted as a sesamoid bone, because it forms inside the tendon of the quadriceps femoris. It protects the front of the knee joint and improves the leverage of the quadriceps. Its back has a smooth surface, split by a ridge into medial and lateral facets, that glides on the femur.',
    'At the front of the knee joint, embedded in the quadriceps tendon. Its broad base faces up and its pointed apex faces down toward the patellar ligament; its back rests on the patellar surface of the femur.',
    '{"type": "sesamoid", "joints": "Knee joint: its back articular surface meets the patellar surface of the femur.", "landmarks": "Base (top border) for rectus femoris and vastus intermedius; medial and lateral borders for vastus medialis and vastus lateralis; apex for the patellar ligament; back articular surface with a vertical ridge and a broader lateral facet and a medial facet."}'::jsonb,
    '[{"text": "Kneecap fractures are the most common knee fracture and usually follow a hard fall or a direct blow to the knee."}, {"text": "A strong impact can knock the kneecap out of its groove on the femur (kneecap dislocation); it usually needs prompt care, though it sometimes slides back by itself."}, {"text": "Runner''s knee causes pain or tenderness near or under the front of the kneecap; it is common in runners, hikers and cyclists."}]'::jsonb,
    'The patella usually starts to ossify from a single centre in the second or third year of life, and ossification is complete about puberty.',
    '[{"title": "Gray''s Anatomy of the Human Body, 20th ed. (1918), The Patella (Knee Cap) - PubAnnotation GrayAnatomy doc 60", "url": "https://pubannotation.org/docs/sourcedb/GrayAnatomy/sourceid/60", "licence": "Public domain"}, {"title": "Appendicular Skeleton - NCI SEER Training Modules", "url": "https://training.seer.cancer.gov/anatomy/skeletal/divisions/appendicular.html", "licence": "Public domain"}, {"title": "Sports Injuries - NIAMS", "url": "https://www.niams.nih.gov/health-topics/sports-injuries", "licence": "Public domain"}]'::jsonb,
    'draft')
on conflict (key) do update set
    kind = excluded.kind,
    fma_ids = excluded.fma_ids,
    layer = excluded.layer,
    system = excluded.system,
    display_name = excluded.display_name,
    aliases = excluded.aliases,
    summary_plain = excluded.summary_plain,
    function_plain = excluded.function_plain,
    description = excluded.description,
    location = excluded.location,
    details = excluded.details,
    clinical = excluded.clinical,
    exam_tip = excluded.exam_tip,
    sources = excluded.sources,
    updated_at = now()
where b.status = 'draft'
  and (b.kind, b.fma_ids, b.layer, b.system, b.display_name, b.aliases, b.summary_plain, b.function_plain, b.description, b.location, b.details, b.clinical, b.exam_tip, b.sources)
  is distinct from (excluded.kind, excluded.fma_ids, excluded.layer, excluded.system, excluded.display_name, excluded.aliases, excluded.summary_plain, excluded.function_plain, excluded.description, excluded.location, excluded.details, excluded.clinical, excluded.exam_tip, excluded.sources);

-- Tibia  (2 FMA ids)
insert into public.body_part_info as b (key, kind, fma_ids, layer, system, display_name, aliases, summary_plain, function_plain, description, location, details, clinical, exam_tip, sources, status)
values ('tibia',
    'part',
    array['FMA24477', 'FMA24478']::text[],
    'bone',
    'musculoskeletal',
    'Tibia',
    array['shin bone']::text[],
    'The tibia is the shin bone. It is the larger of the two bones in the lower leg and runs on the inner side from the knee down to the ankle.',
    'It carries body weight from the thigh bone down to the ankle and forms part of both the knee and the ankle joints.',
    'The tibia is a long, three-sided (prismoid) bone, widest at its upper end and narrowest in its lower third. Its upper end spreads into the medial and lateral condyles that meet the femur; its shaft has anterior, medial and interosseous borders; its lower end extends downward on the inner side as the medial malleolus.',
    'On the medial (inner) side of the leg, between the knee above and the ankle below, with the fibula alongside it on the lateral side. Its medial surface and medial malleolus lie just under the skin.',
    '{"type": "long", "joints": "Knee joint: its condyles meet the femoral condyles, with the menisci between them. Superior and inferior tibiofibular joints with the fibula. Ankle joint: the lower articular surface and medial malleolus meet the talus.", "landmarks": "Medial and lateral condyles; intercondylar eminence with two tubercles; tibial tuberosity for the patellar ligament; facet for the fibular head on the lateral condyle; sharp anterior border (shin); popliteal line and a large nutrient foramen behind; medial malleolus."}'::jsonb,
    '[{"text": "Shin splints are pain from inflammation where muscle attaches along the shinbone; they are seen mainly in runners, especially those just starting a running program."}, {"text": "Stress fractures occur mostly in the weight-bearing bones of the lower limb, including the tibia."}, {"text": "Fractures of the tibial shaft are among the leg injuries MedlinePlus lists."}]'::jsonb,
    'Apart from the femur, the tibia is the longest bone in the skeleton.',
    '[{"title": "Gray''s Anatomy of the Human Body, 20th ed. (1918), The Tibia (Shin Bone) - PubAnnotation GrayAnatomy doc 61", "url": "https://pubannotation.org/docs/sourcedb/GrayAnatomy/sourceid/61", "licence": "Public domain"}, {"title": "Classification of Bones - NCI SEER Training Modules", "url": "https://training.seer.cancer.gov/anatomy/skeletal/classification.html", "licence": "Public domain"}, {"title": "Sports Injuries - NIAMS", "url": "https://www.niams.nih.gov/health-topics/sports-injuries", "licence": "Public domain"}, {"title": "Leg Injuries and Disorders - MedlinePlus (NLM)", "url": "https://medlineplus.gov/leginjuriesanddisorders.html", "licence": "Public domain"}]'::jsonb,
    'draft')
on conflict (key) do update set
    kind = excluded.kind,
    fma_ids = excluded.fma_ids,
    layer = excluded.layer,
    system = excluded.system,
    display_name = excluded.display_name,
    aliases = excluded.aliases,
    summary_plain = excluded.summary_plain,
    function_plain = excluded.function_plain,
    description = excluded.description,
    location = excluded.location,
    details = excluded.details,
    clinical = excluded.clinical,
    exam_tip = excluded.exam_tip,
    sources = excluded.sources,
    updated_at = now()
where b.status = 'draft'
  and (b.kind, b.fma_ids, b.layer, b.system, b.display_name, b.aliases, b.summary_plain, b.function_plain, b.description, b.location, b.details, b.clinical, b.exam_tip, b.sources)
  is distinct from (excluded.kind, excluded.fma_ids, excluded.layer, excluded.system, excluded.display_name, excluded.aliases, excluded.summary_plain, excluded.function_plain, excluded.description, excluded.location, excluded.details, excluded.clinical, excluded.exam_tip, excluded.sources);

-- Fibula  (2 FMA ids)
insert into public.body_part_info as b (key, kind, fma_ids, layer, system, display_name, aliases, summary_plain, function_plain, description, location, details, clinical, exam_tip, sources, status)
values ('fibula',
    'part',
    array['FMA24480', 'FMA24481']::text[],
    'bone',
    'musculoskeletal',
    'Fibula',
    array['calf bone']::text[],
    'The fibula is the thin outer bone of the lower leg. It runs beside the shin bone from just below the knee down to the outer ankle.',
    'It gives attachment to many leg muscles and forms the outer part of the ankle joint.',
    'The fibula is the smaller of the two leg bones and, for its length, the most slender of all the long bones. It has a small head with an upward-pointing apex, a shaft with four borders and four surfaces, and a lower end, the lateral malleolus. It is joined to the tibia at both ends but takes no part in the knee joint.',
    'On the lateral (outer) side of the leg, beside the tibia. Its head sits toward the back of the tibia''s lateral condyle, below the level of the knee joint; its lower end reaches lower than the medial malleolus.',
    '{"type": "long", "joints": "Superior tibiofibular joint: the head meets the lateral condyle of the tibia. It is also joined to the tibia below. Ankle joint: the lateral malleolus meets the lateral side of the talus. It is excluded from the knee joint.", "landmarks": "Head with its apex (styloid process); shaft with interosseous border for the interosseous membrane and a nutrient foramen on the back; lateral malleolus with a groove behind it for the fibularis tendons."}'::jsonb,
    '[{"text": "Stress fractures occur mostly in the weight-bearing bones of the lower limb, including the fibula."}]'::jsonb,
    'Gray''s Anatomy calls the fibula, relative to its length, the most slender of all the long bones.',
    '[{"title": "Gray''s Anatomy of the Human Body, 20th ed. (1918), The Fibula (Calf Bone) - PubAnnotation GrayAnatomy doc 62", "url": "https://pubannotation.org/docs/sourcedb/GrayAnatomy/sourceid/62", "licence": "Public domain"}, {"title": "Classification of Bones - NCI SEER Training Modules", "url": "https://training.seer.cancer.gov/anatomy/skeletal/classification.html", "licence": "Public domain"}, {"title": "Sports Injuries - NIAMS", "url": "https://www.niams.nih.gov/health-topics/sports-injuries", "licence": "Public domain"}]'::jsonb,
    'draft')
on conflict (key) do update set
    kind = excluded.kind,
    fma_ids = excluded.fma_ids,
    layer = excluded.layer,
    system = excluded.system,
    display_name = excluded.display_name,
    aliases = excluded.aliases,
    summary_plain = excluded.summary_plain,
    function_plain = excluded.function_plain,
    description = excluded.description,
    location = excluded.location,
    details = excluded.details,
    clinical = excluded.clinical,
    exam_tip = excluded.exam_tip,
    sources = excluded.sources,
    updated_at = now()
where b.status = 'draft'
  and (b.kind, b.fma_ids, b.layer, b.system, b.display_name, b.aliases, b.summary_plain, b.function_plain, b.description, b.location, b.details, b.clinical, b.exam_tip, b.sources)
  is distinct from (excluded.kind, excluded.fma_ids, excluded.layer, excluded.system, excluded.display_name, excluded.aliases, excluded.summary_plain, excluded.function_plain, excluded.description, excluded.location, excluded.details, excluded.clinical, excluded.exam_tip, excluded.sources);

-- Diaphragm  (1 FMA ids)
insert into public.body_part_info as b (key, kind, fma_ids, layer, system, display_name, aliases, summary_plain, function_plain, description, location, details, clinical, exam_tip, sources, status)
values ('diaphragm',
    'part',
    array['FMA13295']::text[],
    'muscle',
    'musculoskeletal',
    'Diaphragm',
    '{}'::text[],
    'The diaphragm is a thin, dome-shaped muscle at the base of the lungs. It forms a wall between the chest and the belly.',
    'It is the main muscle for breathing: it tightens and moves down to pull air in, then relaxes to let air out.',
    'The diaphragm is a dome-shaped sheet of muscle that separates the thoracic cavity from the abdominal cavity. It has three openings that let structures pass from chest to abdomen, including the oesophageal hiatus. Its contraction drives breathing in; breathing out at rest is mostly passive.',
    'Below the lungs and above the abdominal organs; the stomach lies just beneath it on the left. It is crossed by the oesophagus through the oesophageal hiatus.',
    '{"action": "Contracts and moves down during inhalation, enlarging the chest cavity so the lungs expand and air flows in; relaxes during exhalation, so elastic recoil shrinks the chest and pushes air out."}'::jsonb,
    '[{"text": "A hiatal hernia occurs when the top of the stomach pushes up through the diaphragm''s opening; risk rises after age 50 and with obesity and smoking.", "disease_id": "gerd"}, {"text": "Hiccups are sudden involuntary movements of the diaphragm with quick closing of the vocal cords, often triggered by something irritating the diaphragm."}, {"text": "Damage to nerves in the upper spinal cord, as in spinal cord injury or stroke, can impair diaphragm movement and lead to respiratory failure."}]'::jsonb,
    'Breathing in is active because the diaphragm contracts; quiet breathing out is passive and needs no muscle effort.',
    '[{"title": "Muscle Groups: Trunk - NCI SEER Training Modules", "url": "https://training.seer.cancer.gov/anatomy/muscular/groups/trunk.html", "licence": "Public domain"}, {"title": "Mechanics of Ventilation - NCI SEER Training Modules", "url": "https://training.seer.cancer.gov/anatomy/respiratory/mechanics.html", "licence": "Public domain"}, {"title": "How the Lungs Work: What Breathing Does for the Body - NHLBI", "url": "https://www.nhlbi.nih.gov/health/lungs/breathing-benefits", "licence": "Public domain"}, {"title": "How the Lungs Work: How Your Body Controls Breathing - NHLBI", "url": "https://www.nhlbi.nih.gov/health/lungs/body-controls-breathing", "licence": "Public domain"}, {"title": "Pharynx & Esophagus - NCI SEER Training Modules", "url": "https://training.seer.cancer.gov/anatomy/digestive/regions/pharynx.html", "licence": "Public domain"}, {"title": "Anatomy of the Stomach - NCI SEER Training Modules", "url": "https://training.seer.cancer.gov/ugi/anatomy/stomach.html", "licence": "Public domain"}, {"title": "Hiatal Hernia - MedlinePlus (NLM)", "url": "https://medlineplus.gov/hiatalhernia.html", "licence": "Public domain"}, {"title": "Hiccups - MedlinePlus (NLM)", "url": "https://medlineplus.gov/hiccups.html", "licence": "Public domain"}]'::jsonb,
    'draft')
on conflict (key) do update set
    kind = excluded.kind,
    fma_ids = excluded.fma_ids,
    layer = excluded.layer,
    system = excluded.system,
    display_name = excluded.display_name,
    aliases = excluded.aliases,
    summary_plain = excluded.summary_plain,
    function_plain = excluded.function_plain,
    description = excluded.description,
    location = excluded.location,
    details = excluded.details,
    clinical = excluded.clinical,
    exam_tip = excluded.exam_tip,
    sources = excluded.sources,
    updated_at = now()
where b.status = 'draft'
  and (b.kind, b.fma_ids, b.layer, b.system, b.display_name, b.aliases, b.summary_plain, b.function_plain, b.description, b.location, b.details, b.clinical, b.exam_tip, b.sources)
  is distinct from (excluded.kind, excluded.fma_ids, excluded.layer, excluded.system, excluded.display_name, excluded.aliases, excluded.summary_plain, excluded.function_plain, excluded.description, excluded.location, excluded.details, excluded.clinical, excluded.exam_tip, excluded.sources);

-- Deltoid  (6 FMA ids)
insert into public.body_part_info as b (key, kind, fma_ids, layer, system, display_name, aliases, summary_plain, function_plain, description, location, details, clinical, exam_tip, sources, status)
values ('group:deltoid',
    'group',
    array['FMA34680', 'FMA34681', 'FMA34682', 'FMA34683', 'FMA34684', 'FMA34685']::text[],
    'muscle',
    'musculoskeletal',
    'Deltoid',
    '{}'::text[],
    'The deltoid is the large, thick, triangle-shaped muscle that forms the rounded cap of the shoulder. It covers the shoulder joint at the front, side and back.',
    'It lifts the arm out to the side, and its front and back parts help swing the arm forward and backward.',
    'The deltoid is a coarse, triangular muscle named for its shape. It has three parts: a clavicular (anterior) part from the clavicle, an acromial (middle) part from the acromion and a spinal (posterior) part from the spine of the scapula. The fibres converge into a thick tendon on the side of the humerus, and the acromial part is multipennate, built around several tendinous bands.',
    'Over the shoulder joint, covering it in front, at the side and behind. It runs from the lateral clavicle, acromion and scapular spine down to the middle of the lateral side of the humerus, under the deep fascia.',
    '{"origin": "Clavicular part: front border and upper surface of the lateral third of the clavicle. Acromial part: lateral margin and upper surface of the acromion. Spinal part: lower lip of the posterior border of the spine of the scapula.", "insertion": "Deltoid tuberosity, midway down the lateral side of the shaft of the humerus.", "action": "Abducts the arm to a right angle with the trunk. The clavicular part, with pectoralis major, draws the arm forward; the spinal part, with teres major and latissimus dorsi, draws it backward.", "nerve_supply": "Axillary nerve (C5, C6).", "blood_supply": "Deltoid and acromial branches of the thoracoacromial artery and the posterior circumflex humeral artery; small branches also from the circumflex scapular artery and the profunda brachii."}'::jsonb,
    '[{"text": "The deltoid is the recommended site for intramuscular vaccine injections in adults and the preferred site for children aged 3 to 18 years (CDC guidance, United States)."}, {"text": "Intramuscular injections go into the middle of the muscle where it is thickest, at 90 degrees, which lowers the chance of hitting nerves or blood vessels."}]'::jsonb,
    'The name deltoid means triangular: the muscle is named for its shape.',
    '[{"title": "Gray''s Anatomy of the Human Body, 20th ed. (1918), full text - Internet Archive", "url": "https://archive.org/download/anatomyofhumanbo1918gray/anatomyofhumanbo1918gray_djvu.txt", "licence": "Public domain"}, {"title": "Muscle Groups - NCI SEER Training Modules", "url": "https://training.seer.cancer.gov/anatomy/muscular/groups/", "licence": "Public domain"}, {"title": "Muscles of the Upper Extremity - NCI SEER Training Modules", "url": "https://training.seer.cancer.gov/anatomy/muscular/groups/upper.html", "licence": "Public domain"}, {"title": "Pink Book Chapter 6: Vaccine Administration - CDC", "url": "https://www.cdc.gov/pinkbook/hcp/table-of-contents/chapter-6-vaccine-administration.html", "licence": "Public domain"}]'::jsonb,
    'draft')
on conflict (key) do update set
    kind = excluded.kind,
    fma_ids = excluded.fma_ids,
    layer = excluded.layer,
    system = excluded.system,
    display_name = excluded.display_name,
    aliases = excluded.aliases,
    summary_plain = excluded.summary_plain,
    function_plain = excluded.function_plain,
    description = excluded.description,
    location = excluded.location,
    details = excluded.details,
    clinical = excluded.clinical,
    exam_tip = excluded.exam_tip,
    sources = excluded.sources,
    updated_at = now()
where b.status = 'draft'
  and (b.kind, b.fma_ids, b.layer, b.system, b.display_name, b.aliases, b.summary_plain, b.function_plain, b.description, b.location, b.details, b.clinical, b.exam_tip, b.sources)
  is distinct from (excluded.kind, excluded.fma_ids, excluded.layer, excluded.system, excluded.display_name, excluded.aliases, excluded.summary_plain, excluded.function_plain, excluded.description, excluded.location, excluded.details, excluded.clinical, excluded.exam_tip, excluded.sources);

-- Biceps brachii  (4 FMA ids)
insert into public.body_part_info as b (key, kind, fma_ids, layer, system, display_name, aliases, summary_plain, function_plain, description, location, details, clinical, exam_tip, sources, status)
values ('biceps brachii',
    'part',
    array['FMA37684', 'FMA37685', 'FMA37686', 'FMA37687']::text[],
    'muscle',
    'musculoskeletal',
    'Biceps brachii',
    '{}'::text[],
    'The biceps brachii is the long muscle on the front of the upper arm. It has two heads that start at the shoulder blade and join to attach just below the elbow.',
    'It bends the elbow and turns the forearm so the palm faces up.',
    'The biceps brachii is a long, spindle-shaped (fusiform) muscle of the front of the arm, named for its two heads. The short head arises from the coracoid process and the long head from the supraglenoid tubercle, its tendon running inside the shoulder joint and down the intertubercular groove. The bellies join above the elbow and end in a tendon on the radius, which also gives off the bicipital aponeurosis.',
    'On the front of the arm, from the scapula over the front of the shoulder joint down to the radius below the elbow. Its long-head tendon lies in the intertubercular groove of the humerus, and the bicipital aponeurosis crosses the brachial artery at the bend of the elbow.',
    '{"origin": "Short head: tip of the coracoid process of the scapula (with coracobrachialis). Long head: supraglenoid tubercle at the top of the glenoid cavity; its tendon arches over the head of the humerus inside the joint and descends in the intertubercular groove.", "insertion": "Back part of the radial tuberosity, with a bursa between tendon and bone; the bicipital aponeurosis passes medially to blend with the deep fascia over the forearm flexors.", "action": "Flexes the elbow and, less strongly, the shoulder; a powerful supinator of the forearm. With the forearm fixed, it pulls the arm up toward the forearm, as in climbing.", "nerve_supply": "Musculocutaneous nerve (C5, C6).", "blood_supply": "Muscular branches of the brachial artery."}'::jsonb,
    '[]'::jsonb,
    'Biceps means two heads. Besides bending the elbow, Gray''s Anatomy calls the biceps a powerful supinator of the forearm.',
    '[{"title": "Gray''s Anatomy of the Human Body, 20th ed. (1918), full text - Internet Archive", "url": "https://archive.org/download/anatomyofhumanbo1918gray/anatomyofhumanbo1918gray_djvu.txt", "licence": "Public domain"}, {"title": "Muscle Groups - NCI SEER Training Modules", "url": "https://training.seer.cancer.gov/anatomy/muscular/groups/", "licence": "Public domain"}, {"title": "Muscles of the Upper Extremity - NCI SEER Training Modules", "url": "https://training.seer.cancer.gov/anatomy/muscular/groups/upper.html", "licence": "Public domain"}]'::jsonb,
    'draft')
on conflict (key) do update set
    kind = excluded.kind,
    fma_ids = excluded.fma_ids,
    layer = excluded.layer,
    system = excluded.system,
    display_name = excluded.display_name,
    aliases = excluded.aliases,
    summary_plain = excluded.summary_plain,
    function_plain = excluded.function_plain,
    description = excluded.description,
    location = excluded.location,
    details = excluded.details,
    clinical = excluded.clinical,
    exam_tip = excluded.exam_tip,
    sources = excluded.sources,
    updated_at = now()
where b.status = 'draft'
  and (b.kind, b.fma_ids, b.layer, b.system, b.display_name, b.aliases, b.summary_plain, b.function_plain, b.description, b.location, b.details, b.clinical, b.exam_tip, b.sources)
  is distinct from (excluded.kind, excluded.fma_ids, excluded.layer, excluded.system, excluded.display_name, excluded.aliases, excluded.summary_plain, excluded.function_plain, excluded.description, excluded.location, excluded.details, excluded.clinical, excluded.exam_tip, excluded.sources);

-- Triceps brachii  (6 FMA ids)
insert into public.body_part_info as b (key, kind, fma_ids, layer, system, display_name, aliases, summary_plain, function_plain, description, location, details, clinical, exam_tip, sources, status)
values ('triceps brachii',
    'part',
    array['FMA37695', 'FMA37696', 'FMA37697', 'FMA37698', 'FMA37699', 'FMA37700']::text[],
    'muscle',
    'musculoskeletal',
    'Triceps brachii',
    '{}'::text[],
    'The triceps brachii is the large muscle on the back of the upper arm. It has three heads that join into one tendon at the point of the elbow.',
    'It straightens the elbow, working against the biceps, which bends it.',
    'The triceps brachii is a large muscle covering the whole back of the humerus, named for its three heads: long, lateral and medial. The long head arises from the scapula and the other two from the back of the humerus, above and below the groove for the radial nerve. They join in a tendon on the olecranon of the ulna.',
    'On the back of the arm, along the full length of the posterior humerus, from the scapula and humerus down to the olecranon. Its long head passes between teres minor and teres major, separating the triangular and quadrangular spaces.',
    '{"origin": "Long head: infraglenoid tubercle of the scapula, blending with the shoulder joint capsule. Lateral head: back of the humerus above the radial groove, lateral border and lateral intermuscular septum. Medial head: back of the humerus below the radial groove, medial border and medial intermuscular septum.", "insertion": "Mainly the upper back part of the olecranon of the ulna; a band continues over anconeus to blend with the deep fascia of the forearm.", "action": "Main extensor of the elbow, the direct antagonist of biceps and brachialis. The long head helps draw the humerus backward and adduct it, and supports the underside of the shoulder joint.", "nerve_supply": "Radial nerve (C7, C8).", "blood_supply": "Branches of the profunda brachii artery (one descends in the medial head, another runs between the long and lateral heads); the circumflex scapular artery also sends branches to the long head."}'::jsonb,
    '[]'::jsonb,
    'Triceps means three heads. The long head separates the triangular space (circumflex scapular vessels) from the quadrangular space (posterior circumflex humeral vessels and axillary nerve).',
    '[{"title": "Gray''s Anatomy of the Human Body, 20th ed. (1918), full text - Internet Archive", "url": "https://archive.org/download/anatomyofhumanbo1918gray/anatomyofhumanbo1918gray_djvu.txt", "licence": "Public domain"}, {"title": "Muscle Groups - NCI SEER Training Modules", "url": "https://training.seer.cancer.gov/anatomy/muscular/groups/", "licence": "Public domain"}, {"title": "Muscles of the Upper Extremity - NCI SEER Training Modules", "url": "https://training.seer.cancer.gov/anatomy/muscular/groups/upper.html", "licence": "Public domain"}]'::jsonb,
    'draft')
on conflict (key) do update set
    kind = excluded.kind,
    fma_ids = excluded.fma_ids,
    layer = excluded.layer,
    system = excluded.system,
    display_name = excluded.display_name,
    aliases = excluded.aliases,
    summary_plain = excluded.summary_plain,
    function_plain = excluded.function_plain,
    description = excluded.description,
    location = excluded.location,
    details = excluded.details,
    clinical = excluded.clinical,
    exam_tip = excluded.exam_tip,
    sources = excluded.sources,
    updated_at = now()
where b.status = 'draft'
  and (b.kind, b.fma_ids, b.layer, b.system, b.display_name, b.aliases, b.summary_plain, b.function_plain, b.description, b.location, b.details, b.clinical, b.exam_tip, b.sources)
  is distinct from (excluded.kind, excluded.fma_ids, excluded.layer, excluded.system, excluded.display_name, excluded.aliases, excluded.summary_plain, excluded.function_plain, excluded.description, excluded.location, excluded.details, excluded.clinical, excluded.exam_tip, excluded.sources);

-- Pectoralis major  (6 FMA ids)
insert into public.body_part_info as b (key, kind, fma_ids, layer, system, display_name, aliases, summary_plain, function_plain, description, location, details, clinical, exam_tip, sources, status)
values ('pectoralis major',
    'part',
    array['FMA34690', 'FMA34691', 'FMA45874', 'FMA45875', 'FMA79979', 'FMA79980']::text[],
    'muscle',
    'musculoskeletal',
    'Pectoralis major',
    array['chest muscle']::text[],
    'The pectoralis major is the main chest muscle. It is a thick, fan-shaped muscle on the upper front of the chest that runs out to the upper arm bone.',
    'It pulls the arm in toward the body and across the chest, turns it inward, and brings a raised arm back down.',
    'The pectoralis major is a thick, fan-shaped muscle with a wide origin from the clavicle, sternum, upper costal cartilages and the external oblique aponeurosis, giving clavicular, sternocostal and abdominal parts. Its fibers converge on a flat tendon about 5 cm wide, made of two layers. The tendon looks twisted because the lowest fibers turn behind the others and insert highest on the humerus.',
    'Upper front of the chest, in front of the armpit (axilla). Its clavicular part covers the clavipectoral fascia, which protects the axillary vessels and nerves.',
    '{"origin": "Front of the sternal (medial) half of the clavicle; front of the sternum down to the sixth or seventh costal cartilage; cartilages of the true ribs (often not the first or seventh); aponeurosis of the external oblique.", "insertion": "By a flat two-layered tendon into the crest of the greater tubercle of the humerus (lateral lip of the intertubercular groove); expansions reach the shoulder-joint capsule, line the groove and join the fascia of the arm.", "action": "Adducts the arm and draws it forward across the chest while rotating it medially; with latissimus dorsi and teres major it lowers a raised arm. With the arms fixed, it lifts the ribs and helps forced inspiration.", "nerve_supply": "Medial and lateral pectoral nerves (Gray''s ''anterior thoracic nerves''), which bring fibers from all the spinal nerves forming the brachial plexus.", "blood_supply": "Pectoral branch of the thoracoacromial artery, which runs down between the pectoralis major and minor."}'::jsonb,
    '[{"text": "In Poland syndrome, muscles on one side of the body are missing or underdeveloped, most often the sternal part of pectoralis major; it affects about 1 in 20,000 newborns, more often males."}, {"text": "Partial absence of the sternocostal part is not uncommon; absence of the clavicular part is less frequent, and absence of the whole muscle is rare."}]'::jsonb,
    'Its tendon is twisted: fibers from the lowest costal cartilages pass behind the upper ones and insert highest on the humerus.',
    '[{"title": "Gray''s Anatomy of the Human Body, 20th ed. (1918), Myology: Pectoralis major (p. 436-438) and Angiology: thoracoacromial artery - Internet Archive full text", "url": "https://archive.org/download/anatomyofhumanbo1918gray/anatomyofhumanbo1918gray_djvu.txt", "licence": "Public domain"}, {"title": "Pectoralis Muscles - MeSH (NLM)", "url": "https://meshb.nlm.nih.gov/record/ui?ui=D010369", "licence": "Public domain"}, {"title": "Upper Extremity (Muscle Groups) - NCI SEER Training Modules", "url": "https://training.seer.cancer.gov/anatomy/muscular/groups/upper.html", "licence": "Public domain"}, {"title": "Poland syndrome - MedlinePlus Genetics (NLM)", "url": "https://medlineplus.gov/genetics/condition/poland-syndrome/", "licence": "Public domain"}]'::jsonb,
    'draft')
on conflict (key) do update set
    kind = excluded.kind,
    fma_ids = excluded.fma_ids,
    layer = excluded.layer,
    system = excluded.system,
    display_name = excluded.display_name,
    aliases = excluded.aliases,
    summary_plain = excluded.summary_plain,
    function_plain = excluded.function_plain,
    description = excluded.description,
    location = excluded.location,
    details = excluded.details,
    clinical = excluded.clinical,
    exam_tip = excluded.exam_tip,
    sources = excluded.sources,
    updated_at = now()
where b.status = 'draft'
  and (b.kind, b.fma_ids, b.layer, b.system, b.display_name, b.aliases, b.summary_plain, b.function_plain, b.description, b.location, b.details, b.clinical, b.exam_tip, b.sources)
  is distinct from (excluded.kind, excluded.fma_ids, excluded.layer, excluded.system, excluded.display_name, excluded.aliases, excluded.summary_plain, excluded.function_plain, excluded.description, excluded.location, excluded.details, excluded.clinical, excluded.exam_tip, excluded.sources);

-- Trapezius  (6 FMA ids)
insert into public.body_part_info as b (key, kind, fma_ids, layer, system, display_name, aliases, summary_plain, function_plain, description, location, details, clinical, exam_tip, sources, status)
values ('trapezius',
    'part',
    array['FMA33581', 'FMA33583', 'FMA33584', 'FMA33585', 'FMA33586', 'FMA33587']::text[],
    'muscle',
    'musculoskeletal',
    'Trapezius',
    '{}'::text[],
    'The trapezius is a large, flat, triangle-shaped muscle on the upper back. It covers the back of the neck and the tops of the shoulders.',
    'It pulls the shoulder blades back, lifts the shoulders when carrying weight, and helps pull the head backward or to one side.',
    'The trapezius is a flat, triangular muscle in the top layer of the back muscles, which move the scapula. Its upper (descending) fibers run down and outward, its middle (transverse) fibers run across, and its lower (ascending) fibers run up and outward toward the shoulder girdle. The right and left muscles together form a diamond-shaped figure, with corners at the shoulders, the external occipital protuberance and the twelfth thoracic spine.',
    'Back of the neck and upper back, from the base of the skull down to the twelfth thoracic vertebra and out to the clavicle and scapula. It lies superficially; its front edge forms the back border of the posterior triangle of the neck, behind the sternocleidomastoid.',
    '{"origin": "External occipital protuberance and medial third of the superior nuchal line; ligamentum nuchae; spinous process of C7 and the spinous processes of all thoracic vertebrae, with the supraspinous ligament.", "insertion": "Upper fibers: posterior border of the lateral third of the clavicle. Middle fibers: medial margin of the acromion and upper lip of the spine of the scapula. Lower fibers: by an aponeurosis to a tubercle at the medial end of the scapular spine.", "action": "Retracts the scapula and braces the shoulder back. Upper fibers raise the point of the shoulder, as in carrying weights; lower fibers help depress the scapula; middle and lower fibers rotate it, raising the acromion. With shoulders fixed, both draw the head back; one tilts it sideways.", "nerve_supply": "Accessory nerve, with branches from the third and fourth cervical nerves.", "blood_supply": "Branches of the transverse cervical artery (its ascending and descending branches) and the descending branch of the occipital artery."}'::jsonb,
    '[{"text": "Neck pain is often due to strained or tense neck muscles, for example after long computer work, sleeping in an awkward position or overdoing exercise."}]'::jsonb,
    'Named for its shape: the right and left trapezius together look like a trapezium, a four-sided figure.',
    '[{"title": "Gray''s Anatomy of the Human Body, 20th ed. (1918), Myology: Trapezius (p. 432-434) and Angiology: occipital and transverse cervical arteries - Internet Archive full text", "url": "https://archive.org/download/anatomyofhumanbo1918gray/anatomyofhumanbo1918gray_djvu.txt", "licence": "Public domain"}, {"title": "Superficial Back Muscles - MeSH (NLM)", "url": "https://meshb.nlm.nih.gov/record/ui?ui=D064171", "licence": "Public domain"}, {"title": "Muscle Groups - NCI SEER Training Modules", "url": "https://training.seer.cancer.gov/anatomy/muscular/groups/", "licence": "Public domain"}, {"title": "Upper Extremity (Muscle Groups) - NCI SEER Training Modules", "url": "https://training.seer.cancer.gov/anatomy/muscular/groups/upper.html", "licence": "Public domain"}, {"title": "Head and Neck (Muscle Groups) - NCI SEER Training Modules", "url": "https://training.seer.cancer.gov/anatomy/muscular/groups/head_neck.html", "licence": "Public domain"}, {"title": "Neck Injuries and Disorders - MedlinePlus (NLM)", "url": "https://medlineplus.gov/neckinjuriesanddisorders.html", "licence": "Public domain"}]'::jsonb,
    'draft')
on conflict (key) do update set
    kind = excluded.kind,
    fma_ids = excluded.fma_ids,
    layer = excluded.layer,
    system = excluded.system,
    display_name = excluded.display_name,
    aliases = excluded.aliases,
    summary_plain = excluded.summary_plain,
    function_plain = excluded.function_plain,
    description = excluded.description,
    location = excluded.location,
    details = excluded.details,
    clinical = excluded.clinical,
    exam_tip = excluded.exam_tip,
    sources = excluded.sources,
    updated_at = now()
where b.status = 'draft'
  and (b.kind, b.fma_ids, b.layer, b.system, b.display_name, b.aliases, b.summary_plain, b.function_plain, b.description, b.location, b.details, b.clinical, b.exam_tip, b.sources)
  is distinct from (excluded.kind, excluded.fma_ids, excluded.layer, excluded.system, excluded.display_name, excluded.aliases, excluded.summary_plain, excluded.function_plain, excluded.description, excluded.location, excluded.details, excluded.clinical, excluded.exam_tip, excluded.sources);

-- Sternocleidomastoid  (2 FMA ids)
insert into public.body_part_info as b (key, kind, fma_ids, layer, system, display_name, aliases, summary_plain, function_plain, description, location, details, clinical, exam_tip, sources, status)
values ('sternocleidomastoid',
    'part',
    array['FMA13408', 'FMA13409']::text[],
    'muscle',
    'musculoskeletal',
    'Sternocleidomastoid',
    array['sternomastoid']::text[],
    'The sternocleidomastoid is a long muscle on each side of the neck. It runs at a slant from the breastbone and collarbone up to the bony bump behind the ear.',
    'It tips the head toward the shoulder and turns the face to the other side, and both muscles together bend the neck forward.',
    'The sternocleidomastoid crosses the side of the neck obliquely; it is thick and narrow in the middle and broader and thinner at each end. It starts as two heads, sternal and clavicular, separated by a small triangular gap, which merge below the middle of the neck into one rounded belly. It divides the side of the neck into the anterior and posterior triangles.',
    'Side of the neck, from the top of the sternum (manubrium) and the inner third of the clavicle up to the mastoid process behind the ear. Its front border bounds the anterior triangle of the neck; its back border bounds the posterior triangle, which the trapezius closes behind.',
    '{"origin": "Sternal head: upper part of the front surface of the manubrium of the sternum. Clavicular head: upper border and front surface of the medial third of the clavicle.", "insertion": "By a strong tendon into the lateral surface of the mastoid process of the temporal bone, from apex to upper border, and by a thin aponeurosis into the lateral half of the superior nuchal line of the occipital bone.", "action": "One muscle: tilts the head toward the shoulder of the same side and rotates the face toward the opposite side. Both together: flex the cervical spine. With the head fixed, they help raise the thorax in forced inspiration.", "nerve_supply": "Accessory nerve, plus branches from the anterior rami of the second and third cervical nerves.", "blood_supply": "Sternocleidomastoid branch of the superior thyroid artery, and the sternocleidomastoid artery, usually from the occipital artery (sometimes from the external carotid), which enters the muscle with the accessory nerve."}'::jsonb,
    '[{"text": "Torticollis (wryneck) is a twisted neck: the head tips to one side and the chin turns to the other, from congenital defects, trauma, inflammation, tumours or nerve disorders."}, {"text": "Neck pain is often due to strained or tense neck muscles, for example after long computer work, sleeping in an awkward position or overdoing exercise."}]'::jsonb,
    'Its name gives its attachments: it arises from the sternum and clavicle and inserts on the mastoid process.',
    '[{"title": "Gray''s Anatomy of the Human Body, 20th ed. (1918), Myology: Sternocleidomastoideus (p. 390-391) and Angiology: superior thyroid and occipital arteries - Internet Archive full text", "url": "https://archive.org/download/anatomyofhumanbo1918gray/anatomyofhumanbo1918gray_djvu.txt", "licence": "Public domain"}, {"title": "Muscle Groups - NCI SEER Training Modules", "url": "https://training.seer.cancer.gov/anatomy/muscular/groups/", "licence": "Public domain"}, {"title": "Head and Neck (Muscle Groups) - NCI SEER Training Modules", "url": "https://training.seer.cancer.gov/anatomy/muscular/groups/head_neck.html", "licence": "Public domain"}, {"title": "Torticollis - MeSH (NLM)", "url": "https://meshb.nlm.nih.gov/record/ui?ui=D014103", "licence": "Public domain"}, {"title": "Neck Injuries and Disorders - MedlinePlus (NLM)", "url": "https://medlineplus.gov/neckinjuriesanddisorders.html", "licence": "Public domain"}]'::jsonb,
    'draft')
on conflict (key) do update set
    kind = excluded.kind,
    fma_ids = excluded.fma_ids,
    layer = excluded.layer,
    system = excluded.system,
    display_name = excluded.display_name,
    aliases = excluded.aliases,
    summary_plain = excluded.summary_plain,
    function_plain = excluded.function_plain,
    description = excluded.description,
    location = excluded.location,
    details = excluded.details,
    clinical = excluded.clinical,
    exam_tip = excluded.exam_tip,
    sources = excluded.sources,
    updated_at = now()
where b.status = 'draft'
  and (b.kind, b.fma_ids, b.layer, b.system, b.display_name, b.aliases, b.summary_plain, b.function_plain, b.description, b.location, b.details, b.clinical, b.exam_tip, b.sources)
  is distinct from (excluded.kind, excluded.fma_ids, excluded.layer, excluded.system, excluded.display_name, excluded.aliases, excluded.summary_plain, excluded.function_plain, excluded.description, excluded.location, excluded.details, excluded.clinical, excluded.exam_tip, excluded.sources);

-- Quadriceps femoris  (8 FMA ids)
insert into public.body_part_info as b (key, kind, fma_ids, layer, system, display_name, aliases, summary_plain, function_plain, description, location, details, clinical, exam_tip, sources, status)
values ('group:quadriceps',
    'group',
    array['FMA38928', 'FMA38929', 'FMA38930', 'FMA38931', 'FMA38932', 'FMA38933', 'FMA38934', 'FMA38935']::text[],
    'muscle',
    'musculoskeletal',
    'Quadriceps femoris',
    array['quadriceps', 'quadriceps extensor']::text[],
    'The quadriceps is the big group of four muscles on the front of the thigh. It covers the front and sides of the thigh bone and ends in a tendon at the kneecap.',
    'It straightens the knee, and one of its parts, the rectus femoris, also helps bend the hip.',
    'The quadriceps femoris is the great extensor of the knee, a large fleshy mass covering the front and sides of the femur. It has four parts: the rectus femoris in the middle of the thigh, and three vasti (lateralis, medialis and intermedius) that cover the femoral shaft from the trochanters to the condyles. Vastus lateralis is the largest. Their tendons join into one quadriceps tendon above the knee.',
    'Front and sides of the thigh, between the hip and the knee. Rectus femoris lies in the middle front; vastus lateralis on the outer side, vastus medialis on the inner side, and vastus intermedius in front, lying directly on the femur.',
    '{"origin": "Rectus femoris: anterior inferior iliac spine (straight head) and a groove above the acetabulum (reflected head). Vasti: the femoral shaft, including the intertrochanteric line, greater trochanter, gluteal tuberosity, linea aspera, and (intermedius) the front and lateral surfaces.", "insertion": "The four tendons unite into the quadriceps tendon on the base of the patella; the patellar ligament continues from the patella to the tibial tuberosity as the true tendon of insertion. Vastus lateralis and medialis also attach to the patellar borders.", "action": "Extends the knee. Rectus femoris also helps flex the hip and supports the pelvis and trunk on the femur; vastus medialis pulls the patella medially as well as upward.", "nerve_supply": "Femoral nerve (second, third and fourth lumbar nerves).", "blood_supply": "Lateral femoral circumflex artery, a branch of the deep femoral artery; its descending branch runs behind rectus femoris and supplies vastus lateralis."}'::jsonb,
    '[{"text": "Patellar tendinitis (''jumper''s knee'') is swelling of the tendon below the kneecap that carries the quadriceps'' pull to the tibia; it usually follows repeated strain, often in sport."}]'::jsonb,
    'The quadriceps (named for its four heads) straightens the knee; the hamstrings at the back of the thigh are its antagonists and bend the knee.',
    '[{"title": "Gray''s Anatomy of the Human Body, 20th ed. (1918), Myology: Quadriceps femoris (p. 470-471) and Angiology: lateral femoral circumflex artery - Internet Archive full text", "url": "https://archive.org/download/anatomyofhumanbo1918gray/anatomyofhumanbo1918gray_djvu.txt", "licence": "Public domain"}, {"title": "Quadriceps Muscle - MeSH (NLM)", "url": "https://meshb.nlm.nih.gov/record/ui?ui=D052097", "licence": "Public domain"}, {"title": "Lower Extremity (Muscle Groups) - NCI SEER Training Modules", "url": "https://training.seer.cancer.gov/anatomy/muscular/groups/lower.html", "licence": "Public domain"}, {"title": "Muscle Groups - NCI SEER Training Modules", "url": "https://training.seer.cancer.gov/anatomy/muscular/groups/", "licence": "Public domain"}, {"title": "Tendinitis - MedlinePlus (NLM)", "url": "https://medlineplus.gov/tendinitis.html", "licence": "Public domain"}, {"title": "Knee Injuries and Disorders - MedlinePlus (NLM)", "url": "https://medlineplus.gov/kneeinjuriesanddisorders.html", "licence": "Public domain"}]'::jsonb,
    'draft')
on conflict (key) do update set
    kind = excluded.kind,
    fma_ids = excluded.fma_ids,
    layer = excluded.layer,
    system = excluded.system,
    display_name = excluded.display_name,
    aliases = excluded.aliases,
    summary_plain = excluded.summary_plain,
    function_plain = excluded.function_plain,
    description = excluded.description,
    location = excluded.location,
    details = excluded.details,
    clinical = excluded.clinical,
    exam_tip = excluded.exam_tip,
    sources = excluded.sources,
    updated_at = now()
where b.status = 'draft'
  and (b.kind, b.fma_ids, b.layer, b.system, b.display_name, b.aliases, b.summary_plain, b.function_plain, b.description, b.location, b.details, b.clinical, b.exam_tip, b.sources)
  is distinct from (excluded.kind, excluded.fma_ids, excluded.layer, excluded.system, excluded.display_name, excluded.aliases, excluded.summary_plain, excluded.function_plain, excluded.description, excluded.location, excluded.details, excluded.clinical, excluded.exam_tip, excluded.sources);

-- Hamstrings  (8 FMA ids)
insert into public.body_part_info as b (key, kind, fma_ids, layer, system, display_name, aliases, summary_plain, function_plain, description, location, details, clinical, exam_tip, sources, status)
values ('group:hamstrings',
    'group',
    array['FMA22358', 'FMA22359', 'FMA22448', 'FMA22449', 'FMA45888', 'FMA45889', 'FMA45891', 'FMA45892']::text[],
    'muscle',
    'musculoskeletal',
    'Hamstrings',
    array['hamstring muscles', 'posterior femoral muscles']::text[],
    'The hamstrings are a group of three muscles that run down the back of the thigh, from the bottom of the pelvis to just below the knee.',
    'They bend the knee, and they help the buttock muscle pull the trunk back upright after bending forward.',
    'The hamstrings (posterior femoral muscles) are the biceps femoris, with a long and a short head, the semitendinosus and the semimembranosus. Except for the short head of biceps, they arise from the ischial tuberosity. The biceps tendon forms the lateral hamstring; the semitendinosus and semimembranosus tendons form the medial hamstrings. They act against the quadriceps.',
    'In the back of the thigh. The biceps femoris lies on the lateral side and passes to the fibula; the semitendinosus and semimembranosus lie medially and pass to the tibia. The semitendinosus tendon runs along the medial side of the popliteal fossa behind the knee.',
    '{"origin": "Long head of biceps femoris and semitendinosus: lower medial impression on the ischial tuberosity. Semimembranosus: upper lateral impression on the ischial tuberosity, by a thick tendon. Short head of biceps: lateral lip of the linea aspera and the lateral intermuscular septum.", "insertion": "Biceps femoris: lateral side of the head of the fibula, with a small slip to the lateral condyle of the tibia. Semitendinosus: upper medial surface of the tibial shaft, behind the sartorius and joined to the gracilis tendon. Semimembranosus: groove on the back of the medial tibial condyle.", "action": "Flex the leg at the knee. With the knee half bent, the biceps turns the leg slightly outward and the semitendinosus (and a little the semimembranosus) turns it inward. They help the gluteus maximus restore the upright posture after stooping.", "nerve_supply": "Sciatic nerve branches (L4 to S3): the tibial nerve to the semitendinosus, semimembranosus and long head of biceps; the common fibular (peroneal) nerve to the short head of biceps.", "blood_supply": "Mainly the perforating branches of the deep femoral (profunda femoris) artery; the inferior gluteal artery supplies the muscles near their attachment to the ischial tuberosity."}'::jsonb,
    '[{"text": "Hamstring strains (stretched or torn muscle or tendon) are common; they cause pain, spasm, swelling and trouble moving the muscle."}, {"text": "Hamstring strains happen in sports with much running, jumping and sudden starts and stops, such as basketball, football and soccer."}, {"text": "Strains are first treated with rest, ice, compression and medicines; exercise and physical therapy may follow."}]'::jsonb,
    'The short head of biceps femoris is the only hamstring part supplied by the common fibular (peroneal) nerve; the others are supplied by the tibial nerve.',
    '[{"title": "Gray''s Anatomy of the Human Body, 20th ed. (1918), Posterior Femoral Muscles and Arteries of the Lower Extremity - Internet Archive full text", "url": "https://archive.org/download/anatomyofhumanbo1918gray/anatomyofhumanbo1918gray_djvu.txt", "licence": "Public domain"}, {"title": "Muscles of the Lower Extremity - NCI SEER Training Modules", "url": "https://training.seer.cancer.gov/anatomy/muscular/groups/lower.html", "licence": "Public domain"}, {"title": "Muscle Groups - NCI SEER Training Modules", "url": "https://training.seer.cancer.gov/anatomy/muscular/groups/", "licence": "Public domain"}, {"title": "Sports Injuries - NIAMS", "url": "https://www.niams.nih.gov/health-topics/sports-injuries", "licence": "Public domain"}, {"title": "Sprains and Strains - MedlinePlus (NLM)", "url": "https://medlineplus.gov/sprainsandstrains.html", "licence": "Public domain"}]'::jsonb,
    'draft')
on conflict (key) do update set
    kind = excluded.kind,
    fma_ids = excluded.fma_ids,
    layer = excluded.layer,
    system = excluded.system,
    display_name = excluded.display_name,
    aliases = excluded.aliases,
    summary_plain = excluded.summary_plain,
    function_plain = excluded.function_plain,
    description = excluded.description,
    location = excluded.location,
    details = excluded.details,
    clinical = excluded.clinical,
    exam_tip = excluded.exam_tip,
    sources = excluded.sources,
    updated_at = now()
where b.status = 'draft'
  and (b.kind, b.fma_ids, b.layer, b.system, b.display_name, b.aliases, b.summary_plain, b.function_plain, b.description, b.location, b.details, b.clinical, b.exam_tip, b.sources)
  is distinct from (excluded.kind, excluded.fma_ids, excluded.layer, excluded.system, excluded.display_name, excluded.aliases, excluded.summary_plain, excluded.function_plain, excluded.description, excluded.location, excluded.details, excluded.clinical, excluded.exam_tip, excluded.sources);

-- Gluteus maximus  (2 FMA ids)
insert into public.body_part_info as b (key, kind, fma_ids, layer, system, display_name, aliases, summary_plain, function_plain, description, location, details, clinical, exam_tip, sources, status)
values ('gluteus maximus',
    'part',
    array['FMA22328', 'FMA22329']::text[],
    'muscle',
    'musculoskeletal',
    'Gluteus maximus',
    '{}'::text[],
    'The gluteus maximus is the big, thick muscle of the buttock. It sits behind the hip and gives the buttock its rounded shape.',
    'It pulls the thigh backward, holds the pelvis and trunk steady when standing, and straightens the body after bending forward.',
    'The gluteus maximus is a broad, thick, four-sided muscle that forms the prominence of the buttock. Its name means the large gluteal muscle. Gray''s Anatomy notes that its great size is one of the most typical features of human muscles, linked to keeping the trunk upright. Bursae lie under its deep surface.',
    'In the gluteal region (buttock), behind the hip joint. It runs from the back of the ilium, sacrum and coccyx down and outward to the upper femur and the iliotibial band, and it covers the gluteus medius.',
    '{"origin": "Posterior gluteal line and nearby iliac crest; back of the lower sacrum and side of the coccyx; aponeurosis of the erector spinae; sacrotuberous ligament; gluteal aponeurosis over the gluteus medius.", "insertion": "Upper and larger part into the iliotibial band (iliotibial tract) of the fascia lata; deeper lower fibres into the gluteal tuberosity of the femur.", "action": "Extends the thigh at the hip; supports the pelvis and trunk on the femur, especially on one leg; strongly restores the upright posture after stooping; tightens the fascia lata; its lower part adducts and laterally rotates the thigh.", "nerve_supply": "Inferior gluteal nerve (L5, S1, S2).", "blood_supply": "Inferior and superior gluteal arteries; the first perforating branch of the deep femoral artery also sends branches."}'::jsonb,
    '[{"text": "CDC advises against using the buttock muscles for vaccine injections in infants and children because of the risk of injuring the sciatic nerve."}, {"text": "If a gluteal injection is needed, it is given above and lateral to a line from the posterior superior iliac spine to the greater trochanter, or at the ventrogluteal site."}, {"text": "Older CDC guidance (2002) reports that hepatitis B and rabies vaccines work less well when given in the buttock than in the deltoid."}]'::jsonb,
    'Gray''s Anatomy calls its large size one of the most characteristic features of human muscles, tied to the human ability to hold the trunk erect.',
    '[{"title": "Gray''s Anatomy of the Human Body, 20th ed. (1918), Muscles of the Gluteal Region and Arteries of the Lower Extremity - Internet Archive full text", "url": "https://archive.org/download/anatomyofhumanbo1918gray/anatomyofhumanbo1918gray_djvu.txt", "licence": "Public domain"}, {"title": "Muscle Groups - NCI SEER Training Modules", "url": "https://training.seer.cancer.gov/anatomy/muscular/groups/", "licence": "Public domain"}, {"title": "Pink Book Chapter 6: Vaccine Administration - CDC", "url": "https://www.cdc.gov/pinkbook/hcp/table-of-contents/chapter-6-vaccine-administration.html", "licence": "Public domain"}, {"title": "General Recommendations on Immunization (ACIP/AAFP, MMWR 2002) - CDC", "url": "https://www.cdc.gov/mmWr/preview/mmwrhtml/rr5102a1.htm", "licence": "Public domain"}]'::jsonb,
    'draft')
on conflict (key) do update set
    kind = excluded.kind,
    fma_ids = excluded.fma_ids,
    layer = excluded.layer,
    system = excluded.system,
    display_name = excluded.display_name,
    aliases = excluded.aliases,
    summary_plain = excluded.summary_plain,
    function_plain = excluded.function_plain,
    description = excluded.description,
    location = excluded.location,
    details = excluded.details,
    clinical = excluded.clinical,
    exam_tip = excluded.exam_tip,
    sources = excluded.sources,
    updated_at = now()
where b.status = 'draft'
  and (b.kind, b.fma_ids, b.layer, b.system, b.display_name, b.aliases, b.summary_plain, b.function_plain, b.description, b.location, b.details, b.clinical, b.exam_tip, b.sources)
  is distinct from (excluded.kind, excluded.fma_ids, excluded.layer, excluded.system, excluded.display_name, excluded.aliases, excluded.summary_plain, excluded.function_plain, excluded.description, excluded.location, excluded.details, excluded.clinical, excluded.exam_tip, excluded.sources);

-- Gastrocnemius  (4 FMA ids)
insert into public.body_part_info as b (key, kind, fma_ids, layer, system, display_name, aliases, summary_plain, function_plain, description, location, details, clinical, exam_tip, sources, status)
values ('gastrocnemius',
    'part',
    array['FMA45957', 'FMA45958', 'FMA45960', 'FMA45961']::text[],
    'muscle',
    'musculoskeletal',
    'Gastrocnemius',
    array['calf muscle']::text[],
    'The gastrocnemius is the muscle that makes up most of the calf, at the back of the lower leg. It has two heads that start just above the knee.',
    'It points the foot down, as when standing on tiptoe, and helps bend the knee.',
    'The gastrocnemius is the most superficial calf muscle and forms most of the calf. It arises by two heads, medial (the larger) and lateral, from the femoral condyles. Its tendon joins that of the soleus to form the calcaneal (Achilles) tendon; together the two muscles are sometimes called the triceps surae.',
    'In the back of the leg (calf), superficial to the soleus. Its two heads start on the back of the femur just above the knee, and the muscle runs down to join the calcaneal tendon, which attaches to the heel bone.',
    '{"origin": "Medial head: upper back part of the medial femoral condyle and the nearby femur. Lateral head: side of the lateral femoral condyle and the back of the femur just above it. Both arise by strong, flat tendons.", "insertion": "Its aponeurosis joins the soleus tendon to form the calcaneal (Achilles) tendon, which inserts into the middle of the back surface of the calcaneus, with a bursa between tendon and bone.", "action": "Plantar flexes the foot at the ankle (with the soleus, the chief muscles doing this) and helps flex the knee.", "nerve_supply": "Tibial nerve (S1, S2).", "blood_supply": "Sural arteries, branches of the popliteal artery that arise opposite the knee joint."}'::jsonb,
    '[{"text": "An Achilles tendon injury is a stretch, tear or irritation of the tendon joining the calf muscle to the back of the heel."}, {"text": "Achilles tendinitis is usually a chronic overuse problem, with pain and stiffness at the back of the heel, worst in the morning; serious cases can tear and may need surgery."}]'::jsonb,
    'Its tendon, the calcaneal (Achilles) tendon, is the largest tendon in the body; Gray''s Anatomy calls it the thickest and strongest.',
    '[{"title": "Gray''s Anatomy of the Human Body, 20th ed. (1918), Posterior Crural Muscles and Arteries of the Lower Extremity - Internet Archive full text", "url": "https://archive.org/download/anatomyofhumanbo1918gray/anatomyofhumanbo1918gray_djvu.txt", "licence": "Public domain"}, {"title": "Muscles of the Lower Extremity - NCI SEER Training Modules", "url": "https://training.seer.cancer.gov/anatomy/muscular/groups/lower.html", "licence": "Public domain"}, {"title": "Sports Injuries - NIAMS", "url": "https://www.niams.nih.gov/health-topics/sports-injuries", "licence": "Public domain"}]'::jsonb,
    'draft')
on conflict (key) do update set
    kind = excluded.kind,
    fma_ids = excluded.fma_ids,
    layer = excluded.layer,
    system = excluded.system,
    display_name = excluded.display_name,
    aliases = excluded.aliases,
    summary_plain = excluded.summary_plain,
    function_plain = excluded.function_plain,
    description = excluded.description,
    location = excluded.location,
    details = excluded.details,
    clinical = excluded.clinical,
    exam_tip = excluded.exam_tip,
    sources = excluded.sources,
    updated_at = now()
where b.status = 'draft'
  and (b.kind, b.fma_ids, b.layer, b.system, b.display_name, b.aliases, b.summary_plain, b.function_plain, b.description, b.location, b.details, b.clinical, b.exam_tip, b.sources)
  is distinct from (excluded.kind, excluded.fma_ids, excluded.layer, excluded.system, excluded.display_name, excluded.aliases, excluded.summary_plain, excluded.function_plain, excluded.description, excluded.location, excluded.details, excluded.clinical, excluded.exam_tip, excluded.sources);

-- Aorta  (5 FMA ids)
insert into public.body_part_info as b (key, kind, fma_ids, layer, system, display_name, aliases, summary_plain, function_plain, description, location, details, clinical, exam_tip, sources, status)
values ('group:fma_FMA3734_v',
    'group',
    array['FMA3736', 'FMA3768', 'FMA3784', 'FMA3789', 'FMA87217']::text[],
    'vessel',
    'cardiovascular',
    'Aorta',
    '{}'::text[],
    'The aorta is the body''s main artery. It leaves the heart, arches over in the chest and runs down through the chest and belly.',
    'It carries oxygen-rich blood from the heart''s left ventricle to the rest of the body through its many branches.',
    'The aorta is the large elastic artery that receives blood from the left ventricle through the aortic valve. It has three parts: the ascending aorta, the aortic arch and the descending aorta, which is divided into thoracic and abdominal parts. Every systemic artery branches from it, directly or indirectly.',
    'It rises from the left ventricle, curves backward and to the left as the arch, then descends through the chest (thoracic aorta) and into the abdomen (abdominal aorta).',
    '{"origin": "Arises from the left ventricle; the aortic valve lies between them.", "territory": "The whole systemic circulation: all systemic arteries come from it, directly or indirectly, including those to the heart wall, head and arms, the lungs'' own tissue, the abdominal and pelvic organs and the legs.", "branches": "Ascending aorta: right and left coronary arteries only. Arch: brachiocephalic, left common carotid, left subclavian. Thoracic: bronchial arteries. Abdominal: celiac, superior mesenteric, suprarenal, renal, gonadal, inferior mesenteric and lumbar arteries; then the iliac arteries."}'::jsonb,
    '[{"text": "An aortic aneurysm is a balloon-like bulge of a weakened aortic wall and usually causes no symptoms; abdominal aortic aneurysms are the most common type, thoracic ones form in the chest."}, {"text": "A ruptured aortic aneurysm or an aortic dissection (a tear in the wall) can cause sudden, life-threatening internal bleeding and is a medical emergency."}, {"text": "Risk factors for aortic aneurysm include atherosclerosis, smoking, high blood pressure, high cholesterol and a family history of aneurysms."}, {"text": "In tetralogy of Fallot the aorta is out of place (overriding aorta), so oxygen-poor blood from the right ventricle can flow into it."}, {"text": "Patent ductus arteriosus is a connection between the aorta and the pulmonary artery that does not close properly after birth."}]'::jsonb,
    'The right and left coronary arteries are the only branches of the ascending aorta.',
    '[{"title": "Circulatory Pathways - NCI SEER Training Modules", "url": "https://training.seer.cancer.gov/anatomy/cardiovascular/blood/pathways.html", "licence": "Public domain"}, {"title": "Structure of the Heart - NCI SEER Training Modules", "url": "https://training.seer.cancer.gov/anatomy/cardiovascular/heart/structure.html", "licence": "Public domain"}, {"title": "Classification & Structure of Blood Vessels - NCI SEER Training Modules", "url": "https://training.seer.cancer.gov/anatomy/cardiovascular/blood/classification.html", "licence": "Public domain"}, {"title": "Lung Anatomy - NCI SEER Training Modules", "url": "https://training.seer.cancer.gov/lung/anatomy/", "licence": "Public domain"}, {"title": "Aortic Aneurysm - MedlinePlus (NLM)", "url": "https://medlineplus.gov/aorticaneurysm.html", "licence": "Public domain"}, {"title": "How the Heart Works: Blood Flow - NHLBI", "url": "https://www.nhlbi.nih.gov/health/heart/blood-flow", "licence": "Public domain"}, {"title": "Congenital Heart Defects: Types - NHLBI", "url": "https://www.nhlbi.nih.gov/health/congenital-heart-defects/types", "licence": "Public domain"}]'::jsonb,
    'draft')
on conflict (key) do update set
    kind = excluded.kind,
    fma_ids = excluded.fma_ids,
    layer = excluded.layer,
    system = excluded.system,
    display_name = excluded.display_name,
    aliases = excluded.aliases,
    summary_plain = excluded.summary_plain,
    function_plain = excluded.function_plain,
    description = excluded.description,
    location = excluded.location,
    details = excluded.details,
    clinical = excluded.clinical,
    exam_tip = excluded.exam_tip,
    sources = excluded.sources,
    updated_at = now()
where b.status = 'draft'
  and (b.kind, b.fma_ids, b.layer, b.system, b.display_name, b.aliases, b.summary_plain, b.function_plain, b.description, b.location, b.details, b.clinical, b.exam_tip, b.sources)
  is distinct from (excluded.kind, excluded.fma_ids, excluded.layer, excluded.system, excluded.display_name, excluded.aliases, excluded.summary_plain, excluded.function_plain, excluded.description, excluded.location, excluded.details, excluded.clinical, excluded.exam_tip, excluded.sources);

-- Superior vena cava  (1 FMA ids)
insert into public.body_part_info as b (key, kind, fma_ids, layer, system, display_name, aliases, summary_plain, function_plain, description, location, details, clinical, exam_tip, sources, status)
values ('superior vena cava',
    'part',
    array['FMA4720']::text[],
    'vessel',
    'cardiovascular',
    'Superior vena cava',
    array['anterior vena cava', 'cranial vena cava']::text[],
    'The superior vena cava is a large vein in the chest. It ends in the right upper chamber of the heart.',
    'It brings blood that has given up its oxygen back to the heart from the head, neck, arms and chest.',
    'The superior vena cava is the large venous trunk that returns deoxygenated blood from the upper body to the heart. It is formed where the left and right brachiocephalic veins join, and it ends in the right atrium. Together with the inferior vena cava, it carries all the blood returning from the systemic circulation into the right atrium.',
    'In the chest, running down to end in the right atrium of the heart. Its opening into the right atrium has no valve.',
    '{"origin": "Formed by the union of the left and right brachiocephalic (innominate) veins; drains into the right atrium.", "territory": "Drains the head, neck, upper limbs (arms) and chest.", "branches": "Main tributaries: the left and right brachiocephalic veins, each formed by the internal jugular vein joining the subclavian vein."}'::jsonb,
    '[{"text": "Superior vena cava syndrome: blockage of the vessel, for example by a tumour, a blood clot, an aneurysm or pressure from outside, stops blood from the head, arms and chest reaching the right atrium."}, {"text": "In superior vena cava syndrome the face, neck and upper arms may swell and turn bluish (Pemberton''s sign)."}, {"text": "A rise in superior vena cava pressure makes the jugular vein bulge, so it is seen higher in the neck than usual (jugular venous distension)."}]'::jsonb,
    'The superior vena cava enters the right atrium through an opening that has no valve.',
    '[{"title": "superior vena cava - NCI Dictionary of Cancer Terms (glossary API)", "url": "https://webapis.cancer.gov/glossary/v1/Terms/Cancer.gov/Patient/en/superior-vena-cava", "licence": "Public domain"}, {"title": "Vena Cava, Superior - MeSH concept M0022585 (NLM)", "url": "https://id.nlm.nih.gov/mesh/M0022585.json", "licence": "Public domain"}, {"title": "Superior Vena Cava Syndrome - MeSH concept M0020822 (NLM)", "url": "https://id.nlm.nih.gov/mesh/M0020822.json", "licence": "Public domain"}, {"title": "Superior Vena Cava C12816 - NCI Thesaurus (EVS API)", "url": "https://api-evsrest.nci.nih.gov/api/v1/concept/ncit/C12816?include=definitions,synonyms", "licence": "CC BY 4.0"}, {"title": "Superior Vena Cava Opening C33702 - NCI Thesaurus (EVS API)", "url": "https://api-evsrest.nci.nih.gov/api/v1/concept/ncit/C33702?include=definitions", "licence": "CC BY 4.0"}, {"title": "Left Brachiocephalic Vein C32964 - NCI Thesaurus (EVS API)", "url": "https://api-evsrest.nci.nih.gov/api/v1/concept/ncit/C32964?include=definitions", "licence": "CC BY 4.0"}, {"title": "Internal Jugular Vein C32849 - NCI Thesaurus (EVS API)", "url": "https://api-evsrest.nci.nih.gov/api/v1/concept/ncit/C32849?include=definitions,synonyms", "licence": "CC BY 4.0"}, {"title": "Jugular Venous Distension C191482 - NCI Thesaurus (EVS API)", "url": "https://api-evsrest.nci.nih.gov/api/v1/concept/ncit/C191482?include=definitions", "licence": "CC BY 4.0"}, {"title": "Circulatory Pathways - NCI SEER Training Modules", "url": "https://training.seer.cancer.gov/anatomy/cardiovascular/blood/pathways.html", "licence": "Public domain"}]'::jsonb,
    'draft')
on conflict (key) do update set
    kind = excluded.kind,
    fma_ids = excluded.fma_ids,
    layer = excluded.layer,
    system = excluded.system,
    display_name = excluded.display_name,
    aliases = excluded.aliases,
    summary_plain = excluded.summary_plain,
    function_plain = excluded.function_plain,
    description = excluded.description,
    location = excluded.location,
    details = excluded.details,
    clinical = excluded.clinical,
    exam_tip = excluded.exam_tip,
    sources = excluded.sources,
    updated_at = now()
where b.status = 'draft'
  and (b.kind, b.fma_ids, b.layer, b.system, b.display_name, b.aliases, b.summary_plain, b.function_plain, b.description, b.location, b.details, b.clinical, b.exam_tip, b.sources)
  is distinct from (excluded.kind, excluded.fma_ids, excluded.layer, excluded.system, excluded.display_name, excluded.aliases, excluded.summary_plain, excluded.function_plain, excluded.description, excluded.location, excluded.details, excluded.clinical, excluded.exam_tip, excluded.sources);

-- Inferior vena cava  (1 FMA ids)
insert into public.body_part_info as b (key, kind, fma_ids, layer, system, display_name, aliases, summary_plain, function_plain, description, location, details, clinical, exam_tip, sources, status)
values ('inferior vena cava',
    'part',
    array['FMA10951']::text[],
    'vessel',
    'cardiovascular',
    'Inferior vena cava',
    array['posterior vena cava', 'caudal vena cava']::text[],
    'The inferior vena cava is a large vein that runs up through the belly and empties into the heart.',
    'It brings blood back to the heart from the legs and feet and from the organs of the belly and pelvis.',
    'The inferior vena cava is the large venous trunk that returns blood from the lower half of the body to the heart. It begins where the two common iliac veins join and receives veins such as the renal veins from the kidneys and the hepatic veins from the liver. Together with the superior vena cava, it drains into the right atrium.',
    'In the abdomen, starting at the right side of the fifth lumbar vertebra, where the two common iliac veins meet, and running up to empty into the right atrium of the heart.',
    '{"origin": "Formed by the union of the left and right common iliac veins near the right side of the fifth lumbar vertebra; drains into the right atrium.", "territory": "Drains the lower limbs (legs and feet) and the organs of the abdomen and pelvis.", "branches": "Main tributaries: the common iliac veins, the renal veins (from the kidneys) and the hepatic veins (from the liver)."}'::jsonb,
    '[{"text": "A vena cava filter is a device placed in the inferior vena cava to stop blood clots from the deep veins of the legs travelling on to the lungs."}]'::jsonb,
    'The inferior vena cava begins where the left and right common iliac veins join, near the right side of the fifth lumbar vertebra.',
    '[{"title": "inferior vena cava - NCI Dictionary of Cancer Terms (glossary API)", "url": "https://webapis.cancer.gov/glossary/v1/Terms/Cancer.gov/Patient/en/inferior-vena-cava", "licence": "Public domain"}, {"title": "Vena Cava, Inferior - MeSH concept M0022584 (NLM)", "url": "https://id.nlm.nih.gov/mesh/M0022584.json", "licence": "Public domain"}, {"title": "Vena Cava Filters - MeSH concept M0024920 (NLM)", "url": "https://id.nlm.nih.gov/mesh/M0024920.json", "licence": "Public domain"}, {"title": "Inferior Vena Cava C12815 - NCI Thesaurus (EVS API)", "url": "https://api-evsrest.nci.nih.gov/api/v1/concept/ncit/C12815?include=definitions,synonyms", "licence": "CC BY 4.0"}, {"title": "Common Iliac Vein C32359 - NCI Thesaurus (EVS API)", "url": "https://api-evsrest.nci.nih.gov/api/v1/concept/ncit/C32359?include=definitions", "licence": "CC BY 4.0"}, {"title": "Hepatic Vein C32736 - NCI Thesaurus (EVS API)", "url": "https://api-evsrest.nci.nih.gov/api/v1/concept/ncit/C32736?include=definitions", "licence": "CC BY 4.0"}, {"title": "Renal Vein C33462 - NCI Thesaurus (EVS API)", "url": "https://api-evsrest.nci.nih.gov/api/v1/concept/ncit/C33462?include=definitions", "licence": "CC BY 4.0"}, {"title": "Circulatory Pathways - NCI SEER Training Modules", "url": "https://training.seer.cancer.gov/anatomy/cardiovascular/blood/pathways.html", "licence": "Public domain"}]'::jsonb,
    'draft')
on conflict (key) do update set
    kind = excluded.kind,
    fma_ids = excluded.fma_ids,
    layer = excluded.layer,
    system = excluded.system,
    display_name = excluded.display_name,
    aliases = excluded.aliases,
    summary_plain = excluded.summary_plain,
    function_plain = excluded.function_plain,
    description = excluded.description,
    location = excluded.location,
    details = excluded.details,
    clinical = excluded.clinical,
    exam_tip = excluded.exam_tip,
    sources = excluded.sources,
    updated_at = now()
where b.status = 'draft'
  and (b.kind, b.fma_ids, b.layer, b.system, b.display_name, b.aliases, b.summary_plain, b.function_plain, b.description, b.location, b.details, b.clinical, b.exam_tip, b.sources)
  is distinct from (excluded.kind, excluded.fma_ids, excluded.layer, excluded.system, excluded.display_name, excluded.aliases, excluded.summary_plain, excluded.function_plain, excluded.description, excluded.location, excluded.details, excluded.clinical, excluded.exam_tip, excluded.sources);

-- Pulmonary trunk  (1 FMA ids)
insert into public.body_part_info as b (key, kind, fma_ids, layer, system, display_name, aliases, summary_plain, function_plain, description, location, details, clinical, exam_tip, sources, status)
values ('pulmonary trunk',
    'part',
    array['FMA8612']::text[],
    'vessel',
    'cardiovascular',
    'Pulmonary trunk',
    array['pulmonary artery']::text[],
    'The pulmonary trunk is the large artery that leaves the right side of the heart and carries blood to the lungs.',
    'It takes oxygen-poor blood from the heart to the lungs, where the blood picks up oxygen and gets rid of carbon dioxide.',
    'The pulmonary trunk carries oxygen-poor blood out of the right ventricle, the pump of the pulmonary circuit. The pulmonary valve sits at its base. It splits into two pulmonary arteries, one for each lung, which keep dividing until they end in capillaries around the air sacs. Unlike systemic arteries, it carries low-oxygen blood.',
    'It leaves the right ventricle at the pulmonary valve and runs toward the lungs; its branches enter each lung at the hilum on the lung''s medial surface.',
    '{"origin": "Arises from the right ventricle; the pulmonary semilunar valve lies between them.", "territory": "Carries blood to both lungs for gas exchange in the capillaries around the alveoli; the lung tissue itself is nourished by the bronchial arteries from the aorta instead.", "branches": "Divides into two pulmonary arteries, one to each lung, which branch into smaller and smaller vessels."}'::jsonb,
    '[{"text": "Pulmonary embolism is a sudden blockage of a lung artery, most often by a clot from a leg vein (deep vein thrombosis)."}, {"text": "Pulmonary hypertension is higher than normal blood pressure in the lung vessels and can lead to heart failure and arrhythmias."}, {"text": "Pulmonary valve stenosis makes the valve too narrow or stiff and limits flow into the pulmonary artery; it is one of the four defects of tetralogy of Fallot."}, {"text": "Patent ductus arteriosus is a connection between the pulmonary artery and the aorta that does not close properly after birth."}]'::jsonb,
    'Pulmonary arteries carry oxygen-poor blood from the right ventricle to the lungs, the opposite of systemic arteries.',
    '[{"title": "Structure of the Heart - NCI SEER Training Modules", "url": "https://training.seer.cancer.gov/anatomy/cardiovascular/heart/structure.html", "licence": "Public domain"}, {"title": "Circulatory Pathways - NCI SEER Training Modules", "url": "https://training.seer.cancer.gov/anatomy/cardiovascular/blood/pathways.html", "licence": "Public domain"}, {"title": "Classification & Structure of Blood Vessels - NCI SEER Training Modules", "url": "https://training.seer.cancer.gov/anatomy/cardiovascular/blood/classification.html", "licence": "Public domain"}, {"title": "Lung Anatomy - NCI SEER Training Modules", "url": "https://training.seer.cancer.gov/lung/anatomy/", "licence": "Public domain"}, {"title": "How the Heart Works: Blood Flow - NHLBI", "url": "https://www.nhlbi.nih.gov/health/heart/blood-flow", "licence": "Public domain"}, {"title": "Pulmonary Embolism - MedlinePlus (NLM)", "url": "https://medlineplus.gov/pulmonaryembolism.html", "licence": "Public domain"}, {"title": "Pulmonary Hypertension - MedlinePlus (NLM)", "url": "https://medlineplus.gov/pulmonaryhypertension.html", "licence": "Public domain"}, {"title": "Congenital Heart Defects: Types - NHLBI", "url": "https://www.nhlbi.nih.gov/health/congenital-heart-defects/types", "licence": "Public domain"}]'::jsonb,
    'draft')
on conflict (key) do update set
    kind = excluded.kind,
    fma_ids = excluded.fma_ids,
    layer = excluded.layer,
    system = excluded.system,
    display_name = excluded.display_name,
    aliases = excluded.aliases,
    summary_plain = excluded.summary_plain,
    function_plain = excluded.function_plain,
    description = excluded.description,
    location = excluded.location,
    details = excluded.details,
    clinical = excluded.clinical,
    exam_tip = excluded.exam_tip,
    sources = excluded.sources,
    updated_at = now()
where b.status = 'draft'
  and (b.kind, b.fma_ids, b.layer, b.system, b.display_name, b.aliases, b.summary_plain, b.function_plain, b.description, b.location, b.details, b.clinical, b.exam_tip, b.sources)
  is distinct from (excluded.kind, excluded.fma_ids, excluded.layer, excluded.system, excluded.display_name, excluded.aliases, excluded.summary_plain, excluded.function_plain, excluded.description, excluded.location, excluded.details, excluded.clinical, excluded.exam_tip, excluded.sources);

-- Common carotid artery  (1 FMA ids)
insert into public.body_part_info as b (key, kind, fma_ids, layer, system, display_name, aliases, summary_plain, function_plain, description, location, details, clinical, exam_tip, sources, status)
values ('common carotid artery',
    'part',
    array['FMA3939']::text[],
    'vessel',
    'cardiovascular',
    'Common carotid artery',
    '{}'::text[],
    'The common carotid arteries are two large blood vessels, one on each side of the neck, that carry blood from the heart up to the head.',
    'They bring oxygen-rich blood to the head and neck, including the brain, through their two branches.',
    'The common carotid arteries are a pair of arteries that supply oxygenated blood to the head and neck. The left one branches from the aorta (at the aortic arch); the right one arises from the brachiocephalic (innominate) artery. Each runs up the side of the neck and divides into an internal carotid artery, which supplies the brain and eyes, and an external carotid artery, which supplies the face, tongue and outer head.',
    'In the neck, one on each side, running upward until it divides at the level of the upper border of the thyroid cartilage.',
    '{"origin": "Left: from the aortic arch. Right: from the brachiocephalic (innominate) artery.", "territory": "The structures of the head and neck, including the brain, eyes, face and tongue, through its branches.", "branches": "Ends by dividing into the internal carotid artery (brain and eyes) and the external carotid artery (face, tongue and outer parts of the head)."}'::jsonb,
    '[{"text": "In carotid artery disease the carotid arteries become narrowed or blocked, usually by atherosclerosis (plaque made of fat, cholesterol, calcium and other substances)."}, {"text": "Carotid artery disease can block blood flow to the brain and cause a stroke; a piece of plaque or a clot may lodge in a smaller brain artery.", "disease_id": "ischemic_stroke"}, {"text": "Carotid disease often causes no symptoms until narrowing is severe; signs include a bruit heard with a stethoscope or a transient ischemic attack (mini-stroke)."}, {"text": "Treatment may include carotid endarterectomy (surgery to remove the plaque) or angioplasty with a stent."}]'::jsonb,
    'Each common carotid artery divides into the internal and external carotid arteries at the level of the upper border of the thyroid cartilage.',
    '[{"title": "Carotid Artery, Common - MeSH concept M0026594 (NLM)", "url": "https://id.nlm.nih.gov/mesh/M0026594.json", "licence": "Public domain"}, {"title": "Carotid artery - NCI Dictionary of Cancer Terms (glossary API)", "url": "https://webapis.cancer.gov/glossary/v1/Terms/Cancer.gov/Patient/en/carotid-artery", "licence": "Public domain"}, {"title": "Common Carotid Artery C12687 - NCI Thesaurus (EVS API)", "url": "https://api-evsrest.nci.nih.gov/api/v1/concept/ncit/C12687?include=definitions", "licence": "CC BY 4.0"}, {"title": "Circulatory Pathways - NCI SEER Training Modules", "url": "https://training.seer.cancer.gov/anatomy/cardiovascular/blood/pathways.html", "licence": "Public domain"}, {"title": "Carotid Artery Disease - MedlinePlus (NLM)", "url": "https://medlineplus.gov/carotidarterydisease.html", "licence": "Public domain"}]'::jsonb,
    'draft')
on conflict (key) do update set
    kind = excluded.kind,
    fma_ids = excluded.fma_ids,
    layer = excluded.layer,
    system = excluded.system,
    display_name = excluded.display_name,
    aliases = excluded.aliases,
    summary_plain = excluded.summary_plain,
    function_plain = excluded.function_plain,
    description = excluded.description,
    location = excluded.location,
    details = excluded.details,
    clinical = excluded.clinical,
    exam_tip = excluded.exam_tip,
    sources = excluded.sources,
    updated_at = now()
where b.status = 'draft'
  and (b.kind, b.fma_ids, b.layer, b.system, b.display_name, b.aliases, b.summary_plain, b.function_plain, b.description, b.location, b.details, b.clinical, b.exam_tip, b.sources)
  is distinct from (excluded.kind, excluded.fma_ids, excluded.layer, excluded.system, excluded.display_name, excluded.aliases, excluded.summary_plain, excluded.function_plain, excluded.description, excluded.location, excluded.details, excluded.clinical, excluded.exam_tip, excluded.sources);

-- Internal jugular vein  (2 FMA ids)
insert into public.body_part_info as b (key, kind, fma_ids, layer, system, display_name, aliases, summary_plain, function_plain, description, location, details, clinical, exam_tip, sources, status)
values ('internal jugular vein',
    'part',
    array['FMA4754', 'FMA4762']::text[],
    'vessel',
    'cardiovascular',
    'Internal jugular vein',
    '{}'::text[],
    'The internal jugular vein is a large vein in the neck. It starts at the base of the skull and runs down the neck to join another large vein.',
    'It carries blood away from the brain, face and neck back toward the heart.',
    'The internal jugular vein is one of the jugular veins, the veins of the neck that drain the brain, face and neck. It begins as a continuation of the sigmoid sinus, a venous channel of the dura mater, and leaves the skull through the jugular foramen. It then joins the subclavian vein to form the brachiocephalic vein, which leads to the superior vena cava.',
    'In the neck. It leaves the skull base through the jugular foramen, where the temporal and occipital bones meet, and ends by joining the subclavian vein.',
    '{"origin": "Continues from the sigmoid sinus of the dura mater; drains into the brachiocephalic vein (formed with the subclavian vein).", "territory": "Drains the brain, face and neck (as stated for the jugular veins)."}'::jsonb,
    '[{"text": "Jugular venous distension: when superior vena cava pressure rises, the jugular vein bulges and can be seen higher in the neck than usual."}, {"text": "Jugular venous distension is one of the signs of heart failure, along with breathlessness and fluid build-up.", "disease_id": "heart_failure"}, {"text": "Jugular venous pressure is estimated from the height of the jugular venous pulse above the right atrium, viewed with the patient lying back with the neck at 45 degrees."}]'::jsonb,
    'The internal jugular vein leaves the skull through the jugular foramen together with the glossopharyngeal, vagus and accessory nerves (cranial nerves IX, X and XI).',
    '[{"title": "Internal Jugular Vein C32849 - NCI Thesaurus (EVS API)", "url": "https://api-evsrest.nci.nih.gov/api/v1/concept/ncit/C32849?include=definitions,synonyms", "licence": "CC BY 4.0"}, {"title": "Jugular Foramen C12496 - NCI Thesaurus (EVS API)", "url": "https://api-evsrest.nci.nih.gov/api/v1/concept/ncit/C12496?include=definitions", "licence": "CC BY 4.0"}, {"title": "Jugular Veins - MeSH concept M0011872 (NLM)", "url": "https://id.nlm.nih.gov/mesh/M0011872.json", "licence": "Public domain"}, {"title": "Left Brachiocephalic Vein C32964 - NCI Thesaurus (EVS API)", "url": "https://api-evsrest.nci.nih.gov/api/v1/concept/ncit/C32964?include=definitions", "licence": "CC BY 4.0"}, {"title": "Jugular Venous Distension C191482 - NCI Thesaurus (EVS API)", "url": "https://api-evsrest.nci.nih.gov/api/v1/concept/ncit/C191482?include=definitions", "licence": "CC BY 4.0"}, {"title": "Jugular Venous Pressure C191459 - NCI Thesaurus (EVS API)", "url": "https://api-evsrest.nci.nih.gov/api/v1/concept/ncit/C191459?include=definitions", "licence": "CC BY 4.0"}, {"title": "Heart Failure C50577 - NCI Thesaurus (EVS API)", "url": "https://api-evsrest.nci.nih.gov/api/v1/concept/ncit/C50577?include=definitions", "licence": "CC BY 4.0"}]'::jsonb,
    'draft')
on conflict (key) do update set
    kind = excluded.kind,
    fma_ids = excluded.fma_ids,
    layer = excluded.layer,
    system = excluded.system,
    display_name = excluded.display_name,
    aliases = excluded.aliases,
    summary_plain = excluded.summary_plain,
    function_plain = excluded.function_plain,
    description = excluded.description,
    location = excluded.location,
    details = excluded.details,
    clinical = excluded.clinical,
    exam_tip = excluded.exam_tip,
    sources = excluded.sources,
    updated_at = now()
where b.status = 'draft'
  and (b.kind, b.fma_ids, b.layer, b.system, b.display_name, b.aliases, b.summary_plain, b.function_plain, b.description, b.location, b.details, b.clinical, b.exam_tip, b.sources)
  is distinct from (excluded.kind, excluded.fma_ids, excluded.layer, excluded.system, excluded.display_name, excluded.aliases, excluded.summary_plain, excluded.function_plain, excluded.description, excluded.location, excluded.details, excluded.clinical, excluded.exam_tip, excluded.sources);

-- Left coronary artery  (7 FMA ids)
insert into public.body_part_info as b (key, kind, fma_ids, layer, system, display_name, aliases, summary_plain, function_plain, description, location, details, clinical, exam_tip, sources, status)
values ('group:v_coronary_l',
    'group',
    array['FMA3855', 'FMA3860', 'FMA3868', 'FMA3872', 'FMA3874', 'FMA3876', 'FMA3895']::text[],
    'vessel',
    'cardiovascular',
    'Left coronary artery',
    '{}'::text[],
    'The left coronary artery is one of the two arteries that feed the heart muscle itself. It starts from the aorta just above the heart and runs over the heart''s surface.',
    'It brings oxygen-rich blood to most of the left side of the heart and to the wall between the two lower chambers.',
    'The left coronary artery is one of the two coronary arteries, which are the only branches of the ascending aorta. It supplies the left atrium, the left ventricle and the septum between the ventricles. Its two main branches are the left anterior descending artery and the circumflex artery.',
    'On the surface of the heart, starting from the ascending aorta.',
    '{"origin": "Arises from the ascending aorta.", "territory": "Left atrium, left ventricle and the interventricular septum; the left anterior descending artery supplies parts of both ventricles, and the circumflex artery part of the left ventricle.", "branches": "Left anterior descending artery; circumflex artery."}'::jsonb,
    '[{"text": "Plaque buildup (atherosclerosis) narrows the coronary arteries in coronary artery disease, the most common heart disease in the United States; reduced flow causes angina.", "disease_id": "acute_coronary_syndrome"}, {"text": "A heart attack happens when a blood clot suddenly blocks blood flow to part of the heart, permanently damaging the muscle.", "disease_id": "acute_coronary_syndrome"}, {"text": "Blocked coronary arteries can be opened with angioplasty or bypassed with coronary artery bypass grafting (CABG)."}]'::jsonb,
    'The right and left coronary arteries are the only branches of the ascending aorta.',
    '[{"title": "How the Heart Works: Blood Flow - NHLBI", "url": "https://www.nhlbi.nih.gov/health/heart/blood-flow", "licence": "Public domain"}, {"title": "Circulatory Pathways - NCI SEER Training Modules", "url": "https://training.seer.cancer.gov/anatomy/cardiovascular/blood/pathways.html", "licence": "Public domain"}, {"title": "Structure of the Heart - NCI SEER Training Modules", "url": "https://training.seer.cancer.gov/anatomy/cardiovascular/heart/structure.html", "licence": "Public domain"}, {"title": "Coronary Artery Disease - MedlinePlus (NLM)", "url": "https://medlineplus.gov/coronaryarterydisease.html", "licence": "Public domain"}]'::jsonb,
    'draft')
on conflict (key) do update set
    kind = excluded.kind,
    fma_ids = excluded.fma_ids,
    layer = excluded.layer,
    system = excluded.system,
    display_name = excluded.display_name,
    aliases = excluded.aliases,
    summary_plain = excluded.summary_plain,
    function_plain = excluded.function_plain,
    description = excluded.description,
    location = excluded.location,
    details = excluded.details,
    clinical = excluded.clinical,
    exam_tip = excluded.exam_tip,
    sources = excluded.sources,
    updated_at = now()
where b.status = 'draft'
  and (b.kind, b.fma_ids, b.layer, b.system, b.display_name, b.aliases, b.summary_plain, b.function_plain, b.description, b.location, b.details, b.clinical, b.exam_tip, b.sources)
  is distinct from (excluded.kind, excluded.fma_ids, excluded.layer, excluded.system, excluded.display_name, excluded.aliases, excluded.summary_plain, excluded.function_plain, excluded.description, excluded.location, excluded.details, excluded.clinical, excluded.exam_tip, excluded.sources);

-- Right coronary artery  (7 FMA ids)
insert into public.body_part_info as b (key, kind, fma_ids, layer, system, display_name, aliases, summary_plain, function_plain, description, location, details, clinical, exam_tip, sources, status)
values ('group:v_coronary_r',
    'group',
    array['FMA3802', 'FMA3815', 'FMA3818', 'FMA3835', 'FMA3840', 'FMA3847', 'FMA3848']::text[],
    'vessel',
    'cardiovascular',
    'Right coronary artery',
    '{}'::text[],
    'The right coronary artery is one of the two arteries that feed the heart muscle itself. It starts from the aorta just above the heart and runs over the heart''s surface.',
    'It brings oxygen-rich blood to the right upper chamber and to parts of both lower chambers, including their underside.',
    'The right coronary artery is one of the two coronary arteries, which are the only branches of the ascending aorta. It supplies the right atrium and parts of both ventricles. Its branches include the marginal arteries and the posterior descending artery, which supplies the bottom of both ventricles.',
    'On the surface of the heart, starting from the ascending aorta.',
    '{"origin": "Arises from the ascending aorta.", "territory": "Right atrium and parts of both ventricles; the marginal arteries supply the surface of the right atrium, and the posterior descending artery the bottom of both ventricles.", "branches": "Marginal arteries; posterior descending artery."}'::jsonb,
    '[{"text": "Plaque buildup (atherosclerosis) narrows the coronary arteries in coronary artery disease, the most common heart disease in the United States; reduced flow causes angina.", "disease_id": "acute_coronary_syndrome"}, {"text": "A heart attack happens when a blood clot suddenly blocks blood flow to part of the heart, permanently damaging the muscle.", "disease_id": "acute_coronary_syndrome"}, {"text": "Blocked coronary arteries can be opened with angioplasty or bypassed with coronary artery bypass grafting (CABG)."}]'::jsonb,
    'The posterior descending artery, which supplies the bottom of both ventricles, is a branch of the right coronary artery.',
    '[{"title": "How the Heart Works: Blood Flow - NHLBI", "url": "https://www.nhlbi.nih.gov/health/heart/blood-flow", "licence": "Public domain"}, {"title": "Circulatory Pathways - NCI SEER Training Modules", "url": "https://training.seer.cancer.gov/anatomy/cardiovascular/blood/pathways.html", "licence": "Public domain"}, {"title": "Structure of the Heart - NCI SEER Training Modules", "url": "https://training.seer.cancer.gov/anatomy/cardiovascular/heart/structure.html", "licence": "Public domain"}, {"title": "Coronary Artery Disease - MedlinePlus (NLM)", "url": "https://medlineplus.gov/coronaryarterydisease.html", "licence": "Public domain"}]'::jsonb,
    'draft')
on conflict (key) do update set
    kind = excluded.kind,
    fma_ids = excluded.fma_ids,
    layer = excluded.layer,
    system = excluded.system,
    display_name = excluded.display_name,
    aliases = excluded.aliases,
    summary_plain = excluded.summary_plain,
    function_plain = excluded.function_plain,
    description = excluded.description,
    location = excluded.location,
    details = excluded.details,
    clinical = excluded.clinical,
    exam_tip = excluded.exam_tip,
    sources = excluded.sources,
    updated_at = now()
where b.status = 'draft'
  and (b.kind, b.fma_ids, b.layer, b.system, b.display_name, b.aliases, b.summary_plain, b.function_plain, b.description, b.location, b.details, b.clinical, b.exam_tip, b.sources)
  is distinct from (excluded.kind, excluded.fma_ids, excluded.layer, excluded.system, excluded.display_name, excluded.aliases, excluded.summary_plain, excluded.function_plain, excluded.description, excluded.location, excluded.details, excluded.clinical, excluded.exam_tip, excluded.sources);

-- Hepatic portal vein  (1 FMA ids)
insert into public.body_part_info as b (key, kind, fma_ids, layer, system, display_name, aliases, summary_plain, function_plain, description, location, details, clinical, exam_tip, sources, status)
values ('hepatic portal vein',
    'part',
    array['FMA50735']::text[],
    'vessel',
    'cardiovascular',
    'Hepatic portal vein',
    array['portal vein']::text[],
    'The hepatic portal vein is a short, thick vein in the belly that carries blood from the gut and nearby organs into the liver.',
    'It brings nutrient-rich blood from digestion to the liver, so the liver handles it before it reaches the rest of the body.',
    'The hepatic portal vein is a short, thick vein formed by the union of the superior mesenteric vein and the splenic vein. It carries blood rich in absorbed products of digestion from the stomach, intestines, spleen, pancreas and gallbladder to the liver. The liver therefore gets blood from two sources: this vein and the common hepatic artery, which brings oxygenated blood.',
    'In the abdomen, running into the liver. At its far end it divides into the left and right portal veins.',
    '{"origin": "Formed by the union of the superior mesenteric vein and the splenic vein; drains into the liver, where it divides into the left and right portal veins.", "territory": "Drains the stomach, intestines, spleen, pancreas and gallbladder.", "branches": "Tributaries: the superior mesenteric vein and the splenic vein. Ends by dividing into the left and right portal veins."}'::jsonb,
    '[{"text": "Portal hypertension: scar tissue in a cirrhotic liver slows blood flow and raises pressure in the portal vein."}, {"text": "Portal hypertension can cause enlarged veins (varices) in the oesophagus, stomach or intestines, which may burst and bleed internally."}, {"text": "Portal hypertension can also cause fluid in the abdomen (ascites), swelling of the legs and confusion from toxins reaching the brain (hepatic encephalopathy)."}, {"text": "A blood clot can form in the portal vein (portal vein thrombosis)."}]'::jsonb,
    'The hepatic portal vein is formed by the union of the superior mesenteric vein and the splenic vein.',
    '[{"title": "Portal Vein - MeSH concept M0017339 (NLM)", "url": "https://id.nlm.nih.gov/mesh/M0017339.json", "licence": "Public domain"}, {"title": "portal vein - NCI Dictionary of Cancer Terms (glossary API)", "url": "https://webapis.cancer.gov/glossary/v1/Terms/Cancer.gov/Patient/en/portal-vein", "licence": "Public domain"}, {"title": "Portal Vein C33343 - NCI Thesaurus (EVS API)", "url": "https://api-evsrest.nci.nih.gov/api/v1/concept/ncit/C33343?include=definitions", "licence": "CC BY 4.0"}, {"title": "Portal Vein Bifurcation C132413 - NCI Thesaurus (EVS API)", "url": "https://api-evsrest.nci.nih.gov/api/v1/concept/ncit/C132413?include=definitions", "licence": "CC BY 4.0"}, {"title": "Portal Vein Thrombosis C78565 - NCI Thesaurus (EVS API)", "url": "https://api-evsrest.nci.nih.gov/api/v1/concept/ncit/C78565?include=definitions", "licence": "CC BY 4.0"}, {"title": "Accessory Organs of the Digestive System - NCI SEER Training Modules", "url": "https://training.seer.cancer.gov/anatomy/digestive/regions/accessory.html", "licence": "Public domain"}, {"title": "Definition & Facts for Cirrhosis - NIDDK", "url": "https://www.niddk.nih.gov/health-information/liver-disease/cirrhosis/definition-facts", "licence": "Public domain"}]'::jsonb,
    'draft')
on conflict (key) do update set
    kind = excluded.kind,
    fma_ids = excluded.fma_ids,
    layer = excluded.layer,
    system = excluded.system,
    display_name = excluded.display_name,
    aliases = excluded.aliases,
    summary_plain = excluded.summary_plain,
    function_plain = excluded.function_plain,
    description = excluded.description,
    location = excluded.location,
    details = excluded.details,
    clinical = excluded.clinical,
    exam_tip = excluded.exam_tip,
    sources = excluded.sources,
    updated_at = now()
where b.status = 'draft'
  and (b.kind, b.fma_ids, b.layer, b.system, b.display_name, b.aliases, b.summary_plain, b.function_plain, b.description, b.location, b.details, b.clinical, b.exam_tip, b.sources)
  is distinct from (excluded.kind, excluded.fma_ids, excluded.layer, excluded.system, excluded.display_name, excluded.aliases, excluded.summary_plain, excluded.function_plain, excluded.description, excluded.location, excluded.details, excluded.clinical, excluded.exam_tip, excluded.sources);

-- Femoral artery  (1 FMA ids)
insert into public.body_part_info as b (key, kind, fma_ids, layer, system, display_name, aliases, summary_plain, function_plain, description, location, details, clinical, exam_tip, sources, status)
values ('femoral artery',
    'part',
    array['FMA70248']::text[],
    'vessel',
    'cardiovascular',
    'Femoral artery',
    '{}'::text[],
    'The femoral artery is the main artery of the thigh. It starts in the groin and runs down toward the leg.',
    'It carries oxygen-rich blood down into the leg.',
    'The femoral artery is the main artery of the thigh and continues on from the external iliac artery. Its first part, the common femoral artery, begins at the inguinal ligament in the groin and splits into the deep and superficial femoral arteries. Through it and its branches, blood reaches the lower limb.',
    'In the groin (inguinal region) and thigh, beginning at the inguinal ligament and running down toward the lower limb.',
    '{"origin": "Continuation of the external iliac artery; the common femoral artery begins at the inguinal ligament.", "territory": "The lower limb (thigh and the leg below).", "branches": "The common femoral artery divides into the deep femoral artery and the superficial femoral artery."}'::jsonb,
    '[{"text": "Peripheral artery disease is narrowing of arteries outside the heart, mostly from atherosclerosis; in the legs it can cause pain on walking and weak or absent pulses in the legs or feet."}, {"text": "In the United States, more than 8 million people aged 40 and older have peripheral artery disease."}, {"text": "For some heart and artery tests, a catheter is passed into an artery in the groin and guided to the heart or the narrowed vessel."}]'::jsonb,
    'A delay between the right radial pulse and the femoral pulse (radial-femoral lag) suggests coarctation of the aorta.',
    '[{"title": "Femoral Artery - MeSH concept M0008311 (NLM)", "url": "https://id.nlm.nih.gov/mesh/M0008311.json", "licence": "Public domain"}, {"title": "Femoral Artery C12715 - NCI Thesaurus (EVS API)", "url": "https://api-evsrest.nci.nih.gov/api/v1/concept/ncit/C12715?include=definitions,synonyms", "licence": "CC BY 4.0"}, {"title": "Common Femoral Artery C32354 - NCI Thesaurus (EVS API)", "url": "https://api-evsrest.nci.nih.gov/api/v1/concept/ncit/C32354?include=definitions", "licence": "CC BY 4.0"}, {"title": "Radial-Femoral Lag C168415 - NCI Thesaurus (EVS API)", "url": "https://api-evsrest.nci.nih.gov/api/v1/concept/ncit/C168415?include=definitions", "licence": "CC BY 4.0"}, {"title": "Circulatory Pathways - NCI SEER Training Modules", "url": "https://training.seer.cancer.gov/anatomy/cardiovascular/blood/pathways.html", "licence": "Public domain"}, {"title": "Peripheral Arterial Disease - MedlinePlus (NLM)", "url": "https://medlineplus.gov/peripheralarterialdisease.html", "licence": "Public domain"}, {"title": "Peripheral Artery Disease - What Is PAD? - NHLBI", "url": "https://www.nhlbi.nih.gov/health/peripheral-artery-disease", "licence": "Public domain"}, {"title": "Peripheral Artery Disease - Diagnosis - NHLBI", "url": "https://www.nhlbi.nih.gov/health/peripheral-artery-disease/diagnosis", "licence": "Public domain"}, {"title": "Cardiac Catheterization - During - NHLBI", "url": "https://www.nhlbi.nih.gov/health/cardiac-catheterization/during", "licence": "Public domain"}]'::jsonb,
    'draft')
on conflict (key) do update set
    kind = excluded.kind,
    fma_ids = excluded.fma_ids,
    layer = excluded.layer,
    system = excluded.system,
    display_name = excluded.display_name,
    aliases = excluded.aliases,
    summary_plain = excluded.summary_plain,
    function_plain = excluded.function_plain,
    description = excluded.description,
    location = excluded.location,
    details = excluded.details,
    clinical = excluded.clinical,
    exam_tip = excluded.exam_tip,
    sources = excluded.sources,
    updated_at = now()
where b.status = 'draft'
  and (b.kind, b.fma_ids, b.layer, b.system, b.display_name, b.aliases, b.summary_plain, b.function_plain, b.description, b.location, b.details, b.clinical, b.exam_tip, b.sources)
  is distinct from (excluded.kind, excluded.fma_ids, excluded.layer, excluded.system, excluded.display_name, excluded.aliases, excluded.summary_plain, excluded.function_plain, excluded.description, excluded.location, excluded.details, excluded.clinical, excluded.exam_tip, excluded.sources);

-- Optic nerve  (2 FMA ids)
insert into public.body_part_info as b (key, kind, fma_ids, layer, system, display_name, aliases, summary_plain, function_plain, description, location, details, clinical, exam_tip, sources, status)
values ('optic nerve',
    'part',
    array['FMA50875', 'FMA50878']::text[],
    'nerve',
    'nervous',
    'Optic nerve',
    '{}'::text[],
    'The optic nerve is a cable of nerve fibers that runs from the back of each eye to the brain.',
    'It carries signals from the retina to the brain, which turns them into the images you see.',
    'The optic nerve is a bundle of more than a million nerve fibers. Each eye has one, linking its retina to the brain. It is one of the cranial nerves serving a special sense (vision), and those nerves carry only sensory fibers. Damage to it can cause vision loss.',
    'It runs from the retina at the back of the eye to the brain, passing through the optic foramen at the apex of the orbit together with the ophthalmic artery. Inside the skull it lies above the tentorium (supratentorial).',
    '{"origin": "The retina at the back of the eye.", "type": "sensory", "supplies": "Carries visual signals from the retina to the brain."}'::jsonb,
    '[{"text": "Glaucoma damages the optic nerve, usually through slowly rising fluid pressure in the eye; it is a leading cause of blindness in the United States."}, {"text": "Optic neuritis is inflammation of the optic nerve, often from infection or immune conditions such as multiple sclerosis."}, {"text": "Optic nerve atrophy is degeneration of the nerve from poor blood flow, disease, injury or toxins."}, {"text": "Optic nerve head drusen are deposits of protein and calcium salts that build up in the nerve over time."}]'::jsonb,
    'Each optic nerve is a bundle of more than a million nerve fibers carrying visual signals.',
    '[{"title": "Optic Nerve Disorders - MedlinePlus (NLM)", "url": "https://medlineplus.gov/opticnervedisorders.html", "licence": "Public domain"}, {"title": "How the Eyes Work - National Eye Institute", "url": "https://www.nei.nih.gov/learn-about-eye-health/healthy-vision/how-eyes-work", "licence": "Public domain"}, {"title": "Peripheral Nervous System - NCI SEER Training Modules", "url": "https://training.seer.cancer.gov/anatomy/nervous/organization/pns.html", "licence": "Public domain"}, {"title": "Gray''s Anatomy of the Human Body, 20th ed. (1918), the skull as a whole - PubAnnotation GrayAnatomy doc 46", "url": "https://pubannotation.org/docs/sourcedb/GrayAnatomy/sourceid/46", "licence": "Public domain"}, {"title": "Gray''s Anatomy of the Human Body, 20th ed. (1918), skull (interior of the base) - PubAnnotation GrayAnatomy doc 47", "url": "https://pubannotation.org/docs/sourcedb/GrayAnatomy/sourceid/47", "licence": "Public domain"}, {"title": "Tentorium - NCI SEER Training Modules", "url": "https://training.seer.cancer.gov/cns/cns-anatomy/tentorium.html", "licence": "Public domain"}, {"title": "Glaucoma - MedlinePlus (NLM)", "url": "https://medlineplus.gov/glaucoma.html", "licence": "Public domain"}]'::jsonb,
    'draft')
on conflict (key) do update set
    kind = excluded.kind,
    fma_ids = excluded.fma_ids,
    layer = excluded.layer,
    system = excluded.system,
    display_name = excluded.display_name,
    aliases = excluded.aliases,
    summary_plain = excluded.summary_plain,
    function_plain = excluded.function_plain,
    description = excluded.description,
    location = excluded.location,
    details = excluded.details,
    clinical = excluded.clinical,
    exam_tip = excluded.exam_tip,
    sources = excluded.sources,
    updated_at = now()
where b.status = 'draft'
  and (b.kind, b.fma_ids, b.layer, b.system, b.display_name, b.aliases, b.summary_plain, b.function_plain, b.description, b.location, b.details, b.clinical, b.exam_tip, b.sources)
  is distinct from (excluded.kind, excluded.fma_ids, excluded.layer, excluded.system, excluded.display_name, excluded.aliases, excluded.summary_plain, excluded.function_plain, excluded.description, excluded.location, excluded.details, excluded.clinical, excluded.exam_tip, excluded.sources);

commit;

-- After the review, to publish this batch (bumps content_version so apps re-download):
-- begin;
-- update public.body_part_info set status = 'published', updated_at = now()
--  where status <> 'published' and key in ('group:fma_FMA7088_o', 'trachea', 'group:airways', 'esophagus', 'stomach', 'group:fma_FMA7197_o', 'gallbladder', 'pancreas', 'spleen', 'group:small_intestine', 'group:large_intestine', 'appendix', 'kidney', 'urinary bladder', 'group:fma_FMA50801_o', 'cerebellum', 'pituitary gland', 'group:eye_ball', 'group:skull', 'mandible', 'group:spine', 'group:ribcage', 'clavicle', 'scapula', 'humerus', 'radius', 'ulna', 'hip bone', 'femur', 'patella', 'tibia', 'fibula', 'diaphragm', 'group:deltoid', 'biceps brachii', 'triceps brachii', 'pectoralis major', 'trapezius', 'sternocleidomastoid', 'group:quadriceps', 'group:hamstrings', 'gluteus maximus', 'gastrocnemius', 'group:fma_FMA3734_v', 'superior vena cava', 'inferior vena cava', 'pulmonary trunk', 'common carotid artery', 'internal jugular vein', 'group:v_coronary_l', 'group:v_coronary_r', 'hepatic portal vein', 'femoral artery', 'optic nerve');
-- update public.content_version set version = version + 1, updated_at = now() where id = 1;
-- commit;
