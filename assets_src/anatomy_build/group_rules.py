"""Teaching-friendly groups for the Body System Explorer (data only).

parts.py reads this table and builds, for every part, a CHAIN of groups from
the smallest meaningful one up to the whole layer ("This molar", "Upper right
teeth", "Upper teeth", "All teeth", "All bones"). A group never mixes layers.

    R(id, label, layer, pattern, ...)    parts of that layer whose name matches
                                          the regex (case-insensitive)
    U(id, label, layer, [ids], ...)      the union of other groups (by id)

Options (keyword):
    sided=True   also make "Left <label>" and "Right <label>" groups, using the
                 words "left" / "right" in the part names. The un-sided group
                 then means both sides. A union of sided groups is sided too.
    alt=True     an ALTERNATIVE grouping (teeth by type, muscles by compartment):
                 shown in a second row of chips, not in the main chain.
    both="..."   the label of the both-sides group when it should not simply be
                 the plain label (e.g. "Both hands").
Groups are listed small to large only for readability; parts.py sorts by size.
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Rule:
    id: str
    label: str
    layer: str
    pattern: Optional[str] = None
    members: list = field(default_factory=list)      # ids of groups, for a union
    sided: bool = False
    alt: bool = False
    both: Optional[str] = None


def R(id, label, layer, pattern, **kw): return Rule(id, label, layer, pattern, **kw)
def U(id, label, layer, members, **kw): return Rule(id, label, layer, None, list(members), **kw)


ORD = r"(first|second|third|fourth|fifth|sixth|seventh|eighth|ninth|tenth|eleventh|twelfth)"
FINGER = r"(thumb|index finger|middle finger|ring finger|little finger)"
TOE = r"(big toe|second toe|third toe|fourth toe|little toe)"

RULES: list[Rule] = [
    # ------------------------------------------------------------------ BONES
    # teeth: quadrant -> upper / lower -> all teeth; by type is an alternative
    R("teeth_ur", "Upper right teeth", "bone", r"^right upper .*tooth"),
    R("teeth_ul", "Upper left teeth", "bone", r"^left upper .*tooth"),
    R("teeth_lr", "Lower right teeth", "bone", r"^right lower .*tooth"),
    R("teeth_ll", "Lower left teeth", "bone", r"^left lower .*tooth"),
    R("teeth_up", "Upper teeth", "bone", r"^(left|right) upper .*tooth"),
    R("teeth_lo", "Lower teeth", "bone", r"^(left|right) lower .*tooth"),
    R("teeth", "All teeth", "bone", r"tooth$"),
    R("teeth_right", "Right teeth", "bone", r"^right (upper|lower) .*tooth", alt=True),
    R("teeth_left", "Left teeth", "bone", r"^left (upper|lower) .*tooth", alt=True),
    R("teeth_incisors", "Incisors", "bone", r"incisor tooth", alt=True),
    R("teeth_canines", "Canines", "bone", r"canine tooth", alt=True),
    R("teeth_premolars", "Premolars", "bone", r"premolar tooth", alt=True),
    R("teeth_molars", "Molars", "bone", r"secondary molar tooth", alt=True),
    R("gums", "Gums", "bone", r"^gingiva"),
    U("teeth_gums", "Teeth and gums", "bone", ["teeth", "gums"]),

    # skull
    R("skull_cranial", "Cranial bones", "bone",
      r"^(frontal bone|(left |right )?parietal bone|(left |right )?temporal bone|occipital bone|sphenoid bone|ethmoid)$"),
    R("skull_facial", "Facial bones", "bone",
      r"^((left |right )?(nasal bone|maxilla|zygomatic bone|lacrimal bone|palatine bone|inferior nasal concha)|vomer|mandible)$"),
    U("skull", "Skull", "bone", ["skull_cranial", "skull_facial"]),
    R("nasal_cartilages", "Nasal cartilages", "bone", r"(lateral nasal cartilage|major alar cartilage|septal nasal cartilage)"),
    R("laryngeal_cartilages", "Laryngeal cartilages", "bone",
      r"(thyroid cartilage|cricoid cartilage|arytenoid cartilage|corniculate cartilage|cuneiform cartilage)"),
    R("hyoid", "Hyoid bone", "bone", r"hyoid bone"),

    # spine
    R("vert_cervical", "Cervical vertebrae", "bone", r"^(atlas|axis|" + ORD + r" cervical vertebra)$"),
    R("vert_thoracic", "Thoracic vertebrae", "bone", r"^" + ORD + r" thoracic vertebra$"),
    R("vert_lumbar", "Lumbar vertebrae", "bone", r"^" + ORD + r" lumbar vertebra$"),
    R("sacrum", "Sacrum", "bone", r"^sacrum$"),
    R("disc_cervical", "Cervical discs", "bone", r"^intervertebral disk of (axis|" + ORD + r" cervical vertebra)"),
    R("disc_thoracic", "Thoracic discs", "bone", r"^intervertebral disk of " + ORD + r" thoracic vertebra"),
    R("disc_lumbar", "Lumbar discs", "bone", r"^intervertebral disk of " + ORD + r" lumbar vertebra"),
    U("discs", "Intervertebral discs", "bone", ["disc_cervical", "disc_thoracic", "disc_lumbar"]),
    U("vert_all", "Vertebrae", "bone", ["vert_cervical", "vert_thoracic", "vert_lumbar", "sacrum"]),
    U("spine_cervical", "Cervical spine (vertebrae and discs)", "bone", ["vert_cervical", "disc_cervical"], alt=True),
    U("spine_thoracic", "Thoracic spine (vertebrae and discs)", "bone", ["vert_thoracic", "disc_thoracic"], alt=True),
    U("spine_lumbar", "Lumbar spine (vertebrae and discs)", "bone", ["vert_lumbar", "disc_lumbar"], alt=True),
    R("symphysis", "Intervertebral symphysis", "bone", r"^intervertebral symphysis"),
    U("spine", "Vertebral column", "bone", ["vert_all", "discs", "symphysis"]),

    # rib cage
    R("ribs", "Ribs", "bone", r"^(left |right )?" + ORD + r" rib$", sided=True),
    R("costal_cartilages", "Costal cartilages", "bone", r"costal cartilage$", sided=True),
    R("sternum", "Sternum", "bone", r"^(manubrium|body of sternum|xiphoid process)$"),
    U("ribcage", "Rib cage", "bone", ["ribs", "costal_cartilages", "sternum"]),

    # hand
    R("carpals", "Carpal bones", "bone", r"^(left |right )?(scaphoid|lunate|triquetral|pisiform|trapezium|trapezoid|capitate|hamate)$", sided=True),
    R("metacarpals", "Metacarpals", "bone", r"metacarpal bone$", sided=True),
    R("finger_phalanges", "Finger bones", "bone", r"phalanx of (left|right) " + FINGER, sided=True),
    U("hand_bones", "Hand bones", "bone", ["carpals", "metacarpals", "finger_phalanges"], sided=True, both="Both hands"),
    R("arm_bones", "Arm and shoulder bones", "bone", r"^(left |right )?(clavicle|scapula|humerus|radius|ulna)$", sided=True),
    U("upper_limb_bones", "Upper limb bones", "bone", ["hand_bones", "arm_bones"], sided=True),
    # foot
    R("tarsals", "Tarsal bones", "bone",
      r"(calcaneus|talus|cuboid bone|navicular bone of|medial cuneiform|intermediate cuneiform|lateral cuneiform)", sided=True),
    R("metatarsals", "Metatarsals", "bone", r"metatarsal bone$", sided=True),
    R("toe_phalanges", "Toe bones", "bone", r"phalanx of (left|right) " + TOE, sided=True),
    R("foot_sesamoids", "Sesamoid bones of the foot", "bone", r"sesamoid bone of (left|right) foot", sided=True),
    U("foot_bones", "Foot bones", "bone", ["tarsals", "metatarsals", "toe_phalanges", "foot_sesamoids"], sided=True, both="Both feet"),
    R("leg_bones", "Hip and leg bones", "bone", r"^(left |right )?(femur|tibia|fibula|patella|hip bone)$", sided=True),
    U("lower_limb_bones", "Lower limb bones", "bone", ["foot_bones", "leg_bones"], sided=True),
    # regions
    U("head_neck_bones", "Head and neck bones", "bone",
      ["skull", "teeth_gums", "hyoid", "nasal_cartilages", "laryngeal_cartilages", "vert_cervical", "disc_cervical"]),
    U("trunk_bones", "Trunk bones", "bone",
      ["vert_thoracic", "vert_lumbar", "sacrum", "disc_thoracic", "disc_lumbar", "symphysis", "ribcage"]),

    # ----------------------------------------------------------------- MUSCLES
    R("quadriceps", "Quadriceps", "muscle", r"(rectus femoris|vastus)", sided=True),
    R("hamstrings", "Hamstrings", "muscle", r"(biceps femoris|semitendinosus|semimembranosus)", sided=True),
    R("adductors", "Adductors of the thigh", "muscle", r"(adductor (brevis|longus|magnus|minimus)|gracilis|pectineus)", sided=True),
    R("thigh_front_other", "Sartorius", "muscle", r"sartorius", sided=True),
    U("thigh_muscles", "Thigh muscles", "muscle", ["quadriceps", "hamstrings", "adductors", "thigh_front_other"], sided=True),
    R("gluteal", "Gluteal and hip rotator muscles", "muscle",
      r"(gluteus|tensor fasciae latae|piriformis|gemellus|obturator|quadratus femoris|iliotibial)", sided=True),
    R("hip_flexors", "Hip flexors (iliopsoas)", "muscle", r"(iliacus|psoas major)", sided=True),
    R("calf", "Calf (posterior leg) muscles", "muscle",
      r"(gastrocnemius|soleus|plantaris|popliteus|tibialis posterior|flexor digitorum longus|flexor hallucis longus|calcaneal tendon)", sided=True),
    R("leg_front", "Anterior leg muscles", "muscle",
      r"(tibialis anterior|extensor digitorum longus|extensor hallucis longus|fibularis tertius)", sided=True),
    R("leg_side", "Lateral leg muscles", "muscle", r"(fibularis longus|fibularis brevis)", sided=True),
    R("foot_muscles", "Foot muscles", "muscle",
      r"(foot$|hallucis brevis|abductor hallucis|adductor hallucis|extensor digitorum brevis|flexor digitorum brevis|flexor accessorius|long plantar ligament)", sided=True),
    R("leg_membrane", "Interosseous membranes", "muscle", r"interosseous membrane", sided=True),
    U("leg_muscles", "Leg and foot muscles", "muscle", ["calf", "leg_front", "leg_side", "foot_muscles"], sided=True),
    R("rotator_cuff", "Rotator cuff", "muscle", r"(supraspinatus|infraspinatus|teres minor|subscapularis)", sided=True),
    R("deltoid", "Deltoid", "muscle", r"deltoid", sided=True),
    R("scapular_back", "Shoulder-blade and upper back muscles", "muscle",
      r"(trapezius|levator scapulae|rhomboid|teres major)", sided=True),
    R("chest_wall", "Chest muscles", "muscle", r"(pectoralis|subclavius|serratus anterior)", sided=True),
    R("arm_front", "Anterior arm muscles", "muscle", r"(biceps brachii|brachialis|coracobrachialis)", sided=True),
    R("arm_back", "Posterior arm muscles", "muscle", r"(triceps brachii|anconeus)", sided=True),
    R("forearm_flexors", "Forearm flexors and pronators", "muscle",
      r"(flexor carpi|palmaris longus|flexor digitorum (superficialis|profundus)|flexor pollicis longus|pronator)", sided=True),
    R("forearm_extensors", "Forearm extensors and supinator", "muscle",
      r"(extensor (carpi|digitorum$|digiti minimi|indicis|pollicis)|abductor pollicis longus|brachioradialis|supinator|^(left |right )?extensor digitorum )", sided=True),
    R("hand_muscles", "Hand muscles", "muscle",
      r"(hand$|flexor retinaculum|abductor pollicis brevis|flexor pollicis brevis|opponens pollicis|adductor pollicis|interossei of|lumbricals of)", sided=True),
    U("arm_muscles", "Arm muscles", "muscle", ["arm_front", "arm_back"], sided=True),
    U("forearm_muscles", "Forearm muscles", "muscle", ["forearm_flexors", "forearm_extensors"], sided=True),
    U("shoulder_muscles", "Shoulder muscles", "muscle", ["rotator_cuff", "deltoid", "scapular_back", "chest_wall"], sided=True),
    R("abdominal_wall", "Abdominal wall muscles", "muscle", r"(external oblique|internal oblique|transversus abdominis|rectus abdominis)", sided=True),
    R("thoracic_wall", "Thoracic wall and breathing muscles", "muscle",
      r"(intercostal|transversus thoracis|serratus posterior|levatores costarum|diaphragm)", sided=True),
    R("erector_spinae", "Erector spinae", "muscle", r"(iliocostalis|longissimus|spinalis)", sided=True),
    R("deep_back", "Deep back muscles", "muscle",
      r"(semispinalis|rotator|interspinales|interspinalis|intertransversari|multifidus)", sided=True),
    R("pelvic_floor", "Pelvic floor muscles", "muscle",
      r"(coccygeus|iliococcygeus|pubococcygeus|puborectalis|tendinous arch of levator ani|perineal)", sided=True),
    R("extraocular", "Eye muscles", "muscle",
      r"(superior rectus|inferior rectus|medial rectus|lateral rectus|superior oblique$|inferior oblique$|levator palpebrae)", sided=True),
    R("tongue_muscles", "Tongue muscles", "muscle", r"(genioglossus|hyoglossus)", sided=True),
    R("pharynx_muscles", "Pharyngeal muscles", "muscle",
      r"(pharyngeal constrictor|palatopharyngeus|salpingopharyngeus|stylopharyngeus|pharyngeal raphe|pterygomandibular raphe)", sided=True),
    R("palate_muscles", "Soft palate muscles", "muscle", r"(veli palatini|uvular)", sided=True),
    R("larynx_muscles", "Laryngeal muscles", "muscle", r"(crico-arytenoid|arytenoid$|thyro-arytenoid|vocalis|conus elasticus)", sided=True),
    R("suprahyoid", "Suprahyoid muscles", "muscle", r"(digastric|mylohyoid|geniohyoid|stylohyoid|intermediate tendon)", sided=True),
    R("infrahyoid", "Infrahyoid muscles", "muscle", r"(sternohyoid|omohyoid|sternothyroid|thyrohyoid)", sided=True),
    R("face_soft", "Lips, mouth and eyelids", "muscle", r"(lip|subdivision of mouth|tarsal plate)", sided=True),
    R("neck_muscles", "Neck muscles", "muscle",
      r"(sternocleidomastoid|scalenus|platysma|longus capitis|longus colli|rectus capitis|obliquus capitis|splenius|longissimus capitis)", sided=True),
    U("trunk_wall_muscles", "Trunk wall muscles", "muscle", ["abdominal_wall", "thoracic_wall"], sided=True),
    U("back_muscles", "Back muscles", "muscle", ["erector_spinae", "deep_back"], sided=True),
    U("throat_muscles", "Throat muscles", "muscle",
      ["tongue_muscles", "pharynx_muscles", "palate_muscles", "larynx_muscles", "suprahyoid", "infrahyoid"], sided=True),
    # regions
    U("upper_limb_muscles", "Upper limb muscles", "muscle",
      ["shoulder_muscles", "arm_muscles", "forearm_muscles", "hand_muscles"], sided=True),
    U("lower_limb_muscles", "Lower limb muscles", "muscle",
      ["thigh_muscles", "gluteal", "hip_flexors", "leg_muscles"], sided=True),
    U("trunk_muscles", "Trunk muscles", "muscle",
      ["trunk_wall_muscles", "back_muscles", "pelvic_floor"], sided=True),
    U("head_neck_muscles", "Head and neck muscles", "muscle",
      ["extraocular", "face_soft", "throat_muscles", "neck_muscles"], sided=True),
    # alternative: by side only
    R("muscles_left", "Left-side muscles", "muscle", r"(^|\W)left\W", alt=True),
    R("muscles_right", "Right-side muscles", "muscle", r"(^|\W)right\W", alt=True),

    # ----------------------------------------------------------------- VESSELS
    R("v_hand", "Hand vessels", "vessel", r"(palmar|metacarpal|dorsal venous network|dorsal digital)", sided=True),
    R("v_foot", "Foot vessels", "vessel", r"(plantar|metatarsal|dorsalis pedis|calcaneal)", sided=True),
    R("v_brain", "Brain vessels", "vessel", r"(cerebral|cerebellar|communicating|basilar|choroidal|sulcus|gyrus|vertebral)", sided=True),
    R("v_coronary", "Coronary and cardiac vessels", "vessel", r"(coronary|cardiac vein|interventricular)", sided=True),
    R("v_intercostal", "Intercostal vessels", "vessel", r"intercostal", sided=True),
    R("v_liver", "Liver vessels", "vessel", r"(hepatic|portal|caudate lobe)", sided=True),
    R("v_gut", "Gut vessels", "vessel", r"(mesenteric|colic|cecal|ileal|jejunal|gastric|splenic|pancreatic|celiac|gastroduodenal|appendicular|oesophageal)", sided=True),
    R("v_kidney", "Kidney vessels", "vessel", r"renal", sided=True),
    # ------------------------------------------------------------ SKIN, NERVES
    R("hair", "Hair", "skin", r"hair"),
    R("skin_features", "Ears and eyebrows", "skin", r"(external ear|eyebrow)"),
    R("optic_path", "Optic pathway", "nerve", r"optic", sided=True),
    R("orbit_nerves", "Orbital nerves", "nerve",
      r"(ophthalmic|nasociliary|frontal nerve|lacrimal nerve|ethmoidal|supra-orbital|supratrochlear|infratrochlear|ciliary|oculomotor|trochlear nerve)", sided=True),
    # ------------------------------------------------------------------ ORGANS
    # brain
    R("brain_basal_ganglia", "Basal ganglia", "organ", r"(caudate nucleus|putamen|globus pallidus)", sided=True),
    R("brain_thalamic", "Thalamus and neighbours", "organ",
      r"(thalamus|geniculate|habenula|stria medullaris|pineal|mammillary|tuber cinereum)", sided=True),
    R("brain_limbic", "Limbic structures", "organ",
      r"(amygdala|hippocampus|fornix|cingulate|parahippocampal|septum of telencephalon)", sided=True),
    R("brain_gyri", "Cerebral cortex (gyri and lobes)", "organ",
      r"(gyrus|lobe$|lobule|insula|precentral|postcentral)", sided=True),
    R("brain_white", "White matter and tracts", "organ",
      r"(corpus callosum|commissure|internal capsule|white matter|decussation|lamina terminalis|stria terminalis)", sided=True),
    R("brain_ventricles", "Ventricles", "organ", r"(ventricle|choroid plexus|cerebral aqueduct|wall of ventricle)", sided=True),
    R("brainstem", "Brainstem", "organ", r"(colliculus|peduncle of midbrain|hindbrain|metencephalon|cardinal segment)", sided=True),
    R("cerebellum", "Cerebellum", "organ", r"cerebellum", sided=True),
    R("brain_hypothalamus", "Hypothalamus", "organ", r"hypothalamus", sided=True),
    R("meninges", "Meninges", "organ", r"(dura mater|subarachnoid)", sided=True),
    # eye
    R("eye_ball", "Eyeball parts", "organ",
      r"(cornea|iris|lens|sclera|vitreous|retina|choroid$|corona ciliaris|anterior chamber|suspensory ligament)", sided=True),
    R("eye_lacrimal", "Tear apparatus", "organ", r"(lacrimal|nasolacrimal)", sided=True),
    R("eye_lids", "Eyelids and muscle attachments", "organ", r"(tarsal plate|check ligament|common tendinous ring|trochlea)", sided=True),
    U("eye_structures", "Eye structures", "organ", ["eye_ball", "eye_lacrimal", "eye_lids"], sided=True),
    # heart
    R("heart_valves", "Heart valves", "organ", r"(cusp of|leaflet of)"),
    R("heart_papillary", "Papillary muscles", "organ", r"papillary muscle"),
    R("heart_atria", "Atria", "organ", r"(cavity|wall) (of )?atrium|atrium"),
    R("heart_ventricles", "Ventricles of the heart", "organ", r"(cavity|papillary muscle).*ventricle|ventricle cavity|cavity of .*ventricle"),
    # lungs / airways
    R("lobe_ur", "Right upper lobe airways", "organ", r"^right (apical|posterior|anterior) segmental bronchial tree"),
    R("lobe_rm", "Right middle lobe airways", "organ", r"^(right )?(lateral|medial) segmental bronchial tree"),
    R("lobe_rl", "Right lower lobe airways", "organ", r"^right (superior|medial basal|anterior basal|lateral basal|posterior basal)"),
    R("lobe_ul", "Left upper lobe airways", "organ", r"(^left (apical|posterior|anterior) segmental|lingular bronchial tree)"),
    R("lobe_ll", "Left lower lobe airways", "organ", r"^left (superior|medial basal|anterior basal|lateral basal|posterior basal)"),
    R("lungs_right", "Right lung airways", "organ", r"(^right .*bronchial tree|right main bronchus|^(lateral|medial) segmental bronchial tree)"),
    R("lungs_left", "Left lung airways", "organ", r"(^left .*bronchial tree|left main bronchus|lingular bronchial tree)"),
    R("airways", "Bronchial tree", "organ", r"(bronchial tree|main bronchus)"),
    R("larynx_ligaments", "Larynx ligaments and membranes", "organ",
      r"(ligament|membrane|aryepiglotticus|cricothyroid$|cricothyroid)"),
    # digestive
    R("liver_segments", "Liver segments", "organ", r"(hepatovenous segment|caudate lobe of liver|^parenchyma)"),
    R("biliary", "Bile ducts", "organ", r"(biliary tree|hepatic duct|cystic duct|duct of caudate)"),
    U("liver_system", "Liver and bile ducts", "organ", ["liver_segments", "biliary", "gallbladder"]),
    R("gallbladder", "Gallbladder", "organ", r"^gallbladder$"),
    R("pancreas_grp", "Pancreas and its duct", "organ", r"(pancrea)"),
    R("jejunum", "Jejunum", "organ", r"part of jejunum"),
    R("ileum", "Ileum", "organ", r"part of ileum"),
    U("small_intestine", "Small intestine", "organ", ["jejunum", "ileum", "duodenum", "mesentery"]),
    R("duodenum", "Duodenum", "organ", r"^duodenum$"),
    R("mesentery", "Mesentery", "organ", r"^mesentery of small intestine"),
    R("colon", "Colon", "organ", r"(ascending colon|transverse colon|descending colon|taenia|mesocolon)"),
    U("large_intestine", "Large intestine", "organ", ["colon", "appendix_grp", "rectum", "ileocecal"]),
    R("appendix_grp", "Appendix", "organ", r"(appendix|mesoappendix)"),
    R("rectum", "Rectum", "organ", r"^rectum$"),
    R("ileocecal", "Ileocecal junction", "organ", r"ileocecal"),
    R("mouth_parts", "Mouth, tongue and salivary glands", "organ", r"(tongue|sublingual gland|submandibular gland|subdivision of mouth)", sided=True),
    R("gut_upper", "Oesophagus and stomach", "organ", r"^(esophagus|stomach)$"),
    # urinary / reproductive / endocrine
    R("kidneys", "Kidneys", "organ", r"kidney", sided=True),
    R("ureters", "Ureters", "organ", r"ureter", sided=True),
    R("urinary_lower", "Bladder and urethra", "organ", r"(urinary bladder|urethra)"),
    R("testes", "Testes and epididymes", "organ", r"(testis|epididymis)", sided=True),
    R("deferent", "Deferent ducts and seminal vesicles", "organ", r"(deferent duct|seminal vesicle)", sided=True),
    R("penis", "Penis", "organ", r"(corpus cavernosum|corpus spongiosum|glans penis)"),
    R("adrenals", "Adrenal glands", "organ", r"adrenal gland", sided=True),
    R("thymus", "Thymus", "organ", r"thymus", sided=True),
]

# Group names to show for "system" level and the whole-layer level.
SYSTEM_LABELS = {
    "nervous": "Nervous system organs", "cardiovascular": "Heart organs", "respiratory": "Respiratory organs",
    "digestive": "Digestive organs", "urinary": "Urinary organs", "endocrine": "Endocrine and lymphoid organs",
    "reproductive": "Reproductive organs", "musculoskeletal": "Musculoskeletal organs", "integumentary": "Skin organs",
}
LAYER_LABELS = {"bone": "All bones", "muscle": "All muscles", "organ": "All organs", "skin": "All skin",
                "vessel": "All blood vessels", "nerve": "All nerves"}
VESSEL_KINDS = {
    "artery": ("arteries", "All arteries"), "pulmonary_artery": ("pulmonary_arteries", "Pulmonary arteries"),
    "vein": ("veins", "All veins"), "pulmonary_vein": ("pulmonary_veins", "Pulmonary veins"),
    "portal_vein": ("portal_veins", "Portal vein system"),
}
