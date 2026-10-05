-- =====================================================================
-- Akeso migration 001: Medication & Drug Safety reference tables
-- =====================================================================
-- Run once in the Supabase SQL editor (project akeso, branch main).
--
-- What this creates (public REFERENCE data, readable by the app, never
-- patient data; patient data is a separate, encrypted step later):
--
--   patient_conditions          the health-profile checkboxes
--   medicine_condition_safety   how safe one medicine is for one condition
--   drug_interactions           one row per drug PAIR
--   interaction_rules           risks that need 3+ drugs, a drug class,
--   interaction_rule_members      or a drug + a condition to appear
--
-- Everything runs inside one transaction: if any line fails, nothing is
-- created, so you can fix the problem and simply run the file again.
-- =====================================================================

begin;

-- ---------------------------------------------------------------------
-- 1. Health-profile conditions
-- ---------------------------------------------------------------------
-- The id is a readable slug. The first five deliberately match the keys
-- in app/models/checker.py COMORBIDITIES, so the Symptom Checker can
-- later read this same table instead of its hard-coded list.
--
-- match_keywords: words the Symptom Checker looks for in a disease's own
-- text (its risk factors, description) to decide the condition applies.
create table public.patient_conditions (
    id              text primary key,
    label           text        not null,
    description     text        not null default '',
    match_keywords  text[]      not null default '{}',
    sort_order      integer     not null default 0,
    is_published    boolean     not null default true,
    created_at      timestamptz not null default now(),
    updated_at      timestamptz not null default now()
);

-- ---------------------------------------------------------------------
-- 2. Medicine x condition safety
-- ---------------------------------------------------------------------
-- One row = "medicine X in a patient with condition Y is safe / caution /
-- avoid". Reuses your existing condition_safety enum (safe, caution,
-- avoid), the same one disease_medicines.safety uses.
--
-- The composite primary key stops the same pair being entered twice.
create table public.medicine_condition_safety (
    medicine_id         text not null references public.medicines (id) on delete cascade,
    condition_id        text not null references public.patient_conditions (id) on delete cascade,
    safety              condition_safety not null,
    summary             text not null default '',  -- the "why" line on the card
    guidance            text not null default '',  -- "Advisory guidance: ..."
    source_attribution  text not null default '',
    created_at          timestamptz not null default now(),
    updated_at          timestamptz not null default now(),
    primary key (medicine_id, condition_id)
);

create index medicine_condition_safety_condition_idx
    on public.medicine_condition_safety (condition_id);

-- ---------------------------------------------------------------------
-- 3. Drug pairs
-- ---------------------------------------------------------------------
-- Each pair is stored ONCE. The check constraint forces the two ids into
-- alphabetical order (medicine_a_id < medicine_b_id), so
-- (med_losartan, med_ibuprofen) must be written as
-- (med_ibuprofen, med_losartan). Without this, A->B and B->A could both
-- exist and slowly disagree. The app sorts the two ids before looking up.
--
-- The check also rules out a drug "interacting with itself".
create table public.drug_interactions (
    id                     bigint generated always as identity primary key,
    medicine_a_id          text not null references public.medicines (id) on delete cascade,
    medicine_b_id          text not null references public.medicines (id) on delete cascade,
    severity               condition_safety not null,
    description            text not null,
    clinical_significance  text not null default '',
    recommendation         text not null default '',
    source_attribution     text not null default '',
    is_published           boolean     not null default true,
    created_at             timestamptz not null default now(),
    updated_at             timestamptz not null default now(),
    constraint drug_interactions_ordered_pair check (medicine_a_id < medicine_b_id),
    constraint drug_interactions_unique_pair unique (medicine_a_id, medicine_b_id)
);

-- The unique constraint already indexes medicine_a_id first; this covers
-- lookups that start from the second drug.
create index drug_interactions_b_idx on public.drug_interactions (medicine_b_id);

-- ---------------------------------------------------------------------
-- 4. Combination rules
-- ---------------------------------------------------------------------
-- A rule fires when EVERY one of its members is matched by a different
-- drug in the check (the candidate plus the ticked current meds), and,
-- if required_condition_id is set, that condition is ticked too.
--
--   triple whammy     3 members (ARB/ACE inhibitor, diuretic, NSAID)
--   NSAID in CKD      1 member (NSAID) + required condition renal_impairment
create table public.interaction_rules (
    id                     text primary key,
    name                   text not null,
    severity               condition_safety not null,
    description            text not null,
    clinical_significance  text not null default '',
    recommendation         text not null default '',
    required_condition_id  text references public.patient_conditions (id) on delete restrict,
    source_attribution     text not null default '',
    is_published           boolean     not null default true,
    created_at             timestamptz not null default now(),
    updated_at             timestamptz not null default now()
);

