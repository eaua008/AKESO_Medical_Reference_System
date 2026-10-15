from refs_auto import R
SYMPTOMS = {
"sym_koilonychia": dict(
  desc_add="It appears in severe iron deficiency together with pica, a smooth sore tongue and cracks at the mouth corners. Iron deficiency is mostly due to blood loss, so in men and women past menopause the bowel is checked for hidden bleeding, which can be the only sign of a gut cancer.",
  tags=["spoon nails"],
  causes=[],
  red_flags=["Iron deficiency in a man or a woman past menopause (look for bowel bleeding)"],
  refs=R("sym_koilonychia"), links=[]),
"sym_neck_stiffness": dict(
  desc_add="Fever and neck stiffness may be missing in newborns, infants, older adults, people with weak immunity and heavy drinkers, so a lumbar puncture should be considered early. Bacterial meningitis is an emergency: antibiotics (with steroids) are given within 30 minutes, and brain imaging comes before the lumbar puncture only if there is papilledema or a focal deficit.",
  tags=["lumbar puncture"],
  causes=[],
  red_flags=["Fever with drowsiness in an infant or older adult, even without a stiff neck"],
  refs=R("sym_neck_stiffness"), links=[]),
"sym_podagra": dict(
  desc_add="Common triggers are injury, surgery, infection, thiazide diuretics, starting urate-lowering drugs, purine-rich food and alcohol. Diagnosis is by finding needle-shaped, negatively birefringent urate crystals in joint fluid; the blood urate level is normal in at least 30% of people during a flare.",
  tags=["urate crystals"],
  causes=[], red_flags=[],
  refs=R("sym_podagra"), links=[]),
"sym_suprapubic_pain": dict(
  desc_add="In cystitis it comes on suddenly with frequency, urgency and burning while passing small volumes. A positive nitrite test is highly specific for bacteria, and leukocyte esterase is fairly sensitive; dysuria with white cells but no bacteria suggests urethritis or an STI.",
  tags=["cystitis"],
  causes=["Prostatitis"],
  red_flags=["Repeated infections, or symptoms in a man"],
  refs=R("sym_suprapubic_pain"), links=[]),
"sym_diaphoresis": dict(
  desc_add="Generalised sweating can come from lymphoma or leukemia, tuberculosis, endocarditis, hyperthyroidism, low blood sugar, drugs, opioid withdrawal and menopause. Sweating that is mainly at night points to cancer or infection, and sweating on only one side suggests a nerve problem.",
  tags=["hyperhidrosis"],
  causes=["Tuberculosis","Lymphoma or leukemia","Endocarditis","Opioid or alcohol withdrawal"],
  red_flags=["Sweating on only one side of the body"],
  refs=R("sym_diaphoresis"), links=[("tuberculosis",2,False,0.3)]),
"sym_goiter": dict(
  desc_add="Iodine deficiency is the leading cause worldwide. Most goiters cause no symptoms, but large ones can cause swallowing difficulty, hoarseness or a feeling of fullness in the throat; assessment uses thyroid function tests, ultrasound, thyroid antibodies and sometimes an iodine uptake scan.",
  tags=["iodine deficiency"],
  causes=["Goitrogens in food (cassava, cruciferous vegetables)","Amiodarone or lithium"],
  red_flags=[],
  refs=R("sym_goiter"), links=[]),
"sym_lymphadenopathy": dict(
  desc_add="Nodes in one area for less than 2 weeks are usually from a local infection, while nodes in several areas suggest a systemic illness such as mononucleosis, lymphoma or lupus. Without red flags, nodes can be watched for up to 4 weeks; steroids should not be given empirically because they can mask lymphoma or leukemia.",
  tags=["supraclavicular"],
  causes=[],
  red_flags=["A node larger than 2 cm, or an enlarged spleen"],
  refs=R("sym_lymphadenopathy"), links=[("tuberculosis",3,False,0.4)]),
"sym_burrows": dict(
  desc_add="Itching usually starts 4 to 6 weeks after a first infestation (sooner on re-infestation), and the face is spared in adults. Scrapings from a burrow can show the mite under a microscope, though a negative result does not rule scabies out; dermoscopy shows a 'delta-wing jet' sign.",
  tags=["dermoscopy"],
  causes=[], red_flags=[],
  refs=R("sym_burrows"), links=[]),
"sym_weight_loss": dict(
  desc_add="Weight loss despite a good appetite suggests hyperthyroidism, uncontrolled diabetes or malabsorption, while weight loss with a poor appetite suggests depression, cancer or medicines. Baseline tests usually include a chest X-ray, urinalysis, blood count, ESR or CRP, HIV test, chemistry and TSH.",
  tags=["cachexia"],
  causes=["Medicines","Substance use"],
  red_flags=["Bone pain or swollen lymph nodes"],
  refs=R("sym_weight_loss"), links=[]),
"sym_urinary_frequency": dict(
  desc_add="Frequency means passing normal or small volumes often, unlike polyuria, where the total volume is over 3 L a day. Getting up at night with a weak stream suggests prostate enlargement.",
  tags=["overactive bladder"],
  causes=["Kidney or bladder stones"],
  red_flags=["Leg weakness, numbness around the buttocks or loss of bladder control (possible spinal cord compression)"],
  refs=R("sym_urinary_frequency"), links=[("type2_diabetes",3,False,0.4)]),
"sym_visual_aura": dict(
  desc_add="About a quarter of people with migraine have aura, usually before the headache and sometimes without any headache. In older adults, aura without headache can be mistaken for a transient ischemic attack.",
  tags=["scintillating scotoma"],
  causes=["Arterial dissection or vasculitis (rare mimics)"],
  red_flags=["Aura with no headache in an older adult (consider TIA)"],
  refs=R("sym_visual_aura"), links=[]),
"sym_posttussive_vomiting": dict(
  desc_add="Pertussis runs over 6 to 10 weeks; infants under 6 months are at highest risk and may have choking or blue spells instead of a whoop. Pertussis should be suspected with a cough of 2 weeks or more plus a whoop, coughing fits or vomiting after coughing, and PCR is the preferred test.",
  tags=["whooping cough"],
  causes=[], red_flags=[],
  refs=R("sym_posttussive_vomiting"), links=[]),
"sym_hematemesis": dict(
  desc_add="Coffee-ground vomit suggests the bleeding has slowed or stopped, whereas bright red blood suggests active bleeding. Initial care is airway protection, large IV lines, fluids and transfusion as needed, an IV proton pump inhibitor and endoscopy.",
  tags=["coffee-ground"],
  causes=["Bleeding in severe dengue","Swallowed blood from a nosebleed"],
  red_flags=["Pale, sweaty skin"],
  refs=R("sym_hematemesis"), links=[("dengue",2,False,0.4),("hepatitis_b",2,False,0.3)]),
"sym_nocturia": dict(
  desc_add="Comparing how much is drunk with how much is passed (and a 24-hour urine collection if unclear) separates high urine output from frequent small voids. Troublesome nocturia often improves by drinking less in the evening.",
  tags=["polyuria"],
  causes=[], red_flags=[],
  refs=R("sym_nocturia"), links=[("heart_failure",2,False,0.3),("type2_diabetes",2,False,0.3)]),
"sym_wheezing": dict(
  desc_add="Medicines such as beta-blockers, ACE inhibitors and NSAIDs can cause it, and in children bronchiolitis and inhaled foreign bodies are important. A wheeze that stays in one place suggests a tumor or foreign body, and noise on breathing in suggests stridor rather than wheeze.",
  tags=["stridor"],
  causes=["Medicines (beta-blockers, ACE inhibitors, NSAIDs)"],
  red_flags=["Drowsiness or exhaustion during an asthma attack"],
  refs=R("sym_wheezing"), links=[("heart_failure",2,False,0.3)]),
"sym_oral_thrush": dict(
  desc_add="The diagnosis is usually clinical, and a KOH preparation of a scraping shows yeast and pseudohyphae. Treatment options include clotrimazole troches, nystatin suspension or oral fluconazole.",
  tags=["candidiasis"],
  causes=[], red_flags=[],
  refs=R("sym_oral_thrush"), links=[]),
}
