-- =====================================================================
-- Akeso migration 002: Accounts (profiles, roles, security, privacy)
-- =====================================================================
-- Run once in the Supabase SQL editor (project akeso, branch main).
-- Safe to run again: every object is created "if not exists" or replaced.
--
-- What this creates
--
--   profiles              one row per account: name, photo, academic info,
--                         public handle, privacy switches, deletion date
--   user_roles            student / educator / admin (only admins change it)
--   user_devices          computers this account signed in from
--   security_events       the account activity log (append-only)
--   consents              which Terms / Privacy version was accepted, when
--   study_activity        per-day counters for the Overview summary
--   school_verifications  pending school-email codes (server only)
--   avatars               private storage bucket, one folder per account
--
-- Security model, in one paragraph
--
--   Every table has row-level security ON. People only ever see their own
--   rows. Anything that must not be forged (roles, the activity log, the
--   verified-student badge, the deletion date) cannot be written by the
--   app at all: it goes through SECURITY DEFINER functions below that
--   check the rules, or through triggers on Supabase's own auth tables.
--   If an account has two-factor turned on, a RESTRICTIVE policy hides
--   all of it until the session has passed the second factor (aal2).
--
-- Everything runs in one transaction: if any line fails, nothing is
-- created, so you can fix the problem and run the file again.
-- =====================================================================

begin;

-- ---------------------------------------------------------------------
-- 0. Types
-- ---------------------------------------------------------------------
do $$ begin
    create type public.app_role as enum ('student', 'educator', 'admin');
exception when duplicate_object then null; end $$;

do $$ begin
    create type public.security_event_kind as enum (
        'sign_in',                 -- a new session (trigger on auth.sessions)
        'sign_out',
        'sign_out_others',
        'password_changed',        -- trigger on auth.users
        'password_check_failed',   -- wrong current password in the app
        'email_change_requested',  -- trigger on auth.users
        'email_changed',           -- trigger on auth.users
        'mfa_enabled',
        'mfa_disabled',
        'mfa_challenge_failed',
        'device_forgotten',
        'profile_updated',
        'data_exported',
        'deletion_requested',
        'deletion_cancelled',
        'school_email_verified',
        'role_changed',
        'consent_accepted'
    );
exception when duplicate_object then null; end $$;


-- ---------------------------------------------------------------------
-- 1. Profiles
-- ---------------------------------------------------------------------
-- id is the auth user's id, so deleting the auth user deletes this row
-- (and, through the other foreign keys, everything else in this file).
create table if not exists public.profiles (
    id                      uuid primary key references auth.users (id) on delete cascade,
    display_name            text        not null default ''
                            check (char_length(display_name) <= 60),
    handle                  text
                            check (handle ~ '^[a-z0-9_]{3,20}$'),
    bio                     text        not null default ''
                            check (char_length(bio) <= 280),
    avatar_path             text,
    program                 text
                            check (program in ('medicine', 'nursing', 'pharmacy',
                                               'medical_technology', 'physical_therapy',
                                               'midwifery', 'dentistry', 'public_health',
                                               'radiologic_technology', 'nutrition', 'other')),
    school                  text        check (char_length(school) <= 120),
    year_level              smallint    check (year_level between 1 and 8),
    interests               text[]      not null default '{}'
                            check (cardinality(interests) <= 10),
    -- what other people may see once Clinical Exchange shows profiles
    is_public               boolean     not null default false,
    show_school             boolean     not null default true,
    show_program            boolean     not null default true,
    -- privacy switches (Privacy & data tab)
    track_study_activity    boolean     not null default true,
    -- set by the school-email Edge Function only (domain, never the address)
    school_email_domain     text,
    school_email_verified_at timestamptz,
    -- set by request_account_deletion() only
    deletion_requested_at   timestamptz,
    deletion_scheduled_for  timestamptz,
    created_at              timestamptz not null default now(),
    updated_at              timestamptz not null default now()
);

-- Handles are unique regardless of case ("Eijkim" and "eijkim" clash).
create unique index if not exists profiles_handle_key
    on public.profiles (lower(handle)) where handle is not null;
create index if not exists profiles_deletion_idx
    on public.profiles (deletion_scheduled_for) where deletion_scheduled_for is not null;


