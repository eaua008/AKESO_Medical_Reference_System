-- =====================================================================
-- Akeso migration 050: Study Hub, part 1 (flashcards)
-- =====================================================================
-- Run AFTER 049. Safe to run again (add-only: new tables and functions).
--
--   study_subjects   Anatomy, Pathology, Pharmacology, Microbiology
--   decks            official (educators draft, admins publish) or personal
--   cards            basic | mcq | cloze | label3d, checked by a trigger
--   card_states      each person's spaced-repetition state per card. card_key
--                    is the card's id, or an "auto:..." key for the cards the
--                    app makes from the encyclopedia (those have no rows here
--                    apart from their states and review history)
--   review_log       every rating, append-only; client_id makes uploads
--                    idempotent, and replaying it (after reset_at) rebuilds
--                    card_states
--   study_settings   new cards a day, reviews a day, learning steps
--   card_reports     "this card is wrong": staff see them in Content
--                    Management -> Decks (the Clinical Exchange queue only
--                    takes posts and replies, so cards get their own list)
--
-- Who can do what:
--   * everyone signed in reads PUBLISHED official decks and their cards
--   * a student reads and writes only their own personal decks and cards,
--     their own states, history and settings
--   * educators and admins (after two-factor) write official decks through
--     the admin_* functions; educators can only save drafts, only admins
--     publish. Every change is in the audit trail (migration 004) and
--     publishing changes content_version.
--   * nobody, educators included, can read another person's progress
-- =====================================================================

begin;

-- ---------------------------------------------------------------------
-- 1. Tables
-- ---------------------------------------------------------------------
create table if not exists public.study_subjects (
    id        text primary key check (id ~ '^[a-z0-9_]{2,40}$'),
    name      text not null check (char_length(name) between 1 and 60),
    icon      text not null default '' check (char_length(icon) <= 40),
    position  integer not null default 0
);
insert into public.study_subjects (id, name, icon, position) values
    ('anatomy', 'Anatomy', 'heart-pulse', 1),
    ('pathology', 'Pathology', 'activity', 2),
    ('pharmacology', 'Pharmacology', 'pill', 3),
    ('microbiology', 'Microbiology', 'microscope', 4)
on conflict (id) do nothing;

create table if not exists public.decks (
    id           uuid primary key default gen_random_uuid(),
    title        text not null check (char_length(btrim(title)) between 1 and 120),
    description  text not null default '' check (char_length(description) <= 1000),
    subject_id   text references public.study_subjects (id) on delete set null,
    origin       text not null default 'personal' check (origin in ('official', 'personal')),
    owner_id     uuid references auth.users (id) on delete cascade,
    status       text not null default 'draft' check (status in ('draft', 'published')),
    visibility   text not null default 'private' check (visibility in ('private', 'shared', 'public')),
    lesson_id    uuid,                                 -- foreign key added in Phase 2
    created_by   uuid references auth.users (id) on delete set null,
    updated_by   uuid references auth.users (id) on delete set null,
    created_at   timestamptz not null default now(),
    updated_at   timestamptz not null default now(),
    deleted_at   timestamptz,
    server_updated_at timestamptz not null default now(),
    -- an official deck belongs to nobody; a personal one to its owner
    constraint decks_owner_matches check (
        (origin = 'official' and owner_id is null) or (origin = 'personal' and owner_id is not null))
);

create table if not exists public.cards (
    id           uuid primary key default gen_random_uuid(),
    deck_id      uuid not null references public.decks (id) on delete cascade,
    type         text not null check (type in ('basic', 'mcq', 'cloze', 'label3d')),
    front        text not null default '' check (char_length(front) <= 2000),
    back         text not null default '' check (char_length(back) <= 2000),
    choices      jsonb not null default '[]',
    cloze_text   text not null default '' check (char_length(cloze_text) <= 2000),
    part_ids     text[] not null default '{}',
    source_kind  text check (source_kind in ('disease', 'symptom', 'medicine', 'article', 'body_part')),
    source_id    text check (char_length(source_id) <= 120),
    tags         text[] not null default '{}',
    position     integer not null default 0,
    created_at   timestamptz not null default now(),
    updated_at   timestamptz not null default now(),
    deleted_at   timestamptz,
    server_updated_at timestamptz not null default now()
);

