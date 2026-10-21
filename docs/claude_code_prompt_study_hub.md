# Claude Code prompt: Study Hub (Course Library + Flashcards)

Paste everything below the line into Claude Code, from the project root (`C:\Users\eijki\IdeaProjects\akeso`).

---

# Task: build "Study Hub" (Flashcards + Course Library) in Akeso

You are working on **Akeso**, a PySide6 desktop medical reference app for students (Supabase backend, OOP architecture: models / repositories / services / controllers / views). Build a new **Study Hub** module in phases. **Finish one phase, test it, give me a summary, then STOP and wait for my OK before starting the next phase.**

## 0. Before writing any code (do this first, report back briefly)
1. Read the project structure and these existing pieces so the new module matches them exactly:
   - `app/ui/dashboard_shell.py` (how screens register: `register_view`, `add_sheet`, `_inspect_here`, `show_tab`), `app/ui/components/sidebar.py` (sections HOME / CLINICAL TOOLS / REFERENCE LIBRARY / COMMUNITY / MY WORKSPACE / ACCOUNT / ADMIN), `app/ui/components/page_sheet.py`, `app/ui/components/sheet_dialog.py`.
   - Study Notebook + its sync (`notebook_sync` controller, the notebook views, the local cache). If a design note exists (search the repo for "notebook sync"), follow that pattern for offline + sync.
   - Health Articles (`health_article_*`): it is the model for "educator drafts, admin publishes" and for the Content Management tab structure (`admin_controller.py`, `app/ui/views/admin/...`).
   - The admin SQL pattern in `database/migrations/004_admin.sql` and later: SECURITY DEFINER functions guarded by `ad_me()`, audit with `ad_log(...)`, `content_version` bump.
   - Encyclopedia data models and services: `app/models/medicine.py` (incl. `DoseRow`, `DoseNote`, `MedicineMonograph.doses`), disease and symptom models, `DiseaseService` / `SymptomService` / `MedicineService` and their local caches.
   - Ctrl+K search providers (e.g. `ArticleProvider`), `app/core/lucide.py` (icons), `app/core/theme.py` (+ per-module `*_styles.py` loaded by theme.py), `app/core/soft_scale.py` (80%/90% sizes: use `soft_scale.exact(...)` for sizes measured from real widgets), `app/ui/components/akeso_loader.py` (`LoaderOverlay`, `LoadingHold`: loaders stay at least 3 s), the moderation queue (Clinical Exchange `ex_report` / mod queue).
   - The Body System Explorer (`body_explorer_view.py`, `assets/anatomy/`, JS bridge `window.akeso.*`) for Phase 3 only.
