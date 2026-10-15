from refs import *
# Session 1 of the symptom review. Nothing is removed: every existing cause,
# red flag, reference and disease link stays; text below is ADDED.
# links: (disease_id, typical_intensity, is_primary, weight_multiplier)
SYMPTOMS = {
"sym_abdominal_pain": dict(
  desc_add="Visceral pain is dull and poorly localised (epigastric for the stomach and duodenum, periumbilical for the small bowel and appendix, suprapubic for the colon), whereas pain from an inflamed parietal peritoneum is sharp and well localised; appendicitis classically starts periumbilically and migrates to the right lower quadrant. Causes outside the abdomen, such as myocardial infarction, lower-lobe pneumonia and diabetic ketoacidosis, must not be missed.",
  tags=["acute abdomen"],
  causes=["Intestinal obstruction","Acute pancreatitis","Ectopic pregnancy and other gynecologic causes (ovarian torsion, pelvic inflammatory disease)","Mesenteric ischemia or abdominal aortic aneurysm (older adults)","Acute hepatitis","Causes outside the abdomen: myocardial infarction, lower-lobe pneumonia, diabetic ketoacidosis"],
  red_flags=["Pain out of proportion to examination findings in an older adult (possible mesenteric ischemia)","Missed period or positive pregnancy test with pain, bleeding or fainting (possible ectopic pregnancy)"],
  refs=[STATPEARLS_ACUTE_ABDOMEN],
  links=[("hepatitis_a",5,False,0.6),("urinary_tract_infection",4,False,0.5)]),
"sym_abdominal_swelling": dict(
  desc_add="The classic causes of a swollen abdomen are remembered as fluid, flatus, fat, fetus and feces. When ascites is tapped, a serum-ascites albumin gradient (SAAG) of 1.1 g/dL or more points to portal hypertension (cirrhosis, heart failure), while a lower gradient suggests peritoneal causes such as tuberculosis or malignancy.",
  tags=["paracentesis"],
  causes=["Peritoneal tuberculosis","Constipation and fecal loading","Pancreatic ascites after pancreatitis"],
  red_flags=["Rapid increase in abdominal girth or new ascites in a patient with known liver disease"],
  refs=[STATPEARLS_ASCITES],
  links=[("heart_failure",3,False,0.5)]),
"sym_regurgitation": dict(
  desc_add="Unlike vomiting, it comes without nausea or forceful abdominal contraction. Regurgitation responds less well to acid-suppressing medicines than heartburn does, so persistent regurgitation on a proton pump inhibitor is a reason for further testing. In infants, effortless spitting up after feeds is common and usually physiological.",
  tags=["infant reflux"],
  causes=["Physiological reflux in infants","Esophageal stricture or Zenker's diverticulum (undigested food, bad breath)"],
  red_flags=["Anemia or persistent vomiting","Poor weight gain, forceful vomiting or feeding refusal in an infant"],
  refs=[ACG_GERD],
  links=[]),
"sym_agitation": dict(
  desc_add="Delirium is suggested when agitation begins suddenly, fluctuates through the day and comes with poor attention; its quiet, withdrawn (hypoactive) form is easily missed. In furious rabies, episodes of agitation, hallucinations and hydrophobia alternate with lucid intervals.",
  tags=["agitation"],
  causes=["Low blood sugar (hypoglycemia)","Head injury or stroke","Bacterial meningitis","Liver failure (hepatic encephalopathy)","Urinary retention, constipation or untreated pain in older adults"],
  red_flags=["Sudden onset in an older adult (possible delirium)","Headache, neck stiffness and fever (possible meningitis)"],
  refs=[MERCK_DELIRIUM],
  links=[("bacterial_meningitis",4,False,0.6),("typhoid_fever",2,False,0.4)]),
"sym_melena": dict(
  desc_add="About 100 to 200 mL of blood in the upper gastrointestinal tract is needed to turn the stool black and tarry, and melena can continue for several days after the bleeding has stopped. Patients are risk-stratified early (for example with the Glasgow-Blatchford score) to decide on admission and endoscopy.",
  tags=["GI bleeding"],
  causes=["Gastrointestinal bleeding in severe dengue","Intestinal bleeding in typhoid fever (usually in the third week)","Bleeding from the small bowel or right colon (less common)"],
  red_flags=["Jaundice, ascites or known liver disease (possible variceal bleeding)","Black stools during dengue, especially around the time the fever settles"],
  refs=[MERCK_GIB, ACG_UGIB],
  links=[("dengue",3,False,0.6),("typhoid_fever",2,False,0.5),("schistosomiasis",2,False,0.5),("hepatitis_b",2,False,0.4)]),
"sym_vesicular_rash": dict(
  desc_add="In unvaccinated people, varicella lesions progress quickly from macules to papules to vesicles before crusting; breakthrough varicella after vaccination is milder, usually with fewer than 50 lesions that are mostly papules. In scabies, small vesicles may appear at the ends of burrows, especially on the hands and wrists.",
  tags=["herpesvirus"],
  causes=["Scabies (vesicles at the ends of burrows)","Insect bites (papular urticaria)"],
  red_flags=["Vesicles on the tip of the nose or around the eye (possible ophthalmic zoster)"],
  refs=[CDC_VARICELLA],
  links=[]),
"sym_bloody_stool": dict(
  desc_add="Streaks of bright blood on the toilet paper or on the surface of formed stool point to an anorectal source, whereas blood mixed into the stool or maroon stools suggest a source higher in the colon. In the tropics, bloody diarrhea (dysentery) is most often due to Shigella or Entamoeba histolytica, and intestinal bleeding is also a complication of typhoid fever and severe dengue.",
  tags=["dysentery"],
  causes=["Typhoid fever (intestinal hemorrhage)","Severe dengue with bleeding","Meckel's diverticulum (children)","Intussusception in infants (red currant jelly stools)"],
  red_flags=["Bloody diarrhea in a child who then passes little urine or becomes pale (possible hemolytic uremic syndrome)","Bleeding during dengue or with a low platelet count"],
  refs=[ACG_LGIB, MERCK_GIB],
  links=[("acute_gastroenteritis",4,False,0.6),("typhoid_fever",2,False,0.5),("dengue",2,False,0.5)]),
"sym_hematuria": dict(
  desc_add="Red or brown urine is not always blood: beets, rifampicin, myoglobin and free hemoglobin can look the same, so a dipstick and urine microscopy are needed. Microscopic hematuria is 3 or more red blood cells per high-power field on a properly collected sample; dysmorphic red cells, red cell casts and protein in the urine favor a glomerular source.",
  tags=["urinalysis"],
  causes=["Leptospirosis (kidney involvement)","Dengue with bleeding","Enlarged prostate","Polycystic kidney disease","Sickle cell disease or trait","Injury to the kidney or urinary tract","Muscle breakdown or hemolysis (dipstick positive without red cells)"],
  red_flags=["Passing blood clots or being unable to pass urine","Blood in the urine after an injury"],
  refs=[AUA_MH],
  links=[("urinary_tract_infection",3,False,0.6),("leptospirosis",2,False,0.5),("dengue",2,False,0.4)]),
"sym_blurred_vision": dict(
  desc_add="Asking whether it came on suddenly or gradually, in one eye or both, with or without pain, and whether it improves with blinking or looking through a pinhole separates refractive and surface problems from retinal, optic nerve and brain causes. Sudden loss of vision is itself a red flag, because most causes are serious.",
  tags=["ophthalmology"],
  causes=["Dry eye and conjunctivitis","Glaucoma, including acute angle-closure","Retinal vein or artery occlusion","Optic neuritis","Thyroid eye disease","Medication effects (e.g., anticholinergic drugs)"],
  red_flags=["Halos around lights with a red, painful eye, headache and vomiting (possible acute angle-closure glaucoma)","New floaters, flashes of light or a curtain over vision (possible retinal detachment)"],
  refs=[MERCK_VISION],
  links=[("graves_disease",3,False,0.5)]),
"sym_orthopnea": dict(
  desc_add="Breathlessness that wakes the patient one to two hours after falling asleep and is relieved by sitting up (paroxysmal nocturnal dyspnea) carries the same meaning. Orthopnea also occurs with pericardial effusion and with weakness of both diaphragms, where breathing worsens immediately on lying flat.",
  tags=["paroxysmal nocturnal dyspnea"],
  causes=["Pericardial effusion or tamponade","Fluid overload in kidney disease or acute glomerulonephritis","Rheumatic heart disease (mitral valve damage)","Obesity"],
  red_flags=["Rapid weight gain with worsening leg or abdominal swelling"],
  refs=[MERCK_DYSPNEA, AHA_HF],
  links=[("rheumatic_fever",3,False,0.6),("post_strep_glomerulonephritis",3,False,0.6),("copd",2,False,0.5),("chronic_kidney_disease",2,False,0.4)]),
}