create table if not exists public.card_states (
    user_id       uuid not null default auth.uid() references auth.users (id) on delete cascade,
    card_key      text not null check (char_length(card_key) between 1 and 200),
    state         text not null default 'new'
                  check (state in ('new', 'learning', 'review', 'relearning', 'suspended')),
    due           timestamptz,
    interval_days real not null default 0,
    ease          real not null default 2.5,
    reps          integer not null default 0,
    lapses        integer not null default 0,
    step          integer not null default 0,
    last_rating   smallint check (last_rating between 1 and 4),
    last_review   timestamptz,
    reset_at      timestamptz,                      -- "Reset progress": history before this is ignored
    updated_at    timestamptz not null default now(),
    server_updated_at timestamptz not null default now(),
    primary key (user_id, card_key)
);

create table if not exists public.review_log (
    id              uuid primary key default gen_random_uuid(),
    user_id         uuid not null default auth.uid() references auth.users (id) on delete cascade,
    card_key        text not null check (char_length(card_key) between 1 and 200),
    rating          smallint not null check (rating between 1 and 4),
    reviewed_at     timestamptz not null,
    elapsed_ms      integer not null default 0 check (elapsed_ms >= 0),
    state_before    text not null default 'new',
    interval_before real not null default 0,
    interval_after  real not null default 0,
    ease_after      real not null default 2.5,
    client_id       uuid not null unique,
    server_received_at timestamptz not null default now()
);

alter table public.card_states add column if not exists reset_at timestamptz;

create table if not exists public.study_settings (
    user_id        uuid primary key default auth.uid() references auth.users (id) on delete cascade,
    new_per_day    integer not null default 20 check (new_per_day between 0 and 500),
    max_reviews    integer not null default 200 check (max_reviews between 0 and 5000),
    learning_steps integer[] not null default '{1,10}',
    relearn_steps  integer[] not null default '{10}',
    updated_at     timestamptz not null default now()
);

create table if not exists public.card_reports (
    id           uuid primary key default gen_random_uuid(),
    reporter_id  uuid not null default auth.uid() references auth.users (id) on delete cascade,
    card_ref     text not null check (char_length(card_ref) between 1 and 200),
    reason       text not null check (reason in ('wrong', 'unclear', 'outdated', 'typo', 'other')),
    note         text not null default '' check (char_length(note) <= 500),
    status       text not null default 'open' check (status in ('open', 'resolved')),
    created_at   timestamptz not null default now(),
    unique (reporter_id, card_ref)
);

create index if not exists cards_deck_idx on public.cards (deck_id);
create index if not exists cards_pull_idx on public.cards (server_updated_at);
create index if not exists card_states_due_idx on public.card_states (user_id, due);
create index if not exists card_states_pull_idx on public.card_states (user_id, server_updated_at);
create index if not exists review_log_user_idx on public.review_log (user_id, reviewed_at);
create index if not exists review_log_pull_idx on public.review_log (user_id, server_received_at);
create index if not exists decks_owner_idx on public.decks (owner_id);
create index if not exists decks_origin_idx on public.decks (origin, status);
create index if not exists decks_pull_idx on public.decks (server_updated_at);
create index if not exists card_reports_open_idx on public.card_reports (status, created_at);


-- ---------------------------------------------------------------------
-- 2. Checks and stamps
-- ---------------------------------------------------------------------
-- A card must make sense for its type.
create or replace function public.st_check_card()
returns trigger
language plpgsql
set search_path = ''
as $$
declare
    n_choices integer;
    n_correct integer;
begin
    if new.deleted_at is not null then
        return new;                               -- a deleted card is not checked again
    end if;
    if new.type = 'basic' then
        if btrim(new.front) = '' or btrim(new.back) = '' then
            raise exception 'A basic card needs a front and a back.';
        end if;
    elsif new.type = 'mcq' then
        if btrim(new.front) = '' then raise exception 'A multiple-choice card needs a question.'; end if;
        if jsonb_typeof(new.choices) <> 'array' then raise exception 'Add the choices.'; end if;
        n_choices := jsonb_array_length(new.choices);
        if n_choices < 2 or n_choices > 6 then
            raise exception 'A multiple-choice card needs 2 to 6 choices.';
        end if;
        select count(*) filter (where coalesce((c ->> 'correct')::boolean, false))
        into n_correct from jsonb_array_elements(new.choices) c;
        if n_correct < 1 then raise exception 'Mark at least one choice as correct.'; end if;
        if exists (select 1 from jsonb_array_elements(new.choices) c
                   where btrim(coalesce(c ->> 'text', '')) = ''
                      or char_length(coalesce(c ->> 'text', '')) > 600
                      or char_length(coalesce(c ->> 'rationale', '')) > 600) then
            raise exception 'Every choice needs its text (and rationales stay under 600 letters).';
        end if;
    elsif new.type = 'cloze' then
        if new.cloze_text !~ '\{\{.+?\}\}' then
            raise exception 'A fill-in-the-blank card needs at least one {{blank}}.';
        end if;
    elsif new.type = 'label3d' then
        if coalesce(array_length(new.part_ids, 1), 0) = 0 then
            raise exception 'A 3D label card needs at least one body part.';
        end if;
    end if;
    return new;
