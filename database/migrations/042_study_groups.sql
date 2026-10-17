-- =====================================================================
-- Akeso migration 042: Study Groups
-- =====================================================================
-- Run AFTER 041_notebook_sharing.sql. Safe to run again.
--
-- What this creates
--
--   study_groups          a group: name, description, Public or Private,
--                         an optional topic and body system
--   study_group_members   who is in it: owner, moderator or member (max 50)
--   study_group_messages  the group chat (plain text, no anonymous posts)
--   study_group_notes     read-only note snapshots shared into the group
--   study_group_invites   friend invites, and invite links (the link's
--                         token is stored only as a SHA-256 hash)
--   study_group_reports   reports on messages and shared notes
--
-- Public groups are listed in Browse and anyone signed in can join.
-- Private groups are never listed: people join only through a friend
-- invite from the owner or a moderator, or an invite link / code.
--
-- Moderation: the owner and moderators can remove members and hide
-- messages and notes. App educators and admins see and act on REPORTED
-- content only; they can't browse private groups.
--
-- Blocking (migration 040): two people where one blocked the other can't
-- invite or add each other, and mentions between them notify no one. If
-- they are already in the same group, their messages stay.
--
-- If an owner's account is deleted, the longest-standing moderator becomes
-- the owner; with no moderator the group is deleted.
--
-- Security model: as Clinical Exchange. RLS on, no grants on the tables,
-- everything through the SECURITY DEFINER functions below.
-- =====================================================================

begin;

-- ---------------------------------------------------------------------
-- 1. Tables
-- ---------------------------------------------------------------------
create table if not exists public.study_groups (
    id              uuid primary key default gen_random_uuid(),
    owner_id        uuid references auth.users (id) on delete set null,
    name            text not null check (char_length(btrim(name)) between 3 and 60),
    description     text not null default '' check (char_length(description) <= 500),
    visibility      text not null check (visibility in ('public', 'private')),
    topic           text not null default '' check (char_length(topic) <= 60),
    body_system_id  text,
    created_at      timestamptz not null default now(),
    updated_at      timestamptz not null default now()
);
create index if not exists study_groups_public_idx
    on public.study_groups (created_at desc) where visibility = 'public';

create table if not exists public.study_group_members (
    group_id      uuid not null references public.study_groups (id) on delete cascade,
    user_id       uuid not null references auth.users (id) on delete cascade,
    role          text not null default 'member' check (role in ('owner', 'moderator', 'member')),
    joined_at     timestamptz not null default now(),
    muted         boolean not null default false,
    last_read_id  bigint not null default 0,
    primary key (group_id, user_id)
);
create index if not exists study_group_members_user_idx on public.study_group_members (user_id);

create table if not exists public.study_group_messages (
    id          bigint generated always as identity primary key,
    group_id    uuid not null references public.study_groups (id) on delete cascade,
    author_id   uuid not null references auth.users (id) on delete cascade,
    body        text not null check (char_length(btrim(body)) between 1 and 2000),
    status      text not null default 'open' check (status in ('open', 'hidden')),
    hidden_by   uuid references auth.users (id) on delete set null,
    hidden_at   timestamptz,
    created_at  timestamptz not null default now()
);
create index if not exists study_group_messages_poll_idx on public.study_group_messages (group_id, id);
create index if not exists study_group_messages_author_idx on public.study_group_messages (author_id, created_at);

create table if not exists public.study_group_notes (
    id              uuid primary key default gen_random_uuid(),
    group_id        uuid not null references public.study_groups (id) on delete cascade,
    owner_id        uuid not null references auth.users (id) on delete cascade,
    source_item_id  text not null check (char_length(source_item_id) between 1 and 64),
    kind            text not null default 'note'
                    check (kind in ('note', 'symptom_case', 'interaction_case')),
    title           text not null check (char_length(btrim(title)) between 1 and 300),
    body            text not null default '' check (char_length(body) <= 200000),
    status          text not null default 'open' check (status in ('open', 'hidden')),
    created_at      timestamptz not null default now(),
    updated_at      timestamptz not null default now(),
    unique (group_id, owner_id, source_item_id)
);

create table if not exists public.study_group_invites (
    id           uuid primary key default gen_random_uuid(),
    group_id     uuid not null references public.study_groups (id) on delete cascade,
    kind         text not null check (kind in ('link', 'friend')),
    token_hash   text unique,                                        -- links only
    invitee_id   uuid references auth.users (id) on delete cascade,  -- friend invites only
    created_by   uuid references auth.users (id) on delete cascade,
    created_at   timestamptz not null default now(),
    expires_at   timestamptz,
    revoked_at   timestamptz,
    answered_at  timestamptz,
    accepted     boolean,
    uses         integer not null default 0,
    check ((kind = 'link') = (token_hash is not null)),
    check ((kind = 'friend') = (invitee_id is not null))
);
create index if not exists study_group_invites_group_idx on public.study_group_invites (group_id);
create index if not exists study_group_invites_invitee_idx
    on public.study_group_invites (invitee_id) where kind = 'friend' and answered_at is null;

