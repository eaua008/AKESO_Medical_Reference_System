# Akeso medicine revision — research brief (batch work, "You fill, the owner checks")

Akeso is a Philippine medical reference app for students/doctors. You revise medicine monographs.
RULE: ADD ONLY. Never repeat or reword what the medicine already has (its current content is in
the JSON brief: description, dosage_text, facts [kind/content], refs, diseases "id:safety").

## Source priority (Philippines first)
1. Philippine sources you can actually open and read:
   - PNF Essential Medicines List (PhilHealth PDF, verified): https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf
     -> use for "Forms in the Philippines" (forms + strengths listed there).
   - FDA Philippines product inserts (verification.fda.gov.ph/files/DRP-xxxx_PI_01.pdf) ONLY if the PDF opens
     and you read the dosing in it. (One of these 404'd for the owner before — so also list a non-PH backup.)
   - DOH / PhilHealth / Philippine society guidelines (PSMID, PHA, PSN, DOH program manuals: malaria, TB, rabies...).
2. WHO guidelines / WHO Model Formulary.
3. Official labels: UK SmPC on medicines.org.uk/emc (".../smpc/print" pages work well), DailyMed (dailymed.nlm.nih.gov), HPRA.
4. Merck Manual Professional, CDC, society guidelines.
Do NOT use NCBI/PubMed pages (they show a CAPTCHA; never solve CAPTCHAs). No blogs, no pharmacy shops, no slideshare.

## Lessons from batch 1 (follow them)
- Links must OPEN in a browser. No links that start a file download (e.g. OJS ".../article/download/..." -> use ".../article/view/<id>").
  PDFs that display in the browser are fine. UK SmPC: use "https://www.medicines.org.uk/emc/product/<n>/smpc/print".
- doh.gov.ph PDFs sit behind a Cloudflare check: OK to cite if WebFetch read them, but prefer another copy if one exists.
- FDA PH product-insert PDFs often 404 for Philippine users: only use one if WebFetch actually reads its dosing text.
- The PNF-EML PhilHealth PDF text (via WebFetch) only covers A to about M. For medicines after M, look for the
  PNF entry another way (try WebFetch with the `offset` parameter; or another official PNF/PhilHealth/DOH list).
  If you can't confirm the PH form, write no forms_ph note and say so.
- Keep disease links to what a source says; if it is your own inference, say so in the note text ("contraindicated in
  active liver disease" etc.) and in your summary.
- Brands: only from a verified page; otherwise leave empty (that's fine).
- MSF Essential Drugs (medicalguidelines.msf.org) is an accepted source.

## Verification (strict)
Every URL you output must have been opened with WebFetch in this task, and the specific fact you cite
must be on that page. If a page does not load or does not contain the fact, do not use it. List each
URL and what you confirmed in "checked". Never invent URLs, numbers or brands. If unsure, leave it out.

## What to produce per medicine (write a Python file; plain literals only)
File: <scratch>/medrev/<batch folder given in your task>/out_<medicine_id>.py containing:

MED = {
  "id": "med_x",
  "desc_add": "1-3 NEW sentences appended to the description (mechanism, place in therapy, PH context). No repeats.",
  "facts": {            # NEW items only (each a short sentence/phrase, same style as existing facts)
    "indication": [...], "adverse": [...], "contraindication": [...], "interaction": [...],
    "brand_ph": [...],    # only brands seen on a verified page (FDA PH portal / product insert); else []
    "brand_intl": [...],
  },
  "refs": [("Source name", "Full citation text", "https://...")],   # 2-5 NEW references (url not already in refs)
  "links": [("disease_id", "safe|caution|avoid", "short note why")],  # NEW disease links only (see list)
  # Dosage table (skip all three ONLY for medicines that already have a table: med_paracetamol)
  "sources": [("Short tag", "Source name", "Full citation", "https://...")],  # tag e.g. "Label · FDA PH", "PNF", "WHO 2024", "Label · UK SmPC"
  "doses": [("adult|child|neonate", "Indication", "PO|IV|IM|SC|Inhaled|Topical", "Dose", "Frequency",
             "Duration", "Max", "source tag", "small grey note or ''")],
  "notes": [("renal|hepatic|elderly|pregnancy|administration|forms_ph|monitor", "content", "label (e.g. 'CrCl 10–30' for renal bands, else '')", "source tag or ''")],
  "checked": [("https://...", "what exactly you confirmed there")],
}

Dose table style (match exactly): short cells; "Every 8 h", "2× a day", "Once a day"; ranges with en dash
"250–500 mg"; children per kg ("10 mg/kg", "40–90 mg/kg/day ÷ 3") with a max where the source gives one;
"—" for none. Adults rows first, then children. Every row's source tag must exist in "sources".
Add a forms_ph note from the PNF EML (tag "PNF") for every medicine that is listed there.
Monitor notes: practical (what to check). Renal/hepatic: only what the source states.

## Disease ids you may link (only these; and not ones already in the medicine's "diseases"):
acute_coronary_syndrome acute_gastroenteritis ischemic_stroke asthma varicella chikungunya cholera copd
community_acquired_pneumonia covid19 dengue hypertension hfmd heart_failure hepatitis_a hepatitis_b
hiv_infection influenza leptospirosis malaria measles migraine peptic_ulcer_disease pertussis tuberculosis
rabies schistosomiasis type2_diabetes typhoid_fever urinary_tract_infection acute_appendicitis gerd
iron_deficiency_anemia chronic_kidney_disease rheumatic_fever post_strep_glomerulonephritis
bacterial_meningitis graves_disease gout scabies
safety meaning: safe = a recognised treatment/OK to use for that disease; caution = use carefully / dose change;
avoid = should not be used in that disease (e.g. aspirin in dengue). Only add links a source supports.

After writing the file, run:  python3 -c "import runpy;m=runpy.run_path('<file>')['MED'];print(m['id'],len(m.get('doses',[])))"
Reply with a short summary: counts per field, and anything you were unsure about or left out.