-- ---------------------------------------------------------------------
-- 2. Roles
-- ---------------------------------------------------------------------
-- Kept out of profiles on purpose: a user can edit their own profile row,
-- and a role column there would be one bad policy away from "make me admin".
create table if not exists public.user_roles (
    user_id     uuid primary key references auth.users (id) on delete cascade,
    role        public.app_role not null default 'student',
    granted_by  uuid references auth.users (id) on delete set null,
    granted_at  timestamptz not null default now()
);


-- ---------------------------------------------------------------------
-- 3. Devices
-- ---------------------------------------------------------------------
-- auth.sessions is not reachable through the API, so the app reports the
-- computer it runs on at every sign-in (touch_device below). device_key is
-- a random id the app keeps in a local file; it identifies an install,
-- not a person.
create table if not exists public.user_devices (
    id          uuid primary key default gen_random_uuid(),
    user_id     uuid not null references auth.users (id) on delete cascade,
    device_key  text not null check (char_length(device_key) between 16 and 64),
    device_name text not null default '' check (char_length(device_name) <= 80),
    platform    text not null default '' check (char_length(platform) <= 80),
    app_version text not null default '' check (char_length(app_version) <= 20),
    session_id  uuid,
    first_seen  timestamptz not null default now(),
    last_seen   timestamptz not null default now(),
    unique (user_id, device_key)
);


-- ---------------------------------------------------------------------
-- 4. Security activity log
-- ---------------------------------------------------------------------
-- Append-only. There is no INSERT, UPDATE or DELETE policy, so nothing
-- the app sends can add, change or remove a line; rows arrive only from
-- log_security_event() (which checks what it is told) and from triggers.
create table if not exists public.security_events (
    id          bigint generated always as identity primary key,
    user_id     uuid not null references auth.users (id) on delete cascade,
    kind        public.security_event_kind not null,
    device_name text not null default '',
    detail      jsonb not null default '{}'::jsonb,
    created_at  timestamptz not null default now()
);
create index if not exists security_events_user_idx
    on public.security_events (user_id, created_at desc);


-- ---------------------------------------------------------------------
-- 5. Consents
-- ---------------------------------------------------------------------
-- History, not a switch: accepting a new version adds a row; nothing is
-- ever overwritten, so "what had they agreed to on date X" stays answerable.
create table if not exists public.consents (
    id          bigint generated always as identity primary key,
    user_id     uuid not null default auth.uid() references auth.users (id) on delete cascade,
    document    text not null check (document in ('terms', 'privacy')),
    version     text not null check (char_length(version) between 1 and 20),
    accepted_at timestamptz not null default now(),
    unique (user_id, document, version)
);


-- ---------------------------------------------------------------------
-- 6. Study activity (private counters for the Overview tab)
-- ---------------------------------------------------------------------
create table if not exists public.study_activity (
    user_id             uuid not null references auth.users (id) on delete cascade,
    day                 date not null,
    diseases_viewed     integer not null default 0 check (diseases_viewed >= 0),
    symptoms_viewed     integer not null default 0 check (symptoms_viewed >= 0),
    medicines_viewed    integer not null default 0 check (medicines_viewed >= 0),
    notebook_edits      integer not null default 0 check (notebook_edits >= 0),
    checker_runs        integer not null default 0 check (checker_runs >= 0),
    interaction_checks  integer not null default 0 check (interaction_checks >= 0),
    primary key (user_id, day)
);


-- ---------------------------------------------------------------------
-- 7. School e-mail codes (read and written by the Edge Function only)
-- ---------------------------------------------------------------------
create table if not exists public.school_verifications (
    user_id      uuid primary key references auth.users (id) on delete cascade,
    email_domain text not null,
    code_hash    text not null,          -- sha-256 of the code, never the code
    expires_at   timestamptz not null,
    attempts     smallint not null default 0,
    sent_count   smallint not null default 1,
    last_sent_at timestamptz not null default now()
);


-- ---------------------------------------------------------------------
-- 8. Helper functions
-- ---------------------------------------------------------------------
-- search_path = '' on every SECURITY DEFINER function: names are written
-- in full (public.x, auth.y) so nobody can slip in a look-alike object.

-- Has this session passed two-factor, if the account uses it?
create or replace function public.mfa_satisfied()
returns boolean
language sql stable security definer set search_path = ''
as $$
    select coalesce(auth.jwt() ->> 'aal', 'aal1') = 'aal2'
        or not exists (
            select 1 from auth.mfa_factors f
            where f.user_id = auth.uid() and f.status = 'verified');
$$;