end $$;

drop trigger if exists cards_check on public.cards;
create trigger cards_check before insert or update on public.cards
    for each row execute function public.st_check_card();

-- When the server last saw a change (what "changed since my last sync" uses).
create or replace function public.st_touch()
returns trigger
language plpgsql
set search_path = ''
as $$
begin
    new.server_updated_at := now();
    return new;
end $$;

drop trigger if exists decks_touch on public.decks;
create trigger decks_touch before insert or update on public.decks
    for each row execute function public.st_touch();
drop trigger if exists cards_touch on public.cards;
create trigger cards_touch before insert or update on public.cards
    for each row execute function public.st_touch();
drop trigger if exists card_states_touch on public.card_states;
create trigger card_states_touch before insert or update on public.card_states
    for each row execute function public.st_touch();

-- A personal deck can only be made by and for yourself.
create or replace function public.st_own_deck()
returns trigger
language plpgsql
set search_path = ''
as $$
begin
    if auth.uid() is not null and new.origin = 'personal' then
        if tg_op = 'INSERT' then
            new.owner_id := auth.uid();
            new.created_by := auth.uid();
        end if;
        new.updated_by := auth.uid();
        new.status := 'draft';                   -- "published" means official only
    end if;
    return new;
end $$;

drop trigger if exists decks_own on public.decks;
create trigger decks_own before insert or update on public.decks
    for each row execute function public.st_own_deck();


-- ---------------------------------------------------------------------
-- 3. Row-level security
-- ---------------------------------------------------------------------
alter table public.study_subjects enable row level security;
alter table public.decks          enable row level security;
alter table public.cards          enable row level security;
alter table public.card_states    enable row level security;
alter table public.review_log     enable row level security;
alter table public.study_settings enable row level security;
alter table public.card_reports   enable row level security;

revoke all on public.study_subjects, public.decks, public.cards, public.card_states,
              public.review_log, public.study_settings, public.card_reports
    from anon, authenticated;
grant select on public.study_subjects to anon, authenticated;
grant select, insert, update, delete on public.decks, public.cards to authenticated;
grant select, insert, update on public.card_states, public.study_settings to authenticated;
grant select, insert on public.review_log to authenticated;
-- card_reports: only through report_card() and the staff functions

drop policy if exists "subjects: read" on public.study_subjects;
create policy "subjects: read" on public.study_subjects
    for select to anon, authenticated using (true);

drop policy if exists "decks: read" on public.decks;
create policy "decks: read" on public.decks
    for select to authenticated
    using ((origin = 'official' and status = 'published' and deleted_at is null)
           or owner_id = (select auth.uid()));
drop policy if exists "decks: own insert" on public.decks;
create policy "decks: own insert" on public.decks
    for insert to authenticated
    with check (origin = 'personal' and owner_id = (select auth.uid()));
drop policy if exists "decks: own update" on public.decks;
create policy "decks: own update" on public.decks
    for update to authenticated
    using (origin = 'personal' and owner_id = (select auth.uid()))
    with check (origin = 'personal' and owner_id = (select auth.uid()));
drop policy if exists "decks: own delete" on public.decks;
create policy "decks: own delete" on public.decks
    for delete to authenticated
    using (origin = 'personal' and owner_id = (select auth.uid()));

drop policy if exists "cards: read" on public.cards;
create policy "cards: read" on public.cards
    for select to authenticated
    using (exists (select 1 from public.decks d where d.id = deck_id
                   and ((d.origin = 'official' and d.status = 'published' and d.deleted_at is null)
                        or d.owner_id = (select auth.uid()))));
