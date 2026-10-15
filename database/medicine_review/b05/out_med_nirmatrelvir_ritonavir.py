SMPC_URL = "https://products.mhra.gov.uk/search/?search=nirmatrelvir#emc-13145"
WHO_URL = "https://www.who.int/news/item/22-04-2022-who-recommends-highly-successful-covid-19-therapy-and-calls-for-wide-geographical-distribution-and-transparency-from-originator"

MED = {
  "id": "med_nirmatrelvir_ritonavir",
  "desc_add": "WHO strongly recommends it for non-severe COVID-19 in patients at highest risk of hospitalisation (such as unvaccinated, older or immunosuppressed people), where it cut hospitalisation by about 85%, but not for lower-risk patients, in whom the benefit was negligible. Because it only works early in the illness, prompt testing is essential to its use.",
  "facts": {
    "indication": [
      "Severely immunocompromised patients: a 10-day course may be considered to reduce virological rebound (limited data)",
    ],
    "adverse": [
      "Headache, nausea",
      "Vomiting, abdominal pain (uncommon)",
      "Malaise (rare)",
    ],
    "contraindication": [
      "Severe hepatic impairment (Child-Pugh C)",
      "Co-administration with colchicine (life-threatening and fatal interactions reported)",
      "Co-administration with quetiapine, lurasidone, pimozide, triazolam or oral midazolam",
      "Co-administration with alfuzosin, ranolazine, ivabradine, eplerenone, finerenone, tolvaptan or ergot derivatives",
      "Sildenafil when used for pulmonary arterial hypertension",
    ],
    "interaction": [
      "Combined hormonal contraceptives: ethinylestradiol exposure falls about 40%; use barrier/non-hormonal contraception during treatment and for one menstrual cycle after.",
      "Sildenafil/tadalafil for erectile dysfunction: limit sildenafil to 25 mg per 48 h and tadalafil to 10 mg per 72 h.",
      "Salmeterol: avoid (large rise in exposure).",
      "Rivaroxaban: not recommended with ritonavir.",
      "Atorvastatin/rosuvastatin: consider pausing; pravastatin or fluvastatin preferred if a statin is needed.",
      "Levothyroxine: monitor TSH for at least the first month after starting or stopping ritonavir.",
      "Parenteral midazolam: only in an ICU-type setting with close monitoring.",
    ],
    "brand_ph": [],
    "brand_intl": [],
  },
  "refs": [
    ("UK SmPC (emc)", "Paxlovid 150 mg/100 mg film-coated tablets. Summary of Product Characteristics. Pfizer Ltd; revised 15 September 2026. electronic medicines compendium (emc).", SMPC_URL),
    ("World Health Organization", "WHO recommends highly successful COVID-19 therapy and calls for wide geographical distribution and transparency from originator. WHO news release, 22 April 2022.", WHO_URL),
  ],
  "links": [
    ("hiv_infection", "caution", "Risk of HIV-1 protease inhibitor resistance in uncontrolled or undiagnosed HIV; patients already on ritonavir/cobicistat regimens need no dose change (UK SmPC)."),
    ("gout", "caution", "Colchicine is contraindicated with it (fatal interactions reported); review gout medicines before starting (UK SmPC)."),
    ("tuberculosis", "caution", "Contraindicated with rifampicin or rifapentine (loss of antiviral effect, resistance), so patients on rifamycin-based TB treatment should not take it (UK SmPC)."),
    ("heart_failure", "caution", "Several heart-failure and antiarrhythmic drugs are contraindicated with it (amiodarone, dronedarone, eplerenone, ivabradine, finerenone, tolvaptan); our inference from the SmPC interaction list."),
  ],
  "sources": [
    ("Label · UK SmPC", "UK SmPC (emc)", "Paxlovid 150 mg/100 mg film-coated tablets. Summary of Product Characteristics. Pfizer Ltd; 15 September 2026.", SMPC_URL),
    ("WHO 2022", "World Health Organization", "WHO recommends highly successful COVID-19 therapy... WHO news release, 22 April 2022.", WHO_URL),
  ],
  "doses": [
    ("adult", "COVID-19, high risk (eGFR ≥60)", "PO", "Nirmatrelvir 300 mg + ritonavir 100 mg", "Every 12 h", "5 days", "—", "Label · UK SmPC", "Start within 5 days of symptoms"),
    ("adult", "COVID-19, eGFR 30–59", "PO", "Nirmatrelvir 150 mg + ritonavir 100 mg", "Every 12 h", "5 days", "—", "Label · UK SmPC", ""),
    ("adult", "COVID-19, eGFR <30 or haemodialysis", "PO", "300/100 mg day 1, then 150/100 mg", "Once a day", "5 days", "—", "Label · UK SmPC", "Give after dialysis on HD days"),
    ("adult", "COVID-19, severely immunocompromised", "PO", "Nirmatrelvir 300 mg + ritonavir 100 mg", "Every 12 h", "10 days", "—", "Label · UK SmPC", "May reduce rebound; limited data"),
  ],
  "notes": [
    ("renal", "No dose adjustment.", "eGFR ≥60", "Label · UK SmPC"),
    ("renal", "Nirmatrelvir 150 mg + ritonavir 100 mg twice daily for 5 days.", "eGFR 30–59", "Label · UK SmPC"),
    ("renal", "300/100 mg once on day 1, then 150/100 mg once daily on days 2–5; after haemodialysis on dialysis days. Discard extra tablets in the pack.", "eGFR <30 / HD", "Label · UK SmPC"),
    ("hepatic", "No adjustment in Child-Pugh A or B; contraindicated in Child-Pugh C. Use with caution in pre-existing liver disease or raised liver enzymes.", "", "Label · UK SmPC"),
    ("elderly", "No dose adjustment. Not established under 18 years.", "", "Label · UK SmPC"),
    ("pregnancy", "Use in pregnancy only if benefit outweighs risk (limited human data). Stop breastfeeding during treatment and for 48 h after the last dose.", "", "Label · UK SmPC"),
    ("administration", "Take the 3 tablets together, with or without food; swallow whole, do not chew, break or crush. Missed dose: take if ≤8 h late, otherwise skip. If hospitalised after starting, the 5-day course may be completed.", "", "Label · UK SmPC"),
    ("monitor", "Review every concomitant medicine (including herbal St John's wort) before and during treatment; stop lovastatin/simvastatin ≥12 h before, during and for 5 days after.", "", "Label · UK SmPC"),
    ("monitor", "Check tacrolimus/ciclosporin/sirolimus levels closely with specialist input; check INR on warfarin.", "", "Label · UK SmPC"),
    ("monitor", "Stop at signs of anaphylaxis or severe skin reaction; check liver tests if hepatitis symptoms appear.", "", "Label · UK SmPC"),
  ],
  "checked": [
    (SMPC_URL, "Paxlovid UK SmPC revised 15 Sep 2026: 300/100 mg q12h x5 days; eGFR 30–<60 150/100 mg BID; eGFR <30 incl HD 300/100 day 1 then 150/100 daily days 2–5 after dialysis; missed dose 8 h; complete course if hospitalised; 10-day course in severely immunocompromised (limited data); Child-Pugh A/B no adjustment, C contraindicated; elderly no adjustment; <18 not established; swallow whole; contraindicated list incl colchicine, quetiapine, lurasidone, pimozide, alfuzosin, ranolazine, ivabradine, eplerenone, finerenone, tolvaptan, ergots, sildenafil for PAH, triazolam, oral midazolam, amiodarone, dronedarone, rifampicin, rifapentine; HIV-1 PI resistance warning; ethinylestradiol AUC -40% and barrier contraception for one cycle; sildenafil ED 25 mg/48 h, tadalafil 10 mg/72 h; salmeterol avoid; rivaroxaban not recommended; statin advice incl stop simvastatin/lovastatin 12 h before and 5 days after, pravastatin/fluvastatin preferred; levothyroxine TSH; parenteral midazolam ICU; breastfeeding stop for 48 h; AEs: common dysgeusia, headache, diarrhoea, nausea; uncommon vomiting, abdominal pain, hypertension; rare malaise. PH forms not confirmed (PNF text ends at M)."),
    (WHO_URL, "WHO 22 Apr 2022: strong recommendation for non-severe COVID-19 at highest risk of hospitalisation (unvaccinated, older, immunosuppressed); 85% reduction in hospitalisation; not recommended for lower-risk patients (negligible benefit); prompt testing essential as works only early."),
  ],
}