create or replace function public.is_admin()
returns boolean
language sql stable security definer set search_path = ''
as $$
    select exists (select 1 from public.user_roles r
                   where r.user_id = auth.uid() and r.role = 'admin');
$$;

-- Internal: add one line to the activity log. Not callable from the app.
create or replace function public._log_event(
    p_user uuid, p_kind public.security_event_kind,
    p_device text default '', p_detail jsonb default '{}'::jsonb)
returns void
language sql security definer set search_path = ''
as $$
    insert into public.security_events (user_id, kind, device_name, detail)
    values (p_user, p_kind, left(coalesce(p_device, ''), 80), coalesce(p_detail, '{}'::jsonb));
$$;

create or replace function public.touch_updated_at()
returns trigger
language plpgsql set search_path = ''
as $$
begin
    new.updated_at := now();
    return new;
end $$;

drop trigger if exists profiles_touch on public.profiles;
create trigger profiles_touch before update on public.profiles
    for each row execute function public.touch_updated_at();


-- ---------------------------------------------------------------------
-- 9. New accounts get a profile and the student role
-- ---------------------------------------------------------------------
create or replace function public.handle_new_user()
returns trigger
language plpgsql security definer set search_path = ''
as $$
begin
    insert into public.profiles (id, display_name)
    values (new.id, left(coalesce(new.raw_user_meta_data ->> 'display_name',
                                  new.raw_user_meta_data ->> 'full_name',
                                  new.raw_user_meta_data ->> 'name',
                                  split_part(new.email, '@', 1), ''), 60))
    on conflict (id) do nothing;
    insert into public.user_roles (user_id) values (new.id)
    on conflict (user_id) do nothing;
    return new;
end $$;

drop trigger if exists akeso_on_auth_user_created on auth.users;
create trigger akeso_on_auth_user_created after insert on auth.users
    for each row execute function public.handle_new_user();

-- Accounts that existed before this migration.
insert into public.profiles (id, display_name)
select u.id, left(coalesce(u.raw_user_meta_data ->> 'display_name',
                           u.raw_user_meta_data ->> 'full_name',
                           u.raw_user_meta_data ->> 'name',
                           split_part(u.email, '@', 1), ''), 60)
from auth.users u
on conflict (id) do nothing;
insert into public.user_roles (user_id) select id from auth.users
on conflict (user_id) do nothing;


-- ---------------------------------------------------------------------
-- 10. Server-side activity log triggers on Supabase's auth tables
-- ---------------------------------------------------------------------
-- These must never break sign-in or account updates, so any error inside
-- them is swallowed: a missed log line is better than a locked-out user.

create or replace function public.log_auth_user_changes()
returns trigger
language plpgsql security definer set search_path = ''
as $$
begin
    begin
        if new.encrypted_password is distinct from old.encrypted_password then
            perform public._log_event(new.id, 'password_changed');
        end if;
        if new.email is distinct from old.email then
            perform public._log_event(new.id, 'email_changed', '',
                jsonb_build_object('from_domain', split_part(old.email, '@', 2),
                                   'to_domain', split_part(new.email, '@', 2)));
        elsif coalesce(new.email_change, '') <> ''
              and new.email_change is distinct from old.email_change then
            perform public._log_event(new.id, 'email_change_requested', '',
                jsonb_build_object('to_domain', split_part(new.email_change, '@', 2)));
        end if;
    exception when others then
        null;
    end;
    return new;
end $$;

drop trigger if exists akeso_on_auth_user_changed on auth.users;
create trigger akeso_on_auth_user_changed after update on auth.users
    for each row execute function public.log_auth_user_changes();

-- Every new session is a sign-in. to_jsonb() reads optional columns
-- (user_agent, ip) without failing on Supabase versions that lack them.
create or replace function public.log_new_session()
returns trigger
language plpgsql security definer set search_path = ''
as $$
declare
    raw jsonb := to_jsonb(new);
begin
    begin
        perform public._log_event(new.user_id, 'sign_in', '',
            jsonb_strip_nulls(jsonb_build_object(
                'session_id', new.id,
                'user_agent', left(raw ->> 'user_agent', 120))));
    exception when others then
        null;
    end;
    return new;
end $$;

drop trigger if exists akeso_on_auth_session_created on auth.sessions;
create trigger akeso_on_auth_session_created after insert on auth.sessions
    for each row execute function public.log_new_session();


