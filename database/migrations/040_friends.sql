-- =====================================================================
-- Akeso migration 040: Friends
-- =====================================================================
-- Run in the Supabase SQL editor AFTER 017_fix_avatar_read.sql (it uses
-- profiles, user_roles, notifications and the ex_* helpers from 002, 003,
-- 008 and 013). Safe to run again. 041 (notebook sharing) and 042 (study
-- groups) need this one first.
--
-- What this creates
--
--   friendships          one row per pair of people, in a fixed order
--                        (user_a < user_b): pending, accepted or blocked
--   friend_outbox        "I asked @handle": one row per request a person
--                        sends, whether or not that handle exists, so the
--                        Sent list can never reveal which handles are real
--   social_rate_log      attempts counted for rate limits (friend requests;
--                        041 and 042 add their own actions)
--
-- Friends are mutual and separate from Clinical Exchange's one-way Follow.
-- Being friends never shows more of a profile than its owner's switches
-- already allow (people are always shown through ex_author).
--
-- Blocking: a blocked person can't send the blocker requests, invites or
-- shares, and the blocker no longer turns up in their friend lookups.
-- Blocking ends any friendship and (with 041 and 042) revokes shares and
-- group invites between the two.
--
-- Security model: as Clinical Exchange. RLS on, no grants on the tables;
-- the app reaches them only through the SECURITY DEFINER functions below,
-- which check the signed-in user (ex_uid) themselves.
-- =====================================================================

begin;

-- ---------------------------------------------------------------------
-- 1. Tables
-- ---------------------------------------------------------------------
create table if not exists public.friendships (
    user_a        uuid not null references auth.users (id) on delete cascade,
    user_b        uuid not null references auth.users (id) on delete cascade,
    status        text not null check (status in ('pending', 'accepted', 'blocked')),
    requested_by  uuid references auth.users (id) on delete cascade,  -- who asked (pending, accepted)
    a_blocked     boolean not null default false,                     -- user_a blocked user_b
    b_blocked     boolean not null default false,                     -- user_b blocked user_a
    created_at    timestamptz not null default now(),
    updated_at    timestamptz not null default now(),
    accepted_at   timestamptz,
    primary key (user_a, user_b),
    check (user_a < user_b),
    check ((status = 'blocked') = (a_blocked or b_blocked))
);
create index if not exists friendships_b_idx on public.friendships (user_b, status);
create index if not exists friendships_a_idx on public.friendships (user_a, status);

create table if not exists public.friend_outbox (
    id          bigint generated always as identity primary key,
    sender_id   uuid not null references auth.users (id) on delete cascade,
    handle      text not null check (char_length(handle) between 1 and 40),
    target_id   uuid references auth.users (id) on delete cascade,   -- null if no such handle
    created_at  timestamptz not null default now(),
    unique (sender_id, handle)
);
create index if not exists friend_outbox_target_idx on public.friend_outbox (target_id);

create table if not exists public.social_rate_log (
    id          bigint generated always as identity primary key,
    user_id     uuid not null references auth.users (id) on delete cascade,
    action      text not null,
    created_at  timestamptz not null default now()
);
create index if not exists social_rate_log_idx on public.social_rate_log (user_id, action, created_at);

do $$
declare t text;
begin
    foreach t in array array['friendships', 'friend_outbox', 'social_rate_log'] loop
        execute format('alter table public.%I enable row level security', t);
        execute format('revoke all on public.%I from anon, authenticated', t);
    end loop;
end $$;

-- Notifications: the new kinds for friends, shared notes and study groups
-- (all three migrations), and a link to what the notification is about.
alter table public.notifications add column if not exists ref_kind text;
alter table public.notifications add column if not exists ref_id text;
alter table public.notifications drop constraint if exists notifications_kind_check;
alter table public.notifications add constraint notifications_kind_check
    check (kind in ('reply', 'best_answer', 'verified', 'reveal', 'moderation', 'mention',
                    'new_post',
                    'friend_request', 'friend_accepted', 'notebook_shared',
                    'group_invite', 'group_mention'));


-- ---------------------------------------------------------------------
-- 2. Helpers (not callable from the app)
-- ---------------------------------------------------------------------

-- The pair in the order the table keeps it.
create or replace function public.fr_pair(p_x uuid, p_y uuid, out a uuid, out b uuid)
language sql immutable set search_path = ''
as $$ select least(p_x, p_y), greatest(p_x, p_y) $$;

