-- =====================================================================
-- Akeso migration 043: change your @handle
-- =====================================================================
-- Run AFTER 009_auto_handles.sql (and after 040-042 if you run those).
-- Safe to run again.
--
-- 009 gave everyone a handle and locked it ("users can no longer change
-- it, so links to a profile never break"). That lock stays: the app still
-- can't write profiles.handle. This adds ONE controlled way to change it,
-- through change_handle(), with rules a modified app can't skip:
--
--   * 3-20 lowercase letters, numbers or underscores (as before);
--   * not taken (any capitalisation), not a reserved word (admin, akeso,
--     support, moderator...);
--   * at most once every 30 days;
--   * a handle someone gave up stays reserved for 30 days, so nobody can
--     take it straight away and pretend to be them.
--
-- Old links and mentions of the old @handle stop working after a change;
-- the app says so before the user confirms.
--
--   handle_history   who had which handle until when (no app access)
--   handle_check(handle)    the reason a handle can't be used, or null
--   handle_change_info()    when the next change is allowed
--   change_handle(handle)   make the change; returns the new handle
-- =====================================================================

begin;

create table if not exists public.handle_history (
    id          bigint generated always as identity primary key,
    user_id     uuid not null references auth.users (id) on delete cascade,
    old_handle  text not null,
    new_handle  text not null,
    changed_at  timestamptz not null default now()
);
create index if not exists handle_history_user_idx on public.handle_history (user_id, changed_at desc);
create index if not exists handle_history_old_idx on public.handle_history (lower(old_handle), changed_at desc);

alter table public.handle_history enable row level security;
revoke all on public.handle_history from anon, authenticated;


-- Why p_handle can't be my handle, or null if it can.
create or replace function public.handle_check(p_handle text)
returns text
language plpgsql stable security definer set search_path = ''
as $$
declare
    me uuid := public.ex_uid();
    clean text := lower(btrim(regexp_replace(coalesce(p_handle, ''), '^@', '')));
begin
    if clean !~ '^[a-z0-9_]{3,20}$' then
        return 'Use 3 to 20 lowercase letters, numbers or underscores.';
    end if;
    if clean ~ '^(admin|administrator|akeso|support|help|moderator|mod|educator|staff|system|official|root|null|undefined|anonymous|everyone|here)'
       or clean ~ '(admin|akeso_team|moderator)$' then
        return 'That handle is reserved. Choose another.';
    end if;
    if exists (select 1 from public.profiles p where lower(p.handle) = clean and p.id <> me) then
        return 'That handle is taken.';
    end if;
    -- Given up by someone else in the last 30 days: still theirs.
    if exists (select 1 from public.handle_history h
               where lower(h.old_handle) = clean and h.user_id <> me
                 and h.changed_at > now() - interval '30 days') then
        return 'That handle is taken.';
    end if;
    return null;
end $$;

-- {last_changed_at, next_change_at (null = now), current}
create or replace function public.handle_change_info()
returns jsonb
language plpgsql stable security definer set search_path = ''
as $$
declare
    me uuid := public.ex_uid();
    last_at timestamptz;
begin
    select max(changed_at) into last_at from public.handle_history where user_id = me;
    return jsonb_build_object(
        'current', (select handle from public.profiles where id = me),
        'last_changed_at', last_at,
        'next_change_at', case when last_at is not null and last_at > now() - interval '30 days'
                               then last_at + interval '30 days' end);
end $$;

create or replace function public.change_handle(p_handle text)
returns text
language plpgsql security definer set search_path = ''
as $$
declare
    me uuid := public.ex_uid();
    clean text := lower(btrim(regexp_replace(coalesce(p_handle, ''), '^@', '')));
    current_handle text;
    last_at timestamptz;
    problem text;
begin
    select handle into current_handle from public.profiles where id = me for update;
    if current_handle is null then raise exception 'Your profile was not found.'; end if;
    if lower(current_handle) = clean then return current_handle; end if;   -- no change

    select max(changed_at) into last_at from public.handle_history where user_id = me;
    if last_at is not null and last_at > now() - interval '30 days' then
        raise exception 'You can change your handle once every 30 days. You can change it again on %.',
            to_char(last_at + interval '30 days', 'FMMonth FMDD, YYYY');
    end if;

    problem := public.handle_check(clean);
    if problem is not null then raise exception '%', problem; end if;

    begin
        update public.profiles set handle = clean, updated_at = now() where id = me;
    exception when unique_violation then
        raise exception 'That handle is taken.';
    end;
    insert into public.handle_history (user_id, old_handle, new_handle)
    values (me, current_handle, clean);
    -- Shown under Account Settings > Security like other profile changes.
    perform public._log_event(me, 'profile_updated', '',
        jsonb_build_object('fields', jsonb_build_array('handle'),
                           'from', current_handle, 'to', clean));
    return clean;
end $$;

do $$
declare fn text;
begin
    foreach fn in array array['public.handle_check(text)', 'public.handle_change_info()',
                              'public.change_handle(text)'] loop
        execute format('revoke execute on function %s from public, anon', fn);
        execute format('grant execute on function %s to authenticated', fn);
    end loop;
end $$;

commit;

notify pgrst, 'reload schema';

-- =====================================================================
-- Check: select to_regprocedure('public.change_handle(text)') is not null;  -- true
-- =====================================================================