create table if not exists public.study_group_reports (
    id           bigint generated always as identity primary key,
    reporter_id  uuid not null references auth.users (id) on delete cascade,
    group_id     uuid not null references public.study_groups (id) on delete cascade,
    target_kind  text not null check (target_kind in ('message', 'note')),
    target_id    text not null,
    reason       text not null check (reason in ('patient_data', 'misinformation', 'harassment',
                                                 'spam', 'off_topic', 'impersonation', 'other')),
    note         text not null default '' check (char_length(note) <= 500),
    status       text not null default 'open' check (status in ('open', 'resolved', 'dismissed')),
    handled_by   uuid references auth.users (id) on delete set null,
    handled_at   timestamptz,
    created_at   timestamptz not null default now(),
    unique (reporter_id, target_kind, target_id)
);
create index if not exists study_group_reports_open_idx
    on public.study_group_reports (status, created_at) where status = 'open';

do $$
declare t text;
begin
    foreach t in array array['study_groups', 'study_group_members', 'study_group_messages',
                             'study_group_notes', 'study_group_invites', 'study_group_reports'] loop
        execute format('alter table public.%I enable row level security', t);
        execute format('revoke all on public.%I from anon, authenticated', t);
    end loop;
end $$;


-- ---------------------------------------------------------------------
-- 2. Helpers (not callable from the app)
-- ---------------------------------------------------------------------
create or replace function public.sg_role(p_group uuid, p_user uuid)
returns text
language sql stable security definer set search_path = ''
as $$
    select role from public.study_group_members where group_id = p_group and user_id = p_user;
$$;

create or replace function public.sg_is_staff(p_group uuid, p_user uuid)
returns boolean
language sql stable security definer set search_path = ''
as $$
    select coalesce(public.sg_role(p_group, p_user) in ('owner', 'moderator'), false);
$$;

-- The member as the app shows them (ex_author), plus their group role.
create or replace function public.sg_person(p_group uuid, p_user uuid, p_viewer uuid)
returns jsonb
language sql stable security definer set search_path = ''
as $$
    select public.fr_person(p_user, p_viewer)
           || jsonb_build_object('group_role', public.sg_role(p_group, p_user));
$$;

-- Token hashing: SHA-256 (built into Postgres), hex.
create or replace function public.sg_hash(p_token text)
returns text
language sql immutable set search_path = ''
as $$
    select pg_catalog.encode(pg_catalog.sha256(pg_catalog.convert_to(p_token, 'UTF8')), 'hex');
$$;

-- Add someone, safely under concurrent joins: the group row is locked, so
-- two joins can't both take the 50th seat.
create or replace function public.sg_add_member(p_group uuid, p_user uuid, p_role text)
returns void
language plpgsql security definer set search_path = ''
as $$
begin
    perform 1 from public.study_groups where id = p_group for update;
    if not found then raise exception 'That study group is no longer available.'; end if;
    if exists (select 1 from public.study_group_members where group_id = p_group and user_id = p_user) then
        return;                                              -- already in it
    end if;
    if (select count(*) from public.study_group_members where group_id = p_group) >= 50 then
        raise exception 'This study group is full (50 members).';
    end if;
    insert into public.study_group_members (group_id, user_id, role, last_read_id)
    values (p_group, p_user, p_role,
            coalesce((select max(id) from public.study_group_messages where group_id = p_group), 0));
end $$;

create or replace function public.sg_row(g public.study_groups, p_viewer uuid)
returns jsonb
language sql stable security definer set search_path = ''
as $$
    select jsonb_build_object(
        'id', g.id, 'name', g.name, 'description', g.description,
        'visibility', g.visibility, 'topic', g.topic, 'body_system_id', g.body_system_id,
        'created_at', g.created_at,
        'members', (select count(*) from public.study_group_members m where m.group_id = g.id),
        'my_role', public.sg_role(g.id, p_viewer),
        'owner', case when g.owner_id is not null then public.fr_person(g.owner_id, p_viewer) end);
$$;

-- An owner's account goes (or the owner_id is cleared): hand the group to
-- the longest-standing moderator, otherwise delete it.
create or replace function public.sg_handover(p_group uuid, p_old_owner uuid)
returns text
language plpgsql security definer set search_path = ''
as $$
declare heir uuid;
begin
    select user_id into heir from public.study_group_members
    where group_id = p_group and role = 'moderator' and user_id is distinct from p_old_owner
    order by joined_at, user_id limit 1;
    if heir is null then
        delete from public.study_groups where id = p_group;
        return 'deleted';
    end if;
    update public.study_group_members set role = 'owner' where group_id = p_group and user_id = heir;
    update public.study_groups set owner_id = heir, updated_at = now() where id = p_group;
    delete from public.study_group_members where group_id = p_group and user_id = p_old_owner;
    return 'transferred';
end $$;

create or replace function public.sg_owner_gone()
returns trigger
language plpgsql security definer set search_path = ''
as $$
begin
    if new.owner_id is null and old.owner_id is not null then
        perform public.sg_handover(new.id, old.owner_id);
    end if;
    return null;
end $$;

drop trigger if exists study_groups_owner_gone on public.study_groups;
create trigger study_groups_owner_gone after update of owner_id on public.study_groups
    for each row execute function public.sg_owner_gone();

-- Blocking someone revokes the friend invites between the two.
create or replace function public.sg_block_revokes_invites()
returns trigger
language plpgsql security definer set search_path = ''
as $$
begin
    if new.status = 'blocked' then
        update public.study_group_invites set revoked_at = now()
        where kind = 'friend' and answered_at is null and revoked_at is null
          and ((created_by = new.user_a and invitee_id = new.user_b)
            or (created_by = new.user_b and invitee_id = new.user_a));
    end if;
    return null;
end $$;

