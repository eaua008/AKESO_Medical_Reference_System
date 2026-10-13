PNF_URL = "https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf"
MSF_URL = "https://medicalguidelines.msf.org/viewport/EssDr/english/ivermectin-oral-16683965.html"
FDA_LABEL = "https://www.accessdata.fda.gov/drugsatfda_docs/label/2009/050742s024s025lbl.pdf"
WHO_COVID = "https://www.who.int/news-room/feature-stories/detail/who-advises-that-ivermectin-only-be-used-to-treat-covid-19-within-clinical-trials"

MED = {
  "id": "med_ivermectin",
  "desc_add": "In the Philippines it is on the national formulary as 3 mg and 6 mg tablets. It is dosed by body weight (about 200 micrograms/kg for strongyloidiasis and scabies, 150 micrograms/kg for onchocerciasis), and because food increases absorption the US label advises taking it on an empty stomach with water. WHO advises that ivermectin be used to treat COVID-19 only within clinical trials.",
  "facts": {
    "indication": [
      "Cutaneous larva migrans (200 micrograms/kg daily for 1–2 days, MSF)",
    ],
    "adverse": [
      "Mazzotti reactions in onchocerciasis: itching, fever, rash, joint pain, lymph node swelling, mostly in the first 4 days",
      "Tachycardia, peripheral oedema and orthostatic hypotension (onchocerciasis treatment)",
      "Raised ALT/AST; hepatitis and raised bilirubin reported after marketing",
      "Fatigue (strongyloidiasis treatment, ≤3%)",
    ],
    "contraindication": [],
    "interaction": [],
    "brand_ph": [],
    "brand_intl": [],
  },
  "refs": [
    ("Philippine National Formulary (PNF) EML", "Philippine National Formulary Essential Medicines List. PhilHealth / Department of Health, 2022.", PNF_URL),
    ("MSF Essential Drugs", "Médecins Sans Frontières. Essential drugs - practical guidelines: Ivermectin oral.", MSF_URL),
    ("FDA label (Stromectol)", "Merck Sharp & Dohme Corp. STROMECTOL (ivermectin) tablets - prescribing information. U.S. Food and Drug Administration; 2009.", FDA_LABEL),
    ("WHO - ivermectin and COVID-19", "World Health Organization. WHO advises that ivermectin only be used to treat COVID-19 within clinical trials. 31 March 2021.", WHO_COVID),
  ],
  "links": [
    ("covid19", "avoid", "WHO (2021) recommends ivermectin be used to treat COVID-19 only within clinical trials."),
  ],
  "sources": [
    ("Label · FDA US", "FDA label (Stromectol)", "STROMECTOL (ivermectin) tablets - prescribing information. Merck, 2009.", FDA_LABEL),
    ("MSF", "MSF Essential Drugs", "MSF Essential drugs: Ivermectin oral.", MSF_URL),
    ("PNF", "Philippine National Formulary (PNF) EML", "Philippine National Formulary Essential Medicines List. PhilHealth / DOH, 2022.", PNF_URL),
  ],
  "doses": [
    ("adult", "Strongyloidiasis", "PO", "200 micrograms/kg", "Single dose", "1 day", "—", "Label · FDA US", "3 mg tabs: 15–24 kg 1, 25–35 kg 2, 36–50 kg 3, 51–65 kg 4, 66–79 kg 5"),
    ("adult", "Scabies (ordinary)", "PO", "200 micrograms/kg", "Single dose; repeat after 1 week", "2 doses", "—", "MSF", "Second dose lowers risk of failure"),
    ("adult", "Crusted scabies", "PO", "200 micrograms/kg", "2 doses 1 week apart (more if needed)", "—", "—", "MSF", "With topical keratolytic and scabicide"),
    ("adult", "Onchocerciasis", "PO", "150 micrograms/kg", "Single dose", "Repeat every 6–12 months", "—", "MSF", "Second dose at 3 months if signs persist; 3 mg tabs: 15–<25 kg 1, 25–<45 kg 2, 45–<65 kg 3, ≥65 kg 4"),
    ("adult", "Cutaneous larva migrans", "PO", "200 micrograms/kg", "Once a day", "1–2 days", "—", "MSF", ""),
    ("child", "Strongyloidiasis / scabies (≥15 kg)", "PO", "200 micrograms/kg", "Single dose (scabies: repeat after 1 week)", "—", "—", "MSF", "Not under 15 kg; tablets may be crushed"),
    ("child", "Onchocerciasis (≥15 kg)", "PO", "150 micrograms/kg", "Single dose", "Repeat every 6–12 months", "—", "MSF", "Not under 15 kg"),
  ],
  "notes": [
    ("hepatic", "No dose adjustment given; the label advises caution in older patients with reduced hepatic function. Raised liver enzymes and hepatitis have been reported.", "", "Label · FDA US"),
    ("pregnancy", "Should not be used in pregnancy (safety not established). Passes into breast milk in low amounts: treat breastfeeding mothers only when delaying treatment is riskier (US label); MSF lists no contraindication in breastfeeding.", "", "Label · FDA US"),
    ("administration", "Take on an empty stomach with water (food increases bioavailability). Tablets may be crushed for small children.", "", "Label · FDA US"),
    ("monitor", "Strongyloidiasis: at least three follow-up stool examinations over 3 months to confirm cure. In people from loiasis-endemic areas assess Loa loa microfilaraemia before treatment. Watch for Mazzotti reactions in onchocerciasis.", "", "Label · FDA US"),
    ("forms_ph", "3 mg and 6 mg tablet.", "", "PNF"),
  ],
  "checked": [
    (PNF_URL, "Ivermectin oral: 3 mg and 6 mg tablet."),
    (MSF_URL, "Onchocerciasis 150 micrograms/kg single dose, second dose at 3 months, repeat 6–12 monthly, weight bands 15–<25 kg 1, 25–<45 2, 45–<65 3, ≥65 4 tablets of 3 mg, <15 kg do not give; ordinary scabies 200 micrograms/kg single dose, second dose 1 week later; crusted scabies two doses a week apart with keratolytic + topical scabicide; strongyloidiasis 200 micrograms/kg single; cutaneous larva migrans 200 micrograms/kg daily 1–2 days; pregnancy avoid; breastfeeding no contraindication; empty stomach; tablets may be crushed."),
    (FDA_LABEL, "Stromectol label 2009: strongyloidiasis ~200 mcg/kg single dose, ≥3 stool exams over 3 months; onchocerciasis ~150 mcg/kg, retreat as early as 3 months; empty stomach with water, food increases bioavailability; weight bands 15–24 kg 1, 25–35 2, 36–50 3, 51–65 4, 66–79 5; <15 kg not established; not in pregnancy; low amounts in milk; Mazzotti reactions, tachycardia, peripheral oedema, orthostatic hypotension; fatigue; ALT/AST elevation, post-marketing hepatitis and raised bilirubin; caution in older patients with reduced hepatic function; increased INR with warfarin."),
    (WHO_COVID, "31 March 2021: until more data is available, WHO recommends that ivermectin only be used within clinical trials (for COVID-19)."),
  ],
}
