# Claude Code prompt: rework auto flashcards (content + study screen)

Paste everything below the line into Claude Code, from the project root (`C:\Users\eijki\IdeaProjects\akeso`).

---

# Task: make Akeso's auto-generated flashcards teach, not just list

Study Hub Phase 1 is built. The auto cards are too blunt. Example:
*"Hallmark symptoms of Acute Rheumatic Fever and Rheumatic Heart Disease?"*, with the back *"• Fever • Joint pain (arthralgia) • Joint swelling"* and a huge empty card.

**Problems to fix:**
1. "List everything" questions. Hard to recall, impossible to grade honestly.
2. Incomplete answers that mislead. The list comes only from linked symptoms. For rheumatic fever, the real key features (carditis, chorea, nodules, erythema marginatum, migratory polyarthritis) are missing, so the card teaches a wrong picture.
3. The back teaches nothing: no "why", no "how to tell it apart", no source, no clinical context.
4. The layout wastes space (a fixed giant card), and there is no hint and no way to answer before flipping.

**Work in two steps. Do Step A, produce the sample report, then STOP and wait for my OK before Step B.**

## Rules
- **Never invent medical facts.** Every card must come only from data already in Akeso (encyclopedia fields, links, dosage tables, notes, references). If the data for a template is missing or thin, **skip that card**.
- Don't break existing review history. Old auto-card keys are **retired** (hidden), not deleted. Their `card_states` and `review_log` rows stay.
- Keep the OOP layering and existing styles/tokens. Must look right at 80–125% sizes. Use `soft_scale.exact(...)` for sizes measured from real widgets.
- Don't open or print `.env`. Never show raw errors to users.
- Add unit tests for every template and quality gate. Keep everything deterministic (same data → same cards, same keys, same distractors).

## 0. Read first (report briefly)
- `app/services/study/auto_cards.py` (or wherever the auto-card generator lives), the `Card` / card-type models, the review view, the deck/decks views, the card editor.
- The encyclopedia models and services, to see exactly which fields exist and are filled:
  - **Disease:** summary/description, pathophysiology (incl. clinicopathologic correlation), causes, cardinal symptoms (with intensity / is_primary), differential diagnosis + distinguishing features, red flags, triage/urgency, prevention, treatments/monitoring, linked medicines with `safety` (safe/caution/avoid) and `note`, references.
  - **Symptom:** description, causes, red flags, linked diseases (intensity, primary).
  - **Medicine:** drug class, description, facts (indication/adverse/contraindication/interaction/brands), `doses` (DoseRow: population, indication, route, dose, frequency, duration, max_dose, source, note), `dose_notes` (renal, hepatic, elderly, pregnancy, administration, forms_ph, monitor), `dose_sources`, linked diseases with safety.
- Print a short **data coverage table**: for each template below, how many entries have enough data to produce at least one card.

## Step A: new card content model + templates + sample report

### A1. Richer card fields (model + local store; server columns only if official cards need them)
Add optional fields to `Card`. Auto cards fill them; the editor for own/official cards gets them too:
- `answer_short`: one line, shown big on the back.
- `explanation`: the "Why": 1–3 sentences taken from the source text (no paraphrasing that changes meaning; trimming is fine).
- `distinguish`: "Don't confuse with: X: distinguishing feature" (from differentials), optional.
- `hint`: e.g. the first letter of the answer, the body system, or "Think: post-infectious".
- `difficulty`: `basic` | `clinical` | `advanced`.
- `family`: the template id (for stats and filtering).
- `source_ref`: {kind, id, field}, plus the reference title/url where available.
- `content_hash`: a hash of the data the card was built from (used for the "Updated" badge, see A4).

### A2. Templates (replace the old blunt ones)
Template id in brackets. Key = `auto2:<kind>:<entry_id>:<template>[:<n>]` (deterministic). Each template lists its data source and its skip rules.

**Disease**
1. **Clinical picture MCQ** `[dz_picture]`, difficulty clinical.
   - Front: one sentence built from 2–3 of the disease's **primary/high-intensity** symptoms plus one distinguishing context phrase, if the entry's text has it (e.g. a cause or trigger from `causes`, an age group or setting if stated in the summary). Template wording: "A patient has {s1}, {s2} and {s3}{context}. Most likely diagnosis?"
   - Choices: the disease + 3 distractors that share ≥1 of the shown symptoms (pick deterministically: most shared symptoms first, then alphabetical).
   - Back: answer_short = disease; explanation = first sentence of the clinical summary; distinguish = for each distractor, its distinguishing feature from the differentials section if present, else "Shares {symptom}, but not typical: {symptom}".
   - Skip if fewer than 2 primary symptoms or fewer than 2 valid distractors.
