-- 030_medicine_doses.sql  -  tables for the new dosage table on the medicine page
--
-- Three new tables, read by the app (SupabaseMedicineRepository) and shown by
-- app/ui/components/dosage_table.py:
--
--   medicine_doses         one row of the table: Adults / Children, indication,
--                          route, dose, frequency, duration, max, source tag
--   medicine_dose_notes    the panels under the table: kidney, liver, older
--                          adults, pregnancy, how to give it, PH forms, monitor
--   medicine_dose_sources  the full citation behind each source tag (shown in
--                          References with its own DOSING TABLE SOURCE badge)
--
-- Nothing existing is changed: medicines.dosage_text stays and is still shown
-- (folded under the table, or on its own while a medicine has no rows yet).
-- Everyone can read rows of published medicines; only admins write (through
-- Content Management functions, added with the row editor). Safe to run again.

begin;

create table if not exists public.medicine_doses (
    id          bigint generated always as identity primary key,
    medicine_id text not null references public.medicines (id) on delete cascade,
    population  text not null default 'adult'
                check (population in ('adult', 'child', 'neonate')),
    position    integer not null default 0,
    indication  text not null,
    route       text not null default '',
    dose        text not null default '',
    frequency   text not null default '',
    duration    text not null default '',
    max_dose    text not null default '',
    source      text not null default '',     -- short tag, matches medicine_dose_sources.tag
    note        text not null default '',     -- small grey line under the indication
    created_at  timestamptz not null default now(),
    updated_at  timestamptz not null default now()
);
create index if not exists medicine_doses_medicine_idx
    on public.medicine_doses (medicine_id, population, position);

create table if not exists public.medicine_dose_notes (
    id          bigint generated always as identity primary key,
    medicine_id text not null references public.medicines (id) on delete cascade,
    kind        text not null check (kind in ('renal', 'hepatic', 'elderly', 'pregnancy',
                                              'administration', 'forms_ph', 'monitor')),
    position    integer not null default 0,
    label       text not null default '',     -- left column, e.g. 'CrCl 10-30'
    content     text not null,
    source      text not null default '',
    created_at  timestamptz not null default now(),
    updated_at  timestamptz not null default now()
);
create index if not exists medicine_dose_notes_medicine_idx
    on public.medicine_dose_notes (medicine_id, kind, position);

create table if not exists public.medicine_dose_sources (
    id            bigint generated always as identity primary key,
    medicine_id   text not null references public.medicines (id) on delete cascade,
    tag           text not null,
    source_name   text not null,
    citation_text text not null default '',
    url           text not null default '',
    position      integer not null default 0,
    created_at    timestamptz not null default now(),
    updated_at    timestamptz not null default now(),
    unique (medicine_id, tag)
);

-- Read: anyone (signed in or not), for published medicines only.
-- Write: no policy, so only SECURITY DEFINER admin functions can write.
alter table public.medicine_doses        enable row level security;
alter table public.medicine_dose_notes   enable row level security;
alter table public.medicine_dose_sources enable row level security;

drop policy if exists "medicine doses: read published" on public.medicine_doses;
create policy "medicine doses: read published" on public.medicine_doses
    for select to anon, authenticated
    using (exists (select 1 from public.medicines m
                   where m.id = medicine_id and m.is_published));

drop policy if exists "medicine dose notes: read published" on public.medicine_dose_notes;
create policy "medicine dose notes: read published" on public.medicine_dose_notes
    for select to anon, authenticated
    using (exists (select 1 from public.medicines m
                   where m.id = medicine_id and m.is_published));

drop policy if exists "medicine dose sources: read published" on public.medicine_dose_sources;
create policy "medicine dose sources: read published" on public.medicine_dose_sources
    for select to anon, authenticated
    using (exists (select 1 from public.medicines m
                   where m.id = medicine_id and m.is_published));

grant select on public.medicine_doses, public.medicine_dose_notes,
                public.medicine_dose_sources to anon, authenticated;

-- Installed apps download the medicines again (with the new tables).
update public.content_version set version = version + 1, updated_at = now() where id = 1;

commit;
