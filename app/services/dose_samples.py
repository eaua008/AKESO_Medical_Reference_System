"""Sample dosage rows for previewing the new table before the database has
them (scripts/preview_dosage.py). The app itself never loads this file.

Values come from the reviewed draft shown to the tester:
    aciclovir    UK SmPC (Aciclovir 400 mg tablets, section 4.2)
    amoxicillin  UK SmPC (Amoxicillin 250 mg/5 ml oral suspension, emc 14145,
                 section 4.2), checked 2026-10-13. Replaced the FDA PH insert
                 PDF, whose link gave 404 for the user.
    paracetamol  bpac NZ (2018); HPRA SmPC (paracetamol 500 mg tablets)
"""

from app.models.medicine import DoseNote as N
from app.models.medicine import DoseSource as S
from app.models.medicine import DoseRow as D

SMPC, FDAPH, BPAC, HPRA = "Label · UK SmPC", "Label · FDA PH", "bpac NZ 2018", "Label · HPRA"

# Full citations for the tags above (shown in References with a DOSING badge).
SOURCES = {
    "med_aciclovir": [
        S(SMPC, "Aciclovir 400 mg Tablets – Summary of Product Characteristics",
          "Aciclovir 400 mg Tablets. Summary of Product Characteristics, section 4.2 "
          "Posology. electronic medicines compendium (emc), UK.",
          "https://www.medicines.org.uk/emc/product/2352/smpc/print"),
    ],
    "med_amoxicillin": [
        S(SMPC, "Amoxicillin 250 mg/5 ml Powder for Oral Suspension – SmPC",
          "Amoxicillin 250 mg/5 ml Powder for Oral Suspension Sugar Free (Flamingo Pharma "
          "UK Ltd). Summary of Product Characteristics, section 4.2 Posology. electronic "
          "medicines compendium (emc), UK.",
          "https://www.medicines.org.uk/emc/product/14145/smpc/print"),
        S(FDAPH, "FDA Philippines Verification Portal – amoxicillin 250 mg/5 mL",
          "Amoxicillin (as trihydrate) 250 mg/5 mL powder for oral suspension, registration "
          "DRP-10727. Search the registration number on the FDA Philippines Verification "
          "Portal (the direct PDF link no longer opens).",
          "https://verification.fda.gov.ph/"),
    ],
    "med_paracetamol": [
        S(BPAC, "bpac NZ – Paracetamol dosing for children",
          "Best Practice Advocacy Centre New Zealand. Paracetamol dosing. bpac NZ; 2018.",
          "https://bpac.org.nz/2018/docs/paracetamol.pdf"),
        S(HPRA, "Paracetamol 500 mg tablets – SmPC (HPRA)",
          "Paralief 500 mg film-coated tablets. Summary of Product Characteristics, "
          "section 4.2. Health Products Regulatory Authority, Ireland.",
          "https://assets.hpra.ie/products/Human/37091/Licence_PA0126-020-008_24022025151042.pdf"),
    ],
}

