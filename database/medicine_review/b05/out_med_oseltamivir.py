SMPC_URL = "https://products.mhra.gov.uk/search/?search=oseltamivir#emc-1194"
CDC_URL = "https://www.cdc.gov/flu/hcp/antivirals/summary-clinicians.html"
EML_URL = "https://list.essentialmeds.org/recommendations/511"

MED = {
  "id": "med_oseltamivir",
  "desc_add": "WHO lists oseltamivir on the complementary Essential Medicines List (30, 45 and 75 mg capsules; 6 mg/mL powder for oral liquid for children), limited to severe confirmed or suspected influenza in critically ill hospitalized patients. CDC advises starting it without waiting for test results in hospitalized, severely ill or high-risk patients, and in hospitalized patients even when more than 48 hours have passed since symptom onset. It is the preferred antiviral in pregnancy and does not replace influenza vaccination.",
  "facts": {
    "indication": [
      "Treatment of influenza in hospitalized or severe, complicated or progressive illness, even if started more than 48 hours after onset (CDC)",
      "Treatment of influenza in infants under 1 year, including full-term neonates",
      "Seasonal prophylaxis in exceptional situations (e.g., vaccine-strain mismatch or pandemic); post-exposure prophylaxis in infants under 1 year only during a pandemic (UK SmPC)",
    ],
    "adverse": [
      "Vomiting is the most common effect in children; also conjunctivitis, earache, otitis media, cough and nasal congestion",
      "Hepatitis, jaundice and hepatic failure (rare, some fatal)",
      "Gastrointestinal bleeding (rare)",
      "Angioedema",
      "Convulsions",
      "Thrombocytopenia, visual disturbance and cardiac arrhythmia (listed in the UK SmPC)",
    ],
    "contraindication": [],
    "interaction": [
      "Probenecid: roughly doubles exposure to the active metabolite; no dose change with normal renal function.",
      "Renally excreted drugs with a narrow margin (e.g., chlorpropamide, methotrexate, phenylbutazone): use with caution.",
      "No interactions reported with paracetamol, aspirin, cimetidine, antacids, warfarin or amoxicillin.",
    ],
    "brand_ph": [],
    "brand_intl": [],
  },
  "refs": [
    ("UK SmPC (emc)", "Tamiflu 30 mg, 45 mg and 75 mg hard capsules. Summary of Product Characteristics. Roche Products Ltd; revised January 2021. electronic medicines compendium (emc).", SMPC_URL),
    ("CDC", "Centers for Disease Control and Prevention. Influenza Antiviral Medications: Summary for Clinicians. Last reviewed 10 March 2026.", CDC_URL),
    ("WHO eEML", "World Health Organization. Electronic Essential Medicines List – Oseltamivir (complementary list, section 6.4.3).", EML_URL),
  ],
  "links": [
    ("chronic_kidney_disease", "caution", "Dose must be reduced when CrCl is 60 mL/min or less; not recommended at CrCl 10 or below without dialysis (UK SmPC, CDC)."),
  ],
  "sources": [
    ("Label · UK SmPC", "UK SmPC (emc)", "Tamiflu hard capsules. SmPC. Roche; January 2021.", SMPC_URL),
    ("CDC", "CDC", "CDC. Influenza Antiviral Medications: Summary for Clinicians. March 2026.", CDC_URL),
  ],
  "doses": [
    ("adult", "Treatment (≥13 y, >40 kg)", "PO", "75 mg", "2× a day", "5 days (10 days if immunocompromised)", "—", "Label · UK SmPC", "Start within 2 days of onset"),
    ("adult", "Post-exposure prophylaxis", "PO", "75 mg", "Once a day", "10 days", "—", "Label · UK SmPC", "Start within 2 days of exposure; CDC: 7 days after last exposure"),
    ("adult", "Prophylaxis during a community epidemic", "PO", "75 mg", "Once a day", "Up to 6 weeks (12 weeks if immunocompromised)", "—", "Label · UK SmPC", ""),
    ("adult", "Institutional outbreak prophylaxis", "PO", "75 mg", "Once a day", "≥2 weeks, until 1 week after last case", "—", "CDC", ""),
    ("child", "Treatment (≥1 y, ≤15 kg)", "PO", "30 mg", "2× a day", "5 days", "—", "Label · UK SmPC", "UK SmPC band 10–15 kg"),
    ("child", "Treatment (≥1 y, >15–23 kg)", "PO", "45 mg", "2× a day", "5 days", "—", "Label · UK SmPC", ""),
    ("child", "Treatment (≥1 y, >23–40 kg)", "PO", "60 mg", "2× a day", "5 days", "—", "Label · UK SmPC", ""),
    ("child", "Treatment (≥1 y, >40 kg)", "PO", "75 mg", "2× a day", "5 days", "—", "Label · UK SmPC", ""),
    ("child", "Prophylaxis (≥1 y)", "PO", "Same weight-band dose as treatment", "Once a day", "10 days", "75 mg", "Label · UK SmPC", "CDC: 7 days after last exposure"),
    ("child", "Treatment (<1 y)", "PO", "3 mg/kg", "2× a day", "5 days (10 days if immunocompromised)", "—", "Label · UK SmPC", "AAP (via CDC): 3.5 mg/kg for 9–11 months"),
    ("child", "Prophylaxis (3 mo to <1 y)", "PO", "3 mg/kg", "Once a day", "10 days", "—", "Label · UK SmPC", "UK: pandemic only; CDC: not under 3 months unless critical"),
    ("neonate", "Treatment, preterm (PMA <38 wk)", "PO", "1 mg/kg", "2× a day", "5 days", "—", "CDC", "Not licensed below 36 weeks post-conceptual age (UK)"),
    ("neonate", "Treatment, preterm (PMA 38–40 wk)", "PO", "1.5 mg/kg", "2× a day", "5 days", "—", "CDC", ""),
  ],
  "notes": [
    ("renal", "Treatment 30 mg 2× a day; prophylaxis 30 mg once a day.", "CrCl 30–60", "Label · UK SmPC"),
    ("renal", "Treatment 30 mg once a day; prophylaxis 30 mg every second day.", "CrCl 10–30", "Label · UK SmPC"),
    ("renal", "Not recommended (no data) unless on dialysis.", "CrCl ≤10", "Label · UK SmPC"),
    ("renal", "Haemodialysis: treatment 30 mg after each session; prophylaxis 30 mg after every second session. CDC: treatment no longer than 5 days.", "Haemodialysis", "Label · UK SmPC"),
    ("renal", "Peritoneal dialysis: treatment 30 mg single dose; prophylaxis 30 mg once a week.", "Peritoneal dialysis", "Label · UK SmPC"),
    ("renal", "No dosing data for children 12 years and under with renal impairment.", "Children", "Label · UK SmPC"),
    ("hepatic", "No dose adjustment needed.", "", "Label · UK SmPC"),
    ("elderly", "No dose adjustment unless moderate or severe renal impairment.", "", "Label · UK SmPC"),
    ("pregnancy", "Preferred antiviral in pregnancy, at the same dose as in non-pregnant adults (CDC). Over 1,000 first-trimester exposures showed no malformative toxicity (UK SmPC). Passes into breast milk in small amounts; may be used when there is clear benefit.", "", "CDC"),
    ("administration", "Can be taken with or without food (food does not change levels); taking it with food may reduce nausea and vomiting. If capsules cannot be swallowed, use the oral suspension; a pharmacy-made 6 mg/mL suspension is preferred, otherwise mix capsule contents with no more than a teaspoon of sweetened food and swallow at once.", "", "Label · UK SmPC"),
    ("administration", "Critically ill adults: standard doses are adequately absorbed by mouth or feeding tube; doubling to 150 mg 2× a day may not add benefit. Extend beyond 5 days if still severely ill.", "", "CDC"),
    ("monitor", "Watch behaviour closely, especially in children and adolescents, for neuropsychiatric events (delirium, self-injury, convulsions).", "", "Label · UK SmPC"),
    ("monitor", "Check creatinine clearance before dosing and adjust for renal function.", "", "Label · UK SmPC"),
  ],
  "checked": [
    (SMPC_URL, "Tamiflu 30/45/75 mg capsules SmPC (Roche, rev. Jan 2021): treatment incl. full-term neonates; seasonal prophylaxis in exceptional situations; infants <1 y PEP pandemic only; adult 75 mg BID 5 d (10 d immunocompromised), PEP 75 mg OD 10 d, epidemic up to 6 wk (12 wk immunocompromised); child weight bands 10–15/15–23/23–40/>40 kg 30/45/60/75 mg BID 5 d, same OD 10 d prophylaxis; infants 3 mg/kg BID 5 d, PEP 3 mg/kg OD 10 d; not for <36 wk PCA; renal treatment and prophylaxis tables incl. HD, PD, ≤10 not recommended; no child renal data; hepatic none; elderly; suspension/6 mg/mL compounded/teaspoon sweetened food; food no effect on levels; neuropsychiatric monitoring; probenecid doubles exposure; caution chlorpropamide/methotrexate/phenylbutazone; no interaction with paracetamol, aspirin, cimetidine, antacids, rimantadine, warfarin, amoxicillin; pregnancy >1,000 exposures, breastfeeding; AEs children vomiting, conjunctivitis, earache, otitis media; hepatitis/hepatic failure, angioedema, GI bleeding, convulsions; thrombocytopenia, visual disturbance, arrhythmia in table (frequency unclear)."),
    (CDC_URL, "CDC Summary for Clinicians (last reviewed 10 Mar 2026): treat hospitalized/severe/high-risk without waiting for confirmation, benefit even >48 h in hospitalized; dosing tables incl. AAP 3.5 mg/kg for 9–11 mo, preterm 1.0 mg/kg (<38 wk PMA), 1.5 mg/kg (38–40 wk), 3.0 mg/kg (>40 wk); prophylaxis 7 days after last exposure, infants 3 mo–<1 y 3 mg/kg OD, <3 mo not unless critical, institutional ≥2 wk to 1 wk after last case; critically ill standard doses absorbed, 150 mg BID may not add benefit, extend if severely ill; renal HD treatment not more than 5 days; pregnancy preferred, same dose; GI AEs less likely with food."),
    (EML_URL, "WHO eEML oseltamivir: section 6.4.3, complementary list; 6 mg/mL powder for oral liquid (children), 30/45/75 mg capsules; limited to severe confirmed/suspected influenza in critically ill hospitalized patients; added 2011, changed 2025."),
    ("https://www.who.int/publications/i/item/9789240097759", "WHO Clinical practice guidelines for influenza (Sept 2024): landing page opened but recommendation text was not readable (nor on the MagicApp summary), so not cited."),
    ("https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf", "Read with offset 64000: text covers Midazolam to Moxifloxacin only; oseltamivir entry not readable, so no forms_ph note."),
  ],
}