drop trigger if exists friendships_block_group_invites on public.friendships;
create trigger friendships_block_group_invites after insert or update of status on public.friendships
    for each row execute function public.sg_block_revokes_invites();

-- Message as a member sees it. Hidden ones keep their place but not their
-- text, except for the author and the group's owner and moderators.
create or replace function public.sg_message_row(m public.study_group_messages, p_viewer uuid,
                                                 p_staff boolean)
returns jsonb
language sql stable security definer set search_path = ''
as $$
    select jsonb_build_object(
        'id', m.id, 'created_at', m.created_at, 'status', m.status,
        'author', public.sg_person(m.group_id, m.author_id, p_viewer),
        'body', case when m.status = 'open' or p_staff or m.author_id = p_viewer then m.body
                     else '' end,
        'is_mine', m.author_id = p_viewer);
$$;


-- ---------------------------------------------------------------------
-- 3. Groups
-- ---------------------------------------------------------------------
create or replace function public.group_create(p_name text, p_description text, p_visibility text,
                                               p_topic text, p_body_system text)
returns uuid
language plpgsql security definer set search_path = ''
as $$
declare
    me uuid := public.ex_uid();
    found text;
    g uuid;
begin
    if p_visibility not in ('public', 'private') then raise exception 'Choose Public or Private.'; end if;
    if char_length(btrim(coalesce(p_name, ''))) < 3 then
        raise exception 'Give the group a name of at least 3 characters.';
    end if;
    found := public.ex_phi_check(coalesce(p_name, '') || ' ' || coalesce(p_description, ''));
    if found is not null then
        raise exception 'This looks like it contains %. Remove anything that could identify a real person.', found;
    end if;
    if (select count(*) from public.study_groups where owner_id = me) >= 20 then
        raise exception 'You own 20 study groups already. Delete one first.';
    end if;
    perform public.social_rate(me, 'group_create', 5, interval '1 day', 'new groups');
    insert into public.study_groups (owner_id, name, description, visibility, topic, body_system_id)
    values (me, btrim(p_name), btrim(coalesce(p_description, '')), p_visibility,
            left(btrim(coalesce(p_topic, '')), 60), nullif(btrim(coalesce(p_body_system, '')), ''))
    returning id into g;
    insert into public.study_group_members (group_id, user_id, role) values (g, me, 'owner');
    return g;
end $$;

-- Browse: public groups only. Groups owned by someone who blocked you (or
-- whom you blocked) are left out.
create or replace function public.group_browse_public(p_search text default null,
                                                      p_topic text default null,
                                                      p_body_system text default null,
                                                      p_limit integer default 30,
                                                      p_offset integer default 0)
returns setof jsonb
language plpgsql stable security definer set search_path = ''
as $$
declare
    me uuid := public.ex_uid();
    words text := lower(btrim(coalesce(p_search, '')));
begin
    return query
    select public.sg_row(g, me)
    from public.study_groups g
    where g.visibility = 'public'
      and (g.owner_id is null or not public.fr_blocked(g.owner_id, me))
      and (words = '' or lower(g.name || ' ' || g.description || ' ' || g.topic) like '%' || words || '%')
      and (coalesce(p_topic, '') = '' or lower(g.topic) = lower(p_topic))
      and (coalesce(p_body_system, '') = '' or g.body_system_id = p_body_system)
    order by (select count(*) from public.study_group_members m where m.group_id = g.id) desc,
             g.created_at desc
    limit least(greatest(p_limit, 1), 100) offset greatest(p_offset, 0);
end $$;

-- My groups, with how many messages I haven't seen.
create or replace function public.group_my_list()
returns setof jsonb
language plpgsql stable security definer set search_path = ''
as $$
declare me uuid := public.ex_uid();
begin
    return query
    select public.sg_row(g, me) || jsonb_build_object(
               'muted', m.muted,
               'unread', (select count(*) from public.study_group_messages x
                          where x.group_id = g.id and x.id > m.last_read_id and x.author_id <> me
                            and x.status = 'open'),
               'last_message_at', (select max(created_at) from public.study_group_messages x
                                   where x.group_id = g.id))
    from public.study_group_members m
    join public.study_groups g on g.id = m.group_id
    where m.user_id = me
    order by coalesce((select max(created_at) from public.study_group_messages x
                       where x.group_id = g.id), g.created_at) desc;
end $$;

-- One group. Members get everything; a public group's non-members get the
-- summary to decide whether to join; a private group is "not available"
-- to anyone outside it (app moderators included).
create or replace function public.group_get(p_group uuid)
returns jsonb
language plpgsql stable security definer set search_path = ''
as $$
declare
    me uuid := public.ex_uid();
    g public.study_groups;
    my_role text;
    link public.study_group_invites;