-- ---------------------------------------------------------------------
-- 11. Guards
-- ---------------------------------------------------------------------
-- Role changes are logged, and the last admin cannot be removed (or the
-- Admin Control Panel would lock everyone out).
create or replace function public.guard_user_roles()
returns trigger
language plpgsql security definer set search_path = ''
as $$
begin
    if tg_op in ('UPDATE', 'DELETE') and old.role = 'admin'
       and (tg_op = 'DELETE' or new.role <> 'admin')
       and (select count(*) from public.user_roles where role = 'admin') <= 1 then
        raise exception 'Akeso needs at least one admin.';
    end if;
    if tg_op = 'UPDATE' and new.role is distinct from old.role then
        new.granted_by := auth.uid();
        new.granted_at := now();
        perform public._log_event(new.user_id, 'role_changed', '',
            jsonb_build_object('from', old.role, 'to', new.role));
    end if;
    return case when tg_op = 'DELETE' then old else new end;
end $$;

drop trigger if exists user_roles_guard on public.user_roles;
create trigger user_roles_guard before update or delete on public.user_roles
    for each row execute function public.guard_user_roles();


-- ---------------------------------------------------------------------
-- 12. Row-level security
-- ---------------------------------------------------------------------
alter table public.profiles             enable row level security;
alter table public.user_roles           enable row level security;
alter table public.user_devices         enable row level security;
alter table public.security_events      enable row level security;
alter table public.consents             enable row level security;
alter table public.study_activity       enable row level security;
alter table public.school_verifications enable row level security;  -- no policies: server only

-- Supabase grants every table to anon and authenticated by default. Start
-- from nothing and hand back only what each table needs.
revoke all on public.profiles, public.user_roles, public.user_devices,
              public.security_events, public.consents, public.study_activity,
              public.school_verifications
    from anon, authenticated;

-- profiles: see and edit your own row
drop policy if exists "own profile: read" on public.profiles;
create policy "own profile: read" on public.profiles
    for select to authenticated using (id = (select auth.uid()));
drop policy if exists "own profile: update" on public.profiles;
create policy "own profile: update" on public.profiles
    for update to authenticated
    using (id = (select auth.uid())) with check (id = (select auth.uid()));

-- ...and only these columns. The badge, deletion dates and timestamps are
-- not in the list, so an UPDATE that touches them is refused outright.
grant select on public.profiles to authenticated;
grant update (display_name, handle, bio, avatar_path, program, school, year_level,
              interests, is_public, show_school, show_program,
              track_study_activity)
    on public.profiles to authenticated;

-- user_roles: read your own; admins read and change everyone's
drop policy if exists "roles: read own or admin" on public.user_roles;
create policy "roles: read own or admin" on public.user_roles
    for select to authenticated
    using (user_id = (select auth.uid()) or (select public.is_admin()));
drop policy if exists "roles: admin changes" on public.user_roles;
create policy "roles: admin changes" on public.user_roles
    for update to authenticated
    using ((select public.is_admin())) with check ((select public.is_admin()));
grant select on public.user_roles to authenticated;
grant update (role) on public.user_roles to authenticated;

-- user_devices: read and forget your own (adding goes through touch_device)
drop policy if exists "devices: read own" on public.user_devices;
create policy "devices: read own" on public.user_devices
    for select to authenticated using (user_id = (select auth.uid()));
drop policy if exists "devices: forget own" on public.user_devices;
create policy "devices: forget own" on public.user_devices
    for delete to authenticated using (user_id = (select auth.uid()));
grant select, delete on public.user_devices to authenticated;

-- security_events: read your own, nothing else
drop policy if exists "events: read own" on public.security_events;
create policy "events: read own" on public.security_events
    for select to authenticated using (user_id = (select auth.uid()));
grant select on public.security_events to authenticated;

-- consents: read and add your own; never change or remove
drop policy if exists "consents: read own" on public.consents;
create policy "consents: read own" on public.consents
    for select to authenticated using (user_id = (select auth.uid()));
drop policy if exists "consents: add own" on public.consents;
create policy "consents: add own" on public.consents
    for insert to authenticated with check (user_id = (select auth.uid()));
grant select, insert on public.consents to authenticated;

-- study_activity: read your own (counting goes through record_activity)
drop policy if exists "activity: read own" on public.study_activity;
create policy "activity: read own" on public.study_activity
    for select to authenticated using (user_id = (select auth.uid()));
grant select on public.study_activity to authenticated;

