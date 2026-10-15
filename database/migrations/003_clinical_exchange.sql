-- =====================================================================
-- Akeso migration 003: Clinical Exchange (case discussion board)
-- =====================================================================
-- Run once in the Supabase SQL editor, AFTER 002_accounts.sql (it uses
-- profiles, user_roles and mfa_satisfied() from there). Safe to run again.
--
-- What this creates
--
--   exchange_posts         hypothetical cases and quick questions
--   exchange_post_tags     links to diseases / symptoms / medicines / body systems
--   exchange_replies       replies, one level of nesting
--   exchange_votes         upvotes on posts and replies
--   exchange_poll_options  "what's the diagnosis?" choices (author's + suggested)
--   exchange_poll_votes    one vote per student per poll, changeable until revealed
--   exchange_follows       who follows which post
--   notifications          replies, best answers, reveals, moderation notices
--   exchange_reports       reports from students
--   exchange_mod_log       every moderator action, append-only
--
-- Security model
--
--   The app can't read or write these tables directly. Everything goes
--   through the SECURITY DEFINER functions at the bottom, because:
--     * anonymous posts must hide WHO posted from everyone except
--       moderators, and row-level security can hide rows but not a column;
--     * every post and reply passes a check for real patient data and a
--       rate limit, and those checks can't be skipped by a modified app;
--     * counts (replies, votes) stay correct because only these functions
--       change them.
--   Moderators = educators and admins (public.user_roles).
-- =====================================================================

begin;

-- ---------------------------------------------------------------------
-- 1. Tables
-- ---------------------------------------------------------------------
create table if not exists public.exchange_posts (
    id                  uuid primary key default gen_random_uuid(),
    author_id           uuid not null references auth.users (id) on delete cascade,
    kind                text not null check (kind in ('case', 'question')),
    title               text not null check (char_length(title) between 5 and 140),
    body                text not null default '' check (char_length(body) <= 5000),
    question            text not null default '' check (char_length(question) <= 500),
    is_anonymous        boolean not null default false,
    -- de-identified case details (a range, never an exact age)
    age_range           text check (age_range in ('0–4', '5–12', '13–17', '18–24', '25–34',
                                                  '35–44', '45–54', '55–64', '65–74',
                                                  '75–84', '85+')),
    sex                 text check (sex in ('female', 'male')),
    setting             text check (char_length(setting) <= 40),
    vitals              jsonb,
    case_data           jsonb not null default '{}'::jsonb
                        check (pg_column_size(case_data) <= 20000),
    source              text check (source in ('symptom_case', 'interaction_case')),
    status              text not null default 'open'
                        check (status in ('open', 'locked', 'hidden', 'removed')),
    has_poll            boolean not null default false,
    revealed_option_id  uuid,
    reveal_explanation  text not null default '' check (char_length(reveal_explanation) <= 2000),
    revealed_at         timestamptz,
    best_reply_id       uuid,
    reply_count         integer not null default 0,
    score               integer not null default 0,
    created_at          timestamptz not null default now(),
    edited_at           timestamptz,
    last_activity_at    timestamptz not null default now()
);
create index if not exists exchange_posts_new_idx on public.exchange_posts (created_at desc);
create index if not exists exchange_posts_active_idx on public.exchange_posts (last_activity_at desc);
create index if not exists exchange_posts_author_idx on public.exchange_posts (author_id);

create table if not exists public.exchange_post_tags (
    post_id  uuid not null references public.exchange_posts (id) on delete cascade,
    kind     text not null check (kind in ('disease', 'symptom', 'medicine', 'body_system', 'topic')),
    ref_id   text not null check (char_length(ref_id) between 1 and 80),
    label    text not null check (char_length(label) between 1 and 80),
    primary key (post_id, kind, ref_id)
);
create index if not exists exchange_post_tags_ref_idx on public.exchange_post_tags (kind, ref_id);

create table if not exists public.exchange_replies (
    id              uuid primary key default gen_random_uuid(),
    post_id         uuid not null references public.exchange_posts (id) on delete cascade,
    parent_id       uuid references public.exchange_replies (id) on delete cascade,
    author_id       uuid not null references auth.users (id) on delete cascade,
    body            text not null check (char_length(body) between 1 and 3000),
    is_anonymous    boolean not null default false,
    -- what the author had voted for in the poll when they wrote this
    poll_option_id  uuid,
    verified_by     uuid references auth.users (id) on delete set null,
    verified_at     timestamptz,
    score           integer not null default 0,
    status          text not null default 'open' check (status in ('open', 'hidden', 'removed')),
    created_at      timestamptz not null default now(),
    edited_at       timestamptz
);
create index if not exists exchange_replies_post_idx on public.exchange_replies (post_id, created_at);

create table if not exists public.exchange_votes (
    user_id      uuid not null references auth.users (id) on delete cascade,
    target_kind  text not null check (target_kind in ('post', 'reply')),
    target_id    uuid not null,
    created_at   timestamptz not null default now(),
    primary key (user_id, target_kind, target_id)
);

create table if not exists public.exchange_poll_options (
    id            uuid primary key default gen_random_uuid(),
    post_id       uuid not null references public.exchange_posts (id) on delete cascade,
    disease_id    text references public.diseases (id) on delete set null,
    label         text not null check (char_length(label) between 1 and 80),
    suggested_by  uuid references auth.users (id) on delete set null,
    by_author     boolean not null default false,
    status        text not null default 'active' check (status in ('active', 'hidden')),
    created_at    timestamptz not null default now()
);
create unique index if not exists exchange_poll_options_unique
    on public.exchange_poll_options (post_id, coalesce(disease_id, lower(label)));

create table if not exists public.exchange_poll_votes (
    post_id    uuid not null references public.exchange_posts (id) on delete cascade,
    user_id    uuid not null references auth.users (id) on delete cascade,
    option_id  uuid not null references public.exchange_poll_options (id) on delete cascade,
    voted_at   timestamptz not null default now(),
    primary key (post_id, user_id)
);

create table if not exists public.exchange_follows (
    user_id     uuid not null references auth.users (id) on delete cascade,
    post_id     uuid not null references public.exchange_posts (id) on delete cascade,
    created_at  timestamptz not null default now(),
    primary key (user_id, post_id)
);

create table if not exists public.notifications (
    id          bigint generated always as identity primary key,
    user_id     uuid not null references auth.users (id) on delete cascade,
    kind        text not null check (kind in ('reply', 'best_answer', 'verified', 'reveal',
                                              'moderation', 'mention')),
    post_id     uuid references public.exchange_posts (id) on delete cascade,
    reply_id    uuid references public.exchange_replies (id) on delete cascade,
    message     text not null check (char_length(message) <= 300),
    created_at  timestamptz not null default now(),
    read_at     timestamptz
);
create index if not exists notifications_user_idx on public.notifications (user_id, created_at desc);

create table if not exists public.exchange_reports (
    id           bigint generated always as identity primary key,
    reporter_id  uuid not null references auth.users (id) on delete cascade,
    target_kind  text not null check (target_kind in ('post', 'reply')),
    target_id    uuid not null,
    reason       text not null check (reason in ('patient_data', 'misinformation', 'harassment',
                                                 'spam', 'off_topic', 'other')),
    note         text not null default '' check (char_length(note) <= 500),
    status       text not null default 'open' check (status in ('open', 'resolved', 'dismissed')),
    handled_by   uuid references auth.users (id) on delete set null,
    handled_at   timestamptz,
    created_at   timestamptz not null default now(),
    unique (reporter_id, target_kind, target_id)
);

create table if not exists public.exchange_mod_log (
    id            bigint generated always as identity primary key,
    moderator_id  uuid references auth.users (id) on delete set null,
    action        text not null,
    target_kind   text not null,
    target_id     uuid not null,
    reason        text not null default '',
    created_at    timestamptz not null default now()
);

-- RLS on, no policies, no grants: only the functions below get in.
do $$
declare t text;
begin
    foreach t in array array['exchange_posts', 'exchange_post_tags', 'exchange_replies',
                             'exchange_votes', 'exchange_poll_options', 'exchange_poll_votes',
                             'exchange_follows', 'notifications', 'exchange_reports',
                             'exchange_mod_log'] loop
        execute format('alter table public.%I enable row level security', t);
        execute format('revoke all on public.%I from anon, authenticated', t);
    end loop;
end $$;


-- ---------------------------------------------------------------------
-- 2. Helpers (not callable from the app)
-- ---------------------------------------------------------------------

-- The signed-in user, after the two-factor check. Every function starts here.
create or replace function public.ex_uid()
returns uuid
language plpgsql stable security definer set search_path = ''
as $$
declare uid uuid := auth.uid();
begin
    if uid is null then raise exception 'Not signed in.'; end if;
    if not public.mfa_satisfied() then raise exception 'Two-factor check required.'; end if;
    return uid;
end $$;

create or replace function public.ex_is_mod(p_user uuid)
returns boolean
language sql stable security definer set search_path = ''
as $$
    select exists (select 1 from public.user_roles r
                   where r.user_id = p_user and r.role in ('educator', 'admin'));
$$;

-- How an author appears to a viewer. Anonymous = "Anonymous student" to
-- everyone except the author and moderators (who see the real name, so
-- anonymity can't be used to harass).
create or replace function public.ex_author(p_author uuid, p_anon boolean, p_viewer uuid)
returns jsonb
language sql stable security definer set search_path = ''
as $$
    select case
        when p_anon and p_viewer <> p_author and not public.ex_is_mod(p_viewer) then
            jsonb_build_object('name', 'Anonymous student', 'anonymous', true)
        else jsonb_build_object(
            'name', coalesce(nullif(p.display_name, ''), 'Akeso student'),
            'anonymous', p_anon,
            'handle', case when p.is_public and not p_anon then p.handle end,
            'program', case when p.show_program and not p_anon then p.program end,
            'verified_domain', case when not p_anon and p.school_email_verified_at is not null
                                    then p.school_email_domain end,
            'role', case when not p_anon then (select r.role::text from public.user_roles r
                                               where r.user_id = p_author) end,
            'is_me', p_viewer = p_author)
        end
    from public.profiles p where p.id = p_author;
$$;

-- Text that looks like real patient data. Returns what was found, or null.
-- A safety net, not a guarantee: it can't recognise every name.
create or replace function public.ex_phi_check(p_text text)
returns text
language plpgsql immutable set search_path = ''
as $$
declare t text := coalesce(p_text, '');
begin
    if t ~ '(\+?63|\m0)9\d{2}[\s.-]?\d{3}[\s.-]?\d{4}' then
        return 'a phone number';
    end if;
    if t ~ '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}' then
        return 'an email address';
    end if;
    if t ~ '\m\d{1,2}[/.-]\d{1,2}[/.-](19|20)\d{2}\M'
       or t ~* '\m(jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)[a-z]*\.?\s+\d{1,2},?\s+(19|20)\d{2}\M'
       or t ~* '\m(birthday|date of birth|dob)\M' then
        return 'an exact date of birth';
    end if;
    if t ~* '\m(mrn|hrn|philhealth|record\s*(no|number|#)|hospital\s*(no|number|#)|case\s*(no|number|#)|bed\s*(no|number|#))\M' then
        return 'a record or ID number';
    end if;
    if t ~ '\m(Mr|Mrs|Ms|Miss|Mx)\.?\s+[A-Z][a-z]+' or t ~* '\m(patient|pt)(''s)?\s*name\M' then
        return 'a patient''s name';
    end if;
    return null;
end $$;

create or replace function public.ex_rate(p_user uuid, p_what text, p_max integer, p_window interval)
returns void
language plpgsql stable security definer set search_path = ''
as $$
declare n integer;
begin
    n := case p_what
        when 'post' then (select count(*) from public.exchange_posts
                          where author_id = p_user and created_at > now() - p_window)
        when 'reply' then (select count(*) from public.exchange_replies
                           where author_id = p_user and created_at > now() - p_window)
        when 'suggest' then (select count(*) from public.exchange_poll_options
                             where suggested_by = p_user and created_at > now() - p_window)
        when 'report' then (select count(*) from public.exchange_reports
                            where reporter_id = p_user and created_at > now() - p_window)
        else 0 end;
    if n >= p_max then
        raise exception 'Slow down: you have reached the limit of % %s per %.', p_max, p_what,
            replace(p_window::text, '01:00:00', 'hour');
    end if;
end $$;

create or replace function public.ex_notify(p_users uuid[], p_kind text, p_post uuid,
                                            p_reply uuid, p_message text, p_except uuid)
returns void
language sql security definer set search_path = ''
as $$
    insert into public.notifications (user_id, kind, post_id, reply_id, message)
    select distinct u, p_kind, p_post, p_reply, left(p_message, 300)
    from unnest(p_users) as u
    where u is not null and u is distinct from p_except;
$$;

create or replace function public.ex_short(p_text text, p_len integer default 60)
returns text
language sql immutable set search_path = ''
as $$
    select case when char_length(p_text) > p_len
                then left(p_text, p_len - 1) || '…' else p_text end;
$$;

-- Can this viewer see this post at all?
create or replace function public.ex_can_see(p_status text, p_author uuid, p_viewer uuid)
returns boolean
language sql stable security definer set search_path = ''
as $$
    select p_status in ('open', 'locked')
        or public.ex_is_mod(p_viewer)
        or (p_status = 'hidden' and p_author = p_viewer);
$$;


-- ---------------------------------------------------------------------
-- 3. Reading
-- ---------------------------------------------------------------------

-- The feed. p_tab: newest | active | unanswered | following | mine
create or replace function public.ex_feed(
    p_tab text default 'newest', p_tag_kind text default null, p_tag_id text default null,
    p_body_system text default null, p_program text default null, p_search text default null,
    p_limit integer default 20, p_offset integer default 0)
returns setof jsonb
language plpgsql stable security definer set search_path = ''
as $$
declare
    me uuid := public.ex_uid();
    q text := nullif(trim(coalesce(p_search, '')), '');
begin
    return query
    select jsonb_build_object(
        'id', p.id, 'kind', p.kind, 'title', p.title,
        'excerpt', public.ex_short(coalesce(nullif(p.body, ''), p.question), 180),
        'author', public.ex_author(p.author_id, p.is_anonymous, me),
        'status', p.status, 'has_poll', p.has_poll,
        'revealed', p.revealed_option_id is not null,
        'has_best', p.best_reply_id is not null,
        'reply_count', p.reply_count, 'score', p.score,
        'age_range', p.age_range, 'sex', p.sex, 'source', p.source,
        'created_at', p.created_at, 'last_activity_at', p.last_activity_at,
        'voted', exists (select 1 from public.exchange_votes v where v.user_id = me
                         and v.target_kind = 'post' and v.target_id = p.id),
        'following', exists (select 1 from public.exchange_follows f
                             where f.user_id = me and f.post_id = p.id),
        'tags', coalesce((select jsonb_agg(jsonb_build_object('kind', t.kind, 'id', t.ref_id,
                                                              'label', t.label) order by t.kind, t.label)
                          from public.exchange_post_tags t where t.post_id = p.id), '[]'))
    from public.exchange_posts p
    left join public.profiles pr on pr.id = p.author_id
    where public.ex_can_see(p.status, p.author_id, me)
      and (p_tab is distinct from 'unanswered' or p.reply_count = 0)
      and (p_tab is distinct from 'following'
           or exists (select 1 from public.exchange_follows f where f.user_id = me and f.post_id = p.id))
      and (p_tab is distinct from 'mine' or p.author_id = me)
      and (p_tag_kind is null or exists (select 1 from public.exchange_post_tags t
                                         where t.post_id = p.id and t.kind = p_tag_kind
                                           and t.ref_id = p_tag_id))
      and (p_body_system is null
           or exists (select 1 from public.exchange_post_tags t
                      where t.post_id = p.id and t.kind = 'body_system' and t.ref_id = p_body_system)
           or exists (select 1 from public.exchange_post_tags t
                      join public.diseases d on d.id = t.ref_id
                      where t.post_id = p.id and t.kind = 'disease'
                        and d.body_system_id = p_body_system))
      -- program of the author; anonymous posts never match (it would hint at who wrote them)
      and (p_program is null or (not p.is_anonymous and pr.show_program and pr.program = p_program))
      and (q is null or p.title ilike '%' || q || '%' or p.body ilike '%' || q || '%'
           or p.question ilike '%' || q || '%'
           or exists (select 1 from public.exchange_post_tags t
                      where t.post_id = p.id and t.label ilike '%' || q || '%'))
    order by case when p_tab = 'active' then p.last_activity_at else p.created_at end desc
    limit least(greatest(p_limit, 1), 50) offset greatest(p_offset, 0);
end $$;

-- One post with everything: case details, tags, poll, replies.
create or replace function public.ex_post(p_id uuid)
returns jsonb
language plpgsql stable security definer set search_path = ''
as $$
declare
    me uuid := public.ex_uid();
    p public.exchange_posts;
    is_mod boolean := public.ex_is_mod(me);
    my_option uuid;
    show_results boolean;
    result jsonb;
begin
    select * into p from public.exchange_posts where id = p_id;
    if not found or not public.ex_can_see(p.status, p.author_id, me) then
        raise exception 'This post is not available.';
    end if;
    select option_id into my_option from public.exchange_poll_votes
    where post_id = p.id and user_id = me;
    show_results := my_option is not null or p.revealed_option_id is not null
                    or p.author_id = me or is_mod;

    select jsonb_build_object(
        'id', p.id, 'kind', p.kind, 'title', p.title, 'body', p.body, 'question', p.question,
        'author', public.ex_author(p.author_id, p.is_anonymous, me),
        'is_anonymous', p.is_anonymous,
        'age_range', p.age_range, 'sex', p.sex, 'setting', p.setting, 'vitals', p.vitals,
        'case_data', p.case_data, 'source', p.source, 'status', p.status,
        'score', p.score, 'reply_count', p.reply_count,
        'created_at', p.created_at, 'edited_at', p.edited_at,
        'best_reply_id', p.best_reply_id,
        'voted', exists (select 1 from public.exchange_votes v where v.user_id = me
                         and v.target_kind = 'post' and v.target_id = p.id),
        'following', exists (select 1 from public.exchange_follows f
                             where f.user_id = me and f.post_id = p.id),
        'is_author', p.author_id = me, 'can_moderate', is_mod,
        'tags', coalesce((select jsonb_agg(jsonb_build_object('kind', t.kind, 'id', t.ref_id,
                                                              'label', t.label) order by t.kind, t.label)
                          from public.exchange_post_tags t where t.post_id = p.id), '[]'),
        'poll', case when not p.has_poll then null else jsonb_build_object(
            'my_option', my_option,
            'show_results', show_results,
            'revealed_option', p.revealed_option_id,
            'explanation', case when p.revealed_option_id is not null then p.reveal_explanation end,
            'total', case when show_results then (select count(*) from public.exchange_poll_votes
                                                  where post_id = p.id) end,
            'options', coalesce((select jsonb_agg(jsonb_build_object(
                    'id', o.id, 'label', o.label, 'disease_id', o.disease_id,
                    'by_author', o.by_author,
                    'suggested', not o.by_author,
                    'votes', case when show_results then (select count(*) from public.exchange_poll_votes v
                                                          where v.option_id = o.id) end)
                    order by o.by_author desc, o.created_at)
                from public.exchange_poll_options o
                where o.post_id = p.id and (o.status = 'active' or is_mod)), '[]')) end,
        'replies', coalesce((select jsonb_agg(jsonb_build_object(
                'id', r.id, 'parent_id', r.parent_id,
                'body', case when r.status = 'removed' and not is_mod then '' else r.body end,
                'status', r.status,
                'author', public.ex_author(r.author_id, r.is_anonymous, me),
                'score', r.score, 'created_at', r.created_at, 'edited_at', r.edited_at,
                'voted', exists (select 1 from public.exchange_votes v where v.user_id = me
                                 and v.target_kind = 'reply' and v.target_id = r.id),
                'is_best', r.id = p.best_reply_id,
                'verified', r.verified_at is not null,
                -- the poll badge: what they had voted when they wrote it, and now
                'voted_label', (select o.label from public.exchange_poll_options o
                                where o.id = r.poll_option_id),
                'current_label', (select o.label from public.exchange_poll_votes pv
                                  join public.exchange_poll_options o on o.id = pv.option_id
                                  where pv.post_id = p.id and pv.user_id = r.author_id),
                'is_mine', r.author_id = me)
                order by r.created_at)
            from public.exchange_replies r
            where r.post_id = p.id
              and (r.status = 'open' or is_mod or r.author_id = me
                   or (r.status = 'removed' and exists (select 1 from public.exchange_replies c
                                                        where c.parent_id = r.id)))), '[]'))
    into result;
    return result;
end $$;


-- ---------------------------------------------------------------------
-- 4. Writing
-- ---------------------------------------------------------------------

-- Tags arrive as [{"kind":"disease","id":"dengue","label":"Dengue"}, ...]
create or replace function public.ex_set_tags(p_post uuid, p_tags jsonb)
returns void
language plpgsql security definer set search_path = ''
as $$
begin
    delete from public.exchange_post_tags where post_id = p_post;
    if jsonb_typeof(p_tags) <> 'array' then return; end if;
    if jsonb_array_length(p_tags) > 12 then raise exception 'Use at most 12 tags.'; end if;
    insert into public.exchange_post_tags (post_id, kind, ref_id, label)
    select p_post, t ->> 'kind', left(t ->> 'id', 80), left(coalesce(t ->> 'label', t ->> 'id'), 80)
    from jsonb_array_elements(p_tags) t
    where t ->> 'kind' in ('disease', 'symptom', 'medicine', 'body_system', 'topic')
      and coalesce(t ->> 'id', '') <> ''
    on conflict do nothing;
end $$;

create or replace function public.ex_create_post(
    p_kind text, p_title text, p_body text default '', p_question text default '',
    p_anonymous boolean default false, p_age_range text default null, p_sex text default null,
    p_setting text default null, p_vitals jsonb default null, p_case jsonb default '{}'::jsonb,
    p_source text default null, p_tags jsonb default '[]'::jsonb,
    p_poll_options jsonb default '[]'::jsonb)
returns uuid
language plpgsql security definer set search_path = ''
as $$
declare
    me uuid := public.ex_uid();
    found_phi text;
    new_id uuid;
    clean_case jsonb;
    opt jsonb;
begin
    perform public.ex_rate(me, 'post', 5, interval '1 hour');
    found_phi := public.ex_phi_check(concat_ws(' ', p_title, p_body, p_question, p_setting));
    if found_phi is not null then
        raise exception 'This looks like it contains %. Cases must be hypothetical: remove anything that could identify a real person.', found_phi;
    end if;
    -- keep only the case fields Akeso knows; nothing else rides along
    select coalesce(jsonb_object_agg(key, value), '{}'::jsonb) into clean_case
    from jsonb_each(coalesce(p_case, '{}'::jsonb))
    where key in ('symptoms', 'medicines', 'conditions', 'exposures', 'comorbidities',
                  'family_history', 'candidate', 'regimen');

    insert into public.exchange_posts (author_id, kind, title, body, question, is_anonymous,
        age_range, sex, setting, vitals, case_data, source, has_poll)
    values (me, p_kind, trim(p_title), coalesce(p_body, ''), coalesce(p_question, ''),
        coalesce(p_anonymous, false), p_age_range, p_sex, nullif(trim(coalesce(p_setting, '')), ''),
        p_vitals, clean_case, p_source,
        jsonb_typeof(p_poll_options) = 'array' and jsonb_array_length(p_poll_options) > 0)
    returning id into new_id;

    perform public.ex_set_tags(new_id, p_tags);

    if jsonb_typeof(p_poll_options) = 'array' then
        if jsonb_array_length(p_poll_options) > 8 then
            raise exception 'A poll can start with at most 8 choices.';
        end if;
        for opt in select * from jsonb_array_elements(p_poll_options) loop
            insert into public.exchange_poll_options (post_id, disease_id, label, suggested_by, by_author)
            values (new_id, nullif(opt ->> 'disease_id', ''), left(trim(opt ->> 'label'), 80), me, true)
            on conflict do nothing;
        end loop;
    end if;

    insert into public.exchange_follows (user_id, post_id) values (me, new_id)
    on conflict do nothing;
    return new_id;
end $$;

create or replace function public.ex_edit_post(p_id uuid, p_title text, p_body text,
                                               p_question text, p_tags jsonb)
returns void
language plpgsql security definer set search_path = ''
as $$
declare
    me uuid := public.ex_uid();
    p public.exchange_posts;
    found_phi text;
begin
    select * into p from public.exchange_posts where id = p_id;
    if not found or p.author_id <> me then raise exception 'Only the author can edit this post.'; end if;
    if p.status in ('locked', 'removed') then raise exception 'This post is locked.'; end if;
    found_phi := public.ex_phi_check(concat_ws(' ', p_title, p_body, p_question));
    if found_phi is not null then
        raise exception 'This looks like it contains %. Cases must be hypothetical: remove anything that could identify a real person.', found_phi;
    end if;
    update public.exchange_posts
    set title = trim(p_title), body = coalesce(p_body, ''), question = coalesce(p_question, ''),
        edited_at = now()
    where id = p_id;
    perform public.ex_set_tags(p_id, p_tags);
end $$;

create or replace function public.ex_delete_post(p_id uuid)
returns void
language plpgsql security definer set search_path = ''
as $$
declare me uuid := public.ex_uid();
begin
    delete from public.exchange_posts where id = p_id and author_id = me;
    if not found then raise exception 'Only the author can delete this post.'; end if;
end $$;

create or replace function public.ex_reply(p_post uuid, p_parent uuid, p_body text,
                                           p_anonymous boolean default false)
returns uuid
language plpgsql security definer set search_path = ''
as $$
declare
    me uuid := public.ex_uid();
    p public.exchange_posts;
    parent_post uuid;
    parent_parent uuid;
    found_phi text;
    new_id uuid;
    my_option uuid;
    who text;
    targets uuid[];
begin
    select * into p from public.exchange_posts where id = p_post;
    if not found or not public.ex_can_see(p.status, p.author_id, me) then
        raise exception 'This post is not available.';
    end if;
    if p.status <> 'open' then raise exception 'This post is locked; no new replies.'; end if;
    perform public.ex_rate(me, 'reply', 30, interval '1 hour');
    if p_parent is not null then
        select post_id, parent_id into parent_post, parent_parent
        from public.exchange_replies where id = p_parent;
        if parent_post is distinct from p_post then raise exception 'That reply is not on this post.'; end if;
        if parent_parent is not null then p_parent := parent_parent; end if;   -- one level only
    end if;
    found_phi := public.ex_phi_check(p_body);
    if found_phi is not null then
        raise exception 'This looks like it contains %. Cases must be hypothetical: remove anything that could identify a real person.', found_phi;
    end if;
    select option_id into my_option from public.exchange_poll_votes
    where post_id = p_post and user_id = me;

    insert into public.exchange_replies (post_id, parent_id, author_id, body, is_anonymous, poll_option_id)
    values (p_post, p_parent, me, trim(p_body), coalesce(p_anonymous, false), my_option)
    returning id into new_id;

    update public.exchange_posts
    set reply_count = reply_count + 1, last_activity_at = now() where id = p_post;
    insert into public.exchange_follows (user_id, post_id) values (me, p_post)
    on conflict do nothing;

    who := case when p_anonymous then 'An anonymous student'
                else coalesce((select nullif(display_name, '') from public.profiles where id = me),
                              'Someone') end;
    select array_agg(user_id) into targets from public.exchange_follows where post_id = p_post;
    if p_parent is not null then
        targets := targets || (select author_id from public.exchange_replies where id = p_parent);
    end if;
    perform public.ex_notify(targets, 'reply', p_post, new_id,
        who || ' replied to “' || public.ex_short(p.title) || '”', me);
    return new_id;
end $$;

create or replace function public.ex_edit_reply(p_id uuid, p_body text)
returns void
language plpgsql security definer set search_path = ''
as $$
declare
    me uuid := public.ex_uid();
    found_phi text;
begin
    found_phi := public.ex_phi_check(p_body);
    if found_phi is not null then
        raise exception 'This looks like it contains %. Cases must be hypothetical: remove anything that could identify a real person.', found_phi;
    end if;
    update public.exchange_replies set body = trim(p_body), edited_at = now()
    where id = p_id and author_id = me and status = 'open';
    if not found then raise exception 'Only the author can edit this reply.'; end if;
end $$;

-- A reply with answers under it keeps its place ("[deleted]"), so the
-- thread still reads; otherwise it is removed for good.
create or replace function public.ex_delete_reply(p_id uuid)
returns void
language plpgsql security definer set search_path = ''
as $$
declare
    me uuid := public.ex_uid();
    r public.exchange_replies;
begin
    select * into r from public.exchange_replies where id = p_id;
    if not found or r.author_id <> me then raise exception 'Only the author can delete this reply.'; end if;
    if exists (select 1 from public.exchange_replies where parent_id = p_id) then
        update public.exchange_replies set status = 'removed', body = '[deleted by the author]'
        where id = p_id;
    else
        delete from public.exchange_replies where id = p_id;
        update public.exchange_posts set reply_count = greatest(reply_count - 1, 0),
            best_reply_id = case when best_reply_id = p_id then null else best_reply_id end
        where id = r.post_id;
    end if;
end $$;

create or replace function public.ex_vote(p_kind text, p_id uuid, p_on boolean)
returns integer
language plpgsql security definer set search_path = ''
as $$
declare
    me uuid := public.ex_uid();
    author uuid;
    changed integer := 0;
    new_score integer;
begin
    if p_kind = 'post' then
        select author_id into author from public.exchange_posts where id = p_id and status in ('open', 'locked');
    elsif p_kind = 'reply' then
        select author_id into author from public.exchange_replies where id = p_id and status = 'open';
    end if;
    if author is null then raise exception 'This is not available.'; end if;
    if author = me then raise exception 'You can''t upvote your own post or reply.'; end if;
    if p_on then
        insert into public.exchange_votes (user_id, target_kind, target_id) values (me, p_kind, p_id)
        on conflict do nothing;
        get diagnostics changed = row_count;
    else
        delete from public.exchange_votes where user_id = me and target_kind = p_kind and target_id = p_id;
        get diagnostics changed = row_count;
        changed := -changed;
    end if;
    if p_kind = 'post' then
        update public.exchange_posts set score = score + changed where id = p_id returning score into new_score;
    else
        update public.exchange_replies set score = score + changed where id = p_id returning score into new_score;
    end if;
    return new_score;
end $$;

create or replace function public.ex_best_answer(p_post uuid, p_reply uuid)
returns void
language plpgsql security definer set search_path = ''
as $$
declare
    me uuid := public.ex_uid();
    p public.exchange_posts;
    reply_author uuid;
begin
    select * into p from public.exchange_posts where id = p_post;
    if not found or p.author_id <> me then raise exception 'Only the author can choose the best answer.'; end if;
    if p_reply is not null then
        select author_id into reply_author from public.exchange_replies
        where id = p_reply and post_id = p_post and status = 'open';
        if reply_author is null then raise exception 'That reply is not on this post.'; end if;
    end if;
    update public.exchange_posts set best_reply_id = p_reply where id = p_post;
    if p_reply is not null then
        perform public.ex_notify(array[reply_author], 'best_answer', p_post, p_reply,
            'Your reply was chosen as the best answer on “' || public.ex_short(p.title) || '”', me);
    end if;
end $$;

create or replace function public.ex_verify_reply(p_reply uuid, p_on boolean)
returns void
language plpgsql security definer set search_path = ''
as $$
declare
    me uuid := public.ex_uid();
    r public.exchange_replies;
    v_title text;
begin
    if not public.ex_is_mod(me) then raise exception 'Only educators and admins can verify answers.'; end if;
    select * into r from public.exchange_replies where id = p_reply and status = 'open';
    if not found then raise exception 'That reply is not available.'; end if;
    update public.exchange_replies
    set verified_by = case when p_on then me end, verified_at = case when p_on then now() end
    where id = p_reply;
    insert into public.exchange_mod_log (moderator_id, action, target_kind, target_id)
    values (me, case when p_on then 'verify' else 'unverify' end, 'reply', p_reply);
    if p_on then
        select p.title into v_title from public.exchange_posts p where p.id = r.post_id;
        perform public.ex_notify(array[r.author_id], 'verified', r.post_id, p_reply,
            'An educator verified your reply on “' || public.ex_short(v_title) || '”', me);
    end if;
end $$;


-- ---------------------------------------------------------------------
-- 5. The differential poll
-- ---------------------------------------------------------------------
-- Anyone may suggest a diagnosis (picked from the Disease Encyclopedia so
-- it links, or typed). One vote per student, changeable until the author
-- reveals the intended answer. The author can't vote on their own case.

create or replace function public.ex_poll_suggest(p_post uuid, p_disease_id text, p_label text)
returns uuid
language plpgsql security definer set search_path = ''
as $$
declare
    me uuid := public.ex_uid();
    p public.exchange_posts;
    v_label text := left(trim(coalesce(p_label, '')), 80);
    new_id uuid;
begin
    select * into p from public.exchange_posts where id = p_post;
    if not found or not public.ex_can_see(p.status, p.author_id, me) then
        raise exception 'This post is not available.';
    end if;
    if not p.has_poll then raise exception 'This post has no poll.'; end if;
    if p.status <> 'open' or p.revealed_option_id is not null then
        raise exception 'The poll is closed.';
    end if;
    if (select count(*) from public.exchange_poll_options where post_id = p_post) >= 12 then
        raise exception 'This poll already has 12 choices. Vote for one of them.';
    end if;
    perform public.ex_rate(me, 'suggest', 10, interval '1 hour');
    if nullif(p_disease_id, '') is not null then
        select coalesce(nullif(v_label, ''), d.name) into v_label from public.diseases d where d.id = p_disease_id;
        if v_label is null then raise exception 'That disease is not in the encyclopedia.'; end if;
    end if;
    if v_label = '' then raise exception 'Name the diagnosis you suggest.'; end if;
    if public.ex_phi_check(v_label) is not null then raise exception 'Use a diagnosis name only.'; end if;

    select o.id into new_id from public.exchange_poll_options o
    where o.post_id = p_post
      and coalesce(o.disease_id, lower(o.label)) = coalesce(nullif(p_disease_id, ''), lower(v_label));
    if new_id is null then
        insert into public.exchange_poll_options (post_id, disease_id, label, suggested_by, by_author)
        values (p_post, nullif(p_disease_id, ''), v_label, me, p.author_id = me)
        returning id into new_id;
    end if;
    return new_id;     -- an existing choice is returned rather than duplicated
end $$;

create or replace function public.ex_poll_vote(p_post uuid, p_option uuid)
returns void
language plpgsql security definer set search_path = ''
as $$
declare
    me uuid := public.ex_uid();
    p public.exchange_posts;
begin
    select * into p from public.exchange_posts where id = p_post;
    if not found or not public.ex_can_see(p.status, p.author_id, me) then
        raise exception 'This post is not available.';
    end if;
    if p.author_id = me then raise exception 'You wrote this case, so you can''t vote on it.'; end if;
    if p.status <> 'open' or p.revealed_option_id is not null then
        raise exception 'The poll is closed.';
    end if;
    if p_option is null then
        delete from public.exchange_poll_votes where post_id = p_post and user_id = me;
        return;
    end if;
    if not exists (select 1 from public.exchange_poll_options
                   where id = p_option and post_id = p_post and status = 'active') then
        raise exception 'That choice is not in this poll.';
    end if;
    insert into public.exchange_poll_votes (post_id, user_id, option_id) values (p_post, me, p_option)
    on conflict (post_id, user_id) do update set option_id = excluded.option_id, voted_at = now();
    update public.exchange_posts set last_activity_at = now() where id = p_post;
end $$;

create or replace function public.ex_poll_reveal(p_post uuid, p_option uuid, p_explanation text)
returns void
language plpgsql security definer set search_path = ''
as $$
declare
    me uuid := public.ex_uid();
    p public.exchange_posts;
    answer text;
    targets uuid[];
begin
    select * into p from public.exchange_posts where id = p_post;
    if not found or p.author_id <> me then raise exception 'Only the author can reveal the answer.'; end if;
    select label into answer from public.exchange_poll_options where id = p_option and post_id = p_post;
    if answer is null then raise exception 'Choose the intended answer from the poll.'; end if;
    if public.ex_phi_check(p_explanation) is not null then
        raise exception 'The explanation looks like it contains patient details. Keep it hypothetical.';
    end if;
    update public.exchange_posts
    set revealed_option_id = p_option, reveal_explanation = coalesce(p_explanation, ''),
        revealed_at = now(), last_activity_at = now()
    where id = p_post;
    select array_agg(distinct u) into targets from (
        select user_id as u from public.exchange_poll_votes where post_id = p_post
        union select user_id from public.exchange_follows where post_id = p_post) s;
    perform public.ex_notify(targets, 'reveal', p_post, null,
        'The answer to “' || public.ex_short(p.title) || '” is out: ' || answer, me);
end $$;


-- ---------------------------------------------------------------------
-- 6. Following, reports, moderation
-- ---------------------------------------------------------------------

create or replace function public.ex_follow(p_post uuid, p_on boolean)
returns void
language plpgsql security definer set search_path = ''
as $$
declare me uuid := public.ex_uid();
begin
    if p_on then
        insert into public.exchange_follows (user_id, post_id) values (me, p_post) on conflict do nothing;
    else
        delete from public.exchange_follows where user_id = me and post_id = p_post;
    end if;
end $$;

create or replace function public.ex_report(p_kind text, p_id uuid, p_reason text, p_note text)
returns void
language plpgsql security definer set search_path = ''
as $$
declare me uuid := public.ex_uid();
begin
    perform public.ex_rate(me, 'report', 10, interval '1 hour');
    if not exists (select 1 from public.exchange_posts where p_kind = 'post' and id = p_id)
       and not exists (select 1 from public.exchange_replies where p_kind = 'reply' and id = p_id) then
        raise exception 'That is not available.';
    end if;
    insert into public.exchange_reports (reporter_id, target_kind, target_id, reason, note)
    values (me, p_kind, p_id, p_reason, left(coalesce(p_note, ''), 500))
    on conflict (reporter_id, target_kind, target_id) do update
        set reason = excluded.reason, note = excluded.note, status = 'open', created_at = now();
end $$;

-- p_action: hide | unhide | lock | unlock | remove
create or replace function public.ex_moderate(p_kind text, p_id uuid, p_action text, p_reason text)
returns void
language plpgsql security definer set search_path = ''
as $$
declare
    me uuid := public.ex_uid();
    author uuid;
    post uuid;
    v_title text;
    new_status text;
begin
    if not public.ex_is_mod(me) then raise exception 'Only educators and admins can moderate.'; end if;
    new_status := case p_action when 'hide' then 'hidden' when 'unhide' then 'open'
                                when 'lock' then 'locked' when 'unlock' then 'open'
                                when 'remove' then 'removed' end;
    if new_status is null then raise exception 'Unknown action.'; end if;
    if p_kind = 'post' then
        update public.exchange_posts set status = new_status where id = p_id
        returning author_id, id, exchange_posts.title into author, post, v_title;
    elsif p_kind = 'reply' then
        if p_action in ('lock', 'unlock') then raise exception 'Replies can''t be locked.'; end if;
        update public.exchange_replies set status = new_status where id = p_id
        returning author_id, post_id into author, post;
        select p.title into v_title from public.exchange_posts p where p.id = post;
    end if;
    if author is null then raise exception 'That is not available.'; end if;

    insert into public.exchange_mod_log (moderator_id, action, target_kind, target_id, reason)
    values (me, p_action, p_kind, p_id, left(coalesce(p_reason, ''), 300));
    update public.exchange_reports set status = 'resolved', handled_by = me, handled_at = now()
    where target_kind = p_kind and target_id = p_id and status = 'open';
    if p_action in ('hide', 'lock', 'remove') then
        perform public.ex_notify(array[author], 'moderation', case when p_action = 'remove'
                and p_kind = 'post' then null else post end, null,
            'A moderator ' || case p_action when 'hide' then 'hid' when 'lock' then 'locked'
                else 'removed' end || ' your ' || p_kind || ' on “' || public.ex_short(v_title) || '”'
            || case when coalesce(p_reason, '') <> '' then ': ' || left(p_reason, 120) else '' end, me);
    end if;
end $$;

create or replace function public.ex_dismiss_reports(p_kind text, p_id uuid)
returns void
language plpgsql security definer set search_path = ''
as $$
declare me uuid := public.ex_uid();
begin
    if not public.ex_is_mod(me) then raise exception 'Only educators and admins can moderate.'; end if;
    update public.exchange_reports set status = 'dismissed', handled_by = me, handled_at = now()
    where target_kind = p_kind and target_id = p_id and status = 'open';
    insert into public.exchange_mod_log (moderator_id, action, target_kind, target_id)
    values (me, 'dismiss_reports', p_kind, p_id);
end $$;

-- Open reports, one row per reported post or reply, most reported first.
create or replace function public.ex_mod_queue()
returns setof jsonb
language plpgsql stable security definer set search_path = ''
as $$
declare me uuid := public.ex_uid();
begin
    if not public.ex_is_mod(me) then raise exception 'Only educators and admins can moderate.'; end if;
    return query
    select jsonb_build_object(
        'target_kind', r.target_kind, 'target_id', r.target_id,
        'reports', count(*), 'reasons', jsonb_agg(distinct r.reason),
        'notes', jsonb_agg(r.note) filter (where r.note <> ''),
        'first_reported', min(r.created_at),
        'post_id', coalesce(p.id, rp.post_id),
        'title', coalesce(p.title, pp.title),
        'excerpt', public.ex_short(coalesce(rp.body, p.body, ''), 200),
        'status', coalesce(rp.status, p.status),
        'author', public.ex_author(coalesce(p.author_id, rp.author_id),
                                   coalesce(p.is_anonymous, rp.is_anonymous), me))
    from public.exchange_reports r
    left join public.exchange_posts p on r.target_kind = 'post' and p.id = r.target_id
    left join public.exchange_replies rp on r.target_kind = 'reply' and rp.id = r.target_id
    left join public.exchange_posts pp on pp.id = rp.post_id
    where r.status = 'open' and (p.id is not null or rp.id is not null)
    group by r.target_kind, r.target_id, p.id, p.title, p.body, p.status, p.author_id,
             p.is_anonymous, rp.post_id, rp.body, rp.status, rp.author_id, rp.is_anonymous, pp.title
    order by count(*) desc, min(r.created_at);
end $$;

-- The card shown when you click a (non-anonymous) author's name.
create or replace function public.ex_profile_card(p_handle text)
returns jsonb
language plpgsql stable security definer set search_path = ''
as $$
declare
    me uuid := public.ex_uid();
    target uuid;
    card jsonb;
begin
    select id into target from public.profiles
    where lower(handle) = lower(p_handle) and is_public and deletion_scheduled_for is null;
    if target is null then raise exception 'This profile is private.'; end if;
    select to_jsonb(pp) into card from public.public_profile(p_handle) pp;
    return card || jsonb_build_object(
        'role', (select role::text from public.user_roles where user_id = target),
        'posts', (select count(*) from public.exchange_posts
                  where author_id = target and not is_anonymous and status in ('open', 'locked')),
        'replies', (select count(*) from public.exchange_replies
                    where author_id = target and not is_anonymous and status = 'open'),
        'best_answers', (select count(*) from public.exchange_posts p
                         join public.exchange_replies r on r.id = p.best_reply_id
                         where r.author_id = target and not r.is_anonymous),
        'verified_answers', (select count(*) from public.exchange_replies
                             where author_id = target and not is_anonymous and verified_at is not null),
        'member_since', (select created_at from public.profiles where id = target),
        'is_me', target = me);
end $$;


-- ---------------------------------------------------------------------
-- 7. Notifications
-- ---------------------------------------------------------------------
create or replace function public.notif_list(p_limit integer default 30, p_before bigint default null)
returns setof jsonb
language plpgsql stable security definer set search_path = ''
as $$
declare me uuid := public.ex_uid();
begin
    return query
    select jsonb_build_object('id', n.id, 'kind', n.kind, 'post_id', n.post_id,
                              'reply_id', n.reply_id, 'message', n.message,
                              'created_at', n.created_at, 'read', n.read_at is not null)
    from public.notifications n
    where n.user_id = me and (p_before is null or n.id < p_before)
    order by n.id desc
    limit least(greatest(p_limit, 1), 100);
end $$;

create or replace function public.notif_unread_count()
returns integer
language sql stable security definer set search_path = ''
as $$
    select count(*)::integer from public.notifications
    where user_id = auth.uid() and read_at is null and public.mfa_satisfied();
$$;

-- p_ids null = mark everything read
create or replace function public.notif_mark_read(p_ids bigint[] default null)
returns void
language plpgsql security definer set search_path = ''
as $$
declare me uuid := public.ex_uid();
begin
    update public.notifications set read_at = now()
    where user_id = me and read_at is null and (p_ids is null or id = any(p_ids));
end $$;

create or replace function public.notif_clear()
returns void
language plpgsql security definer set search_path = ''
as $$
declare me uuid := public.ex_uid();
begin
    delete from public.notifications where user_id = me and read_at is not null;
end $$;


-- ---------------------------------------------------------------------
-- 8. Who may call what
-- ---------------------------------------------------------------------
do $$
declare fn text;
begin
    -- internal helpers: nobody from outside
    foreach fn in array array[
        'public.ex_uid()', 'public.ex_is_mod(uuid)', 'public.ex_author(uuid, boolean, uuid)',
        'public.ex_rate(uuid, text, integer, interval)',
        'public.ex_notify(uuid[], text, uuid, uuid, text, uuid)',
        'public.ex_can_see(text, uuid, uuid)', 'public.ex_set_tags(uuid, jsonb)'] loop
        execute format('revoke execute on function %s from public, anon, authenticated', fn);
    end loop;
    -- the app's functions: signed-in users only
    foreach fn in array array[
        'public.ex_feed(text, text, text, text, text, text, integer, integer)',
        'public.ex_post(uuid)',
        'public.ex_create_post(text, text, text, text, boolean, text, text, text, jsonb, jsonb, text, jsonb, jsonb)',
        'public.ex_edit_post(uuid, text, text, text, jsonb)', 'public.ex_delete_post(uuid)',
        'public.ex_reply(uuid, uuid, text, boolean)', 'public.ex_edit_reply(uuid, text)',
        'public.ex_delete_reply(uuid)', 'public.ex_vote(text, uuid, boolean)',
        'public.ex_best_answer(uuid, uuid)', 'public.ex_verify_reply(uuid, boolean)',
        'public.ex_poll_suggest(uuid, text, text)', 'public.ex_poll_vote(uuid, uuid)',
        'public.ex_poll_reveal(uuid, uuid, text)', 'public.ex_follow(uuid, boolean)',
        'public.ex_report(text, uuid, text, text)', 'public.ex_moderate(text, uuid, text, text)',
        'public.ex_dismiss_reports(text, uuid)', 'public.ex_mod_queue()',
        'public.ex_profile_card(text)', 'public.ex_phi_check(text)',
        'public.notif_list(integer, bigint)', 'public.notif_unread_count()',
        'public.notif_mark_read(bigint[])', 'public.notif_clear()'] loop
        execute format('revoke execute on function %s from public, anon', fn);
        execute format('grant execute on function %s to authenticated', fn);
    end loop;
end $$;

commit;

-- =====================================================================
-- Checks:
--   select count(*) from public.exchange_posts;            -- 0 at first
--   select public.ex_phi_check('call me at 09171234567');   -- 'a phone number'
-- Moderators are educators and admins:
--   update public.user_roles set role = 'educator' where user_id = '<their id>';
-- =====================================================================
