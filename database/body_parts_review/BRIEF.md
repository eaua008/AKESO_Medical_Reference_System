# Akeso body part descriptions: research brief ("You fill, the owner checks")

Akeso is a Philippine medical study app. Its Body System Explorer shows a 3D body
(BodyParts3D). When someone clicks a part, the side panel should say what it is, where
it is, what it does and why it matters. You write that text for a few parts, **in your
own words, from sources you actually opened**. The owner reviews every entry.

**RULE: nothing is invented.** Every fact must come from a page you opened in this
task. If you can't find a source for a field, leave it blank (`""`). A blank is fine;
a guess is not.

## Sources (decided by the owner, 2026-10-19)
Use these. They are US federal government works (public domain), so we may reuse and
paraphrase them:
1. **NCI SEER Training Modules**: anatomy and physiology, https://training.seer.cancer.gov/anatomy/
   (skeleton, muscles, cardiovascular, respiratory, digestive, urinary, nervous, endocrine...).
   Licence: `"Public domain"`.
2. **MedlinePlus health topics** written by NLM, https://medlineplus.gov/<topic>.html.
   Licence: `"Public domain"`. **Not** the A.D.A.M. Medical Encyclopedia pages
   (medlineplus.gov/ency/...): those are copyrighted, so don't use them.
3. **NIH institute and CDC pages**, e.g. NIDDK "Your Digestive System & How It Works",
   NHLBI "How the Heart Works", NEI eye anatomy, NINDS "Brain Basics", NIAMS, NCI
   Dictionary of Cancer Terms (cancer.gov/publications/dictionaries). Licence: `"Public domain"`.
4. **Gray's Anatomy, 20th ed. (1918)**, public domain. The full text opens on
   PubAnnotation: https://pubannotation.org/docs/sourcedb/GrayAnatomy/sourceid/<n>
   (e.g. 59 = The Femur). Find the doc number with WebSearch, or by trying nearby numbers.
   bartleby.com returns 403. Gray's is best for landmarks, origin/insertion, joints and
   branches. 1918 terms can be old, so write the modern term (e.g. "intercondylar
   fossa", not "intercondyloid") and say so in your notes when you change one.

## Lessons from the pilot (follow them)
- Clinical lines are about conditions, injuries, procedures or exam findings, not
  plain anatomy facts (those go in description/details).
- A statistic from a US page must say so ("in the United States").
- The NCI Dictionary pages often show only navigation via WebFetch: don't cite them
  unless you actually read the definition.

Do **not** use or open these:
- OpenStax *Anatomy & Physiology*: its licence forbids use with AI.
- NCBI/PubMed/StatPearls: they show a CAPTCHA; never solve CAPTCHAs.
- Kenhub, TeachMeAnatomy, Radiopaedia, Wikipedia: their terms or share-alike
  licences don't allow it. Don't cite them or copy from them.
- No blogs, hospital marketing pages, slideshare or AI-written sites.

**Your own words:** paraphrase. Never copy a sentence, and never lift more than a short
technical phrase (e.g. "medial epicondyle of the humerus").

**Spelling:** use the official anatomical terms (Terminologia Anatomica, Latin-based
English), e.g. "sternocleidomastoid" and "biceps brachii". In plain text, give everyday
English names. `display_name` is set by the manifest; you don't change it.

## Verification (strict)
Every URL in `sources` must have been opened with WebFetch in this task, and the fact
you use must be on that page. List each URL and exactly what you confirmed there in
`checked`. Never invent a URL. If a page fails or lacks the fact, don't use it.

## What to write per entry
File: `database/body_parts_review/<batch>/out_<slug>.py`, where slug = the key in
lower case, `group:` -> `group_`, and every other run of non-letters/digits -> `_`.
For example: `femur` -> `out_femur.py`, `group:fma_FMA7088_o` -> `out_group_fma_fma7088_o.py`,
`hip bone` -> `out_hip_bone.py`. Use plain Python literals only.

```python
PART = {
  "key": "femur",                         # exactly as in MANIFEST.py
  "aliases": ["thigh bone"],              # everyday names a source uses; [] if none
  # Plain level (anyone, no jargon, Grade 8 English):
  "summary_plain": "",                    # what and where; 1-2 sentences, <= 40 words
  "function_plain": "",                   # what it does; 1 sentence, <= 30 words
  # For students:
  "description": "",                      # 2-4 sentences, <= 100 words
  "location": "",                         # region, position, what it borders; <= 60 words
  "details": {},                          # layer fields below; text <= 50 words each; omit unsourced
  "clinical": [],                         # (text <= 35 words, disease_id or ""), at most 5
  "exam_tip": "",                         # one memorable, sourced fact, <= 35 words; or ""
  "sources": [("Title of page - Publisher", "https://...", "Public domain")],
  "checked": [("https://...", "what exactly you confirmed there")],
}
```

The `details` keys depend on the layer (use only these):
- bone: `type` (long/short/flat/irregular/sesamoid), `joints` (the joints it forms and with which bones), `landmarks`
- muscle: `origin`, `insertion`, `action`, `nerve_supply`, `blood_supply`
- organ: `functions`, `blood_supply`, `nerve_supply`, `lymph_drainage`
- vessel: `origin` (arises from / drains into), `territory` (what it supplies / drains), `branches` (main branches or tributaries)
- nerve: `origin`, `type` (sensory/motor/mixed), `supplies`

**Group entries** (key starts with `group:`) describe the whole structure: the heart,
the liver, the skull, the quadriceps and so on. Mention their main parts.

**Clinical lines:** short, factual, in a student register, e.g. "Inflammation of the
appendix (appendicitis) is a common surgical emergency." Link a disease page only when
the line is about that disease. Disease ids you may use (no others):

acute_coronary_syndrome acute_gastroenteritis ischemic_stroke asthma varicella chikungunya cholera copd
community_acquired_pneumonia covid19 dengue hypertension hfmd heart_failure hepatitis_a hepatitis_b
hiv_infection influenza leptospirosis malaria measles migraine peptic_ulcer_disease pertussis tuberculosis
rabies schistosomiasis type2_diabetes typhoid_fever urinary_tract_infection acute_appendicitis gerd
iron_deficiency_anemia chronic_kidney_disease rheumatic_fever post_strep_glomerulonephritis
bacterial_meningitis graves_disease gout scabies

A clinical line about a condition with no page here (e.g. a hip fracture) still goes
in, with `""` as the id.

**Exam tip:** a memorable, sourced fact, e.g. "the longest and strongest bone in the
body". No mnemonics unless a source page gives one. Don't claim "commonly tested".

**Licence** values the checker accepts: "Public domain", "CC BY 4.0" (any other CC
value must be justified in NOTES).

## When you're done
Check each file:
`.venv/Scripts/python.exe database/body_parts_review/gen_body_parts.py b01 --check out_<slug>.py`
Fix it until it prints `ok`.

Then write `database/body_parts_review/<batch>/notes_<your agent tag>.md` with:
- every field you left blank and why;
- anything you weren't sure about (conflicting sources, terminology, a disease link
  that is your inference);
- any URL that only opened after retrying, or that might not open for the owner.

Reply with a short summary of each entry: the fields that were filled and the fields
that were left blank.
