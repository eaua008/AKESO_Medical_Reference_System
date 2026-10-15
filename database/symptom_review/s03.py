from refs_auto import R
SYMPTOMS = {
"sym_hemoptysis": dict(
  desc_add="In adults the commonest causes are bronchitis, bronchiectasis, necrotizing pneumonia, tuberculosis and COPD, with lung cancer important in heavy smokers; in children, lower respiratory infection and inhaled foreign bodies predominate. In up to half of patients no cause is found, and most of these settle within 6 months.",
  tags=["bronchiectasis"],
  causes=["COPD flare","Necrotizing pneumonia or lung abscess","Inhaled foreign body (children)","Mitral stenosis"],
  red_flags=["Any hemoptysis in a heavy smoker","Absent breath sounds on one side or breathlessness at rest"],
  refs=R("sym_hemoptysis"), links=[("community_acquired_pneumonia",4,False,0.5),("copd",2,False,0.4)]),
"sym_pica": dict(
  desc_add="It is diagnosed when the eating of non-food material lasts at least a month and is not normal for the person's age or culture (it is not diagnosed under age 2). Clay can bind iron and zinc and worsen the deficiency, and pica often coexists with autism or intellectual disability.",
  tags=["geophagia","pagophagia"],
  causes=["Intellectual disability"],
  red_flags=["Swallowing hair, sharp objects or other hard items"],
  refs=R("sym_pica"), links=[]),
"sym_dark_urine": dict(
  desc_add="Conjugated bilirubin can darken the urine before jaundice is visible, so dark urine is an early sign of hepatitis or bile duct blockage; unconjugated bilirubin (as in hemolysis) does not pass into urine. Several drugs, including rifampicin, phenazopyridine, levodopa, methyldopa and senna, change urine color.",
  tags=["bilirubinuria"],
  causes=["Bile duct blockage (gallstones, tumor)","Leptospirosis (jaundice and kidney involvement)","Specific drugs: rifampicin, phenazopyridine, levodopa, methyldopa, senna"],
  red_flags=["Abdominal pain with fever and jaundice (possible cholangitis)","Bruising, small red spots or bleeding"],
  refs=R("sym_dark_urine"), links=[("leptospirosis",3,False,0.5)]),
"sym_decreased_urine": dict(
  desc_add="Some references use under 500 mL in 24 hours for adults, and under 1 mL/kg/h in newborns. A palpable bladder suggests outlet obstruction, a sudden drop in a catheterised patient with normal blood pressure suggests a blocked catheter, and dark brown urine suggests myoglobin from muscle breakdown.",
  tags=["oliguria"],
  causes=["Kidney stones or enlarged prostate","Muscle breakdown (rhabdomyolysis)","Severe dengue with plasma leakage"],
  red_flags=["Full, palpable bladder with inability to pass urine","Dark brown urine with muscle pain (possible rhabdomyolysis)"],
  refs=R("sym_decreased_urine"), links=[("dengue",3,False,0.5),("heart_failure",2,False,0.4)]),
"sym_diarrhea": dict(
  desc_add="It arises from too much osmotic load, increased secretion or reduced absorption, or fast transit, and infection is the commonest cause of acute secretory diarrhea. Diarrhea that wakes the patient at night, comes with weight loss or lasts weeks points to an organic cause rather than irritable bowel syndrome.",
  tags=["malabsorption"],
  causes=["Celiac disease and lactose intolerance","Overactive thyroid","Laxative misuse","Clostridioides difficile after antibiotics"],
  red_flags=["Diarrhea that wakes the patient at night, or with weight loss","Recent antibiotics or hospital stay (possible C. difficile)"],
  refs=R("sym_diarrhea"), links=[]),
"sym_dysphagia": dict(
  desc_add="Oropharyngeal dysphagia usually comes from nerve or muscle disease such as stroke, Parkinson disease or myasthenia gravis; esophageal dysphagia comes from motility disorders or mechanical narrowing. Upper endoscopy is the usual first test, with biopsies for eosinophilic esophagitis if no structural cause is seen.",
  tags=["oropharyngeal"],
  causes=["Parkinson disease or myasthenia gravis","Rabies (painful throat spasms)"],
  red_flags=["Repeated chest infections from aspiration"],
  refs=R("sym_dysphagia"), links=[("ischemic_stroke",4,False,0.6),("rabies",3,False,0.5)]),
"sym_dizziness": dict(
  desc_add="Common inner-ear causes are benign positional vertigo, Meniere disease and vestibular neuritis or labyrinthitis; the commonest central cause is vestibular migraine, followed by drug effects, especially blood pressure medicines. Ringing, fullness or hearing loss in the ear suggests an inner-ear cause, whereas nystagmus that is not suppressed by fixing the gaze suggests a central cause.",
  tags=["vertigo"],
  causes=["Meniere disease","Vestibular migraine","Labyrinthitis","Severe dengue with low blood pressure"],
  red_flags=["Unsteady walking or inability to stand","Constant severe vertigo lasting more than an hour"],
  refs=R("sym_dizziness"), links=[("dengue",2,False,0.3)]),
"sym_epigastric_pain": dict(
  desc_add="Medicines such as NSAIDs, opioids and iron, delayed stomach emptying and celiac disease can also cause it, and when all tests are normal the diagnosis is functional dyspepsia. If ischemia is possible, cardiac causes are checked first; endoscopy is advised for new symptoms after about age 60.",
  tags=["dyspepsia"],
  causes=["Medicines (NSAIDs, opioids, iron)","Stomach or esophageal cancer","Myocardial ischemia","Early appendicitis"],
  red_flags=["New symptoms after age 60","Symptoms not improving on acid-suppressing medicine"],
  refs=R("sym_epigastric_pain"), links=[("acute_appendicitis",3,False,0.4)]),
"sym_hypersalivation": dict(
  desc_add="In children, drooling without a barking cough strongly suggests epiglottitis rather than croup, and drooling with stridor means the airway may need urgent securing; the child should not be upset or examined in the throat until then. Excess saliva with tears, sweating, small pupils and muscle twitching suggests organophosphate poisoning.",
  tags=["epiglottitis","poisoning"],
  causes=["Epiglottitis"],
  red_flags=["Small pupils, sweating, vomiting and muscle twitching (possible organophosphate poisoning)"],
  refs=R("sym_hypersalivation"), links=[("hfmd",3,False,0.5)]),
"sym_polydipsia": dict(
  desc_add="Diabetes mellitus is the commonest cause of thirst with heavy urination; others are diuretics, diabetes insipidus and primary polydipsia. People with primary polydipsia may drink up to 6 L a day and usually do not wake at night to pass urine; drinking that much can cause dangerously low sodium.",
  tags=["diabetes insipidus"],
  causes=["Nephrogenic diabetes insipidus (vasopressin resistance)"],
  red_flags=["Headache, vomiting or confusion after drinking very large amounts (possible low sodium)"],
  refs=R("sym_polydipsia"), links=[]),
}
