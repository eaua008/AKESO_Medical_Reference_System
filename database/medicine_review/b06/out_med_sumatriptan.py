UK_TAB = "https://products.mhra.gov.uk/search/?search=sumatriptan#emc-524"
UK_INJ = "https://products.mhra.gov.uk/search/?search=sumatriptan#emc-944"
UK_NAS = "https://products.mhra.gov.uk/search/?search=sumatriptan#emc-2214"
PH_SURVEY = "https://neurology-asia.org/system/index.php/neuro/article/view/675"

MED = {
  "id": "med_sumatriptan",
  "desc_add": "Sumatriptan is also given as a nasal spray, which UK labeling allows for adolescents aged 12–17 under specialist advice. In a 2022 survey of Filipino neurologists, NSAIDs were the most preferred acute migraine drugs and about half would not consider a triptan even for moderate to severe episodic attacks, so triptans remain little used in the Philippines.",
  "facts": {
    "indication": [
      "Acute migraine in adolescents 12–17 years (nasal spray, specialist recommendation; UK labeling)",
    ],
    "adverse": [
      "Flushing, dyspnoea, nausea and vomiting",
      "Transient rise in blood pressure; hypotension, bradycardia or tachycardia",
      "Visual disturbance (flickering, diplopia, scotoma, reduced vision)",
      "Tremor, dystonia, nystagmus",
      "Raynaud's phenomenon and ischaemic colitis",
      "Hypersensitivity reactions up to anaphylaxis",
      "Medication overuse headache with frequent use",
    ],
    "contraindication": [
      "Moderate or severe hypertension (and mild uncontrolled hypertension)",
      "Previous myocardial infarction",
      "Intravenous administration (vasospasm risk)",
    ],
    "interaction": [
      "Lithium: possible serotonin syndrome.",
      "St John's wort: adverse effects may be more frequent.",
      "After sumatriptan wait at least 6 hours before ergotamine and 24 hours before another triptan.",
      "No interaction with propranolol, flunarizine, pizotifen or alcohol.",
    ],
    "brand_ph": [],
    "brand_intl": [],
  },
  "refs": [
    ("UK SmPC (emc)", "Sumatriptan 50 mg tablets. Summary of Product Characteristics. Milpharm Ltd; revised 9 June 2026. electronic medicines compendium (emc).", UK_TAB),
    ("UK SmPC (emc)", "Imigran Injection / Imigran Subject (sumatriptan 6 mg). Summary of Product Characteristics. GlaxoSmithKline UK; revised 15 October 2025. emc.", UK_INJ),
    ("UK SmPC (emc)", "Imigran 10 mg Nasal Spray. Summary of Product Characteristics. GlaxoSmithKline UK; revised 15 October 2025. emc.", UK_NAS),
    ("Neurology Asia", "Roxas AA Jr, Quiles LE, Diamante PA. The practice patterns of migraine management among neurologists in the Philippines: a cross-sectional survey. Neurology Asia. 2022;27(3):717-724.", PH_SURVEY),
  ],
  "links": [
    ("hypertension", "avoid", "Contraindicated in moderate or severe hypertension and in mild uncontrolled hypertension; use with caution in mild controlled hypertension (UK SmPC)."),
    ("chronic_kidney_disease", "caution", "UK SmPC advises caution in impaired renal function; no specific dose adjustment given."),
  ],
  "sources": [
    ("Label · UK SmPC", "UK SmPC (emc)", "Sumatriptan 50 mg tablets. Summary of Product Characteristics. Milpharm Ltd; revised 9 June 2026.", UK_TAB),
    ("Label · UK SmPC inj", "UK SmPC (emc)", "Imigran Injection (sumatriptan 6 mg). Summary of Product Characteristics. GlaxoSmithKline UK; revised 15 October 2025.", UK_INJ),
    ("Label · UK SmPC nasal", "UK SmPC (emc)", "Imigran 10 mg Nasal Spray. Summary of Product Characteristics. GlaxoSmithKline UK; revised 15 October 2025.", UK_NAS),
  ],
  "doses": [
    ("adult", "Acute migraine", "PO", "50 mg (some need 100 mg)", "Single dose; repeat once if it recurs, ≥2 h apart", "Per attack", "300 mg/24 h", "Label · UK SmPC", "No second dose if the first fails; use paracetamol, aspirin or an NSAID"),
    ("adult", "Acute migraine", "SC", "6 mg", "Single dose; repeat once if it recurs, ≥1 h apart", "Per attack", "12 mg/24 h", "Label · UK SmPC inj", "Never IV"),
    ("adult", "Cluster headache attack", "SC", "6 mg", "Per attack, ≥1 h apart", "Per attack", "12 mg/24 h", "Label · UK SmPC inj", ""),
    ("adult", "Acute migraine", "Nasal", "20 mg (some respond to 10 mg)", "Single dose; repeat once if it recurs, ≥2 h apart", "Per attack", "40 mg/24 h", "Label · UK SmPC nasal", "Into one nostril"),
    ("child", "Acute migraine, 12–17 years", "Nasal", "10 mg", "Single dose; repeat once if it recurs, ≥2 h apart", "Per attack", "20 mg/24 h", "Label · UK SmPC nasal", "Specialist recommendation only; not under 12; tablets and injection not recommended under 18"),
  ],
  "notes": [
    ("renal", "No dose adjustment stated; use with caution in renal impairment.", "", "Label · UK SmPC"),
    ("hepatic", "Mild to moderate impairment: consider low doses of 25–50 mg orally. Contraindicated in severe impairment.", "", "Label · UK SmPC"),
    ("elderly", "Not recommended over 65 years because of limited experience.", "", "Label · UK SmPC"),
    ("pregnancy", "Over 1,000 first-trimester exposures without a clear rise in birth defects, but data are insufficient; use only if benefit outweighs risk. Relative infant dose in milk is below 4%; avoid breastfeeding and discard milk for 12 hours after a dose.", "", "Label · UK SmPC"),
    ("administration", "Use only when the diagnosis of migraine is clear; take at the first sign of the attack. Swallow tablets whole with water. The injection needle shield may contain latex.", "", "Label · UK SmPC inj"),
    ("monitor", "Assess cardiovascular risk before first use (smokers, nicotine replacement users, men over 40, postmenopausal women with risk factors). Stop if chest symptoms suggest ischaemia. Ask about headache days per month to detect medication overuse headache.", "", "Label · UK SmPC"),
  ],
  "checked": [
    (UK_TAB, "Milpharm sumatriptan 50 mg SmPC (rev 09/06/2026): 50 mg, some 100 mg; no second dose for non-response; recurrence repeat ≥2 h; max 300 mg/24 h; not recommended 10–17 y or >65; hepatic 25–50 mg, severe contraindicated; renal caution (4.4); swallow whole with water; 4.3 MI, moderate/severe and mild uncontrolled hypertension; 4.4 MOH, CV evaluation risk groups, seizures, sulphonamide; 4.5 lithium, St John's wort, 6 h/24 h rules, no interaction propranolol/flunarizine/pizotifen/alcohol; 4.6 >1000 exposures, RID <4%, avoid breastfeeding 12 h; 4.8 flushing, dyspnoea, nausea, BP rise, visual effects, tremor, dystonia, nystagmus, Raynaud's, ischaemic colitis, anaphylaxis."),
    (UK_INJ, "Imigran Injection SmPC (rev 15/10/2025): migraine 6 mg SC, repeat ≥1 h if recurrence, max 12 mg/24 h; cluster headache 6 mg per attack same limits; not <18 or >65; not IV (vasospasm); latex needle shield; injection-site pain very common."),
    (UK_NAS, "Imigran 10 mg Nasal Spray SmPC (rev 15/10/2025): adults 20 mg (some 10 mg) one nostril, repeat ≥2 h, max two 20 mg doses/24 h; adolescents 12–17 10 mg specialist only, max two 10 mg doses/24 h; not <12 or >65."),
    (PH_SURVEY, "Roxas et al., Neurology Asia 2022;27(3):717-724: NSAIDs most preferred acute migraine class (48.26%); about half would not consider triptans for moderate–severe episodic attacks; no PH forms/availability data."),
  ],
}
