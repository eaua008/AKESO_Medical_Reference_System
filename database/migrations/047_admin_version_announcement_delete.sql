-- =====================================================================
-- Akeso migration 047: friend request answers, app version, announcements
-- =====================================================================
-- Run AFTER 046_group_mention_handles.sql. Safe to run again. Adds and
-- replaces functions only; no table changes.
--
--   friend_request       an @handle that matches nobody now answers
--                        'not_found' (the app shows "No user with that
--                        @handle"). Before, it said "sent" for any handle.
--                        This is a deliberate trade: a typo is far more
--                        common than a person probing for accounts. Two
--                        things limit the probing: the 20-per-hour limit
--                        still counts every try (the answer is returned,
--                        not raised, so the count is kept), and someone
--                        who has blocked you, or whom you blocked, still
--                        looks exactly like a normal "sent".
--   admin_users          also returns the Akeso version each account last
--                        used (from the computers it signed in from).
--   admin_delete_announcement
--                        permanently removes an announcement, for admins.
--   announcements_stamp  a tiny fingerprint of the announcements the caller
--                        can see right now, so the app can check every
--                        couple of seconds and download the full list only
--                        when the fingerprint changes.
-- =====================================================================

begin;

-- ---------------------------------------------------------------------
-- 1. Friend requests: say so when the handle matches nobody
-- ---------------------------------------------------------------------
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

    -- Returned, not raised: raising would undo the rate-limit count above.
    if target is null then
        return jsonb_build_object('status', 'not_found');
    end if;
    if target = me then
        return jsonb_build_object('status', 'self');
    end if;

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

    if fr.status is distinct from 'accepted' then
        insert into public.friend_outbox (sender_id, handle, target_id)
        values (me, clean, target)
        on conflict (sender_id, handle) do nothing;
    end if;
    return jsonb_build_object('status', 'sent');
end $$;

-- ---------------------------------------------------------------------
-- 2. Admin: the Akeso version each account is on
-- ---------------------------------------------------------------------
create or replace function public.admin_users()
returns jsonb
language plpgsql stable security definer set search_path = ''
as $$
declare me uuid := public.ad_me();
begin
    return coalesce((
        select jsonb_agg(jsonb_build_object(
            'id', u.id,
            'email', u.email,
            'display_name', coalesce(nullif(p.display_name, ''), split_part(u.email, '@', 1)),
            'handle', p.handle,
            'role', coalesce(r.role::text, 'student'),
            'created_at', u.created_at,
            'last_sign_in_at', u.last_sign_in_at,
            'suspended', p.suspended_at is not null,
            'suspended_reason', coalesce(p.suspended_reason, ''),
            'deletion_scheduled_for', p.deletion_scheduled_for,
            'registry_id', 'AK-' || lpad((abs(hashtext(u.id::text)) % 10000)::text, 4, '0'),
            'is_me', u.id = me,
            -- the version on the computer used most recently ('' = never reported)
            'app_version', coalesce((select d.app_version from public.user_devices d
                                     where d.user_id = u.id
                                     order by d.last_seen desc limit 1), '')
        ) order by u.created_at)
        from auth.users u
        left join public.profiles p on p.id = u.id
        left join public.user_roles r on r.user_id = u.id
    ), '[]'::jsonb);
end $$;

-- ---------------------------------------------------------------------
-- 3. Admin: delete an announcement
-- ---------------------------------------------------------------------
create or replace function public.admin_delete_announcement(p_id uuid)
returns void
language plpgsql security definer set search_path = ''
as $$
declare v_title text;
begin
    perform public.ad_me();
    delete from public.announcements where id = p_id returning title into v_title;
    if v_title is not null then
        perform public.ad_log('announce_delete', 'announcement', p_id::text, v_title);
    end if;
end $$;

-- ---------------------------------------------------------------------
-- 4. A fingerprint of the announcements this account can see now
-- ---------------------------------------------------------------------
-- Changes when one is published, edited, ended, deleted, or reaches its
-- start or end time. Dismissing does not change it (the app already knows).
create or replace function public.announcements_stamp()
returns text
language plpgsql stable security definer set search_path = ''
as $$
declare
    uid uuid := auth.uid();
    v_role text;
begin
    if uid is null then raise exception 'Not signed in.'; end if;
    select role::text into v_role from public.user_roles where user_id = uid;
    v_role := coalesce(v_role, 'student');
    return coalesce((
        select md5(string_agg(a.id::text || ':' || a.updated_at::text, ',' order by a.id))
        from public.announcements a
        where a.ended_at is null
          and a.starts_at <= now()
          and (a.ends_at is null or a.ends_at > now())
          and (a.audience = 'everyone' or a.audience = v_role)), '');
end $$;

do $$
declare fn text;
begin
    foreach fn in array array['public.friend_request(text)', 'public.admin_users()',
        'public.admin_delete_announcement(uuid)', 'public.announcements_stamp()'] loop
        execute format('revoke execute on function %s from public, anon', fn);
        execute format('grant execute on function %s to authenticated', fn);
    end loop;
end $$;

commit;

notify pgrst, 'reload schema';
