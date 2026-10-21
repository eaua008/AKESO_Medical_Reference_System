# Batch 01 (B1): mixed high-yield parts. See docs/body-part-descriptions-plan.md, Batches.
# One row per description: (key, display name, layer, what it covers in parts.json).
#   "c:<concept>"  every part whose name, with left/right removed, is that concept
#   "g:<group id>" every part in that group
# gen_body_parts.py turns these into fma_ids (both sides) and checks they exist.
# The coronary arteries are two entries: "left"/"right" is part of their name there,
# not the body side, so they are keyed by the curated v_coronary_l / v_coronary_r groups.

ENTRIES = [
    # Organs (18)
    ("group:fma_FMA7088_o", "Heart", "organ", ["g:fma_FMA7088_o"]),
    ("trachea", "Trachea", "organ", ["c:trachea"]),
    ("group:airways", "Bronchial tree", "organ", ["g:airways"]),
    ("esophagus", "Oesophagus", "organ", ["c:esophagus"]),
    ("stomach", "Stomach", "organ", ["c:stomach"]),
    ("group:fma_FMA7197_o", "Liver", "organ", ["g:fma_FMA7197_o"]),
    ("gallbladder", "Gallbladder", "organ", ["c:gallbladder"]),
    ("pancreas", "Pancreas", "organ", ["c:pancreas"]),
    ("spleen", "Spleen", "organ", ["c:spleen"]),
    ("group:small_intestine", "Small intestine", "organ", ["g:small_intestine"]),
    ("group:large_intestine", "Large intestine", "organ", ["g:large_intestine"]),
    ("appendix", "Appendix", "organ", ["c:appendix"]),
    ("kidney", "Kidney", "organ", ["c:kidney"]),
    ("urinary bladder", "Urinary bladder", "organ", ["c:urinary bladder"]),
    ("group:fma_FMA50801_o", "Brain", "organ", ["g:fma_FMA50801_o"]),
    ("cerebellum", "Cerebellum", "organ", ["c:cerebellum"]),
    ("pituitary gland", "Pituitary gland", "organ", ["c:pituitary gland"]),
    ("group:eye_ball", "Eyeball", "organ", ["g:eye_ball_l", "g:eye_ball_r"]),
    # Bones (14)
    ("group:skull", "Skull", "bone", ["g:skull"]),
    ("mandible", "Mandible", "bone", ["c:mandible"]),
    ("group:spine", "Vertebral column", "bone", ["g:spine"]),
    ("group:ribcage", "Rib cage", "bone", ["g:ribcage"]),
    ("clavicle", "Clavicle", "bone", ["c:clavicle"]),
    ("scapula", "Scapula", "bone", ["c:scapula"]),
    ("humerus", "Humerus", "bone", ["c:humerus"]),
    ("radius", "Radius", "bone", ["c:radius"]),
    ("ulna", "Ulna", "bone", ["c:ulna"]),
    ("hip bone", "Hip bone", "bone", ["c:hip bone"]),
    ("femur", "Femur", "bone", ["c:femur"]),
    ("patella", "Patella", "bone", ["c:patella"]),
    ("tibia", "Tibia", "bone", ["c:tibia"]),
    ("fibula", "Fibula", "bone", ["c:fibula"]),
    # Muscles (11). Biceps, triceps, pectoralis major, trapezius and gastrocnemius
    # exist in the model only as their heads/parts, so the entry covers those.
    ("diaphragm", "Diaphragm", "muscle", ["c:diaphragm"]),
    ("group:deltoid", "Deltoid", "muscle", ["g:deltoid"]),
    ("biceps brachii", "Biceps brachii", "muscle",
     ["c:long head of biceps brachii", "c:short head of biceps brachii"]),
    ("triceps brachii", "Triceps brachii", "muscle",
     ["c:long head of triceps brachii", "c:lateral head of triceps brachii", "c:medial head of triceps brachii"]),
    ("pectoralis major", "Pectoralis major", "muscle",
     ["c:clavicular part of pectoralis major", "c:sternocostal part of pectoralis major",
      "c:abdominal part of pectoralis major"]),
    ("trapezius", "Trapezius", "muscle",
     ["c:descending part of trapezius", "c:transverse part of trapezius", "c:ascending part of trapezius"]),
    ("sternocleidomastoid", "Sternocleidomastoid", "muscle", ["c:sternocleidomastoid"]),
    ("group:quadriceps", "Quadriceps femoris", "muscle", ["g:quadriceps"]),
    ("group:hamstrings", "Hamstrings", "muscle", ["g:hamstrings"]),
    ("gluteus maximus", "Gluteus maximus", "muscle", ["c:gluteus maximus"]),
    ("gastrocnemius", "Gastrocnemius", "muscle",
     ["c:medial head of gastrocnemius", "c:lateral head of gastrocnemius"]),
    # Vessels (10)
    ("group:fma_FMA3734_v", "Aorta", "vessel", ["g:fma_FMA3734_v"]),
    ("superior vena cava", "Superior vena cava", "vessel", ["c:superior vena cava"]),
    ("inferior vena cava", "Inferior vena cava", "vessel", ["c:inferior vena cava"]),
    ("pulmonary trunk", "Pulmonary trunk", "vessel", ["c:pulmonary trunk"]),
    ("common carotid artery", "Common carotid artery", "vessel", ["c:common carotid artery"]),
    ("internal jugular vein", "Internal jugular vein", "vessel", ["c:internal jugular vein"]),
    ("group:v_coronary_l", "Left coronary artery", "vessel", ["g:v_coronary_l"]),
    ("group:v_coronary_r", "Right coronary artery", "vessel", ["g:v_coronary_r"]),
    ("hepatic portal vein", "Hepatic portal vein", "vessel", ["c:hepatic portal vein"]),
    ("femoral artery", "Femoral artery", "vessel", ["c:femoral artery"]),
    # Nerves (1)
    ("optic nerve", "Optic nerve", "nerve", ["c:optic nerve"]),
]