-- Two-factor gate: RESTRICTIVE policies are ANDed with the ones above, so
-- with 2FA on, none of this is visible or writable from a session that
-- has only passed the password.
do $$
declare t text;
begin
    foreach t in array array['profiles', 'user_roles', 'user_devices',
                             'security_events', 'consents', 'study_activity'] loop
        execute format('drop policy if exists "require 2FA when enabled" on public.%I', t);
        execute format('create policy "require 2FA when enabled" on public.%I '
                       'as restrictive for all to authenticated '
                       'using ((select public.mfa_satisfied())) '
                       'with check ((select public.mfa_satisfied()))', t);
    end loop;
end $$;


-- ---------------------------------------------------------------------
-- 13. Functions the app calls (supabase .rpc())
-- ---------------------------------------------------------------------

-- Record (or refresh) this computer for the signed-in account.
create or replace function public.touch_device(
    p_device_key text, p_device_name text, p_platform text, p_app_version text)
returns void
language plpgsql security definer set search_path = ''
as $$
declare
    uid uuid := auth.uid();
    sid uuid := nullif(auth.jwt() ->> 'session_id', '')::uuid;
begin
    if uid is null then raise exception 'Not signed in.'; end if;
    if not public.mfa_satisfied() then raise exception 'Two-factor check required.'; end if;
    if p_device_key is null or char_length(p_device_key) not between 16 and 64 then
        raise exception 'Invalid device key.';
    end if;

    insert into public.user_devices (user_id, device_key, device_name, platform,
                                     app_version, session_id)
    values (uid, p_device_key, left(coalesce(p_device_name, ''), 80),
            left(coalesce(p_platform, ''), 80), left(coalesce(p_app_version, ''), 20), sid)
    on conflict (user_id, device_key) do update
        set device_name = excluded.device_name, platform = excluded.platform,
            app_version = excluded.app_version, session_id = excluded.session_id,
            last_seen = now();

    -- Put the computer's name on this session's sign-in line.
    if sid is not null then
        update public.security_events
        set device_name = left(coalesce(p_device_name, ''), 80)
        where user_id = uid and kind = 'sign_in'
          and detail ->> 'session_id' = sid::text and device_name = '';
    end if;
end $$;

-- Devices, with "this computer" and "still signed in" worked out here.
create or replace function public.my_devices()
returns table (id uuid, device_name text, platform text, app_version text,
               first_seen timestamptz, last_seen timestamptz,
               is_current boolean, is_active boolean)
language plpgsql stable security definer set search_path = ''
as $$
declare
    uid uuid := auth.uid();
    sid uuid := nullif(auth.jwt() ->> 'session_id', '')::uuid;
    live uuid[] := '{}';
begin
    if uid is null or not public.mfa_satisfied() then return; end if;
    begin
        select coalesce(array_agg(s.id), '{}') into live
        from auth.sessions s where s.user_id = uid;
    exception when others then
        live := null;   -- auth.sessions unreadable: "unknown", not "signed out"
    end;
    return query
        select d.id, d.device_name, d.platform, d.app_version, d.first_seen, d.last_seen,
               d.session_id is not distinct from sid and sid is not null,
               case when live is null then null else d.session_id = any(live) end
        from public.user_devices d
        where d.user_id = uid
        order by d.last_seen desc;
end $$;

-- Events the app may report. Everything else comes from triggers or from
-- the functions below; the claims that can be checked are checked.
create or replace function public.log_security_event(
    p_kind text, p_device_name text default '', p_detail jsonb default '{}'::jsonb)
returns void
language plpgsql security definer set search_path = ''
as $$
declare
    uid uuid := auth.uid();
    kind public.security_event_kind;
    has_factor boolean;
begin
    if uid is null then raise exception 'Not signed in.'; end if;
    if p_kind not in ('sign_out', 'sign_out_others', 'mfa_enabled', 'mfa_disabled',
                      'mfa_challenge_failed', 'device_forgotten', 'profile_updated',
                      'data_exported') then
        raise exception 'This event cannot be reported by the app.';
    end if;
    -- A flood of fake lines would bury the real ones.
    if (select count(*) from public.security_events
        where user_id = uid and created_at > now() - interval '1 hour') >= 120 then
        return;
    end if;

    kind := p_kind::public.security_event_kind;
    if kind in ('mfa_enabled', 'mfa_disabled') then
        select exists (select 1 from auth.mfa_factors f
                       where f.user_id = uid and f.status = 'verified') into has_factor;
        if (kind = 'mfa_enabled') <> has_factor then
            raise exception 'Two-factor status does not match.';
        end if;
    end if;
    if kind <> 'mfa_challenge_failed' and not public.mfa_satisfied() then
        raise exception 'Two-factor check required.';
    end if;
    if pg_column_size(p_detail) > 2000 then
        p_detail := '{}'::jsonb;
    end if;

    perform public._log_event(uid, kind, p_device_name, coalesce(p_detail, '{}'::jsonb));