drop policy if exists "cards: own write" on public.cards;
create policy "cards: own write" on public.cards
    for all to authenticated
    using (exists (select 1 from public.decks d where d.id = deck_id
                   and d.origin = 'personal' and d.owner_id = (select auth.uid())))
    with check (exists (select 1 from public.decks d where d.id = deck_id
                        and d.origin = 'personal' and d.owner_id = (select auth.uid())));

drop policy if exists "card states: own" on public.card_states;
create policy "card states: own" on public.card_states
    for all to authenticated
    using (user_id = (select auth.uid())) with check (user_id = (select auth.uid()));

drop policy if exists "review log: own read" on public.review_log;
create policy "review log: own read" on public.review_log
    for select to authenticated using (user_id = (select auth.uid()));
drop policy if exists "review log: own add" on public.review_log;
create policy "review log: own add" on public.review_log
    for insert to authenticated with check (user_id = (select auth.uid()));

drop policy if exists "study settings: own" on public.study_settings;
create policy "study settings: own" on public.study_settings
    for all to authenticated
    using (user_id = (select auth.uid())) with check (user_id = (select auth.uid()));


-- ---------------------------------------------------------------------
-- 4. Who is staff
-- ---------------------------------------------------------------------
-- An educator or an admin, after two-factor. Returns their id.
create or replace function public.st_staff()
returns uuid
language plpgsql stable security definer set search_path = ''
as $$
declare
    uid uuid := auth.uid();
    v_role text;
begin
    if uid is null then raise exception 'Not signed in.'; end if;
    if not public.mfa_satisfied() then raise exception 'Two-factor check required.'; end if;
    select role::text into v_role from public.user_roles where user_id = uid;
    if coalesce(v_role, 'student') not in ('educator', 'admin') then
        raise exception 'Only educators and admins can do that.';
    end if;
    return uid;
end $$;


-- ---------------------------------------------------------------------
-- 5. Official decks (Content Management -> Decks)
-- ---------------------------------------------------------------------
create or replace function public.st_card_json(c public.cards)
returns jsonb
language sql stable security definer set search_path = ''
as $$
    select jsonb_build_object(
        'id', c.id, 'type', c.type, 'front', c.front, 'back', c.back,
        'choices', c.choices, 'cloze_text', c.cloze_text, 'part_ids', to_jsonb(c.part_ids),
        'source_kind', c.source_kind, 'source_id', c.source_id, 'tags', to_jsonb(c.tags),
        'position', c.position, 'updated_at', c.updated_at);
$$;

create or replace function public.admin_list_decks()
returns jsonb
language plpgsql stable security definer set search_path = ''
as $$
begin
    perform public.st_staff();
    return coalesce((
        select jsonb_agg(jsonb_build_object(
            'id', d.id, 'title', d.title, 'subject_id', d.subject_id, 'status', d.status,
            'updated_at', d.updated_at,
            'author', coalesce((select nullif(p.display_name, '') from public.profiles p
                                where p.id = coalesce(d.updated_by, d.created_by)), ''),
            'card_count', (select count(*) from public.cards c
                           where c.deck_id = d.id and c.deleted_at is null),
            'open_reports', (select count(*) from public.card_reports r
                             join public.cards c on c.id::text = r.card_ref
                             where c.deck_id = d.id and r.status = 'open')
        ) order by d.updated_at desc)
        from public.decks d
        where d.origin = 'official' and d.deleted_at is null
    ), '[]'::jsonb);
end $$;

create or replace function public.admin_get_deck(p_id uuid)
returns jsonb
language plpgsql stable security definer set search_path = ''
as $$
declare v jsonb;
begin
    perform public.st_staff();
    select jsonb_build_object(
        'id', d.id, 'title', d.title, 'description', d.description,
        'subject_id', d.subject_id, 'status', d.status, 'updated_at', d.updated_at,
        'cards', coalesce((select jsonb_agg(public.st_card_json(c) order by c.position, c.created_at)
                           from public.cards c where c.deck_id = d.id and c.deleted_at is null),
                          '[]'::jsonb))
    into v
    from public.decks d
    where d.id = p_id and d.origin = 'official' and d.deleted_at is null;
    if v is null then raise exception 'That deck no longer exists.'; end if;
    return v;
end $$;

-- p: {id?, title, description, subject_id, cards: [card...]}. Cards not in the
-- list are deleted (softly, so other computers learn about it). Returns the id.
create or replace function public.admin_save_deck(p jsonb)
returns uuid
language plpgsql security definer set search_path = ''
as $$
declare
    me uuid := public.st_staff();
    v_id uuid := nullif(p ->> 'id', '')::uuid;
    v_title text := btrim(coalesce(p ->> 'title', ''));
    v_status text;
    v_new boolean := false;
    v_keep uuid[] := '{}';
    c jsonb;
    v_card uuid;
    pos integer := 0;