begin
    select * into g from public.study_groups where id = p_group;
    my_role := public.sg_role(p_group, me);
    if g.id is null or (my_role is null and (g.visibility <> 'public'
                                             or (g.owner_id is not null and public.fr_blocked(g.owner_id, me)))) then
        raise exception 'That study group is not available.';
    end if;
    if my_role is null then
        return public.sg_row(g, me) || jsonb_build_object('can_join',
            (select count(*) from public.study_group_members where group_id = g.id) < 50);
    end if;
    select * into link from public.study_group_invites
    where group_id = g.id and kind = 'link' and revoked_at is null
      and (expires_at is null or expires_at > now())
    order by created_at desc limit 1;
    return public.sg_row(g, me) || jsonb_build_object(
        'muted', (select muted from public.study_group_members where group_id = g.id and user_id = me),
        'members_list', coalesce((
            select jsonb_agg(public.sg_person(g.id, m.user_id, me)
                             || jsonb_build_object('joined_at', m.joined_at,
                                                   'blocked', public.fr_blocked(m.user_id, me))
                             order by case m.role when 'owner' then 0 when 'moderator' then 1 else 2 end,
                                      m.joined_at)
            from public.study_group_members m where m.group_id = g.id), '[]'::jsonb),
        'invite_link', case when my_role in ('owner', 'moderator') and link.id is not null then
            jsonb_build_object('id', link.id, 'created_at', link.created_at,
                               'expires_at', link.expires_at, 'uses', link.uses) end,
        'pending_invites', case when my_role in ('owner', 'moderator') then coalesce((
            select jsonb_agg(public.fr_person(i.invitee_id, me) || jsonb_build_object('invite_id', i.id))
            from public.study_group_invites i
            where i.group_id = g.id and i.kind = 'friend' and i.answered_at is null
              and i.revoked_at is null), '[]'::jsonb) end);
end $$;

create or replace function public.group_join_public(p_group uuid)
returns void
language plpgsql security definer set search_path = ''
as $$
declare
    me uuid := public.ex_uid();
    g public.study_groups;
begin
    select * into g from public.study_groups where id = p_group;
    if g.id is null or g.visibility <> 'public'
       or (g.owner_id is not null and public.fr_blocked(g.owner_id, me)) then
        raise exception 'That study group is not available.';
    end if;
    perform public.sg_add_member(p_group, me, 'member');
end $$;

-- Join with an invite link or its code. Wrong, expired and revoked tokens
-- get the same answer.
create or replace function public.group_join_with_token(p_token text)
returns uuid
language plpgsql security definer set search_path = ''
as $$
declare
    me uuid := public.ex_uid();
    inv public.study_group_invites;
    owner uuid;
begin
    perform public.social_rate(me, 'group_join_token', 20, interval '1 hour', 'invite codes');
    select * into inv from public.study_group_invites
    where kind = 'link' and token_hash = public.sg_hash(btrim(coalesce(p_token, '')));
    select owner_id into owner from public.study_groups where id = inv.group_id;
    if inv.id is null or inv.revoked_at is not null
       or (inv.expires_at is not null and inv.expires_at <= now())
       or (inv.created_by is not null and public.fr_blocked(inv.created_by, me))
       or (owner is not null and public.fr_blocked(owner, me)) then
        raise exception 'This invite link is not valid or has expired. Ask for a new one.';
    end if;
    if public.sg_role(inv.group_id, me) is null then
        perform public.sg_add_member(inv.group_id, me, 'member');
        update public.study_group_invites set uses = uses + 1 where id = inv.id;
    end if;
    return inv.group_id;
end $$;

-- A new invite link (the previous one stops working). Returns the token:
-- shown once, never stored in readable form. p_expires_hours null = no expiry.
create or replace function public.group_invite_link_create(p_group uuid, p_expires_hours integer default null)
returns jsonb
language plpgsql security definer set search_path = ''
as $$
declare
    me uuid := public.ex_uid();
    token text;
    inv uuid;
    expires timestamptz;
begin
    if not public.sg_is_staff(p_group, me) then
        raise exception 'Only the owner and moderators can make invite links.';
    end if;
    perform public.social_rate(me, 'group_link', 20, interval '1 hour', 'invite links');
    if p_expires_hours is not null and (p_expires_hours < 1 or p_expires_hours > 24 * 90) then
        raise exception 'Choose an expiry between 1 hour and 90 days.';
    end if;
    update public.study_group_invites set revoked_at = now()
    where group_id = p_group and kind = 'link' and revoked_at is null;
    -- Two random UUIDs: 244 random bits, as 64 letters and digits.
    token := replace(gen_random_uuid()::text || gen_random_uuid()::text, '-', '');
    expires := case when p_expires_hours is null then null
                    else now() + make_interval(hours => p_expires_hours) end;
    insert into public.study_group_invites (group_id, kind, token_hash, created_by, expires_at)
    values (p_group, 'link', public.sg_hash(token), me, expires)
    returning id into inv;
    return jsonb_build_object('invite_id', inv, 'token', token, 'expires_at', expires);
end $$;

create or replace function public.group_invite_link_revoke(p_group uuid)
returns void
language plpgsql security definer set search_path = ''
as $$
declare me uuid := public.ex_uid();
begin
    if not public.sg_is_staff(p_group, me) then
        raise exception 'Only the owner and moderators can manage invite links.';
    end if;
    update public.study_group_invites set revoked_at = now()
    where group_id = p_group and kind = 'link' and revoked_at is null;
end $$;

-- Invite a friend (owner or moderator). They get a notification and answer
-- it with group_invite_respond.
create or replace function public.group_invite_friend(p_group uuid, p_friend uuid)
returns void
language plpgsql security definer set search_path = ''
as $$
declare
    me uuid := public.ex_uid();
    inv uuid;
    gname text;
