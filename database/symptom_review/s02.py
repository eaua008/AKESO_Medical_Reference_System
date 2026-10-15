from refs_auto import R
SYMPTOMS = {
"sym_proptosis": dict(
  desc_add="Graves disease is the commonest cause in adults and orbital cellulitis in children. Sudden one-sided bulging suggests bleeding or inflammation in the orbit, while slow progression suggests a tumor; it is confirmed with an exophthalmometer, and CT or MRI of the orbits shows the cause.",
  tags=["orbit"],
  causes=["Bleeding inside the orbit after injury","Sinus infection spreading into the orbit"],
  red_flags=["Pulsating eye or a whooshing sound in the head (possible carotid-cavernous fistula)","Sudden bulging of one eye"],
  refs=R("sym_proptosis"), links=[]),
"sym_calf_pain": dict(
  desc_add="Deep vein thrombosis is among the commonest causes of non-injury leg pain, and the swelling, warmth and redness can be slight, so ultrasound is often needed. Calf pain that comes on reliably with walking and settles with rest is claudication from peripheral arterial disease.",
  tags=["DVT","claudication"],
  causes=["Sudden blockage of a leg artery (acute arterial occlusion)","Deep soft-tissue infection (cellulitis, necrotizing fasciitis)","Benign acute myositis in children after influenza"],
  red_flags=["Crackling under the skin, blisters or rapidly spreading tense swelling (possible deep tissue infection)","Sudden severe pain with a pulseless leg"],
  refs=R("sym_calf_pain"), links=[("influenza",2,False,0.4)]),
"sym_tophi": dict(
  desc_add="They are found on the fingers, hands and feet, around the elbow (olecranon) and Achilles tendon, and in the skin of the ear, and they mark chronic gouty arthritis. Material aspirated from a tophus shows needle-shaped, strongly negatively birefringent urate crystals under polarised light.",
  tags=["urate"],
  causes=["Long-standing high uric acid, made worse by kidney disease or diuretics"],
  red_flags=["Tophus over a joint with loss of movement or deformity"],
  refs=R("sym_tophi"), links=[]),
"sym_chest_pain": dict(
  desc_add="The immediately life-threatening causes to exclude first are acute coronary syndrome, aortic dissection, tension pneumothorax, esophageal rupture and pulmonary embolism; most other chest pain comes from the chest wall, pleura or digestive tract. Pain that has been present for weeks to months is rarely immediately dangerous.",
  tags=["differential"],
  causes=["Tension pneumothorax","Esophageal rupture or spasm","Peptic ulcer or gallstones","Pericarditis","Pneumonia or pleurisy"],
  red_flags=["Unequal pulses or blood pressure between the arms, or a new heart murmur","Sudden sharp pain with breathlessness (possible pneumothorax or pulmonary embolism)"],
  refs=R("sym_chest_pain"), links=[]),
"sym_chest_tightness": dict(
  desc_add="Tightness that comes in episodes with wheeze, cough and typical triggers (exercise, cold air, allergens) points to asthma, whereas pressure behind the breastbone spreading to the arm or jaw needs an ECG and cardiac enzymes to exclude ischemia. A normal oxygen saturation does not rule out pulmonary embolism.",
  tags=["bronchospasm"],
  causes=["Pulmonary embolism or pneumothorax","Heart failure"],
  red_flags=["Sudden sharp chest pain with rapid breathing"],
  refs=R("sym_chest_tightness"), links=[("acute_coronary_syndrome",3,False,0.5)]),
"sym_chills": dict(
  desc_add="Rigors suggest an infectious cause but are not specific to any one infection. In adults, an acute fever of 4 days or less with chills is very likely infectious, usually from the respiratory, digestive or urinary tract or the skin.",
  tags=["rigors"],
  causes=["Abscess or other deep infection","Cholangitis (bile duct infection)","Dengue"],
  red_flags=["Temperature above 40 °C or below 35 °C","Rash of small purple spots that do not fade when pressed (possible meningococcal infection)"],
  refs=R("sym_chills"), links=[("dengue",3,False,0.4)]),
"sym_confusion": dict(
  desc_add="The commonest triggers are medicines (especially anticholinergic drugs and opioids), dehydration and infection. Delirium is marked by poor attention and a level of alertness that fluctuates and is often worse at night; unlike dementia it starts quickly and is often reversible.",
  tags=["delirium"],
  causes=["Dehydration","Liver or kidney failure","Head injury"],
  red_flags=["An older adult who becomes suddenly quiet or drowsy (hypoactive delirium)"],
  refs=R("sym_confusion"), links=[]),
"sym_constipation": dict(
  desc_add="New, acute constipation suggests an organic cause, and bowel obstruction must be considered when it is sudden and severe. When fibre and laxatives fail, anorectal tests can show dyssynergic defecation, where the pelvic floor muscles do not relax during straining.",
  tags=["bowel obstruction"],
  causes=["Neurological disease (Parkinson's disease, spinal cord injury)","Pelvic floor dysfunction (dyssynergic defecation)","High calcium and diabetes","Anticholinergic drugs"],
  red_flags=["Family history of colorectal cancer or iron-deficiency anemia"],
  refs=R("sym_constipation"), links=[]),
"sym_cough": dict(
  desc_add="Acute cough is mostly from upper respiratory infection, sinusitis, pneumonia, COPD flares, pertussis or heart failure; subacute cough is usually post-infectious airway hyperresponsiveness; chronic cough is mainly from upper airway cough syndrome (postnasal drip), reflux, asthma, chronic bronchitis or ACE inhibitors.",
  tags=["chronic cough"],
  causes=["Postnasal drip (upper airway cough syndrome)","Post-infectious cough","Pertussis","Heart failure"],
  red_flags=["Known HIV infection or contact with someone with TB"],
  refs=R("sym_cough"), links=[]),
"sym_paroxysmal_cough": dict(
  desc_add="Pertussis runs through a catarrhal stage (runny nose, low fever, mild cough), a paroxysmal stage and a slow convalescent stage. Coughing fits are worse at night, may number around 15 in 24 hours and are often followed by vomiting; in young infants apnea may be the only sign.",
  tags=["whooping cough"],
  causes=[],
  red_flags=["Coughing fits followed by vomiting or exhaustion"],
  refs=R("sym_paroxysmal_cough"), links=[]),
}