begin
    if v_title = '' then raise exception 'Give the deck a title.'; end if;
    if char_length(v_title) > 120 then raise exception 'Keep the title under 120 letters.'; end if;
    if jsonb_typeof(coalesce(p -> 'cards', '[]'::jsonb)) <> 'array' then
        raise exception 'The cards could not be read.';
    end if;
    if jsonb_array_length(coalesce(p -> 'cards', '[]'::jsonb)) > 2000 then
        raise exception 'A deck can hold up to 2,000 cards.';
    end if;

    if v_id is null or not exists (select 1 from public.decks where id = v_id) then
        v_new := true;
        insert into public.decks (id, title, origin, owner_id, status, created_by, updated_by)
        values (coalesce(v_id, gen_random_uuid()), v_title, 'official', null, 'draft', me, me)
        returning id into v_id;
    else
        select status into v_status from public.decks
        where id = v_id and origin = 'official' and deleted_at is null;
        if v_status is null then raise exception 'That deck no longer exists.'; end if;
        if v_status = 'published' and not public.is_admin() then
            raise exception 'This deck is published. Ask an admin to unpublish it before editing.';
        end if;
    end if;

    update public.decks set
        title = v_title,
        description = left(btrim(coalesce(p ->> 'description', '')), 1000),
        subject_id = nullif(p ->> 'subject_id', ''),
        updated_by = me,
        updated_at = now()
    where id = v_id;

    for c in select * from jsonb_array_elements(coalesce(p -> 'cards', '[]'::jsonb)) loop
        pos := pos + 1;
        v_card := nullif(c ->> 'id', '')::uuid;
        if v_card is not null and exists (select 1 from public.cards where id = v_card and deck_id = v_id) then
            update public.cards set
                type = c ->> 'type', front = coalesce(c ->> 'front', ''),
                back = coalesce(c ->> 'back', ''),
                choices = coalesce(c -> 'choices', '[]'::jsonb),
                cloze_text = coalesce(c ->> 'cloze_text', ''),
                part_ids = coalesce((select array_agg(x) from jsonb_array_elements_text(c -> 'part_ids') x), '{}'),
                source_kind = nullif(c ->> 'source_kind', ''), source_id = nullif(c ->> 'source_id', ''),
                tags = coalesce((select array_agg(x) from jsonb_array_elements_text(c -> 'tags') x), '{}'),
                position = pos, deleted_at = null, updated_at = now()
            where id = v_card;
        else
            insert into public.cards (id, deck_id, type, front, back, choices, cloze_text, part_ids,
                                      source_kind, source_id, tags, position)
            values (coalesce(v_card, gen_random_uuid()), v_id, c ->> 'type', coalesce(c ->> 'front', ''),
                    coalesce(c ->> 'back', ''), coalesce(c -> 'choices', '[]'::jsonb),
                    coalesce(c ->> 'cloze_text', ''),
                    coalesce((select array_agg(x) from jsonb_array_elements_text(c -> 'part_ids') x), '{}'),
                    nullif(c ->> 'source_kind', ''), nullif(c ->> 'source_id', ''),
                    coalesce((select array_agg(x) from jsonb_array_elements_text(c -> 'tags') x), '{}'), pos)
            returning id into v_card;
        end if;
        v_keep := v_keep || v_card;
    end loop;

    update public.cards set deleted_at = now(), updated_at = now()
    where deck_id = v_id and deleted_at is null and not (id = any (v_keep));

    if v_status = 'published' then
        perform public.ad_bump();                 -- students' copy of a live deck changed
    end if;
    perform public.ad_log(case when v_new then 'create' else 'update' end, 'deck', v_id::text, v_title);
    return v_id;
end $$;

create or replace function public.admin_set_deck_status(p_id uuid, p_status text)
returns void
language plpgsql security definer set search_path = ''
as $$
declare v_title text;
begin
    perform public.st_staff();
    if not public.is_admin() then raise exception 'Only admins can publish or unpublish decks.'; end if;
    if p_status not in ('draft', 'published') then raise exception 'Unknown status.'; end if;
    update public.decks set status = p_status, updated_by = auth.uid(), updated_at = now()
    where id = p_id and origin = 'official' and deleted_at is null
    returning title into v_title;
    if v_title is null then raise exception 'That deck no longer exists.'; end if;
    perform public.ad_bump();
    perform public.ad_log(case when p_status = 'published' then 'publish' else 'unpublish' end,
                          'deck', p_id::text, v_title);