end $$;

-- "Enter your current password" before changing it. Checked here against
-- the bcrypt hash, so it does not create a new session (which would also
-- drop a 2FA-verified session back to aal1). 5 wrong tries per 15 minutes.
create or replace function public.verify_current_password(p_password text)
returns boolean
language plpgsql security definer set search_path = ''
as $$
declare
    uid uuid := auth.uid();
    stored text;
    ok boolean;
begin
    if uid is null then raise exception 'Not signed in.'; end if;
    if not public.mfa_satisfied() then raise exception 'Two-factor check required.'; end if;
    if (select count(*) from public.security_events
        where user_id = uid and kind = 'password_check_failed'
          and created_at > now() - interval '15 minutes') >= 5 then
        raise exception 'Too many wrong attempts. Try again in 15 minutes.';
    end if;

    select u.encrypted_password into stored from auth.users u where u.id = uid;
    if coalesce(stored, '') = '' then
        return true;   -- Google-only account: there is no password yet
    end if;
    ok := stored = extensions.crypt(coalesce(p_password, ''), stored);
    if not ok then
        perform public._log_event(uid, 'password_check_failed');
    end if;
    return ok;
end $$;

-- Does this account have a password at all (Google sign-in only)?
create or replace function public.has_password()
returns boolean
language sql stable security definer set search_path = ''
as $$
    select coalesce((select u.encrypted_password from auth.users u
                     where u.id = auth.uid()), '') <> '';
$$;

create or replace function public.handle_available(p_handle text)
returns boolean
language sql stable security definer set search_path = ''
as $$
    select p_handle ~ '^[a-z0-9_]{3,20}$'
       and not exists (select 1 from public.profiles p
                       where lower(p.handle) = lower(p_handle)
                         and p.id <> coalesce(auth.uid(), '00000000-0000-0000-0000-000000000000'));
$$;

-- What another student may see (for Clinical Exchange later). Only public
-- profiles, only the columns their switches allow.
create or replace function public.public_profile(p_handle text)
returns table (handle text, display_name text, bio text, avatar_path text,
               program text, school text, verified_school_domain text, year_level smallint)
language sql stable security definer set search_path = ''
as $$
    select p.handle, p.display_name, p.bio, p.avatar_path,
           case when p.show_program then p.program end,
           case when p.show_school then p.school end,
           case when p.school_email_verified_at is not null then p.school_email_domain end,
           case when p.show_program then p.year_level end
    from public.profiles p
    where lower(p.handle) = lower(p_handle) and p.is_public
      and p.deletion_scheduled_for is null
      and auth.uid() is not null;
$$;

-- Study counters, sent in batches by the app (one call a minute at most).
create or replace function public.record_activity(p_counts jsonb)
returns void
language plpgsql security definer set search_path = ''
as $$
declare
    uid uuid := auth.uid();
    today date := (now() at time zone 'Asia/Manila')::date;
    f text;
    n integer;
    vals integer[] := array[0, 0, 0, 0, 0, 0];
    fields text[] := array['diseases_viewed', 'symptoms_viewed', 'medicines_viewed',
                           'notebook_edits', 'checker_runs', 'interaction_checks'];
begin
    if uid is null or not public.mfa_satisfied() then return; end if;
    if not coalesce((select p.track_study_activity from public.profiles p where p.id = uid), false) then
        return;   -- switched off in Privacy & data
    end if;
    for i in 1 .. array_length(fields, 1) loop
        f := fields[i];
        n := coalesce((p_counts ->> f)::integer, 0);
        vals[i] := greatest(0, least(n, 500));   -- ignore nonsense values
    end loop;
    if (select sum(v) from unnest(vals) v) = 0 then return; end if;

    insert into public.study_activity as a (user_id, day, diseases_viewed, symptoms_viewed,
        medicines_viewed, notebook_edits, checker_runs, interaction_checks)
    values (uid, today, vals[1], vals[2], vals[3], vals[4], vals[5], vals[6])
    on conflict (user_id, day) do update set
        diseases_viewed    = a.diseases_viewed    + excluded.diseases_viewed,
        symptoms_viewed    = a.symptoms_viewed    + excluded.symptoms_viewed,
        medicines_viewed   = a.medicines_viewed   + excluded.medicines_viewed,
        notebook_edits     = a.notebook_edits     + excluded.notebook_edits,
        checker_runs       = a.checker_runs       + excluded.checker_runs,
        interaction_checks = a.interaction_checks + excluded.interaction_checks;