create or replace function public.fr_are_friends(p_x uuid, p_y uuid)
returns boolean
language sql stable security definer set search_path = ''
as $$
    select exists (select 1 from public.friendships
                   where user_a = least(p_x, p_y) and user_b = greatest(p_x, p_y)
                     and status = 'accepted');
$$;

-- Has either person blocked the other?
create or replace function public.fr_blocked(p_x uuid, p_y uuid)
returns boolean
language sql stable security definer set search_path = ''
as $$
    select exists (select 1 from public.friendships
                   where user_a = least(p_x, p_y) and user_b = greatest(p_x, p_y)
                     and status = 'blocked');
$$;

-- Count an attempt and refuse once the limit is reached. Counted even when
-- the attempt goes nowhere (an unknown handle), so trying many handles is
-- slowed down just the same.
create or replace function public.social_rate(p_user uuid, p_action text, p_max integer,
                                              p_window interval, p_label text)
returns void
language plpgsql security definer set search_path = ''
as $$
begin
    if (select count(*) from public.social_rate_log
        where user_id = p_user and action = p_action and created_at > now() - p_window) >= p_max then
        raise exception 'Slow down: you can send at most % % per %.', p_max, p_label,
            case when p_window = interval '1 hour' then 'hour'
                 when p_window = interval '1 minute' then 'minute'
                 else p_window::text end;
    end if;
    insert into public.social_rate_log (user_id, action) values (p_user, p_action);
    -- Keep the log small: nothing older than a day is ever counted.
    delete from public.social_rate_log
    where user_id = p_user and action = p_action and created_at < now() - interval '1 day';
end $$;

-- A notification that points at something other than a post.
create or replace function public.social_notify(p_user uuid, p_kind text, p_ref_kind text,
                                                p_ref_id text, p_message text)
returns void
language sql security definer set search_path = ''
as $$
    insert into public.notifications (user_id, kind, message, ref_kind, ref_id)
    select p_user, p_kind, left(p_message, 300), p_ref_kind, p_ref_id
    where p_user is not null;
$$;

-- "Name (@handle)" for notification text, by the same rules as ex_author.
create or replace function public.social_name(p_user uuid)
returns text
language sql stable security definer set search_path = ''
as $$
    select coalesce(nullif(p.display_name, ''), 'Akeso student')
           || case when p.visibility <> 'private' and p.handle is not null
                   then ' (@' || p.handle || ')' else '' end
    from public.profiles p where p.id = p_user;
$$;

-- Someone who can take part: has a profile and isn't leaving.
create or replace function public.social_active(p_user uuid)
returns boolean
language sql stable security definer set search_path = ''
as $$
    select exists (select 1 from public.profiles p
                   where p.id = p_user and p.deletion_scheduled_for is null);
$$;

-- One person as the app shows them, with the extra fields lists need.
create or replace function public.fr_person(p_user uuid, p_viewer uuid)
returns jsonb
language sql stable security definer set search_path = ''
as $$
    select coalesce(public.ex_author(p_user, false, p_viewer), '{}'::jsonb)
           || jsonb_build_object('id', p_user);
$$;


-- ---------------------------------------------------------------------
-- 3. Requests
-- ---------------------------------------------------------------------

-- Ask @handle to be friends. The reply is the same ("sent") whether or not
-- the handle exists, is blocked or blocked you, so handles can't be tested.
-- The one exception: if they had already asked you, you become friends
-- ("accepted"), which only tells you what you already knew.
create or replace function public.friend_request(p_handle text)
returns jsonb
language plpgsql security definer set search_path = ''
as $$
declare
    me uuid := public.ex_uid();
    clean text := lower(btrim(regexp_replace(coalesce(p_handle, ''), '^@', '')));
    target uuid;
    pa uuid; pb uuid;
    fr public.friendships;