end $$;

-- Delete an official deck (admins). Soft, so every computer drops it on sync.
create or replace function public.admin_delete_deck(p_id uuid)
returns void
language plpgsql security definer set search_path = ''
as $$
declare v_title text; v_status text;
begin
    perform public.st_staff();
    select title, status into v_title, v_status from public.decks
    where id = p_id and origin = 'official' and deleted_at is null;
    if v_title is null then raise exception 'That deck no longer exists.'; end if;
    if v_status = 'published' and not public.is_admin() then
        raise exception 'Only admins can delete a published deck.';
    end if;
    update public.decks set deleted_at = now(), status = 'draft', updated_by = auth.uid(), updated_at = now()
    where id = p_id;
    update public.cards set deleted_at = now(), updated_at = now() where deck_id = p_id and deleted_at is null;
    if v_status = 'published' then perform public.ad_bump(); end if;
    perform public.ad_log('delete', 'deck', p_id::text, v_title);
end $$;


-- ---------------------------------------------------------------------
-- 6. Reporting a card
-- ---------------------------------------------------------------------
create or replace function public.report_card(p_card_ref text, p_reason text, p_note text)
returns void
language plpgsql security definer set search_path = ''
as $$
declare me uuid := auth.uid();
begin
    if me is null then raise exception 'Not signed in.'; end if;
    if p_reason not in ('wrong', 'unclear', 'outdated', 'typo', 'other') then
        raise exception 'Choose what is wrong with the card.';
    end if;
    if coalesce(p_card_ref, '') = '' or char_length(p_card_ref) > 200 then
        raise exception 'That card can''t be reported.';
    end if;
    if (select count(*) from public.card_reports
        where reporter_id = me and created_at > now() - interval '1 hour') >= 20 then
        raise exception 'Slow down: you can report up to 20 cards an hour.';
    end if;
    insert into public.card_reports (reporter_id, card_ref, reason, note)
    values (me, p_card_ref, p_reason, left(coalesce(p_note, ''), 500))
    on conflict (reporter_id, card_ref) do update
        set reason = excluded.reason, note = excluded.note, status = 'open', created_at = now();
end $$;

create or replace function public.admin_list_card_reports()
returns jsonb
language plpgsql stable security definer set search_path = ''
as $$
begin
    perform public.st_staff();
    return coalesce((
        select jsonb_agg(jsonb_build_object(
            'id', r.id, 'card_ref', r.card_ref, 'reason', r.reason, 'note', r.note,
            'created_at', r.created_at,
            'deck_id', c.deck_id, 'deck_title', d.title,
            'front', coalesce(c.front, ''), 'cloze_text', coalesce(c.cloze_text, ''))
            order by r.created_at desc)
        from public.card_reports r
        left join public.cards c on c.id::text = r.card_ref
        left join public.decks d on d.id = c.deck_id
        where r.status = 'open'
          and (c.id is null or d.origin = 'official')        -- personal cards are their owner's business
    ), '[]'::jsonb);
end $$;

create or replace function public.admin_resolve_card_report(p_id uuid)
returns void
language plpgsql security definer set search_path = ''
as $$
begin
    perform public.st_staff();
    update public.card_reports set status = 'resolved' where id = p_id;
    perform public.ad_log('resolve_report', 'card', p_id::text, '');
end $$;


-- ---------------------------------------------------------------------
-- 7. Who may call what
-- ---------------------------------------------------------------------
revoke execute on function public.st_card_json(public.cards) from public, anon, authenticated;
do $$
declare fn text;
begin
    foreach fn in array array[
        'public.st_staff()', 'public.admin_list_decks()', 'public.admin_get_deck(uuid)',
        'public.admin_save_deck(jsonb)', 'public.admin_set_deck_status(uuid, text)',
        'public.admin_delete_deck(uuid)', 'public.report_card(text, text, text)',
        'public.admin_list_card_reports()', 'public.admin_resolve_card_report(uuid)'] loop
        execute format('revoke execute on function %s from public, anon', fn);
        execute format('grant execute on function %s to authenticated', fn);
    end loop;
end $$;

commit;

notify pgrst, 'reload schema';