begin
    if not public.sg_is_staff(p_group, me) then
        raise exception 'Only the owner and moderators can invite people.';
    end if;
    if not public.fr_are_friends(me, p_friend) or not public.social_active(p_friend) then
        raise exception 'You can only invite your friends.';
    end if;
    if public.sg_role(p_group, p_friend) is not null then
        raise exception 'They are already in this group.';
    end if;
    if exists (select 1 from public.study_group_members m
               where m.group_id = p_group and public.fr_blocked(m.user_id, p_friend)
                 and m.role in ('owner', 'moderator')) then
        raise exception 'They can''t be invited to this group.';
    end if;
    if exists (select 1 from public.study_group_invites where group_id = p_group and kind = 'friend'
               and invitee_id = p_friend and answered_at is null and revoked_at is null) then
        return;                                              -- already invited
    end if;
    perform public.social_rate(me, 'group_invite', 30, interval '1 hour', 'group invites');
    insert into public.study_group_invites (group_id, kind, invitee_id, created_by)
    values (p_group, 'friend', p_friend, me) returning id into inv;
    select name into gname from public.study_groups where id = p_group;
    perform public.social_notify(p_friend, 'group_invite', 'group_invite', inv::text,
        public.social_name(me) || ' invited you to the study group “' || public.ex_short(gname) || '”');
end $$;

create or replace function public.group_my_invites()
returns setof jsonb
language plpgsql stable security definer set search_path = ''
as $$
declare me uuid := public.ex_uid();
begin
    return query
    select jsonb_build_object('invite_id', i.id, 'invited_at', i.created_at,
                              'from', public.fr_person(i.created_by, me))
           || jsonb_build_object('group', public.sg_row(g, me))
    from public.study_group_invites i join public.study_groups g on g.id = i.group_id
    where i.kind = 'friend' and i.invitee_id = me and i.answered_at is null and i.revoked_at is null
      and not public.fr_blocked(i.created_by, me)
    order by i.created_at desc;
end $$;

create or replace function public.group_invite_respond(p_invite uuid, p_accept boolean)
returns uuid
language plpgsql security definer set search_path = ''
as $$
declare
    me uuid := public.ex_uid();
    inv public.study_group_invites;
begin
    select * into inv from public.study_group_invites
    where id = p_invite and kind = 'friend' and invitee_id = me;
    if inv.id is null or inv.revoked_at is not null or inv.answered_at is not null
       or public.fr_blocked(inv.created_by, me) then
        raise exception 'That invite is no longer valid.';
    end if;
    if p_accept then
        perform public.sg_add_member(inv.group_id, me, 'member');
    end if;
    update public.study_group_invites set answered_at = now(), accepted = p_accept where id = p_invite;
    return inv.group_id;
end $$;

-- Leave. The owner can leave only once someone else can take over: the
-- longest-standing moderator becomes the owner. Alone in it, the group goes.
create or replace function public.group_leave(p_group uuid)
returns text
language plpgsql security definer set search_path = ''
as $$
declare
    me uuid := public.ex_uid();
    my_role text := public.sg_role(p_group, me);
begin
    if my_role is null then return 'not_member'; end if;
    if my_role = 'owner' then
        if not exists (select 1 from public.study_group_members where group_id = p_group and user_id <> me) then
            delete from public.study_groups where id = p_group;
            return 'deleted';
        end if;
        if not exists (select 1 from public.study_group_members where group_id = p_group
                       and role = 'moderator') then
            raise exception 'Make someone a moderator first (they become the owner when you leave), or delete the group.';
        end if;
        return public.sg_handover(p_group, me);
    end if;
    delete from public.study_group_members where group_id = p_group and user_id = me;
    return 'left';
end $$;

-- Owner only. p_role: moderator | member | owner (hands the group over;
-- the old owner becomes a moderator).
create or replace function public.group_set_role(p_group uuid, p_user uuid, p_role text)
returns void
language plpgsql security definer set search_path = ''
as $$
declare me uuid := public.ex_uid();
begin
    if public.sg_role(p_group, me) is distinct from 'owner' then
        raise exception 'Only the owner can change roles.';
    end if;
    if p_user = me then raise exception 'Choose another member.'; end if;
    if public.sg_role(p_group, p_user) is null then raise exception 'They are not in this group.'; end if;
    if p_role not in ('owner', 'moderator', 'member') then raise exception 'Unknown role.'; end if;
    if p_role = 'owner' then
        update public.study_group_members set role = 'moderator' where group_id = p_group and user_id = me;
        update public.study_group_members set role = 'owner' where group_id = p_group and user_id = p_user;
        update public.study_groups set owner_id = p_user, updated_at = now() where id = p_group;
    else
        update public.study_group_members set role = p_role where group_id = p_group and user_id = p_user;
    end if;
end $$;

-- Owner removes anyone; a moderator removes members only.
create or replace function public.group_remove_member(p_group uuid, p_user uuid)
returns void
language plpgsql security definer set search_path = ''
as $$
declare
    me uuid := public.ex_uid();
    my_role text := public.sg_role(p_group, me);
    their_role text := public.sg_role(p_group, p_user);
begin
    if their_role is null then return; end if;
    if p_user = me then raise exception 'Use Leave group instead.'; end if;
    if not (my_role = 'owner' or (my_role = 'moderator' and their_role = 'member')) then
        raise exception 'You can''t remove this member.';
    end if;
    delete from public.study_group_members where group_id = p_group and user_id = p_user;
end $$;

create or replace function public.group_set_muted(p_group uuid, p_muted boolean)
returns void
language plpgsql security definer set search_path = ''
as $$
declare me uuid := public.ex_uid();
begin
    update public.study_group_members set muted = coalesce(p_muted, false)
    where group_id = p_group and user_id = me;
end $$;