begin
    if clean !~ '^[a-z0-9_]{3,20}$' then
        raise exception 'Enter a handle like @maria_santos (3 to 20 letters, numbers or _).';
    end if;
    perform public.social_rate(me, 'friend_request', 20, interval '1 hour', 'friend requests');
    if (select count(*) from public.friend_outbox where sender_id = me) >= 50 then
        raise exception 'You have 50 requests waiting. Cancel some under Friends > Requests first.';
    end if;

    select id into target from public.profiles
    where lower(handle) = clean and deletion_scheduled_for is null;

    if target is not null and target <> me then
        select a, b into pa, pb from public.fr_pair(me, target);
        select * into fr from public.friendships where user_a = pa and user_b = pb;
        if fr.status = 'pending' and fr.requested_by = target then
            update public.friendships
            set status = 'accepted', accepted_at = now(), updated_at = now()
            where user_a = pa and user_b = pb;
            delete from public.friend_outbox
            where (sender_id = me and target_id = target) or (sender_id = target and target_id = me);
            perform public.social_notify(target, 'friend_accepted', 'friend', me::text,
                public.social_name(me) || ' accepted your friend request.');
            return jsonb_build_object('status', 'accepted');
        end if;
        if fr.user_a is null then
            insert into public.friendships (user_a, user_b, status, requested_by)
            values (pa, pb, 'pending', me);
            perform public.social_notify(target, 'friend_request', 'friend', me::text,
                public.social_name(me) || ' sent you a friend request.');
        end if;
        -- already pending from me, already friends, or blocked: nothing new
    end if;

    if fr.status is distinct from 'accepted' then
        insert into public.friend_outbox (sender_id, handle, target_id)
        values (me, clean, case when target = me then null else target end)
        on conflict (sender_id, handle) do nothing;
    end if;
    return jsonb_build_object('status', 'sent');
end $$;

-- Accept or decline a request from p_from (their user id, from friend_requests()).
create or replace function public.friend_respond(p_from uuid, p_accept boolean)
returns void
language plpgsql security definer set search_path = ''
as $$
declare
    me uuid := public.ex_uid();
    pa uuid; pb uuid;
begin
    select a, b into pa, pb from public.fr_pair(me, p_from);
    if not exists (select 1 from public.friendships where user_a = pa and user_b = pb
                   and status = 'pending' and requested_by = p_from) then
        raise exception 'That request is no longer waiting.';
    end if;
    if p_accept then
        update public.friendships set status = 'accepted', accepted_at = now(), updated_at = now()
        where user_a = pa and user_b = pb;
        perform public.social_notify(p_from, 'friend_accepted', 'friend', me::text,
            public.social_name(me) || ' accepted your friend request.');
    else
        delete from public.friendships where user_a = pa and user_b = pb;   -- quietly
    end if;
    delete from public.friend_outbox where sender_id = p_from and target_id = me;
end $$;

-- Take back a request I sent (by its outbox id).
create or replace function public.friend_cancel(p_request bigint)
returns void
language plpgsql security definer set search_path = ''
as $$
declare
    me uuid := public.ex_uid();
    target uuid;
begin
    delete from public.friend_outbox where id = p_request and sender_id = me
    returning target_id into target;
    if target is not null then
        delete from public.friendships
        where user_a = least(me, target) and user_b = greatest(me, target)
          and status = 'pending' and requested_by = me;
    end if;
end $$;


-- ---------------------------------------------------------------------
-- 4. Lists
-- ---------------------------------------------------------------------
create or replace function public.friend_list()
returns setof jsonb
language plpgsql stable security definer set search_path = ''
as $$
declare me uuid := public.ex_uid();
begin
    return query
    select public.fr_person(other, me) || jsonb_build_object('since', f.accepted_at)
    from public.friendships f
    cross join lateral (select case when f.user_a = me then f.user_b else f.user_a end as other) o
    where (f.user_a = me or f.user_b = me) and f.status = 'accepted'
      and public.social_active(other)
    order by lower(coalesce((select display_name from public.profiles where id = other), ''));
end $$;

-- incoming: people waiting for my answer. sent: the handles I asked, as typed.
create or replace function public.friend_requests()
returns jsonb
language plpgsql stable security definer set search_path = ''
as $$
declare me uuid := public.ex_uid();
begin
    return jsonb_build_object(
        'incoming', coalesce((
            select jsonb_agg(public.fr_person(f.requested_by, me)
                             || jsonb_build_object('requested_at', f.created_at)
                             order by f.created_at desc)
            from public.friendships f
            where (f.user_a = me or f.user_b = me) and f.status = 'pending'
              and f.requested_by <> me and public.social_active(f.requested_by)), '[]'::jsonb),
        'sent', coalesce((
            select jsonb_agg(jsonb_build_object('request_id', o.id, 'handle', o.handle,
                                                'requested_at', o.created_at)
                             order by o.created_at desc)
            from public.friend_outbox o
            where o.sender_id = me
              and not (o.target_id is not null and public.fr_are_friends(me, o.target_id))),
            '[]'::jsonb));
