from refs_auto import R
SYMPTOMS = {
"sym_ruq_pain": dict(
  desc_add="Acute cholecystitis feels like biliary colic but is more severe and lasts over 6 hours, with a positive Murphy sign and guarding; ultrasound is the best first test. In dengue, abdominal pain and an enlarging liver are warning signs of severe disease.",
  tags=["Murphy sign"],
  causes=["Right kidney stone or kidney infection","Dengue (enlarged, tender liver)"],
  red_flags=["Pain lasting more than 6 hours with fever (possible acute cholecystitis)"],
  refs=R("sym_ruq_pain"), links=[("dengue",3,False,0.4),("heart_failure",2,False,0.3)]),
"sym_rhinorrhea": dict(
  desc_add="Rhinoviruses cause about half of colds; symptoms start 1 to 3 days after exposure and usually clear within about 10 days. Thick, colored mucus does not by itself mean a bacterial infection.",
  tags=["common cold"],
  causes=[],
  red_flags=["Symptoms lasting more than 10 days, or worsening after first improving (possible bacterial sinusitis)"],
  refs=R("sym_rhinorrhea"), links=[]),
"sym_seizures": dict(
  desc_add="Status epilepticus is a convulsion lasting more than 5 minutes or repeated seizures without recovery in between, and needs an IV benzodiazepine promptly. Tongue biting, incontinence and prolonged confusion afterwards favour a seizure over a faint.",
  tags=["status epilepticus"],
  causes=["Brain tumor","Drug toxicity","Cerebral malaria"],
  red_flags=["Seizure in someone with cancer or a weakened immune system"],
  refs=R("sym_seizures"), links=[("malaria",3,False,0.4),("rabies",2,False,0.3),("ischemic_stroke",2,False,0.3)]),
"sym_photophobia": dict(
  desc_add="In true photophobia from eye disease, light shone into the healthy eye causes pain in the affected eye, as with corneal injury or uveitis. In migraine it comes with nausea and sensitivity to sound and smells, and patients prefer a dark, quiet room.",
  tags=["uveitis"],
  causes=[],
  red_flags=["Halos around lights or vomiting with eye pain (possible acute glaucoma)"],
  refs=R("sym_photophobia"), links=[("measles",3,False,0.4)]),
"sym_tremor": dict(
  desc_add="A tremor while reaching for a target (intention tremor) suggests cerebellar disease. Hyperthyroidism and drugs such as lithium, SSRIs, valproate and theophylline cause or worsen tremor.",
  tags=["essential tremor"],
  causes=["Cerebellar disease (tremor on reaching for a target)","SSRIs and theophylline"],
  red_flags=["Tremor starting before age 50 with no family history"],
  refs=R("sym_tremor"), links=[]),
"sym_dyspnea": dict(
  desc_add="Wheeze points to asthma or COPD, stridor to upper airway obstruction, and crackles to heart failure, pneumonia or interstitial lung disease. A normal oxygen saturation does not exclude pulmonary embolism.",
  tags=["wheeze"],
  causes=["Pneumothorax","Interstitial lung disease","Physical deconditioning"],
  red_flags=["Using the neck and shoulder muscles to breathe"],
  refs=R("sym_dyspnea"), links=[]),
"sym_dehydration": dict(
  desc_add="Mild volume loss (under 5%) gives thirst and reduced urine; moderate loss (5 to 10%) adds dizziness on standing; severe loss (over 10%) leads to shock with low blood pressure, confusion and slow capillary refill. Skin turgor and a dry mouth are unreliable signs in older adults.",
  tags=["volume depletion"],
  causes=["Burns or bleeding"],
  red_flags=["Infant or older adult with ongoing diarrhea or vomiting"],
  refs=R("sym_dehydration"), links=[("acute_gastroenteritis",5,False,0.6),("type2_diabetes",2,False,0.3)]),
"sym_rash": dict(
  desc_add="Lesions are described by their size (under or over 10 mm) and type, and their arrangement gives clues: target lesions suggest erythema multiforme, grouped vesicles herpes simplex, and a band on one side zoster. Redness can be subtle on darker skin.",
  tags=["morphology"],
  causes=["Erythema multiforme"],
  red_flags=["A black, scab-like sore (eschar)"],
  refs=R("sym_rash"), links=[]),
"sym_speech_difficulty": dict(
  desc_add="In Broca (expressive) aphasia speech is halting but understanding is preserved; in Wernicke (receptive) aphasia speech flows but makes little sense and understanding is poor. Assessment covers spontaneous speech, naming, repetition and comprehension, followed by brain imaging.",
  tags=["aphasia","dysarthria"],
  causes=["Encephalitis","Brain tumor or dementia (gradual onset)"],
  red_flags=["Speech that gets steadily worse over weeks"],
  refs=R("sym_speech_difficulty"), links=[]),
"sym_sore_throat": dict(
  desc_add="Group A streptococcus causes about 10 to 25% of cases in adults. Testing is reasonable when two or more Centor criteria are present (tonsil exudate, tender neck nodes, fever, no cough), and severe pain with a normal-looking throat suggests epiglottitis.",
  tags=["Centor criteria"],
  causes=["Epiglottitis","Peritonsillar abscess"],
  red_flags=["Severe pain but the throat looks normal (possible epiglottitis)"],
  refs=R("sym_sore_throat"), links=[]),
}
