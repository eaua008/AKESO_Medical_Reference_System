# Body part descriptions: Body System Explorer (plan, 2026-10-19)

Status: PLAN, decisions agreed. Nothing built or written yet.
Goal: when a part is clicked, the side panel says what it is, where it is, what it does and why it matters, instead of only its name and linked conditions.

## Decisions (Eijkim, 2026-10-19)
- **Two reading levels.**
  - A plain summary anyone can read (general public).
  - A "For students" section with anatomical terms and clinical notes.
- **Fields:**
  - summary + function;
  - location + neighbours (attachments, borders, blood/nerve supply);
  - clinical relevance, linked to existing disease pages;
  - an exam tip or memorable fact.
- **First batch:** a mix of all layers, about 50 high-yield parts.
- **Source process:** Claude researches and writes from open sources with a source on every entry. Eijkim reviews the sheets, the same as the medicine revision ("You fill, I check"). Nothing is invented; anything without a source is left blank.

## What the model has (from assets/anatomy/parts.json, 2026-10-19)
- **Parts:** 2,233 parts.
  - By layer: vessel 1,035, muscle 447, organ 418, bone 287, nerve 41, skin 5.
  - 1,634 unique FMA ids.
- **Concepts:** removing "left"/"right" from the names leaves **1,019 concepts** (vessel 412, muscle 220, organ 189, bone 173, nerve 20, skin 5). One description covers both sides.
- **Groups:** 510 in total; **157 curated groups** if auto `fma_*`/`old_*` groups and `_l`/`_r` side copies are left out.
- **Organs as groups:** many organs are groups, not single parts.
  - Heart = `fma_FMA7088_o`, liver = `fma_FMA7197_o`, brain = `fma_FMA50801_o`, lungs = bronchial-tree groups.
  - So descriptions must attach to **groups as well as parts**.
- **Sub-parts:** many parts are pieces of a bigger structure, e.g. "long head of left biceps brachii", "acromial part of left deltoid", the leaflets of the mitral valve. They show the parent's description with their own one-line note.

## How a description is found (lookup chain)
1. The part's **concept key**: the name with left/right removed, lower case, e.g. `femur`, `long head of biceps brachii`.
2. If empty, the **nearest described group**: walk `groups` from most specific to least, e.g. long head of biceps brachii → biceps brachii → Anterior arm muscles → Upper limb muscles.
   - Shown as "Part of **Biceps brachii**", with that group's text and a "Show the whole group" button.
3. If nothing is found: **auto facts only**. These are name, side, region, layer, body system, group breadcrumb and linked conditions; no prose, nothing invented.
   - A muted line reads "No description yet".
   - Educators/admins see a "Suggest a description" button.

## Fields (table `body_part_info`)
- **Keys:**
  - `key` text PK: a concept key or `group:<id>`.
  - `kind`: `part` | `group`.
  - `fma_ids` text[]: every FMA id it covers (both sides).
  - `layer`, `system`.
- **Names:**
  - `display_name`, e.g. "Femur".
  - `aliases` text[]: common names, e.g. "thigh bone", "collarbone", "voice box". These are used by "Find a body part" search too.
  - `name_tl` (optional, Filipino common name, later).
- **Plain level:**
  - `summary_plain`: one or two sentences, about 30 words, no jargon.
  - `function_plain`: one sentence.
- **Student level:**
  - `description`: 2–4 sentences.
  - `location`: region, position, what it borders.
  - **Layer-specific details** (`details` jsonb):
    - bone: type (long/short/flat/irregular/sesamoid), joints it forms, key landmarks.
    - muscle: origin, insertion, action, nerve supply, blood supply.
    - organ: main functions, blood supply, nerve supply, lymph drainage (where well sourced).
    - vessel: arises from / drains into, supplies / drains, main branches.
    - nerve: origin, type (sensory/motor/mixed), what it supplies.
  - `clinical`: list of {text, disease_id?}. Each disease_id links to an existing disease page, for example the femur → hip fracture, the appendix → appendicitis.
  - `exam_tip`: one line (mnemonic, "commonly tested", or a memorable fact).
- **Sources and review:**
  - `sources`: list of {title, url, licence}.
  - `status`: `draft` | `reviewed` | `published`; `reviewed_by`, `updated_at`.
- **Access:**
  - RLS: everyone reads published rows; writes only through SECURITY DEFINER admin functions, logged with ad_log.
  - Publishing bumps content_version, so the data is cached offline like the encyclopedia.

## Side panel layout (on select)
1. Breadcrumb: Musculoskeletal › Lower limb bones › **Femur** (Left). Layer pill and side.
2. **Summary** (plain), then **What it does** (plain).
3. **For students** section (collapsible, open by default for Student/Educator accounts, closed for General):
   - Description;
   - Location & neighbours;
   - the layer-specific details as a small key–value list;
   - Blood / nerve supply.