end $$;

-- How I stand with the person behind a profile I can open (for its buttons).
-- none | friends | sent | received | blocked (only when I blocked them;
-- someone who blocked me just looks like "none").
create or replace function public.friend_status(p_handle text)
returns text
language plpgsql stable security definer set search_path = ''
as $$
declare
    me uuid := public.ex_uid();
    target uuid;
    fr public.friendships;
begin
    select id into target from public.profiles where lower(handle) = lower(p_handle);
    if target is null or target = me or public.ex_profile_access(target, me) is not null then
        return 'none';
    end if;
    select * into fr from public.friendships
    where user_a = least(me, target) and user_b = greatest(me, target);
    if fr.user_a is null then
        return case when exists (select 1 from public.friend_outbox
                                 where sender_id = me and target_id = target)
                    then 'sent' else 'none' end;
    end if;
    if fr.status = 'blocked' then
        return case when (fr.user_a = me and fr.a_blocked) or (fr.user_b = me and fr.b_blocked)
                    then 'blocked' else 'none' end;
    end if;
    if fr.status = 'accepted' then return 'friends'; end if;
    return case when fr.requested_by = me then 'sent' else 'received' end;
end $$;


-- ---------------------------------------------------------------------
-- 5. Unfriend, block, unblock
-- ---------------------------------------------------------------------
create or replace function public.friend_remove(p_user uuid)
returns void
language plpgsql security definer set search_path = ''
as $$
declare me uuid := public.ex_uid();
begin
    delete from public.friendships
    where user_a = least(me, p_user) and user_b = greatest(me, p_user)
      and status in ('accepted', 'pending');
    delete from public.friend_outbox
    where (sender_id = me and target_id = p_user) or (sender_id = p_user and target_id = me);
end $$;

create or replace function public.friend_block(p_user uuid)
returns void
language plpgsql security definer set search_path = ''
as $$
declare
    me uuid := public.ex_uid();
    pa uuid; pb uuid;
begin
    if p_user is null or p_user = me then raise exception 'You can''t block yourself.'; end if;
    if not exists (select 1 from auth.users where id = p_user) then
        raise exception 'That person is not available.';
    end if;
    select a, b into pa, pb from public.fr_pair(me, p_user);
    insert into public.friendships (user_a, user_b, status, requested_by, a_blocked, b_blocked)
    values (pa, pb, 'blocked', null, me = pa, me = pb)
    on conflict (user_a, user_b) do update
        set status = 'blocked', requested_by = null, accepted_at = null, updated_at = now(),
            a_blocked = public.friendships.a_blocked or (me = pa),
            b_blocked = public.friendships.b_blocked or (me = pb);
    delete from public.friend_outbox
    where (sender_id = me and target_id = p_user) or (sender_id = p_user and target_id = me);
end $$;

-- Unblocking does not bring a friendship back; they would ask again.
create or replace function public.friend_unblock(p_user uuid)
returns void
language plpgsql security definer set search_path = ''
as $$
declare
    me uuid := public.ex_uid();
    pa uuid; pb uuid;
begin
    select a, b into pa, pb from public.fr_pair(me, p_user);
    -- Nobody blocks any more: the row goes (no friendship is restored).
    delete from public.friendships
    where user_a = pa and user_b = pb and status = 'blocked'
      and ((me = pa and a_blocked and not b_blocked) or (me = pb and b_blocked and not a_blocked));
    -- The other person still blocks me: only my side is cleared.
    update public.friendships
    set a_blocked = case when me = pa then false else a_blocked end,
        b_blocked = case when me = pb then false else b_blocked end,
        updated_at = now()
    where user_a = pa and user_b = pb and status = 'blocked';
end $$;

