from refs_auto import R
SYMPTOMS = {
"sym_chorea": dict(
  desc_add="The movements mainly affect the face and the hands and feet and are often blended into semi-purposeful actions to disguise them. They arise from reduced inhibition in the basal ganglia; Huntington disease is the commonest degenerative cause, and Sydenham chorea is usually self-limited.",
  tags=["basal ganglia"],
  causes=["Phenytoin, cocaine, tricyclic antidepressants or oral contraceptives","Tardive dyskinesia after long-term antipsychotics"],
  red_flags=["Family history of a similar movement disorder or early dementia (possible Huntington disease)"],
  refs=R("sym_chorea"), links=[]),
"sym_pruritus": dict(
  desc_add="It is most often due to skin disease such as dry skin, dermatitis or fungal infection. Prominent itching without any visible skin changes should raise suspicion of a systemic, drug or nerve-related cause.",
  tags=["xerosis"],
  causes=["Dry skin (xerosis)","Fungal skin infection","Opioids and IV contrast","Blood disorders such as lymphoma and polycythemia"],
  red_flags=["Itching with heavy urination and thirst","Itching with numbness, tingling or weakness in the limbs"],
  refs=R("sym_pruritus"), links=[]),
"sym_jaundice": dict(
  desc_add="It can be visible from a bilirubin of about 2 to 3 mg/dL (34 to 51 µmol/L). Very high aminotransferases (over 500 U/L) with alkaline phosphatase under three times normal suggest liver-cell injury, whereas lower aminotransferases with alkaline phosphatase over three times normal suggest cholestasis.",
  tags=["cholestasis"],
  causes=["Autoimmune hepatitis","Cancer of the pancreas or bile ducts"],
  red_flags=["Vomiting blood or black stools"],
  refs=R("sym_jaundice"), links=[]),
"sym_arthralgia": dict(
  desc_add="Sudden pain in many joints is usually from a viral or other infection, a flare of inflammatory disease or crystal arthritis; chronic pain in many joints in adults is usually rheumatoid arthritis, spondyloarthritis or osteoarthritis. Pain at rest and on starting to move suggests inflammation, while pain that worsens with use and eases with rest suggests a mechanical cause.",
  tags=["polyarthralgia"],
  causes=["Reactive arthritis after infection","Systemic lupus erythematosus","Spondyloarthritis"],
  red_flags=["Joint pain with fever, rash, red eyes or weight loss"],
  refs=R("sym_arthralgia"), links=[]),
"sym_joint_swelling": dict(
  desc_add="Septic arthritis is the most dangerous cause at any age, so a new swollen joint with fluid needs joint aspiration (cell count, Gram stain, culture and crystal search). Finding crystals does not rule out infection, and a joint white cell count over 50,000/µL can occur in both.",
  tags=["arthrocentesis"],
  causes=["Bleeding into the joint (hemarthrosis) on anticoagulants or with a bleeding disorder","Lyme disease"],
  red_flags=["Joint swelling in someone on anticoagulants or with a bleeding disorder"],
  refs=R("sym_joint_swelling"), links=[]),
"sym_koplik_spots": dict(
  desc_add="They are seen in about 70% of cases, usually opposite the first and second upper molars, and may persist for a day or two after the rash appears. They follow a prodrome of fever, cough, runny nose and conjunctivitis; the rash then spreads from the head down, and patients are contagious from 4 days before to 4 days after rash onset.",
  tags=["enanthem"],
  causes=[],
  red_flags=[],
  refs=R("sym_koplik_spots"), links=[]),
"sym_edema": dict(
  desc_add="Heart failure gives symmetrical, painless pitting edema in the lowest parts of the body, whereas a sudden, painful swelling of one leg suggests deep vein thrombosis and usually needs an ultrasound. Generalised edema mostly comes from heart, liver or kidney disease.",
  tags=["pitting"],
  causes=["Lymphatic obstruction (lymphedema)","Cellulitis","Angioedema","Low blood protein from malnutrition"],
  red_flags=["Sudden onset of swelling","Swelling of the face, lips or tongue"],
  refs=R("sym_edema"), links=[("hepatitis_b",2,False,0.3)]),
"sym_anorexia": dict(
  desc_add="Weight loss with a poor appetite most often comes from depression, cancer, medicine side effects or substance use, whereas weight loss despite a good appetite suggests hyperthyroidism, uncontrolled diabetes or malabsorption.",
  tags=["weight loss"],
  causes=["Substance use","Malaria","HIV infection"],
  red_flags=["Swollen lymph nodes, bone pain or coughing blood","Fear of weight gain in a young person (possible eating disorder)"],
  refs=R("sym_anorexia"), links=[("malaria",3,False,0.4),("hiv_infection",3,False,0.4)]),
"sym_anosmia": dict(
  desc_add="Most people with anosmia can still taste salty, sweet, sour and bitter but report a loss of taste because flavour depends on smell. Head injury is the main cause in young adults and Alzheimer disease in older adults, and smell loss persists after an upper respiratory infection in a minority of people.",
  tags=["dysgeusia"],
  causes=["Alzheimer disease (older adults)","Medicines and toxins","Radiation or nasal surgery","Influenza"],
  red_flags=["Sudden loss of smell"],
  refs=R("sym_anosmia"), links=[("influenza",2,False,0.3)]),
"sym_bleeding": dict(
  desc_add="Bleeding into the skin and mucous membranes with petechiae suggests a platelet or blood-vessel problem, while deep bleeding into joints and muscles suggests a clotting-factor disorder. The first tests are a full blood count, blood smear, PT and aPTT.",
  tags=["thrombocytopenia"],
  causes=["Disseminated intravascular coagulation (DIC) in sepsis","Kidney failure (uremic platelet dysfunction)","Von Willebrand disease","NSAIDs and aspirin"],
  red_flags=["Bleeding in pregnancy","Bloody diarrhea with low platelets (possible hemolytic uremic syndrome)"],
  refs=R("sym_bleeding"), links=[("leptospirosis",3,False,0.5),("chronic_kidney_disease",2,False,0.3)]),
}