2. **Tell them apart** `[dz_vs]`, clinical.
   - Source: the differential diagnosis entries with distinguishing features.
   - Front: "{Disease} vs {Differential}: what's the key difference?" Back: the distinguishing feature text; explanation = one line of each disease's summary.
   - One card per differential that has a distinguishing-feature text. Max 3 per disease.
3. **Mechanism cloze** `[dz_mech]`, advanced.
   - Source: pathophysiology. Pick the 1–2 sentences that contain a mechanism keyword (e.g. "because", "leads to", "causes", "cross-react", "obstruct", "inflammation", "deficiency"). Blank ONE key noun phrase: the medical term in that sentence, preferring terms that are also entry names, symptom names or bracketed terms.
   - Back: the full sentence + explanation = the next sentence if any.
   - Skip if no sentence is under ~45 words or no clear term exists.
4. **Red flag / urgency** `[dz_redflag]`, clinical.
   - Source: red flags + triage level. Front: "In {disease}, which finding means urgent care is needed?" as MCQ: 1 real red flag of this disease + 3 distractors (milder symptoms of the same disease that are NOT red flags; else red flags of unrelated diseases are NOT allowed, so skip instead).
   - Back: the red flag + the triage text as explanation.
5. **Treatment with reason** `[dz_tx]`, clinical.
   - Source: linked medicines with safety + note.
   - (a) "Which medicine is used for {disease}?" MCQ: correct = a `safe` medicine, distractors = medicines from other diseases' safe lists in a different body system; explanation = the link note.
   - (b) "Which medicine should be AVOIDED in {disease}, and why?": correct = an `avoid` medicine; explanation = the note (e.g. dengue → NSAIDs: bleeding risk).
   - Skip (b) if there is no `avoid` link.
6. **Key feature (fair list)** `[dz_feature]`, basic.
   - Only if the entry has an authored list of key features/criteria (e.g. a diagnostic criteria field, if one exists). **Do NOT build "key features" from symptom links alone.**
   - Use overlapping cloze (hide one item at a time, max 4 cards) or "Name 2 of the {n}…". If no such field exists, skip this template and list it in the report as "needs a diagnostic criteria field".

**Medicine**
7. **Dose calculation** `[rx_calc]`, clinical.
   - Source: child DoseRows whose `dose` is weight-based (`mg/kg` or `mg/kg/day`, optional `÷ N`, ranges allowed) with a parseable max.
   - Front: "Child, {w} kg, {indication}: {medicine} dose per intake?" Pick w deterministically from {10, 15, 20, 25, 30} kg (key suffix = w; max 2 weights per row).
   - Back: worked steps. Example: "40–90 mg/kg/day × 15 kg = 600–1,350 mg/day → ÷ 3 = 200–450 mg every 8 h (max 3 g/day: within limit)". If the result passes a per-dose or daily max, show the capped value and say it was capped.
   - If a liquid form exists in `forms_ph` (e.g. "250 mg/5 mL"), add the volume: "= 4–9 mL of 250 mg/5 mL".
   - Always end with "Practice calculation: always check the prescriber and product insert."
   - Strict parser. If anything is ambiguous (units, frequency, "÷" missing for /day without a frequency), **skip**. Unit-test many real dose strings from the DB.
8. **Dose recall** `[rx_dose]`, basic.
   - Adult row: "{medicine} for {indication} (adult): dose and how often?" Back: dose + frequency + duration + max; explanation = the row note.
   - One card per indication, max 3.
9. **Mechanism / class** `[rx_class]`, basic.
   - "{medicine} belongs to which drug class?" as MCQ, distractors = other classes in the DB. Explanation = the first sentence of the description.
10. **Side effect discrimination** `[rx_se]`, clinical.
    - "Which is NOT an adverse effect of {medicine}?": 3 real adverse facts + 1 adverse fact of a medicine from a different class that is NOT listed for this medicine. Explanation names the correct option's real source medicine.
11. **Contraindication / caution** `[rx_contra]`, clinical.
    - "{medicine} is contraindicated in which situation?" MCQ from contraindication facts; distractors = contraindications of other medicines not listed for this one.