-- A member targets EITHER one exact medicine OR a drug class, never both
-- and never neither (the <> between the two tests is an exclusive or).
--
-- drug_class_keyword is matched case-insensitively INSIDE
-- medicines.drug_class, because that column holds long text such as
-- "Non-Opioid Analgesic & Antipyretic (Para-aminophenol derivative)".
-- So the keyword 'nsaid' matches any class text containing "NSAID".
create table public.interaction_rule_members (
    id                  bigint generated always as identity primary key,
    rule_id             text not null references public.interaction_rules (id) on delete cascade,
    medicine_id         text references public.medicines (id) on delete cascade,
    drug_class_keyword  text,
    constraint interaction_rule_members_one_target
        check ((medicine_id is not null) <> (drug_class_keyword is not null))
);

create index interaction_rule_members_rule_idx
    on public.interaction_rule_members (rule_id);

-- ---------------------------------------------------------------------
-- 5. Row-level security: read-only for the app
-- ---------------------------------------------------------------------
-- RLS on + a SELECT policy only = the app (anon / logged-in users) can
-- read published rows but can never insert, update or delete. You still
-- edit freely from the Supabase dashboard, which bypasses RLS.
alter table public.patient_conditions        enable row level security;
alter table public.medicine_condition_safety enable row level security;
alter table public.drug_interactions         enable row level security;
alter table public.interaction_rules         enable row level security;
alter table public.interaction_rule_members  enable row level security;

create policy "read published conditions" on public.patient_conditions
    for select to anon, authenticated using (is_published);

create policy "read condition safety" on public.medicine_condition_safety
    for select to anon, authenticated using (true);

create policy "read published interactions" on public.drug_interactions
    for select to anon, authenticated using (is_published);

create policy "read published rules" on public.interaction_rules
    for select to anon, authenticated using (is_published);

create policy "read rule members" on public.interaction_rule_members
    for select to anon, authenticated using (true);

-- ---------------------------------------------------------------------
-- 6. Seed: the 8 health-profile conditions from the design
-- ---------------------------------------------------------------------
-- Only the checkbox list is seeded. Safety ratings, pairs and rules are
-- medical content: you fill those from your references (see the
-- templates at the bottom of this file).
insert into public.patient_conditions (id, label, description, match_keywords, sort_order) values
    ('hypertension',     'Hypertension',             'High blood pressure',                 '{hypertension,"blood pressure"}',           1),
    ('diabetes',         'Diabetes Mellitus',        'Type 1 or Type 2',                    '{diabetes,glycemic,glucose}',               2),
    ('pregnant',         'Pregnancy',                'Gestational / 1st-3rd trimester',     '{pregnan}',                                 3),
    ('asthma',           'Asthma / Reactive Airway', 'Bronchial hyperreactivity',           '{asthma,copd,bronch}',                      4),
    ('peptic_ulcer',     'Peptic Ulcer / GI Bleed',  'Gastric erosion or ulcer history',    '{peptic,ulcer,"gi bleed","gastrointestinal bleed"}', 5),
    ('renal_impairment', 'Chronic Kidney Disease',   'Impaired renal filtration',           '{kidney,renal,nephro}',                     6),
    ('liver_disease',    'Liver Disease',            'Hepatic impairment or cirrhosis',     '{liver,hepat,cirrhosis}',                   7),
    ('autoimmune',       'Autoimmune Condition',     'Systemic lupus, RA, or biologics',    '{autoimmune,lupus,rheumatoid}',             8);

-- ---------------------------------------------------------------------
-- 7. Tell every installed app there is new content
-- ---------------------------------------------------------------------
-- The offline caches only re-download when this number goes up.
update public.content_version
   set version = version + 1, updated_at = now()
 where id = 1;

commit;


-- =====================================================================
-- TEMPLATES (commented out): how to add medical content later
-- =====================================================================
-- Replace the ids with ones that exist in your medicines table.
-- Check with:  select id, name, drug_class from medicines order by id;
--
-- A drug pair. Ids in alphabetical order: 'med_a...' < 'med_b...'.
-- insert into public.drug_interactions
--     (medicine_a_id, medicine_b_id, severity, description,
--      clinical_significance, recommendation, source_attribution)
-- values
--     ('med_amlodipine', 'med_simvastatin', 'caution',
--      '<what happens when the two are combined>',
--      '<why it matters clinically>',
--      '<what the patient or prescriber should do>',
--      '<your reference>');
--
-- A medicine in a condition:
-- insert into public.medicine_condition_safety
--     (medicine_id, condition_id, safety, summary, guidance, source_attribution)
-- values
--     ('med_paracetamol', 'liver_disease', 'caution',
--      '<why>', '<advisory guidance>', '<your reference>');
--
-- A combination rule with three class members:
-- insert into public.interaction_rules
--     (id, name, severity, description, clinical_significance, recommendation)
-- values
--     ('triple_whammy', '<rule name>', 'avoid', '<...>', '<...>', '<...>');
-- insert into public.interaction_rule_members (rule_id, drug_class_keyword) values
--     ('triple_whammy', '<class keyword 1>'),
--     ('triple_whammy', '<class keyword 2>'),
--     ('triple_whammy', '<class keyword 3>');
--
-- After adding content, bump the version so the apps re-download:
-- update public.content_version set version = version + 1, updated_at = now() where id = 1;
