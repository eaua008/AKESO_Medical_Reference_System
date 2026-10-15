from refs_auto import R
SYMPTOMS = {
"sym_palpitations": dict(
  desc_add="Most are caused by harmless extra beats (premature atrial or ventricular contractions); others include supraventricular tachycardia, atrial fibrillation or flutter, ventricular tachycardia and non-cardiac triggers such as thyrotoxicosis, anemia, caffeine and low potassium. An ECG recorded during symptoms is the key test.",
  tags=["ECG"],
  causes=["Harmless extra beats (premature contractions)","Supraventricular tachycardia","Ventricular tachycardia","Low potassium"],
  red_flags=["Heart rate over 120 or under 45 at rest","Palpitations during exercise, or a family history of sudden death"],
  refs=R("sym_palpitations"), links=[]),
"sym_erythema_marginatum": dict(
  desc_add="The rash is flat or slightly raised, painless and leaves no scar, sometimes lasting less than a day, and is seen in fewer than 6% of children with acute rheumatic fever. It is one of the five major Jones criteria: diagnosis needs two major, or one major and two minor criteria, plus evidence of recent group A streptococcal infection.",
  tags=["Jones criteria"],
  causes=[], red_flags=[],
  refs=R("sym_erythema_marginatum"), links=[]),
"sym_pleuritic_chest_pain": dict(
  desc_add="Pulmonary embolism comes with breathlessness, fast heart rate and sometimes coughing blood; pneumothorax with reduced breath sounds on one side; pericarditis with pain worse lying flat and better leaning forward and a friction rub. Pain that worsens with breathing or pressing on the chest does not by itself prove a chest-wall cause.",
  tags=["pleurisy"],
  causes=[],
  red_flags=["Pain worse lying flat and better leaning forward (possible pericarditis)"],
  refs=R("sym_pleuritic_chest_pain"), links=[]),
"sym_productive_cough": dict(
  desc_add="Chronic bronchitis is defined as a productive cough for 3 months a year for 2 years in a row, usually in smokers. The color or thickness of sputum does not reliably tell bacterial from viral infection.",
  tags=["chronic bronchitis"],
  causes=["Heart failure (pink frothy sputum)"],
  red_flags=["Known HIV infection or contact with someone with TB"],
  refs=R("sym_productive_cough"), links=[("heart_failure",2,False,0.3)]),
"sym_watery_diarrhea": dict(
  desc_add="Cholera diarrhea starts suddenly and is painless, often with vomiting, and the white stool contains no fecal material. Without treatment it causes low blood potassium, acidosis and circulatory collapse with a death rate above 50%, falling to about 1% with prompt rehydration.",
  tags=["oral rehydration"],
  causes=[],
  red_flags=["Several cases in a household or community, especially after flooding or water contamination"],
  refs=R("sym_watery_diarrhea"), links=[("acute_gastroenteritis",5,False,0.6)]),
"sym_periorbital_edema": dict(
  desc_add="Post-infectious glomerulonephritis typically begins 6 to 21 days after a throat or skin infection, with edema, blood and protein in the urine, reduced urine output and high blood pressure; complement C3 is low and usually returns to normal within 6 to 8 weeks. Angioedema causes sudden, uneven facial or lip swelling that can involve the airway.",
  tags=["nephritic"],
  causes=[],
  red_flags=["Swelling 1 to 3 weeks after a sore throat or skin infection, with dark urine"],
  refs=R("sym_periorbital_edema"), links=[("chronic_kidney_disease",2,False,0.4)]),
"sym_nonblanching_rash": dict(
  desc_add="In meningococcal disease the rash appears soon after onset, mainly on the trunk and legs; in fulminant cases the spots merge into bruises and dark patches of dead skin, with shock and DIC. Antibiotics (a third-generation cephalosporin) are started immediately, before tests come back.",
  tags=["purpura"],
  causes=[],
  red_flags=["Spots merging into large bruises or dark patches"],
  refs=R("sym_nonblanching_rash"), links=[("dengue",4,False,0.5)]),
"sym_conjunctivitis": dict(
  desc_add="Most red eyes are infectious or allergic conjunctivitis, which causes no real pain, no light sensitivity and no corneal staining; viral and bacterial conjunctivitis cannot be told apart reliably on clinical grounds.",
  tags=["red eye"],
  causes=[],
  red_flags=["Shingles rash on the forehead or nose tip with a red eye"],
  refs=R("sym_conjunctivitis"), links=[]),
"sym_retroorbital_pain": dict(
  desc_add="In dengue it starts abruptly with fever, headache, lower back pain and prostration after a 3 to 15 day incubation; warning signs appear around days 4 to 7. Deep aching or throbbing eye pain in someone without fever suggests serious eye disease such as glaucoma, uveitis, scleritis or orbital cellulitis.",
  tags=["dengue warning signs"],
  causes=["Glaucoma","Scleritis or uveitis","Chikungunya"],
  red_flags=["Halos around lights with vomiting (possible acute glaucoma)"],
  refs=R("sym_retroorbital_pain"), links=[("migraine",3,False,0.4),("chikungunya",2,False,0.3)]),
"sym_rlq_pain": dict(
  desc_add="Classic signs include tenderness at McBurney point with rebound, and the Rovsing, psoas and obturator signs, but more than half of patients present atypically, especially older adults and pregnant women. Classic cases are diagnosed clinically, while CT or ultrasound helps when the picture is unclear.",
  tags=["McBurney point"],
  causes=["Typhoid fever (inflamed or perforated ileum)"],
  red_flags=["Abdominal pain in a pregnant woman or older adult (appendicitis is often atypical)"],
  refs=R("sym_rlq_pain"), links=[("typhoid_fever",2,False,0.4)]),
}
