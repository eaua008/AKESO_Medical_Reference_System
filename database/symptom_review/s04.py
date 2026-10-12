from refs_auto import R
SYMPTOMS = {
"sym_polyuria": dict(
  desc_add="Some references use more than 3 L a day. Uncontrolled diabetes and diuretics are the commonest causes, followed by primary polydipsia and diabetes insipidus; a high blood sodium suggests diabetes insipidus, while a low sodium suggests drinking too much water.",
  tags=["diabetes insipidus"],
  causes=["Primary polydipsia","Lithium and other drugs that block vasopressin"],
  red_flags=["Onset in early childhood or a sudden, abrupt start","Night sweats, cough or weight loss"],
  refs=R("sym_polyuria"), links=[("chronic_kidney_disease",3,False,0.5)]),
"sym_facial_droop": dict(
  desc_add="Peripheral facial palsy has many causes besides Bell's palsy (usually herpes simplex): herpes zoster of the ear, Lyme disease, sarcoidosis, diabetes, skull fractures and tumors near the ear. MRI is needed when there are other neurological signs or the weakness comes on gradually.",
  tags=["Bell palsy"],
  causes=["Herpes zoster of the ear (Ramsay Hunt syndrome)","Diabetes","Sarcoidosis","Skull base fracture"],
  red_flags=["Weakness on both sides of the face","Weakness that develops slowly over weeks (possible tumor)"],
  refs=R("sym_facial_droop"), links=[]),
"sym_fatigue": dict(
  desc_add="The likely causes change with duration: under a month, mostly medicines, anemia, stress or depression; one to six months, diabetes, hypothyroidism, sleep apnea or cancer; beyond six months, chronic fatigue syndrome, post-viral or psychiatric causes. Fatigue that worsens with activity and improves with rest suggests a physical cause.",
  tags=["chronic fatigue"],
  causes=["Medicines","Obstructive sleep apnea","Cancer","Chronic fatigue syndrome (ME/CFS) and post-viral fatigue"],
  red_flags=["Swollen lymph nodes in several areas, or fever with night sweats","New headache or vision problems in an older adult (possible giant cell arteritis)"],
  refs=R("sym_fatigue"), links=[]),
"sym_hydrophobia": dict(
  desc_add="About 80% of rabies cases are furious, with agitation, hallucinations and insomnia; the remaining 20% are paralytic, with ascending paralysis and no hydrophobia. The incubation period averages 1 to 2 months but can exceed a year, death usually follows within days of symptom onset, and prompt post-exposure prophylaxis almost always prevents the disease.",
  tags=["post-exposure prophylaxis"],
  causes=[],
  red_flags=["Pain, itching or tingling at the site of an old bite"],
  refs=R("sym_hydrophobia"), links=[]),
"sym_fever": dict(
  desc_add="An oral temperature of 37.8 °C or more after early morning, or 37.2 °C or more in the early morning, is raised; fever differs from hyperthermia (such as heat stroke), where the set point is normal. Older adults may have little or no fever despite a serious infection.",
  tags=["hyperthermia"],
  causes=["Abscess or other hidden infection","Heat stroke (hyperthermia, not a true fever)"],
  red_flags=["Temperature above 40 °C or below 35 °C","Recent travel or a weakened immune system"],
  refs=R("sym_fever"), links=[]),
"sym_flank_pain": dict(
  desc_add="Kidney stone colic is excruciating, comes in waves of 20 to 60 minutes with nausea, and makes the patient writhe or pace, unlike peritonitis where the patient lies still. Pain spreading across the abdomen suggests a stone high in the ureter, and pain spreading to the groin or genitals suggests one lower down.",
  tags=["renal colic"],
  causes=["Aortic dissection or aneurysm (older patients)"],
  red_flags=["Fever or cloudy urine with a blocked kidney (needs urgent drainage)"],
  refs=R("sym_flank_pain"), links=[]),
"sym_foamy_urine": dict(
  desc_add="Glomerular disease is the commonest cause of heavy proteinuria, including diabetic nephropathy, membranous nephropathy and focal segmental glomerulosclerosis; nephrotic-range proteinuria is more than 3.5 g a day. Persistent proteinuria on a dipstick should be measured (urine protein-to-creatinine ratio) and investigated.",
  tags=["nephrotic syndrome"],
  causes=["Membranous nephropathy and focal segmental glomerulosclerosis"],
  red_flags=["Persistent foamy urine in someone with diabetes or high blood pressure"],
  refs=R("sym_foamy_urine"), links=[("type2_diabetes",2,False,0.5),("hypertension",2,False,0.4)]),
"sym_headache": dict(
  desc_add="A new headache after age 50 is treated as secondary until proven otherwise. A sudden thunderclap headache needs urgent brain imaging and, if imaging is normal, a lumbar puncture to look for bleeding.",
  tags=["thunderclap"],
  causes=["Cluster headache","Giant cell arteritis (older adults)","Medication-overuse headache","Carbon monoxide poisoning"],
  red_flags=["Jaw pain on chewing, scalp tenderness or vision changes in someone over 50","Headache in a person with cancer or a weakened immune system"],
  refs=R("sym_headache"), links=[]),
"sym_heartburn": dict(
  desc_add="Heartburn, with or without regurgitation, is the main symptom of GERD in adolescents and adults. Long-standing reflux can lead to esophagitis, stricture, Barrett esophagus and adenocarcinoma, and reflux into the airway can cause chronic cough, hoarseness or wheeze.",
  tags=["Barrett esophagus"],
  causes=["Eosinophilic esophagitis"],
  red_flags=["No improvement after a course of acid-suppressing medicine","Hoarseness, chronic cough or wheeze"],
  refs=R("sym_heartburn"), links=[]),
"sym_heat_intolerance": dict(
  desc_add="It reflects increased sensitivity to adrenaline and comes with warm moist skin, tremor and a fast heart rate. Eye changes (bulging eyes) and shin skin thickening point specifically to Graves disease; older adults may have apathetic hyperthyroidism with low mood, weight loss and atrial fibrillation rather than heat intolerance.",
  tags=["hyperthyroidism"],
  causes=["Taking too much thyroid hormone medicine"],
  red_flags=["Irregular heartbeat (possible atrial fibrillation)"],
  refs=R("sym_heat_intolerance"), links=[]),
}