-- Owner only: the group, its chat, notes and invites all go.
create or replace function public.group_delete(p_group uuid)
returns void
language plpgsql security definer set search_path = ''
as $$
declare me uuid := public.ex_uid();
begin
    if public.sg_role(p_group, me) is distinct from 'owner' then
        raise exception 'Only the owner can delete the group.';
    end if;
    delete from public.study_groups where id = p_group;
end $$;


-- ---------------------------------------------------------------------
-- 4. Chat
-- ---------------------------------------------------------------------
-- Plain text, 2,000 characters at most, checked for patient data, at most
-- 10 a minute and 120 an hour. @handle mentions of group members notify
-- them (not if muted, not between people where one blocked the other).
create or replace function public.group_send_message(p_group uuid, p_body text)
returns jsonb
language plpgsql security definer set search_path = ''
as $$
declare
    me uuid := public.ex_uid();
    clean text := btrim(coalesce(p_body, ''));
    found text;
    msg public.study_group_messages;
    gname text;
    target uuid;
begin
    if public.sg_role(p_group, me) is null then raise exception 'Join the group to post in it.'; end if;
    if clean = '' then raise exception 'Write a message first.'; end if;
    if char_length(clean) > 2000 then raise exception 'Keep messages under 2,000 characters.'; end if;
    found := public.ex_phi_check(clean);
    if found is not null then
        raise exception 'Not sent: this looks like it contains %. Cases must be hypothetical; remove anything that could identify a real person.', found;
    end if;
    if (select count(*) from public.study_group_messages
        where author_id = me and created_at > now() - interval '1 minute') >= 10 then
        raise exception 'Slow down: at most 10 messages a minute.';
    end if;
    if (select count(*) from public.study_group_messages
        where author_id = me and created_at > now() - interval '1 hour') >= 120 then
        raise exception 'Slow down: at most 120 messages an hour.';
    end if;
    insert into public.study_group_messages (group_id, author_id, body)
    values (p_group, me, clean) returning * into msg;
    update public.study_group_members set last_read_id = msg.id where group_id = p_group and user_id = me;

    select name into gname from public.study_groups where id = p_group;
    for target in
        select distinct m.user_id
        from regexp_matches(clean, '@([A-Za-z0-9_]{3,20})', 'g') as h(parts)
        join public.profiles p on lower(p.handle) = lower(h.parts[1])
        join public.study_group_members m on m.group_id = p_group and m.user_id = p.id
        where m.user_id <> me and not m.muted and not public.fr_blocked(m.user_id, me)
        limit 10
    loop
        perform public.social_notify(target, 'group_mention', 'group', p_group::text,
            public.social_name(me) || ' mentioned you in “' || public.ex_short(gname, 40) || '”: '
            || public.ex_short(clean, 120));
    end loop;
    return public.sg_message_row(msg, me, public.sg_is_staff(p_group, me));
end $$;

-- New messages since p_after (the last id the app has), oldest first.
-- p_after null: the latest p_limit messages. Also marks them read.
create or replace function public.group_messages_after(p_group uuid, p_after bigint default null,
                                                       p_limit integer default 50)
returns jsonb
language plpgsql security definer set search_path = ''
as $$
declare
    me uuid := public.ex_uid();
    staff boolean;
    out_rows jsonb;
    newest bigint;
    n integer := least(greatest(coalesce(p_limit, 50), 1), 100);
begin
    if public.sg_role(p_group, me) is null then
        raise exception 'That study group is not available.';
    end if;
    staff := public.sg_is_staff(p_group, me);
    if p_after is null then
        select coalesce(jsonb_agg(public.sg_message_row(m, me, staff) order by m.id), '[]'::jsonb),
               max(m.id)
          into out_rows, newest
          from (select * from public.study_group_messages where group_id = p_group
                order by id desc limit n) m;
    else
        select coalesce(jsonb_agg(public.sg_message_row(m, me, staff) order by m.id), '[]'::jsonb),
               max(m.id)
          into out_rows, newest
          from (select * from public.study_group_messages where group_id = p_group and id > p_after
                order by id limit n) m;
    end if;
    if newest is not null then
        update public.study_group_members set last_read_id = greatest(last_read_id, newest)
        where group_id = p_group and user_id = me;
    end if;
    return jsonb_build_object('messages', out_rows, 'more', jsonb_array_length(out_rows) >= n);
end $$;


-- ---------------------------------------------------------------------
-- 5. Shared notes shelf
-- ---------------------------------------------------------------------
-- p_item: {source_item_id, kind, title, body}. Same rules as sharing with
-- friends (041): text only, patient-data check, counted with those shares.
create or replace function public.group_share_note(p_group uuid, p_item jsonb)
returns uuid
language plpgsql security definer set search_path = ''
as $$
declare
    me uuid := public.ex_uid();
    v_title text := btrim(coalesce(p_item ->> 'title', ''));
    v_body text := public.ns_clean_body(p_item ->> 'body');
    found text;
    note uuid;
begin
    if public.sg_role(p_group, me) is null then raise exception 'Join the group to share in it.'; end if;
    if v_title = '' or coalesce(p_item ->> 'source_item_id', '') = '' then
        raise exception 'That note has no title.';
    end if;
    found := public.ex_phi_check(v_title || ' ' || public.ns_plain(v_body));
    if found is not null then
        raise exception 'Not shared: this note looks like it contains %. Shared notes must be hypothetical; remove anything that could identify a real person.', found;
    end if;
    perform public.social_rate(me, 'notebook_share', 30, interval '1 hour', 'shares');
    insert into public.study_group_notes (group_id, owner_id, source_item_id, kind, title, body)
    values (p_group, me, p_item ->> 'source_item_id',
            coalesce(nullif(p_item ->> 'kind', ''), 'note'), left(v_title, 300), v_body)
    on conflict (group_id, owner_id, source_item_id) do update
        set title = excluded.title, body = excluded.body, updated_at = now(), status = 'open'
    returning id into note;
    return note;
