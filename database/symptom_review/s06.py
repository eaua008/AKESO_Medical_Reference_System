from refs_auto import R
SYMPTOMS = {
"sym_myalgia": dict(
  desc_add="In adults over 50, aching and morning stiffness lasting over an hour in both shoulders and hips, with a markedly raised ESR and CRP but no true weakness, suggests polymyalgia rheumatica; 40 to 60% of patients with giant cell arteritis also have it.",
  tags=["polymyalgia rheumatica"],
  causes=["Polymyalgia rheumatica (adults over 50)","Inflammatory myositis"],
  red_flags=["Shoulder and hip stiffness with headache, jaw pain or vision changes in someone over 50"],
  refs=R("sym_myalgia"), links=[]),
"sym_muscle_cramps": dict(
  desc_add="Most cramps are benign night-time calf cramps or cramps during exercise, helped by tight calf muscles, dehydration, low potassium or magnesium and some medicines. Stretching and fluids are preferred; drugs for cramps have little proven benefit.",
  tags=["nocturnal leg cramps"],
  causes=["Benign night-time leg cramps","Low magnesium"],
  red_flags=["Cramps in the arms or trunk, or with muscle twitching, wasting or weakness"],
  refs=R("sym_muscle_cramps"), links=[("acute_gastroenteritis",2,False,0.3)]),
"sym_nausea_vomiting": dict(
  desc_add="The commonest causes are gastroenteritis, medicines or drugs and toxins. Repeated cycles of vomiting in an adult who uses cannabis heavily, eased by hot showers, suggest cannabinoid hyperemesis, which settles when cannabis is stopped; a pregnancy test is advised in women who could be pregnant.",
  tags=["cyclic vomiting"],
  causes=["Cannabinoid hyperemesis syndrome","Toxins and poisoning","Bowel obstruction","Diabetic ketoacidosis"],
  red_flags=["Swollen, drum-like abdomen (possible bowel obstruction)","Vomiting with confusion or drowsiness"],
  refs=R("sym_nausea_vomiting"), links=[]),
"sym_night_sweats": dict(
  desc_add="In active TB they come with fever, weight loss, poor appetite and fatigue, plus a cough of 3 weeks or more in pulmonary TB. In lymphoma, fever, drenching night sweats and weight loss of more than 10% in 6 months are the 'B symptoms' that affect staging and prognosis.",
  tags=["lymphoma"],
  causes=["HIV infection"],
  red_flags=["Weight loss of more than 10% in 6 months","Cough lasting 3 weeks or more"],
  refs=R("sym_night_sweats"), links=[]),
"sym_hemiparesis": dict(
  desc_add="Arm and leg weakness on one side with spasticity, brisk reflexes and an upgoing plantar response points to a lesion in the opposite brain hemisphere. Weakness that becomes severe within minutes is usually stroke or injury.",
  tags=["upper motor neuron"],
  causes=["Weakness after a seizure (Todd paralysis)"],
  red_flags=["Weakness reaching its worst within minutes"],
  refs=R("sym_hemiparesis"), links=[]),
"sym_bite_site_paresthesia": dict(
  desc_add="The incubation period averages 1 to 2 months but can exceed a year, and brain symptoms usually follow within about 2 weeks of the first symptoms. Immediate wound washing and post-exposure prophylaxis (vaccine plus rabies immune globulin) after a bite prevent the disease; any contact with a bat is an indication.",
  tags=["post-exposure prophylaxis"],
  causes=[],
  red_flags=["Any contact with a bat"],
  refs=R("sym_bite_site_paresthesia"), links=[]),
"sym_mouth_sores": dict(
  desc_add="The commonest causes are recurrent aphthous ulcers, herpes viruses, Candida, injury and irritants, and chemotherapy or radiation. Mouth sores alone without fever or other signs are usually viral or aphthous; blistering skin that peels with light rubbing (Nikolsky sign) suggests Stevens-Johnson syndrome or pemphigus.",
  tags=["stomatitis"],
  causes=["Oral thrush (Candida)","Chemotherapy or radiation","Stevens-Johnson syndrome or pemphigus"],
  red_flags=["Fever with skin blisters or red, painful eyes"],
  refs=R("sym_mouth_sores"), links=[("varicella",3,False,0.4),("hiv_infection",2,False,0.3)]),
"sym_dysuria": dict(
  desc_add="Cystitis and sexually transmitted urethritis are the commonest causes. Pus from the urethra suggests gonorrhea, a tender prostate suggests prostatitis, and red cells without white cells with a sterile culture may point to a stone or cancer.",
  tags=["urethritis"],
  causes=["Bladder cancer (blood without infection)"],
  red_flags=["Recent catheter or urinary procedure","Weakened immune system or known urinary tract abnormality"],
  refs=R("sym_dysuria"), links=[]),
"sym_pale_stool": dict(
  desc_add="Cholestasis shows alkaline phosphatase and GGT more than three times normal with aminotransferases usually under 200 U/L, and dark urine may appear before jaundice is visible. Ultrasound is the first imaging test to look for a blocked bile duct.",
  tags=["acholic"],
  causes=[],
  red_flags=[],
  refs=R("sym_pale_stool"), links=[("hepatitis_b",3,False,0.5)]),
"sym_pallor": dict(
  desc_add="Pallor is usually obvious only with severe anemia (hemoglobin under about 7 g/dL), so its absence does not rule anemia out. A reticulocyte count separates low production from blood loss or hemolysis.",
  tags=["reticulocytes"],
  causes=["Hemolysis (e.g., malaria)","Intestinal worms and schistosomiasis"],
  red_flags=["Pallor with jaundice and dark urine (possible hemolysis)"],
  refs=R("sym_pallor"), links=[("malaria",4,False,0.5),("schistosomiasis",2,False,0.3),("peptic_ulcer_disease",2,False,0.3)]),
}