4. **Clinical relevance**: bullet lines; linked diseases appear as chips that open on top (the existing `_inspect_here`).
5. **Exam tip** card (lightbulb icon).
6. Existing sections stay as they are: related conditions and symptoms, health articles, Clinical Exchange posts.
7. Footer: sources (open in the reference browser); "Study this part" (Study Hub label cards); "Report an issue".
- Sub-part view: "Part of **Biceps brachii**" + the parent's text + the sub-part's own one-liner when it has one.

## Study Hub link
- Anatomy label cards (Study Hub phase 3) use `summary_plain` / `description` on the back.
- New data-only templates once text exists:
  - "Which bone is this?";
  - "What does this muscle do?" (from `details.action`);
  - "Which nerve supplies X?";
  - "Where does the X drain into?".

## Sources and licences
- **OpenStax *Anatomy & Physiology 2e*** (CC BY 4.0): main source. Same licence as BodyParts3D; credited per entry.
- **FIPAT Terminologia Anatomica 2** (TA2): official term spelling. BodyParts3D names come from FMA.
- **NCBI Bookshelf / StatPearls** (CC BY-NC-ND): clinical relevance. **Paraphrase and cite only, never copy text.**
- **Kenhub, TeachMeAnatomy, Wikipedia:** cross-checking only, never copied (licence terms or share-alike).
- Every entry is written in our own words, with at least one source link checked from Eijkim's browser (same rule as the medicine links).

## Process (same pipeline as the medicine revision)
1. `database/body_parts_review/BRIEF.md`: fields, word limits, tone for each level, source rules, "leave blank if unsourced".
2. Subagents research 4–5 parts each → `bNN/out_<key>.py` (a PART dict) + `bNN/NOTES.md` (doubts, missing sources).
3. `gen_body_parts.py bNN 0XX_body_parts_0N.sql` writes:
   - an idempotent upsert into `body_part_info`;
   - a `.md` review sheet;
   - checks: no duplicate keys, every FMA id exists in parts.json, every disease_id exists.
4. Test on local Postgres (run twice; the second run must change nothing). Check links in Eijkim's browser. Commit to the device.
5. Eijkim reviews the .md and runs the SQL in Supabase.

## Batches
- **B1, mixed high-yield (53, the first batch):**
  - Organs (18): heart (group), trachea, bronchial tree (group), esophagus, stomach, liver (group), gallbladder, pancreas, spleen, small intestine (group), large intestine (group), appendix, kidney, urinary bladder, brain (group), cerebellum, pituitary gland, eyeball (group).
  - Bones (14): skull (group), mandible, vertebral column (group), rib cage (group), clavicle, scapula, humerus, radius, ulna, hip bone, femur, patella, tibia, fibula.
  - Muscles (11): diaphragm, deltoid (group), biceps brachii, triceps brachii, pectoralis major, trapezius, sternocleidomastoid, quadriceps (group), hamstrings (group), gluteus maximus, gastrocnemius.
  - Vessels (9): aorta (group), superior vena cava, inferior vena cava, pulmonary trunk, common carotid artery, internal jugular vein, coronary arteries (left + right), hepatic portal vein, femoral artery.
  - Nerves (1): optic nerve.
- **B2:** the rest of the 157 curated groups (short group descriptions), e.g. Rotator cuff, Carpal bones, Heart valves, Basal ganglia, Upper teeth.
- **B3–B6:** remaining named bones and muscles (vertebrae by region, hand/foot bones, forearm/leg muscles).
- **B7+:** remaining organs, brain parts, then major named vessels.
  - Small vessel branches, bronchopulmonary segments and similar stay on auto facts plus their group text.
- Pace: about 50 entries per session, like the medicine batches.

## Code work (a separate Claude Code prompt, after B1 is reviewed)
- Migration for `body_part_info` + RLS + admin functions.
- Repository + offline cache.
- Explorer side-panel sections and the lookup chain.
- Alias search in "Find a body part".
- Content Management tab "Body parts" (edit, review, publish).
- "Suggest a description" goes to the moderation queue.

## Also noticed (2026-10-19 screenshot)
- On the Skin layer, red muscle/vessel patches show through the skin at the neck, shins, eyes and nose. This is likely z-fighting, or deeper meshes poking through the simplified skin (skin simplification 0.3).
- To add to the next Explorer prompt: a small polygon offset or depth bias on the skin, or hide deeper layers while the slider is on Skin.

## Open questions
- Filipino common names (`name_tl`) now or later? Default: later.
- Should General accounts see the "For students" section collapsed or hidden? Default: collapsed.