end $$;

-- Totals for the Overview: last 7 days, last 30 days, all time, and the
-- current streak (consecutive days with any activity, ending today or
-- yesterday so an unfinished today does not break it).
create or replace function public.activity_summary()
returns jsonb
language plpgsql stable security definer set search_path = ''
as $$
declare
    uid uuid := auth.uid();
    today date := (now() at time zone 'Asia/Manila')::date;
    streak integer := 0;
    d date;
    result jsonb;
begin
    if uid is null or not public.mfa_satisfied() then return '{}'::jsonb; end if;

    d := case when exists (select 1 from public.study_activity
                           where user_id = uid and day = today) then today else today - 1 end;
    while exists (select 1 from public.study_activity where user_id = uid and day = d) loop
        streak := streak + 1;
        d := d - 1;
    end loop;

    select jsonb_build_object(
        'streak', streak,
        'active_days_30', count(*) filter (where day > today - 30),
        'week', jsonb_build_object(
            'diseases_viewed',    coalesce(sum(diseases_viewed)    filter (where day > today - 7), 0),
            'symptoms_viewed',    coalesce(sum(symptoms_viewed)    filter (where day > today - 7), 0),
            'medicines_viewed',   coalesce(sum(medicines_viewed)   filter (where day > today - 7), 0),
            'notebook_edits',     coalesce(sum(notebook_edits)     filter (where day > today - 7), 0),
            'checker_runs',       coalesce(sum(checker_runs)       filter (where day > today - 7), 0),
            'interaction_checks', coalesce(sum(interaction_checks) filter (where day > today - 7), 0)),
        'all_time', jsonb_build_object(
            'diseases_viewed',    coalesce(sum(diseases_viewed), 0),
            'symptoms_viewed',    coalesce(sum(symptoms_viewed), 0),
            'medicines_viewed',   coalesce(sum(medicines_viewed), 0),
            'notebook_edits',     coalesce(sum(notebook_edits), 0),
            'checker_runs',       coalesce(sum(checker_runs), 0),
            'interaction_checks', coalesce(sum(interaction_checks), 0)),
        'last_14_days', coalesce((
            select jsonb_agg(jsonb_build_object('day', g.day::date,
                       'total', coalesce(a.diseases_viewed + a.symptoms_viewed + a.medicines_viewed
                                         + a.notebook_edits + a.checker_runs
                                         + a.interaction_checks, 0)) order by g.day)
            from generate_series(today - 13, today, interval '1 day') as g(day)
            left join public.study_activity a on a.user_id = uid and a.day = g.day::date), '[]'))
    into result
    from public.study_activity
    where user_id = uid;
    return result;
end $$;

-- Delete my account: 30 days to change your mind.
create or replace function public.request_account_deletion(p_confirm text)
returns timestamptz
language plpgsql security definer set search_path = ''
as $$
declare
    uid uuid := auth.uid();
    due timestamptz := now() + interval '30 days';
begin
    if uid is null then raise exception 'Not signed in.'; end if;
    if not public.mfa_satisfied() then raise exception 'Two-factor check required.'; end if;
    if p_confirm is distinct from 'DELETE' then
        raise exception 'Type DELETE to confirm.';
    end if;
    if exists (select 1 from public.user_roles where user_id = uid and role = 'admin')
       and (select count(*) from public.user_roles where role = 'admin') <= 1 then
        raise exception 'You are the only admin. Make someone else an admin first.';
    end if;
    update public.profiles
    set deletion_requested_at = now(), deletion_scheduled_for = due
    where id = uid;
    perform public._log_event(uid, 'deletion_requested', '',
        jsonb_build_object('scheduled_for', due));
    return due;
end $$;