SAMPLES = {
    "med_aciclovir": (
        [
            D("adult", "Herpes simplex, treatment", "PO", "200 mg",
              "5× a day, about every 4 h, skip the night dose",
              "5 days; longer for a severe first episode",
              "400 mg/dose if severely immunocompromised", SMPC,
              "Cold sores, first or recurrent genital herpes"),
            D("adult", "Herpes simplex, suppression", "PO", "400 mg",
              "2× a day (or 200 mg 4× a day)", "Pause every 6–12 months to review",
              "", SMPC, "Frequent recurrences, immunocompetent"),
            D("adult", "Herpes simplex, prophylaxis", "PO", "200 mg",
              "4× a day, about every 6 h", "While at risk",
              "400 mg/dose if severe", SMPC, "Immunocompromised"),
            D("adult", "Varicella and herpes zoster", "PO", "800 mg",
              "5× a day, about every 4 h, skip the night dose", "7 days", "800 mg/dose", SMPC),
            D("child", "Herpes simplex, treatment", "PO", "≥ 2 y: 200 mg\n< 2 y: 100 mg",
              "5× a day", "5 days", "Adult dose", SMPC, "Neonatal herpes: IV only"),
            D("child", "Varicella", "PO", "20 mg/kg", "4× a day", "5 days", "800 mg/dose", SMPC),
        ],
        [
            N("renal", "Zoster: 800 mg every 8 h", "CrCl 10–25", SMPC),
            N("renal", "Zoster: 800 mg every 12 h. Herpes simplex: 200 mg every 12 h",
              "CrCl < 10", SMPC),
            N("elderly", "Adjust for kidney function and keep well hydrated.", "", SMPC),
            N("monitor", "Kidney function in older adults and in kidney disease"),
            N("monitor", "Fluid intake: keep the patient hydrated"),
        ],
    ),
    "med_amoxicillin": (
        [
            D("adult", "Acute bacterial sinusitis", "PO", "250–500 mg",
              "Every 8 h (or 750 mg – 1 g every 12 h)", "As short as possible; follow guidelines",
              "", SMPC, "Also asymptomatic bacteriuria in pregnancy. Adults and children 40 kg and over"),
            D("adult", "Acute otitis media", "PO", "500 mg",
              "Every 8 h (or 750 mg – 1 g every 12 h)", "As short as possible; follow guidelines",
              "", SMPC),
            D("adult", "Streptococcal tonsillitis or pharyngitis; acute exacerbation of chronic bronchitis",
              "PO", "750 mg – 1 g", "Every 8 h", "10 days", "", SMPC, "Severe infections"),
            D("adult", "Community-acquired pneumonia", "PO", "500 mg – 1 g", "Every 8 h",
              "As short as possible; follow guidelines", "", SMPC),
            D("adult", "Acute pyelonephritis; dental abscess with spreading cellulitis", "PO",
              "750 mg – 1 g", "Every 8 h", "As short as possible; follow guidelines", "", SMPC,
              "Severe infections"),
            D("adult", "Acute cystitis", "PO", "3 g", "2× a day", "1 day", "", SMPC),
            D("adult", "Typhoid and paratyphoid fever", "PO", "500 mg – 2 g", "Every 8 h",
              "Follow guidelines", "", SMPC),
            D("adult", "Endocarditis prophylaxis", "PO", "2 g",
              "Once, 30–60 min before the procedure", "Single dose", "", SMPC),
            D("adult", "H. pylori eradication", "PO", "750 mg – 1 g", "2× a day", "7 days", "",
              SMPC, "With a proton pump inhibitor and another antibiotic"),
            D("adult", "Lyme disease, early stage", "PO", "500 mg – 1 g", "Every 8 h",
              "14 days (10–21)", "4 g/day", SMPC),
            D("child", "Sinusitis, otitis media, pneumonia, cystitis, pyelonephritis, dental abscess",
              "PO", "20–90 mg/kg/day, divided",
              "Divided doses; 2× a day only at the upper range",
              "As short as possible; follow guidelines", "", SMPC,
              "Under 40 kg (40 kg and over: adult dose)"),
            D("child", "Streptococcal tonsillitis or pharyngitis", "PO", "40–90 mg/kg/day, divided",
              "Divided doses; 2× a day only at the upper range",
              "As short as possible; follow guidelines", "", SMPC),
            D("child", "Typhoid and paratyphoid fever", "PO", "100 mg/kg/day ÷ 3", "Every 8 h",
              "Follow guidelines", "", SMPC),
        ],
        [
            N("renal", "No change", "GFR > 30", SMPC),
            N("renal", "40 kg and over: at most 500 mg 2× a day. Under 40 kg: 15 mg/kg 2× a day",
              "GFR 10–30", SMPC),
            N("renal", "40 kg and over: at most 500 mg a day. Under 40 kg: 15 mg/kg once a day",
              "GFR < 10", SMPC),
            N("renal", "40 kg and over: 500 mg every 24 h, plus 500 mg before and 500 mg after "
              "each session. Under 40 kg: 15 mg/kg once a day (max 500 mg), plus 15 mg/kg "
              "before and after", "Haemodialysis", SMPC),
            N("renal", "At most 500 mg a day", "Peritoneal dialysis", SMPC),
            N("hepatic", "Dose with caution and check liver function regularly.", "", SMPC),
            N("elderly", "No dose change needed.", "", SMPC),
            N("administration", "Can be taken with or without food; food does not affect absorption.",
              "", SMPC),
            N("forms_ph", "Powder for suspension 250 mg/5 mL, 60 mL bottle (add 41 mL water)",
              "", FDAPH),
            N("monitor", "Ask about penicillin allergy before the first dose"),
            N("monitor", "Rash or diarrhoea during treatment"),
            N("monitor", "Avoid if infectious mononucleosis is suspected (it can cause a rash)",
              "", SMPC),
        ],
    ),
    "med_paracetamol": (
        [
            D("adult", "Fever, mild to moderate pain", "PO", "500 mg – 1 g",
              "Every 4–6 h as needed, at least 4 h apart", "As needed",
              "1 g/dose · 4 g/day", BPAC),
            D("adult", "Same, with a risk factor", "PO", "Up to 60 mg/kg/day", "Every 4–6 h",
              "As needed", "2 g/day", HPRA,
              "Under 50 kg, liver disease, Gilbert's, dehydration, malnutrition, chronic alcohol use"),
            D("child", "Fever, mild to moderate pain", "PO", "15 mg/kg", "Every 4–6 h as needed",
              "As needed", "1 g/dose · 60 mg/kg/day, not over 4 g", BPAC, "1 month to 18 years"),
            D("child", "Underweight or malnourished child", "PO", "10 mg/kg",
              "Every 4–6 h, or longer apart", "As needed", "60 mg/kg/day", BPAC),
        ],
        [
            N("renal", "500 mg every 6 h", "GFR 10–50", HPRA),
            N("renal", "500 mg every 8 h; at least 6 h between doses", "GFR < 10", HPRA),
            N("monitor", "Add up paracetamol from every product taken, including cold and flu mixes"),
            N("monitor", "Liver risk in malnourished or acutely unwell young children", "", BPAC),
        ],
    ),
}


def apply_samples(medicine) -> bool:
    """Fill a MedicineMonograph with sample rows if there are any for it."""
    sample = SAMPLES.get(medicine.id)
    if not sample:
        return False
    medicine.doses, medicine.dose_notes = list(sample[0]), list(sample[1])
    medicine.dose_sources = list(SOURCES.get(medicine.id, []))
    return True