create or replace function public.friend_blocked_list()
returns setof jsonb
language plpgsql stable security definer set search_path = ''
as $$
declare me uuid := public.ex_uid();
begin
    return query
    select jsonb_build_object('id', other,
                              'name', coalesce((select coalesce(nullif(display_name, ''), 'Akeso student')
                                                from public.profiles where id = other), 'Akeso student'),
                              'blocked_at', f.updated_at)
    from public.friendships f
    cross join lateral (select case when f.user_a = me then f.user_b else f.user_a end as other) o
    where f.status = 'blocked'
      and ((f.user_a = me and f.a_blocked) or (f.user_b = me and f.b_blocked))
    order by f.updated_at desc;
end $$;


-- ---------------------------------------------------------------------
-- 6. Notifications list, now with the link to a friend / share / group
-- ---------------------------------------------------------------------
-- Same fields as before (migration 003), plus ref_kind and ref_id.
create or replace function public.notif_list(p_limit integer default 30, p_before bigint default null)
returns setof jsonb
language plpgsql stable security definer set search_path = ''
as $$
declare me uuid := public.ex_uid();
begin
    return query
    select jsonb_build_object('id', n.id, 'kind', n.kind, 'post_id', n.post_id,
                              'reply_id', n.reply_id, 'message', n.message,
                              'created_at', n.created_at, 'read', n.read_at is not null,
                              'ref_kind', n.ref_kind, 'ref_id', n.ref_id)
    from public.notifications n
    where n.user_id = me and (p_before is null or n.id < p_before)
    order by n.id desc
    limit least(greatest(p_limit, 1), 100);
end $$;


-- ---------------------------------------------------------------------
-- 7. Account deletion (called by the purge-deleted-accounts Edge Function
--    with the service-role key, just before the sign-in account goes)
-- ---------------------------------------------------------------------
-- Everything below would also go by cascade when auth.users is deleted;
-- doing it first, in order, lets study groups pass to a moderator
-- (migration 042) and shares end cleanly (041). Each part runs only if its
-- migration is installed, so this one function covers all three.
create or replace function public.social_purge_user(p_user uuid)
returns jsonb
language plpgsql security definer set search_path = ''
as $$
declare
    groups jsonb := '{}'::jsonb;
    shares integer := 0;
    friends integer := 0;
begin
    if to_regprocedure('public.group_purge_user(uuid)') is not null then
        execute 'select public.group_purge_user($1)' into groups using p_user;
    end if;
    if to_regprocedure('public.notebook_share_purge_user(uuid)') is not null then
        execute 'select public.notebook_share_purge_user($1)' into shares using p_user;
    end if;
    delete from public.friendships where user_a = p_user or user_b = p_user;
    get diagnostics friends = row_count;
    delete from public.friend_outbox where sender_id = p_user or target_id = p_user;
    delete from public.social_rate_log where user_id = p_user;
    return jsonb_build_object('friendships', friends, 'shares', shares, 'groups', groups);
end $$;


-- ---------------------------------------------------------------------
-- 8. Who may call what
-- ---------------------------------------------------------------------
do $$
declare fn text;
begin
    foreach fn in array array[
        'public.fr_pair(uuid, uuid)', 'public.fr_are_friends(uuid, uuid)',
        'public.fr_blocked(uuid, uuid)',
        'public.social_rate(uuid, text, integer, interval, text)',
        'public.social_notify(uuid, text, text, text, text)', 'public.social_name(uuid)',
        'public.social_active(uuid)', 'public.fr_person(uuid, uuid)',
        'public.social_purge_user(uuid)'] loop
        execute format('revoke execute on function %s from public, anon, authenticated', fn);
    end loop;
    foreach fn in array array[
        'public.friend_request(text)', 'public.friend_respond(uuid, boolean)',
        'public.friend_cancel(bigint)', 'public.friend_list()', 'public.friend_requests()',
        'public.friend_status(text)', 'public.friend_remove(uuid)', 'public.friend_block(uuid)',
        'public.friend_unblock(uuid)', 'public.friend_blocked_list()',
        'public.notif_list(integer, bigint)'] loop
        execute format('revoke execute on function %s from public, anon', fn);
        execute format('grant execute on function %s to authenticated', fn);
    end loop;
end $$;
-- Only the purge function (service-role key) may remove a whole account's data.
grant execute on function public.social_purge_user(uuid) to service_role;

commit;

notify pgrst, 'reload schema';

-- =====================================================================
-- Checks:
--   select to_regprocedure('public.friend_request(text)') is not null;   -- true
--   select count(*) from public.friendships;                             -- 0 at first
-- =====================================================================
