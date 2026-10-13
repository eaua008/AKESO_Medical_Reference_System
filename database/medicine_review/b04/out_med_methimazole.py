DM = "https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=2185e6e0-7c21-4348-a7b4-d898f50a0184"
EU = "https://docetp.mpa.se/LMF/Thiamazole%20Uni-Pharma%20tablet%20SmPC_09001bee807a75ba.pdf"
PNF = "https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf"
WHOEML = "https://list.essentialmeds.org/medicines/506"

MED = {
  "id": "med_methimazole",
  "desc_add": "In the Philippines it is listed in the PNF Essential Medicines List as 5 mg and 10 mg tablets, and it was added to the WHO Model List of Essential Medicines in 2019 for thyrotoxicosis. It is the preferred antithyroid drug in children because propylthiouracil has caused severe liver injury in children. It is well absorbed (bioavailability about 93%) with a plasma half-life of 3–5 hours that lengthens in liver or kidney impairment, yet the maintenance dose can be taken once daily.",
  "facts": {
    "indication": [
      "Hyperthyroidism in children from 3 years of age (EU label)",
    ],
    "adverse": [
      "Aplastic anaemia, thrombocytopenia, leukopenia and pancytopenia",
      "Insulin autoimmune syndrome (marked hypoglycaemia, can cause coma)",
      "Acute pancreatitis (postmarketing; recurs faster on re-exposure)",
      "Hypoprothrombinaemia with bleeding risk",
      "Loss or change of taste, hair loss, salivary gland swelling, lymphadenopathy",
      "Drug fever, neuritis/polyneuropathy, nephritis (very rare)",
      "Hypothyroidism if the dose is too high",
    ],
    "contraindication": [
      "Severe hypersensitivity to other thionamides (carbimazole, propylthiouracil)",
      "Moderate to severe granulocytopenia",
      "Pre-existing cholestasis not caused by hyperthyroidism",
      "Previous acute pancreatitis after thiamazole or carbimazole",
      "Combination with thyroid hormone (levothyroxine) during pregnancy",
    ],
    "interaction": [
      "Other drugs known to cause agranulocytosis: use with particular care.",
    ],
    "brand_ph": [],
    "brand_intl": [],
  },
  "refs": [
    ("DailyMed (US National Library of Medicine)", "Methimazole tablets, USP. Prescribing information. Upsher-Smith Laboratories, LLC; revised 12/2023. DailyMed.", DM),
    ("Swedish Medical Products Agency (Läkemedelsverket)", "Thiamazole Uni-Pharma 5 mg tablets. Summary of Product Characteristics. Uni-Pharma Kleon Tsetis Pharmaceutical Laboratories S.A.; text revised 2022-10-04.", EU),
    ("Philippine National Formulary (PhilHealth)", "Philippine National Formulary Essential Medicines List (PNF-EML), 2022. Department of Health / PhilHealth.", PNF),
    ("WHO Model List of Essential Medicines", "World Health Organization. eEML – Electronic Essential Medicines List: Methimazole (first added 2019, TRS 1021).", WHOEML),
  ],
  "links": [],
  "sources": [
    ("Label · DailyMed", "DailyMed (US National Library of Medicine)", "Methimazole tablets, USP. Upsher-Smith Laboratories; revised 12/2023.", DM),
    ("Label · EU SmPC", "Swedish Medical Products Agency (Läkemedelsverket)", "Thiamazole Uni-Pharma 5 mg tablets SmPC; text revised 2022-10-04.", EU),
    ("PNF", "Philippine National Formulary (PhilHealth)", "PNF Essential Medicines List, 2022.", PNF),
  ],
  "doses": [
    ("adult", "Hyperthyroidism, mild (initial)", "PO", "15 mg/day ÷ 3", "Every 8 h", "Until euthyroid", "—", "Label · DailyMed", ""),
    ("adult", "Hyperthyroidism, moderately severe (initial)", "PO", "30–40 mg/day ÷ 3", "Every 8 h", "Until euthyroid", "—", "Label · DailyMed", ""),
    ("adult", "Hyperthyroidism, severe (initial)", "PO", "60 mg/day ÷ 3", "Every 8 h", "Until euthyroid", "—", "Label · DailyMed", ""),
    ("adult", "Hyperthyroidism (maintenance)", "PO", "5–15 mg/day", "Once a day or divided", "Long-term", "—", "Label · DailyMed", "Lower the dose if TSH rises"),
    ("adult", "Hyperthyroidism, mild (initial)", "PO", "10–20 mg/day", "Once or 2× a day", "Until euthyroid", "—", "Label · EU SmPC", ""),
    ("adult", "Hyperthyroidism, severe (initial)", "PO", "30–40 mg/day", "Divided doses", "Until euthyroid", "—", "Label · EU SmPC", "Higher start may be needed with large goitre or after iodine exposure"),
    ("adult", "Hyperthyroidism (maintenance)", "PO", "5–10 mg", "Once a day", "Long-term", "—", "Label · EU SmPC", "Morning, with or after breakfast; levothyroxine may be added"),
    ("child", "Hyperthyroidism (initial)", "PO", "0.4 mg/kg/day ÷ 3", "Every 8 h", "Until euthyroid", "—", "Label · DailyMed", "Maintenance about half the initial dose"),
    ("child", "Hyperthyroidism, 3–17 years (initial)", "PO", "0.5 mg/kg/day ÷ 2–3", "2–3× a day", "Until euthyroid", "40 mg/day", "Label · EU SmPC", "Not recommended at 2 years or younger"),
  ],
  "notes": [
    ("renal", "Half-life is prolonged; individualise the dose, use the lowest effective dose and follow up closely.", "", "Label · EU SmPC"),
    ("hepatic", "Clearance is reduced; use the lowest possible dose with close monitoring.", "", "Label · EU SmPC"),
    ("pregnancy", "Women of childbearing potential should use effective contraception. If used in pregnancy, give the lowest effective dose without added thyroid hormone; excess dosing can cause fetal goitre and hypothyroidism. Reported first-trimester defects include aplasia cutis, craniofacial malformations, omphalocele and oesophageal atresia. Breastfeeding: possible at up to 10 mg/day without added thyroid hormone, checking the infant's thyroid function regularly.", "", "Label · EU SmPC"),
    ("administration", "Swallow with fluid; do not chew (bitter). High starting doses can be spread over the day; give the maintenance dose once in the morning. Do not stop methimazole and continue levothyroxine alone.", "", "Label · EU SmPC"),
    ("forms_ph", "Methimazole (thiamazole) 5 mg and 10 mg oral tablet.", "", "PNF"),
    ("monitor", "Blood count before and after starting, and at once if fever, sore throat or mouth ulcers appear (stop if agranulocytosis); liver tests if anorexia, itching or right upper abdominal pain (stop if transaminases exceed 3× the upper limit of normal); TSH and free T4 regularly to avoid hypothyroidism; prothrombin time/INR especially before surgery. (Blood count before/after start from EU SmPC; rest from DailyMed label.)", "", ""),
  ],
  "checked": [
    (PNF, "PNF-EML lists 'Methimazole (thiamazole) Oral: 5 mg and 10 mg tablet'."),
    (DM, "Upsher-Smith methimazole label (rev 12/2023): adults initial 15 mg/day mild, 30–40 mg moderately severe, 60 mg severe, in 3 doses ~8 h apart; maintenance 5–15 mg/day; pediatric 0.4 mg/kg/day ÷3, maintenance ~half; agranulocytosis warning; stop if transaminases >3× ULN; hepatotoxicity lower than PTU; TSH/FT4 monitoring; prothrombin time before surgery (hypoprothrombinaemia); vasculitis ANCA-positive; preferred in pediatrics over PTU; ADRs incl. aplastic anaemia, thrombocytopenia, insulin autoimmune syndrome (hypoglycaemic coma), periarteritis, hypoprothrombinaemia, nephritis, loss of taste, hair loss, sialadenopathy, lymphadenopathy, drug fever; postmarketing acute pancreatitis; nursing: monitor mother's thyroid every 1–2 weeks."),
    (EU, "Thiamazole Uni-Pharma 5 mg SmPC (MPA Sweden, rev 2022-10-04): adults ≥3 y indication; severe 30–40 mg/day divided, mild 10–20 mg/day (1–2 doses), maintenance 5–10 mg/day once in morning; higher start with large goitre/prior iodine; children 3–17 y 0.5 mg/kg/day in 2–3 doses, max 40 mg/day; ≤2 y not recommended; hepatic/renal lowest dose; contraindications: thionamide hypersensitivity, moderate–severe granulocytopenia, pre-existing cholestasis, previous bone marrow damage or pancreatitis after thiamazole/carbimazole, thyroid hormone combination in pregnancy; agranulocytosis 0.3–0.6%, blood count before/after start; pancreatitis recurrence on re-exposure; contraception; don't stop thiamazole and continue levothyroxine alone; malformations list; breastfeeding up to 10 mg/day; ADRs neuritis, polyneuropathy, nephritis, autoimmune insulin syndrome; bioavailability 93%, t½ 3–5 h, longer in hepatic/renal impairment; swallow with fluid, don't chew."),
    (WHOEML, "WHO eEML: methimazole (thiamazole), thyroid/antithyroid section, oral tablet 5 mg and 10 mg, first added 2019 (TRS 1021), thyrotoxicosis."),
  ],
}