12. **Kidney / liver adjustment** `[rx_renal]`, advanced.
    - From renal/hepatic notes with a label (e.g. "CrCl 10–30"): "{medicine}, {label}: dose change?" Back: the note.
13. **Interaction** `[rx_ix]`, clinical.
    - From interaction facts that name another drug: "{medicine} + {other}: what's the risk?" Back: the interaction text.

**Symptom**
14. **Causes MCQ** `[sx_cause]`, basic. "Which is a common cause of {symptom}?": 1 real cause + 3 causes of unrelated symptoms not listed here.
15. **Red flag** `[sx_redflag]`, clinical. Like `[dz_redflag]`, from the symptom's red flags.

### A3. Quality gates (apply to every auto card; unit-tested)
- Skip if the answer text appears in the question (case-insensitive, ignoring brackets).
- Skip a card whose answer has more than 6 items. Turn it into cloze/MCQ, or skip it.
- Skip if any field is empty after trimming, or the front is longer than about 220 characters.
- MCQ: exactly one correct; 2–4 distractors; no duplicate or near-duplicate choices (normalised text, and also synonyms in brackets); distractors must not be correct for this entry (check all of the entry's lists).
- De-duplicate near-identical cards across templates (same answer_short + same entry).
- Cap per entry: about 8 cards per disease, 8 per medicine, 3 per symptom (priority: picture, vs, tx, redflag, mech, then the rest).
- Retire all old auto keys (`auto:` prefix) and hide them. They stay in the DB.

### A4. "Updated" handling
If an auto card's `content_hash` changes since the user last reviewed it, show a small **Updated** badge on the card and keep the review state (don't reset).

### A5. SAMPLE REPORT, then STOP
Generate `docs/flashcards_sample.md` (and an `.html` version if easy) with **about 30 cards**:
- 4 diseases: rheumatic fever, dengue, acute appendicitis, plus one more of your choice.
- 4 medicines: amoxicillin, paracetamol, ciprofloxacin, plus one more.
- 2 symptoms.

For each card show the front, choices if any, back (answer_short, explanation, distinguish), hint, difficulty, template, source field. Include the **data coverage table** and a list of templates that had to be skipped and why (e.g. "dz_feature: no diagnostic criteria field").
**STOP and wait for my OK** (I may ask to change wording or templates).

## Step B (after my OK): study screen + editor
1. **Card layout**:
   - The card height fits its content (min ~260 px, max = available space, then it scrolls inside).
   - The front is vertically centred, readable font (≥ 16 px at 100%, scales with soft_scale), max text width ~760 px.
   - The back is in sections:
     - **Answer** (large),
     - **Why** (explanation),
     - **Don't confuse with** (distinguish),
     - a footer with source + "Open {entry}" + Report.
   - Badges in the top corner: subject, body system, difficulty, Updated.
2. **Show answer** button (Space/Enter) under the front. The rating buttons appear only after flipping.
3. **Hint** button (H) reveals `hint` under the question. It is noted in review_log as `hinted` (add the column; local + server).
4. **Type your answer** (optional, toggle in Study settings, default off): a text box before flipping. After flipping, show the typed answer next to the correct one with matching words highlighted. Pre-select Again/Good based on a simple match score; the user can change it.
5. **MCQ**: after choosing, mark right/wrong and show the rationale for every choice (already exists: keep it, restyle to the section layout).
6. **Calculation cards**: show the worked steps as a small numbered list with the numbers in a monospace font.
7. **Filters**: on the deck page and in Study settings, filter by difficulty and template family (e.g. "only calculations", "only tell-apart").
8. **Card editor** (own/official cards): add the fields answer_short, explanation, distinguish, hint, difficulty. Show a live preview of the front and back in the new layout.
9. Keep keyboard shortcuts: Space flip, 1–4 rate, H hint, Ctrl+Z undo, E edit, R report, Esc end.

## Done when
- The sample report is approved and the generator produces only cards that pass the gates.
- The rheumatic fever deck has no "list all symptoms" card. Its cards are a picture MCQ, a tell-apart card, a mechanism cloze, and treatment cards, as far as the data allows.
- Calculation cards are correct for all tested dose strings (unit tests with real DB strings, including capping at the max).
- Old review history is kept; the new layout works at 80–125%; offline still works.
- Give me: files changed, any migration (only if server columns were added: list it in order), how to test, and the list of **content gaps** that blocked templates (e.g. diseases missing differentials or diagnostic criteria), so I can plan a content batch.