end $$;

create or replace function public.group_notes_list(p_group uuid)
returns setof jsonb
language plpgsql stable security definer set search_path = ''
as $$
declare
    me uuid := public.ex_uid();
    staff boolean;
begin
    if public.sg_role(p_group, me) is null then raise exception 'That study group is not available.'; end if;
    staff := public.sg_is_staff(p_group, me);
    return query
    select jsonb_build_object('id', n.id, 'title', n.title, 'kind', n.kind, 'status', n.status,
                              'owner', public.sg_person(p_group, n.owner_id, me),
                              'is_mine', n.owner_id = me,
                              'created_at', n.created_at, 'updated_at', n.updated_at)
    from public.study_group_notes n
    where n.group_id = p_group and (n.status = 'open' or staff or n.owner_id = me)
    order by n.updated_at desc;
end $$;

create or replace function public.group_note_get(p_note uuid)
returns jsonb
language plpgsql stable security definer set search_path = ''
as $$
declare
    me uuid := public.ex_uid();
    n public.study_group_notes;
begin
    select * into n from public.study_group_notes where id = p_note;
    if n.id is null or public.sg_role(n.group_id, me) is null
       or (n.status <> 'open' and n.owner_id <> me and not public.sg_is_staff(n.group_id, me)) then
        raise exception 'That note is not available.';
    end if;
    return jsonb_build_object('id', n.id, 'title', n.title, 'kind', n.kind, 'body', n.body,
                              'owner', public.sg_person(n.group_id, n.owner_id, me),
                              'group_id', n.group_id, 'updated_at', n.updated_at);
end $$;

-- Take a note off the shelf: its owner, or the group's owner / moderators.
create or replace function public.group_note_remove(p_note uuid)
returns void
language plpgsql security definer set search_path = ''
as $$
declare
    me uuid := public.ex_uid();
    n public.study_group_notes;
begin
    select * into n from public.study_group_notes where id = p_note;
    if n.id is null then return; end if;
    if n.owner_id <> me and not public.sg_is_staff(n.group_id, me) then
        raise exception 'You can''t remove this note.';
    end if;
    delete from public.study_group_notes where id = p_note;
end $$;


-- ---------------------------------------------------------------------
-- 6. Reports and moderation
-- ---------------------------------------------------------------------
create or replace function public.group_report(p_group uuid, p_kind text, p_id text,
                                               p_reason text, p_note text)
returns void
language plpgsql security definer set search_path = ''
as $$
declare me uuid := public.ex_uid();
begin
    if public.sg_role(p_group, me) is null then raise exception 'That is not available.'; end if;
    if not ((p_kind = 'message' and exists (select 1 from public.study_group_messages
                                            where id::text = p_id and group_id = p_group))
         or (p_kind = 'note' and exists (select 1 from public.study_group_notes
                                         where id::text = p_id and group_id = p_group))) then
        raise exception 'That is not available.';
    end if;
    perform public.social_rate(me, 'group_report', 10, interval '1 hour', 'reports');
    insert into public.study_group_reports (reporter_id, group_id, target_kind, target_id, reason, note)
    values (me, p_group, p_kind, p_id, p_reason, left(coalesce(p_note, ''), 500))
    on conflict (reporter_id, target_kind, target_id) do update
        set reason = excluded.reason, note = excluded.note, status = 'open', created_at = now();
end $$;