2. Find the **latest migration number** in `database/migrations/` and number new migrations after it. (Friends / Study Groups migrations may already exist or be planned; don't reuse their numbers.)
3. Tell me in a few lines: where you will put each new file, the migration numbers, and anything in this spec that conflicts with the existing code. Then start Phase 1.

## Global rules (all phases)
- **Add, don't break.** Don't rename or remove existing tables, functions, files, ids or behaviour.
- Never open or print `.env`. The app only has the publishable key. No service-role key anywhere.
- **Never show raw server errors** to users. Map them to friendly messages, as other modules do.
- Follow the app's OOP layering: `models/` dataclasses, `repositories/` (Supabase + local SQLite), `services/` (logic, caching, scheduling), `controllers/` (signals and slots), `ui/views/` (widgets only). Views never call Supabase directly.
- UI: match the existing dark/light theme tokens (`Theme.token(...)`), cards, chips, `PageSheet` for full-page detail and review screens, `LoaderOverlay` + `LoadingHold` for loading. The sidebar never scrolls. Only the content area scrolls. Must look right at 80/90/100/110/125% display sizes.
- Every new user-facing text is plain, short English (layman's terms first, medical term in brackets where useful).
- Educational disclaimer on review and course pages: "Akeso is a study tool, not medical advice."
- SQL: idempotent (`create table if not exists`, `create or replace function`, guarded inserts), RLS on every new table, grants explicit, bump `content_version` only when **official** content changes.
- Tests: add unit tests for pure logic (scheduler, auto-card generator, cloze parser, sync merge). Run the app offscreen to smoke-test new screens if possible. Test SQL on a local Postgres if available; otherwise give me the exact test queries to run.
- At the end of each phase give me: files added/changed, migrations to run (in order), how to test it by hand, known limits, and anything you guessed.

## Decisions already made (don't re-ask)
- One sidebar item **Study Hub** in **MY WORKSPACE** (icon: lucide `graduation-cap` or `layers`), with tabs **Today | Courses | Decks**. Sidebar badge = number of cards due today.
- Card sources: **Auto** (generated from the encyclopedias), **Student-made**, **Official** (educators draft, admins publish), **Shared**.
- Labels everywhere: **Official** (accent check badge), **Auto** (sync icon), **Student-made** (muted, shows author), **Shared** (people icon). Student content is never mixed into official lists without its label.
- Review: **spaced repetition, SM-2** with learning steps; keep the scheduler behind an interface so FSRS can be added later.
- Card types: **basic** (front/back), **mcq** (choices, each with `correct` and a `rationale`), **cloze** (`{{answer}}` blanks, multiple blanks allowed: `{{c1::...}}`, `{{c2::...}}`), **label3d** (highlight body part(s) on the 3D model, ask for the name).
- Courses: **curated**. Subject → course → units → lessons. A lesson = intro text + links to encyclopedia entries/articles/3D parts + its deck + a quiz (MCQ cards). Progress tracked.
- Subjects at launch: **Anatomy, Pathology, Pharmacology, Microbiology**.
- **Offline + sync** for decks, card states and progress.
- Defaults (I may change later): new cards/day **20**, max reviews/day **200**, learning steps **1 min, 10 min**, relearning step **10 min**, graduating interval **1 d**, easy interval **4 d**, starting ease **2.5**, min ease **1.3**.
- Student-made decks: **private by default**, shareable with chosen people (Phase 5). No "publish to everyone" for students for now. Keep a `visibility` column so it can be added later.
- Educators do **not** see students' progress or quiz scores (no table/grant for that).

---

## PHASE 1: Flashcards core

### 1.1 Database (new migration, e.g. `0NN_study_hub_flashcards.sql`)
Tables (all with RLS on):
- `study_subjects` (id text pk, name, icon, position). Seed: `anatomy`, `pathology`, `pharmacology`, `microbiology` (guarded insert).
- `decks`:
  - columns: `id uuid pk default gen_random_uuid()`, `title text not null check (length<=120)`, `description text default ''`, `subject_id text references study_subjects`, `origin text check in ('official','personal')`, `owner_id uuid null` (null for official), `status text check in ('draft','published') default 'draft'`, `visibility text check in ('private','shared','public') default 'private'`, `lesson_id uuid null` (FK added in Phase 2), `created_at`, `updated_at`, `deleted_at timestamptz null` (soft delete for sync).
- `cards`:
  - columns: `id uuid pk`, `deck_id uuid references decks on delete cascade`, `type text check in ('basic','mcq','cloze','label3d')`, `front text`, `back text`, `choices jsonb` (array of `{text, correct bool, rationale}`), `cloze_text text`, `part_ids text[]` (3D FJ ids), `source_kind text null check in ('disease','symptom','medicine','article','body_part')`, `source_id text null`, `tags text[] default '{}'`, `position int`, `created_at`, `updated_at`, `deleted_at`.
  - Validation via CHECK or trigger: mcq needs ≥2 choices and exactly ≥1 correct; cloze needs at least one `{{...}}`; basic needs front and back; label3d needs part_ids. Length limits (front/back ≤ 2000, rationale ≤ 600).
- `card_states`:
  - columns: `user_id uuid`, `card_key text`, `state text check in ('new','learning','review','relearning','suspended')`, `due timestamptz`, `interval_days real`, `ease real`, `reps int`, `lapses int`, `step int`, `last_rating smallint`, `last_review timestamptz`, `updated_at`.
  - pk `(user_id, card_key)`.
  - `card_key` = card uuid for real cards, or the auto-card key (see 1.3), so auto cards need no server rows.
- `review_log` (id uuid pk, user_id, card_key, rating smallint 1..4, reviewed_at timestamptz, elapsed_ms int, state_before, interval_before real, interval_after real, ease_after real, client_id uuid unique) for sync and stats. Append-only.
- `study_settings` (user_id pk, new_per_day int default 20, max_reviews int default 200, learning_steps int[] default '{1,10}', relearn_steps int[] default '{10}', updated_at).

RLS / grants:
- `study_subjects`: readable by anon and authenticated.
- `decks` / `cards`: SELECT if (origin='official' and status='published' and deleted_at is null) OR owner_id = auth.uid(). (Shared access is added in Phase 5.) INSERT/UPDATE/DELETE for students only on their own personal decks/cards (owner_id = auth.uid(), origin='personal'). Official rows are written only by SECURITY DEFINER admin functions.
- `card_states`, `review_log`, `study_settings`: each user reads and writes only their own rows.
- Admin functions (pattern of `admin_save_article`):
  - `admin_list_decks()`, `admin_get_deck(id)`, `admin_save_deck(jsonb)` (deck + cards; educators may save drafts, only admins may set `published`), `admin_set_deck_status(id, status)`.
  - All guarded by `ad_me()`, logged with `ad_log(...)`. Publishing/unpublishing official decks bumps `content_version`.
- A `report_card(card_ref text, reason text, note text)` path into the existing moderation queue (reuse the queue/table shape the app already has; don't create a parallel queue if one can be extended).
- Indexes on `cards(deck_id)`, `card_states(user_id, due)`, `review_log(user_id, reviewed_at)`, `decks(owner_id)`, `decks(origin,status)`.

### 1.2 Models, scheduler
- `app/models/study.py`: dataclasses `Subject`, `Deck`, `Card`, `Choice`, `CardState`, `ReviewLogEntry`, `StudySettings`, enums for card type / state / rating / origin.
- `app/services/srs/` with `Scheduler` interface and `Sm2Scheduler`:
  - New → learning steps (1 min, 10 min) → graduate (1 d; Easy = 4 d).
  - Review: Again → lapse, ease −0.20 (min 1.3), go to relearning step (10 min), new interval = max(1, interval×0.5); Hard → interval×1.2, ease −0.15; Good → interval×ease; Easy → interval×ease×1.3, ease +0.15.
  - Small fuzz (±5%, deterministic per card+day) for intervals ≥ 3 d.
  - `preview(state) -> {rating: next_interval_label}` for the button labels ("10 min · 1 d · 3 d · 7 d").
  - Unit tests covering each transition and the day boundary (use the local day, start of day 04:00 like Anki).
- Daily queue builder: due learning cards first, then due reviews (oldest due first, capped at max_reviews), then new cards (capped at new_per_day, counting today's already-introduced new cards from review_log).

### 1.3 Auto decks (generated on the device)
`app/services/study/auto_cards.py`:
- Input: the cached encyclopedia models (no network calls). Output: `Card` objects with a stable **card_key** = `auto:<kind>:<entry_id>:<template_id>[:<n>]` (deterministic; never random). Review history survives content edits; the card text is regenerated from current data each time.
- Templates (skip any template whose data is empty; never invent content):
  - **Medicine** (Pharmacology, grouped by drug_class):
    - `class`: "Drug class of {name}?"
    - `max_adult`: "Maximum adult dose of {name}?" (from dose rows with max_dose)
    - `child_dose:{indication}`: "Children: dose of {name} for {indication}?" (dose + frequency + max)
    - `side_effects`: "Common side effects of {name}?" (first 5 adverse facts)
    - `contra`: "{name} should be avoided in…?"
    - `renal`: "{name}: kidney dose changes?" (renal notes)
    - `cloze_dose`: "{name} adult dose for {indication}: {{dose}} {{frequency}}"
    - `mcq_not_se`: "Which is NOT a side effect of {name}?" (1 correct = a side effect of another medicine in a different class, 3 distractors = real side effects of {name}; rationale per choice)
  - **Disease** (Pathology, grouped by body system):
    - `hallmark`: "Hallmark symptoms of {name}?" (cardinal/primary symptoms)
    - `red_flags`
    - `causes`
    - `first_line`: "Medicines used for {name}?" (linked medicines marked safe)
    - `avoid`: "Which medicine should be AVOIDED in {name}?" as MCQ, from `disease_medicines.safety='avoid'`, distractors = safe medicines, rationale from the link note
    - `mcq_diff`: "A patient has {3 hallmark symptoms}. Most likely?" (correct = this disease, distractors = diseases sharing ≥1 symptom; rationale names the distinguishing feature from each entry's summary where available, otherwise "Shares {symptom} but lacks {symptom}")
  - **Symptom**: `causes`: "Common causes of {name}?"; `red_flags`: "Red flags with {name}?"
- Auto decks shown in the Decks tab as e.g. "Pharmacology · Antibiotics (Auto)", "Pathology · Cardiovascular (Auto)", one per group, plus one per entry reachable from its encyclopedia page ("Study {name} cards").
- Every auto card's back has "Open {entry}" (opens the encyclopedia page on top via `_inspect_here`) and "Report card".
- Auto cards whose source entry disappears are hidden (their card_state stays).
- Unit tests: deterministic keys, templates skipped when data missing, MCQ always has exactly one correct and 4 choices when possible (else fewer, min 2), no duplicate choices.

### 1.4 Local store + sync (offline first)
- `app/repositories/study_local_repository.py`: SQLite file in the same user-data folder as the other caches (find how the encyclopedia/notebook caches choose their path and reuse it). Tables mirror: decks, cards (own + cached official), card_states, review_log (with `synced` flag), settings, sync_meta (last_pull per table).
- `app/repositories/supabase_study_repository.py`: fetch official published decks/cards changed since `updated_at`; push own decks/cards (upsert, soft deletes); push unsynced review_log (idempotent via `client_id`); pull card_states and review_log newer than last pull.
- **Merge rule** for card_states: rebuild the state by replaying review_log entries for that card in `reviewed_at` order (server + local, de-duplicated by client_id). For own deck/card edits: last `updated_at` wins.
- `StudySyncController`: sync on Study Hub open, after a review session, every 5 min while open, and on reconnect. A status chip (Synced · Offline · Syncing · Sync error) like the notebook's. Reviews work fully offline.
- Unit tests: replay merge with interleaved devices; duplicate push is a no-op.

### 1.5 UI
- **Sidebar**: "Study Hub" under MY WORKSPACE with a due-count badge (hide when 0). Registers a tab id `study-hub` in `dashboard_shell.py`.
- **Today tab** (`ui/views/study/today_view.py`):
  - Hero: "{due} due · {new} new" + **Start review** (disabled with "All done for today" when nothing is due) + streak (days with ≥1 review).
  - Rows: "Decks with cards due" (deck cards with counts), "Weak cards" (top 10 by lapses, "Review these").
  - Empty state for first-time users: a 3-step guide (pick a deck → review → come back tomorrow) with buttons to the Decks tab.
  - Dashboard Overview gets a small "Study: {due} due today" card linking to Study Hub.
- **Decks tab** (`decks_view.py`):
  - Toolbar: search, subject dropdown, origin filter chips (All · Official · Auto · Mine · Shared), "New deck".
  - Deck cards: title, badge (Official/Auto/Student-made/Shared), subject, counts (new / due / learned), "Study" and "Browse". **The whole card is clickable** (testers asked for this).
  - Deck page (PageSheet): header with badge + counts + "Study now"; card list (front preview, type icon, state); for own decks: Add card, Edit, Delete (confirm), Rename inline in the header (testers asked for inline renaming in the notebook too).
- **Card editor** (dialog/sheet):
  - Type picker; fields per type.
  - MCQ: up to 6 choices, a "correct" toggle each, rationale each.
  - Cloze: text box with a "Make blank" button around the selection + live preview.
  - label3d: Phase 3 (show the type disabled with "Coming soon").
  - Tags; optional "Linked entry" picker (disease/symptom/medicine search).
  - Validation messages inline.
- **Make a flashcard**: a context-menu / small button "Make a flashcard" on selected text in (a) encyclopedia pages (disease, symptom, medicine monograph text areas) and (b) Study Notebook notes. It opens the card editor pre-filled (front empty, back = selected text, linked entry set) with a deck picker (default: a personal deck "My cards"; create it if missing). If text selection is not possible on a page, make the text selectable first (testers asked for text selection/copy).
- **Review screen** (PageSheet, `review_view.py`):
  - Progress bar ("12 / 40"), deck name, a large card.
  - Space/Enter or click = show answer.
  - Ratings: buttons Again/Hard/Good/Easy with interval previews, keys 1–4.
  - Ctrl+Z = undo last rating.
  - E = edit (own cards). R = report (official/auto). Esc = end session.
  - MCQ: choices as buttons. Click → mark correct/wrong in colour and reveal **every** choice's rationale → then the rating buttons (preselect Good if correct, Again if wrong, but let the user change it).
  - Cloze: blanks shown as "[ … ]"; answer shows the full sentence with the blanks highlighted.
  - Back side: "Open {entry}" link for linked/auto cards.
  - End-of-session summary: reviewed, correct %, time, next due.
  - Smooth card flip/slide animation (respect the existing animation settings; make it instant if animations are off).
  - Fonts readable at 80%; long text scrolls inside the card.
- **Settings** (in Study Hub, gear icon): new cards/day, max reviews/day, learning steps, "Reset progress for a deck" (confirm).
- **Ctrl+K**: a provider for decks (open deck) and for own cards (open card in its deck).
- Styles in a new `app/core/study_styles.py` loaded by `theme.py`; icons from `lucide.py` (add any missing).

### 1.6 Content Management: Decks tab (admin/educator)
- List official decks (draft/published, subject, card count, author, updated).
- Editor: deck fields + card table with the same card editor. **Bulk import CSV** (columns: type, front, back, choices_json, cloze_text, tags) with a preview + validation report before saving.
- Educators: save as draft. Admins: Publish / Unpublish. Every action is logged.

### Phase 1 done when
- I can create a personal deck, add basic/MCQ/cloze cards, review them with correct SM-2 scheduling, undo, and see due counts on Today, the sidebar badge and the dashboard.
- Auto decks for Pharmacology and Pathology appear from the cached encyclopedia and work offline.
- Reviews done offline sync later with no duplicates. A second device converges to the same states.
- An admin can publish an official deck; students see it with the Official badge; educators can only draft.
- Unit tests pass. Give me the migration(s) to run and a manual test checklist. **STOP.**

---

## PHASE 2: Course Library
- **Migration**:
  - `courses` (id, subject_id, title, summary, level text check in ('intro','core','advanced'), cover_icon, status draft|published, author_id, position, updated_at, deleted_at).
  - `course_units` (id, course_id, title, position).
  - `course_lessons` (id, unit_id, title, intro text ≤ 6000, est_minutes, position, deck_id null).
  - `lesson_links` (lesson_id, kind check in ('disease','symptom','medicine','article','body_part','body_system'), ref_id, label, position).
  - `lesson_progress` (user_id, lesson_id, completed_at, quiz_score real, quiz_total int, updated_at; pk user_id+lesson_id).
  - Add the FK `decks.lesson_id → course_lessons`.
  - RLS: published courses/units/lessons/links readable by all. Progress: own rows only. Writes via `admin_save_course(jsonb)` (the whole tree), `admin_set_course_status`, guarded and logged like decks. Publishing bumps content_version.
- **Courses tab**:
  - Shelves per subject (Anatomy, Pathology, Pharmacology, Microbiology).
  - Course cards: title, level, lesson count, progress bar. The whole card is clickable.
  - "Continue" button on courses in progress.
- **Course page** (PageSheet): summary, units with lessons (tick when complete, est. minutes), overall progress, "Continue where you left off".
- **Lesson page** (PageSheet):
  - Intro text (supports the same light formatting as Health Articles: `## ` headings, `- ` bullets, blank-line paragraphs).
  - "Read" section: link chips that open the linked encyclopedia pages / articles on top (`_inspect_here`). Body-part links open the Body System Explorer focused on that part/system.
  - "Practice": Study this lesson's deck (counts).
  - "Quiz": 5–10 MCQ cards from the lesson deck flagged in tags as `quiz` (or all MCQ if none flagged). One question per screen; after answering show right/wrong + all rationales; final score. Quiz answers also count as reviews for SRS only if the user ticks "Add to my reviews" (default on).
  - "Mark complete" (auto-completes when the quiz score is ≥ 70%). Previous / Next lesson buttons (testers asked for back/next navigation).
- Today tab: "Continue course" row.
- **Content Management → Courses**:
  - Tree editor (course → units → lessons) with drag-reorder (or up/down buttons).
  - Lesson editor: intro, est. minutes, link picker (search diseases/symptoms/medicines/articles/body systems/body parts), deck picker or "Create lesson deck".
  - Preview as student. Draft (educators) / Publish (admins).
- **Seed** (as draft, for me to review and publish), using ONLY existing Akeso content (don't invent facts):
  - "Pharmacology: Antibiotics basics" (units by class: penicillins, cephalosporins, macrolides, fluoroquinolones, others; lessons link the existing medicine entries; lesson decks = filtered auto cards copied into official draft decks).
  - "Pharmacology: Antihypertensives".
  - "Pathology: Cardiovascular diseases".
  - "Pathology: Infectious diseases in the Philippines" (dengue, leptospirosis, TB, typhoid, malaria, rabies, cholera… whichever exist).
  - Lesson intros as short neutral summaries built from the linked entries, marked as drafts with a "Review before publishing" note.
- **Phase 2 done when**: an admin can build and publish a course; a student can follow it, open linked pages, study the lesson deck, take the quiz, and see progress (synced). **STOP.**

---

## PHASE 3: Anatomy (3D label cards + Anatomy course)
- Prerequisite: the Body System Explorer **part-groups** work (multi-level groups per part). If it isn't done, tell me and stop.
- Card type **label3d**:
  - The card editor gets a 3D picker (embedded explorer, click parts or pick a group; stores FJ `part_ids`).
  - Review shows the explorer in **quiz mode**: labels/hover names off, the target part(s) highlighted (glow), the camera framed on them; others faded. The answer shows the name, "Part of" group and system.
- **Auto anatomy decks** per group from `parts.json` groups (e.g. "Bones of the hand", "Cervical vertebrae", "Teeth", "Muscles of the rotator cuff"): card_key `auto:part:<group_id>:<fj_id>`. Only parts with a clear English name. Skip tiny/duplicate pieces.
- JS bridge additions (keep existing API): `akeso.quizMode(on)`, `akeso.quizShow(part_ids)`, `akeso.quizReveal()`. Rebuild the bundle with esbuild as the anatomy README says.
- Seed draft course "Anatomy: Skeleton & muscles basics" using the explorer links and the anatomy auto decks.
- **STOP** after testing.

---

## PHASE 4: Microbiology content
- Migration: `organisms` (id, name, gram text check in ('positive','negative','variable','not applicable'), shape, oxygen, type check in ('bacterium','virus','parasite','fungus'), summary, first_line text, sources jsonb, updated_at) + `organism_diseases` (organism_id, disease_id, note). RLS read-all; admin writes via SECURITY DEFINER; content_version bump.
- Do NOT fill medical content yourself. Create the schema, an admin editor (Content Management → Organisms), auto-card templates (Gram stain, shape, diseases caused, first-line treatment), and an empty "Microbiology" shelf that shows "Coming soon" until published organisms exist. Tell me what content is needed. **STOP.**

---

## PHASE 5: Sharing
- Only if Friends / Study Groups tables exist (check). Otherwise tell me and stop.
- `deck_shares` (deck_id, target_kind 'user'|'group', target_id, can_edit bool, created_at). RLS: the owner manages shares; targets can SELECT the deck/cards; `can_edit` targets can edit cards.
- UI: "Share" on own decks (pick friends/groups, toggle can edit); "Shared with me" filter; a "Copy to my decks" button.
- Notifications: "{name} shared a deck with you" via the existing notifications system. **STOP.**

---

## PHASE 6: Stats
- Study Hub → Stats (or a section on Today):
  - streak, reviews per day (last 30 days bar chart), retention % (Good/Easy ÷ all reviews of mature cards)
  - a heat-map calendar
  - weak topics (subjects/decks with the most lapses)
  - time studied
- All computed locally from review_log (works offline). Use the app's existing chart approach if there is one; otherwise draw simple QPainter charts matching the theme.

---

## Final reminders
- After each phase: list the migrations to run in Supabase **in order**, and remind me that new asset files must be in `akeso.spec` if any were added.
- Don't release a new version yourself. I'll run `scripts/release.ps1` when ready.
- If anything in this spec is unclear or conflicts with the code, ask me instead of guessing, especially about medical content.