create or replace function public.cancel_account_deletion()
returns void
language plpgsql security definer set search_path = ''
as $$
declare uid uuid := auth.uid();
begin
    if uid is null then raise exception 'Not signed in.'; end if;
    if not public.mfa_satisfied() then raise exception 'Two-factor check required.'; end if;
    update public.profiles
    set deletion_requested_at = null, deletion_scheduled_for = null
    where id = uid and deletion_scheduled_for is not null;
    if found then
        perform public._log_event(uid, 'deletion_cancelled');
    end if;
end $$;

-- Record acceptance of the current Terms and Privacy Notice.
create or replace function public.accept_documents(p_terms_version text, p_privacy_version text)
returns void
language plpgsql security definer set search_path = ''
as $$
declare uid uuid := auth.uid();
begin
    if uid is null then raise exception 'Not signed in.'; end if;
    if not public.mfa_satisfied() then raise exception 'Two-factor check required.'; end if;
    insert into public.consents (user_id, document, version)
    values (uid, 'terms', left(p_terms_version, 20)), (uid, 'privacy', left(p_privacy_version, 20))
    on conflict (user_id, document, version) do nothing;
    if found then
        perform public._log_event(uid, 'consent_accepted', '',
            jsonb_build_object('terms', p_terms_version, 'privacy', p_privacy_version));
    end if;
end $$;

-- Who may call what. Nothing here is for signed-out visitors.
revoke execute on function public._log_event(uuid, public.security_event_kind, text, jsonb)
    from public, anon, authenticated;
revoke execute on function public.handle_new_user() from public, anon, authenticated;
revoke execute on function public.log_auth_user_changes() from public, anon, authenticated;
revoke execute on function public.log_new_session() from public, anon, authenticated;
revoke execute on function public.guard_user_roles() from public, anon, authenticated;

do $$
declare fn text;
begin
    foreach fn in array array[
        'public.mfa_satisfied()', 'public.is_admin()',
        'public.touch_device(text, text, text, text)', 'public.my_devices()',
        'public.log_security_event(text, text, jsonb)',
        'public.verify_current_password(text)', 'public.has_password()',
        'public.handle_available(text)', 'public.public_profile(text)',
        'public.record_activity(jsonb)', 'public.activity_summary()',
        'public.request_account_deletion(text)', 'public.cancel_account_deletion()',
        'public.accept_documents(text, text)'] loop
        execute format('revoke execute on function %s from public, anon', fn);
        execute format('grant execute on function %s to authenticated', fn);
    end loop;
end $$;


-- ---------------------------------------------------------------------
-- 14. Profile photos: private bucket, one folder per account
-- ---------------------------------------------------------------------
-- Path inside the bucket: <user id>/avatar.png. The policies compare the
-- first folder with the signed-in user's id, so nobody can read or
-- overwrite someone else's photo. 1 MB limit, images only.
insert into storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
values ('avatars', 'avatars', false, 1048576, array['image/png', 'image/jpeg'])
on conflict (id) do update
    set public = false, file_size_limit = 1048576,
        allowed_mime_types = array['image/png', 'image/jpeg'];

drop policy if exists "avatars: read own" on storage.objects;
create policy "avatars: read own" on storage.objects
    for select to authenticated
    using (bucket_id = 'avatars' and (storage.foldername(name))[1] = (select auth.uid())::text);
drop policy if exists "avatars: upload own" on storage.objects;
create policy "avatars: upload own" on storage.objects
    for insert to authenticated
    with check (bucket_id = 'avatars' and (storage.foldername(name))[1] = (select auth.uid())::text);
drop policy if exists "avatars: replace own" on storage.objects;
create policy "avatars: replace own" on storage.objects
    for update to authenticated
    using (bucket_id = 'avatars' and (storage.foldername(name))[1] = (select auth.uid())::text)
    with check (bucket_id = 'avatars' and (storage.foldername(name))[1] = (select auth.uid())::text);
drop policy if exists "avatars: remove own" on storage.objects;
create policy "avatars: remove own" on storage.objects
    for delete to authenticated
    using (bucket_id = 'avatars' and (storage.foldername(name))[1] = (select auth.uid())::text);

commit;

-- =====================================================================
-- After running: make yourself the first admin (run separately, with
-- your own sign-in email):
--
--   update public.user_roles set role = 'admin'
--   where user_id = (select id from auth.users where email = 'you@example.com');
--
-- Checks:
--   select count(*) from public.profiles;        -- = number of accounts
--   select role, count(*) from public.user_roles group by role;
-- =====================================================================