-- p_action: hide | unhide | dismiss. The group's owner and moderators may
-- act on anything in their group; app educators and admins only on
-- content that has an open report (they can't browse private groups).
create or replace function public.group_moderate(p_group uuid, p_kind text, p_id text, p_action text)
returns void
language plpgsql security definer set search_path = ''
as $$
declare
    me uuid := public.ex_uid();
    group_staff boolean := public.sg_is_staff(p_group, me);
    app_mod boolean := public.ex_is_mod(me);
    reported boolean;
    target_author uuid;
begin
    reported := exists (select 1 from public.study_group_reports where group_id = p_group
                        and target_kind = p_kind and target_id = p_id and status = 'open');
    if not group_staff and not (app_mod and reported) then
        raise exception 'You can''t moderate this.';
    end if;
    if p_action not in ('hide', 'unhide', 'dismiss') then raise exception 'Unknown action.'; end if;
    if p_action <> 'dismiss' then
        if p_kind = 'message' then
            update public.study_group_messages
            set status = case when p_action = 'hide' then 'hidden' else 'open' end,
                hidden_by = case when p_action = 'hide' then me end,
                hidden_at = case when p_action = 'hide' then now() end
            where id::text = p_id and group_id = p_group
            returning author_id into target_author;
        elsif p_kind = 'note' then
            update public.study_group_notes
            set status = case when p_action = 'hide' then 'hidden' else 'open' end
            where id::text = p_id and group_id = p_group
            returning owner_id into target_author;
        else
            raise exception 'Unknown item.';
        end if;
        if target_author is null then raise exception 'That is not available.'; end if;
    end if;
    update public.study_group_reports
    set status = case when p_action = 'dismiss' then 'dismissed' else 'resolved' end,
        handled_by = me, handled_at = now()
    where group_id = p_group and target_kind = p_kind and target_id = p_id and status = 'open';
    if app_mod and not group_staff then
        perform public.ad_log('group_' || p_action, 'group_' || p_kind, p_id,
            (select name from public.study_groups where id = p_group),
            jsonb_build_object('group_id', p_group));
    end if;
end $$;

-- For app educators and admins: open reports, with just the reported item.
create or replace function public.group_report_queue()
returns setof jsonb
language plpgsql stable security definer set search_path = ''
as $$
declare me uuid := public.ex_uid();
begin
    if not public.ex_is_mod(me) then raise exception 'Only educators and admins can moderate.'; end if;
    return query
    select jsonb_build_object(
        'group_id', r.group_id, 'group_name', g.name, 'target_kind', r.target_kind,
        'target_id', r.target_id, 'reports', count(*), 'reasons', jsonb_agg(distinct r.reason),
        'notes', jsonb_agg(r.note) filter (where r.note <> ''), 'first_reported', min(r.created_at),
        'excerpt', public.ex_short(coalesce(
            (select m.body from public.study_group_messages m where r.target_kind = 'message'
                                                              and m.id::text = r.target_id),
            (select n.title || ': ' || public.ns_plain(n.body) from public.study_group_notes n
              where r.target_kind = 'note' and n.id::text = r.target_id), ''), 300),
        'author', public.fr_person(coalesce(
            (select m.author_id from public.study_group_messages m where r.target_kind = 'message'
                                                                   and m.id::text = r.target_id),
            (select n.owner_id from public.study_group_notes n where r.target_kind = 'note'
                                                              and n.id::text = r.target_id)), me))
    from public.study_group_reports r join public.study_groups g on g.id = r.group_id
    where r.status = 'open'
    group by r.group_id, g.name, r.target_kind, r.target_id
    order by count(*) desc, min(r.created_at);
end $$;


-- ---------------------------------------------------------------------
-- 7. Account deletion (called through social_purge_user, migration 040)
-- ---------------------------------------------------------------------
create or replace function public.group_purge_user(p_user uuid)
returns jsonb
language plpgsql security definer set search_path = ''
as $$
declare
    g uuid;
    transferred integer := 0;
    deleted integer := 0;
    outcome text;
    messages integer;
begin
    for g in select id from public.study_groups where owner_id = p_user loop
        outcome := public.sg_handover(g, p_user);
        if outcome = 'deleted' then deleted := deleted + 1; else transferred := transferred + 1; end if;
    end loop;
    delete from public.study_group_messages where author_id = p_user;
    get diagnostics messages = row_count;
    delete from public.study_group_notes where owner_id = p_user;
    delete from public.study_group_members where user_id = p_user;
    delete from public.study_group_invites where invitee_id = p_user or created_by = p_user;
    delete from public.study_group_reports where reporter_id = p_user;
    return jsonb_build_object('transferred', transferred, 'deleted', deleted, 'messages', messages);
end $$;


-- ---------------------------------------------------------------------
-- 8. Who may call what
-- ---------------------------------------------------------------------
do $$
declare fn text;
begin
    foreach fn in array array[
        'public.sg_role(uuid, uuid)', 'public.sg_is_staff(uuid, uuid)',
        'public.sg_person(uuid, uuid, uuid)', 'public.sg_hash(text)',
        'public.sg_add_member(uuid, uuid, text)', 'public.sg_row(public.study_groups, uuid)',
        'public.sg_handover(uuid, uuid)', 'public.sg_owner_gone()',
        'public.sg_block_revokes_invites()',
        'public.sg_message_row(public.study_group_messages, uuid, boolean)',
        'public.group_purge_user(uuid)'] loop
        execute format('revoke execute on function %s from public, anon, authenticated', fn);
    end loop;
    foreach fn in array array[
        'public.group_create(text, text, text, text, text)',
        'public.group_browse_public(text, text, text, integer, integer)',
        'public.group_my_list()', 'public.group_get(uuid)', 'public.group_join_public(uuid)',
        'public.group_join_with_token(text)', 'public.group_invite_link_create(uuid, integer)',
        'public.group_invite_link_revoke(uuid)', 'public.group_invite_friend(uuid, uuid)',
        'public.group_my_invites()', 'public.group_invite_respond(uuid, boolean)',
        'public.group_leave(uuid)', 'public.group_set_role(uuid, uuid, text)',
        'public.group_remove_member(uuid, uuid)', 'public.group_set_muted(uuid, boolean)',
        'public.group_delete(uuid)', 'public.group_send_message(uuid, text)',
        'public.group_messages_after(uuid, bigint, integer)',
        'public.group_share_note(uuid, jsonb)', 'public.group_notes_list(uuid)',
        'public.group_note_get(uuid)', 'public.group_note_remove(uuid)',
        'public.group_report(uuid, text, text, text, text)',
        'public.group_moderate(uuid, text, text, text)', 'public.group_report_queue()'] loop
        execute format('revoke execute on function %s from public, anon', fn);
        execute format('grant execute on function %s to authenticated', fn);
    end loop;
end $$;
grant execute on function public.group_purge_user(uuid) to service_role;

commit;

notify pgrst, 'reload schema';

-- =====================================================================
-- Check: select to_regprocedure('public.group_messages_after(uuid, bigint, integer)') is not null;
-- =====================================================================
