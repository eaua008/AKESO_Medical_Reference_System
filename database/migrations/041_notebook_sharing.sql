-- =====================================================================
-- Akeso migration 041: share a Study Notebook note with friends
-- =====================================================================
-- Run AFTER 040_friends.sql. Safe to run again.
--
-- A share is a READ-ONLY SNAPSHOT of one note: its title and text at the
-- moment it was shared (or last "Update shared copy"). The owner's note
-- keeps syncing as before (migration 011 is untouched: notebook_items,
-- its row-level security and the notebook-images bucket stay owner-only).
-- Recipients read the snapshot and can save their own copy, which then
-- becomes a normal note in THEIR notebook.
--
--   notebook_shares             one snapshot per shared note
--   notebook_share_recipients   who it is shared with; revoked_at when the
--                               owner unshares, or when the two stop being
--                               friends or one blocks the other
--
-- Rules, enforced here (a modified app can't skip them):
--   * only accepted friends can receive, and only while still friends;
--   * text only: pictures are removed from the snapshot ("image not
--     shared"), because recipients can't read the owner's picture folder;
--   * the same patient-data check as Clinical Exchange (ex_phi_check);
--   * at most 30 shares an hour.
-- =====================================================================

begin;

-- ---------------------------------------------------------------------
-- 1. Tables
-- ---------------------------------------------------------------------
create table if not exists public.notebook_shares (
    id              uuid primary key default gen_random_uuid(),
    owner_id        uuid not null references auth.users (id) on delete cascade,
    source_item_id  text not null check (char_length(source_item_id) between 1 and 64),
    kind            text not null default 'note'
                    check (kind in ('note', 'symptom_case', 'interaction_case')),
    title           text not null check (char_length(btrim(title)) between 1 and 300),
    body            text not null default '' check (char_length(body) <= 200000),
    created_at      timestamptz not null default now(),
    updated_at      timestamptz not null default now(),
    unique (owner_id, source_item_id)
);

create table if not exists public.notebook_share_recipients (
    share_id      uuid not null references public.notebook_shares (id) on delete cascade,
    recipient_id  uuid not null references auth.users (id) on delete cascade,
    created_at    timestamptz not null default now(),
    opened_at     timestamptz,
    revoked_at    timestamptz,
    primary key (share_id, recipient_id)
);
create index if not exists notebook_share_recipients_to_idx
    on public.notebook_share_recipients (recipient_id) where revoked_at is null;

do $$
declare t text;
begin
    foreach t in array array['notebook_shares', 'notebook_share_recipients'] loop
        execute format('alter table public.%I enable row level security', t);
        execute format('revoke all on public.%I from anon, authenticated', t);
    end loop;
end $$;


-- ---------------------------------------------------------------------
-- 2. Helpers (not callable from the app)
-- ---------------------------------------------------------------------

-- The snapshot as stored: pictures replaced, nothing that could load
-- from elsewhere. The app does the same before sending; this is the
-- safety net.
create or replace function public.ns_clean_body(p_body text)
returns text
language sql immutable set search_path = ''
as $$
    select left(regexp_replace(
                regexp_replace(coalesce(p_body, ''), '<img[^>]*>', '[image not shared]', 'gi'),
                '<(script|iframe|object|embed)[^>]*>.*?</\1>', '', 'gis'), 200000);
$$;

-- Words only, for the patient-data check.
create or replace function public.ns_plain(p_body text)
returns text
language sql immutable set search_path = ''
as $$
    select regexp_replace(regexp_replace(coalesce(p_body, ''), '<[^>]+>', ' ', 'g'),
                          '&nbsp;|&#160;', ' ', 'g');
$$;

-- May p_viewer read this share right now?
create or replace function public.ns_can_read(p_share uuid, p_viewer uuid)
returns boolean
language sql stable security definer set search_path = ''
as $$
    select exists (
        select 1 from public.notebook_shares s
        where s.id = p_share
          and (s.owner_id = p_viewer
               or (exists (select 1 from public.notebook_share_recipients r
                           where r.share_id = s.id and r.recipient_id = p_viewer
                             and r.revoked_at is null)
                   and public.fr_are_friends(s.owner_id, p_viewer)
                   and public.social_active(s.owner_id))));
$$;

create or replace function public.ns_row(s public.notebook_shares, p_viewer uuid, p_body boolean)
returns jsonb
language sql stable security definer set search_path = ''
as $$
    select jsonb_build_object(
        'id', s.id, 'kind', s.kind, 'title', s.title,
        'source_item_id', case when s.owner_id = p_viewer then s.source_item_id end,
        'owner', public.fr_person(s.owner_id, p_viewer),
        'is_mine', s.owner_id = p_viewer,
        'created_at', s.created_at, 'updated_at', s.updated_at,
        'opened', (select r.opened_at is not null from public.notebook_share_recipients r
                   where r.share_id = s.id and r.recipient_id = p_viewer))
        || case when p_body then jsonb_build_object('body', s.body) else '{}'::jsonb end;
$$;

-- When two people stop being friends (unfriend, block, a declined request
-- that was never accepted is not affected), their shares to each other end.
create or replace function public.ns_friendship_ended()
returns trigger
language plpgsql security definer set search_path = ''
as $$
declare x uuid; y uuid;
begin
    x := old.user_a; y := old.user_b;
    if tg_op = 'UPDATE' and new.status = 'accepted' then return new; end if;
    update public.notebook_share_recipients r set revoked_at = now()
    from public.notebook_shares s
    where s.id = r.share_id and r.revoked_at is null
      and ((s.owner_id = x and r.recipient_id = y) or (s.owner_id = y and r.recipient_id = x));
    return coalesce(new, old);
end $$;

drop trigger if exists friendships_end_shares on public.friendships;
create trigger friendships_end_shares
    after update of status or delete on public.friendships
    for each row execute function public.ns_friendship_ended();


-- ---------------------------------------------------------------------
-- 3. Sharing (owner)
-- ---------------------------------------------------------------------

-- p_item: {source_item_id, kind, title, body}. p_recipients: friends' ids.
-- Shares (or re-shares) the note's current text with those friends.
-- Returns {share_id, shared_with}.
create or replace function public.notebook_share_create(p_item jsonb, p_recipients uuid[])
returns jsonb
language plpgsql security definer set search_path = ''
as $$
declare
    me uuid := public.ex_uid();
    v_title text := btrim(coalesce(p_item ->> 'title', ''));
    v_body text := public.ns_clean_body(p_item ->> 'body');
    v_kind text := coalesce(nullif(p_item ->> 'kind', ''), 'note');
    v_source text := btrim(coalesce(p_item ->> 'source_item_id', ''));
    found text;
    share uuid;
    who uuid;
    added integer := 0;
begin
    if v_source = '' or v_title = '' then raise exception 'That note has no title.'; end if;
    if coalesce(cardinality(p_recipients), 0) = 0 then
        raise exception 'Choose at least one friend to share with.';
    end if;
    if cardinality(p_recipients) > 50 then
        raise exception 'Share with at most 50 friends at a time.';
    end if;
    found := public.ex_phi_check(v_title || ' ' || public.ns_plain(v_body));
    if found is not null then
        raise exception 'Not shared: this note looks like it contains %. Shared notes must be hypothetical; remove anything that could identify a real person.', found;
    end if;
    foreach who in array p_recipients loop
        if who = me or not public.fr_are_friends(me, who) or not public.social_active(who) then
            raise exception 'You can only share notes with your friends.';
        end if;
    end loop;
    perform public.social_rate(me, 'notebook_share', 30, interval '1 hour', 'shares');

    insert into public.notebook_shares (owner_id, source_item_id, kind, title, body)
    values (me, v_source, v_kind, left(v_title, 300), v_body)
    on conflict (owner_id, source_item_id) do update
        set title = excluded.title, body = excluded.body, kind = excluded.kind,
            updated_at = now()
    returning id into share;

    foreach who in array p_recipients loop
        if not exists (select 1 from public.notebook_share_recipients
                       where share_id = share and recipient_id = who and revoked_at is null) then
            insert into public.notebook_share_recipients (share_id, recipient_id)
            values (share, who)
            on conflict (share_id, recipient_id) do update
                set revoked_at = null, opened_at = null, created_at = now();
            perform public.social_notify(who, 'notebook_shared', 'notebook_share', share::text,
                public.social_name(me) || ' shared a note with you: “'
                || public.ex_short(v_title) || '”');
            added := added + 1;
        end if;
    end loop;
    return jsonb_build_object('share_id', share, 'shared_with', added);
end $$;

-- Who has this note of mine (by my notebook item id), for "Manage sharing".
create or replace function public.notebook_share_manage(p_item_id text)
returns jsonb
language plpgsql stable security definer set search_path = ''
as $$
declare
    me uuid := public.ex_uid();
    s public.notebook_shares;
begin
    select * into s from public.notebook_shares where owner_id = me and source_item_id = p_item_id;
    if s.id is null then return null; end if;
    return public.ns_row(s, me, false) || jsonb_build_object('recipients', coalesce((
        select jsonb_agg(public.fr_person(r.recipient_id, me)
                         || jsonb_build_object('shared_at', r.created_at,
                                               'opened', r.opened_at is not null)
                         order by r.created_at)
        from public.notebook_share_recipients r
        where r.share_id = s.id and r.revoked_at is null), '[]'::jsonb));
end $$;

-- My notes that are currently shared with someone (for the "Shared" badge).
create or replace function public.notebook_share_my_items()
returns setof text
language sql stable security definer set search_path = ''
as $$
    select s.source_item_id from public.notebook_shares s
    where s.owner_id = public.ex_uid()
      and exists (select 1 from public.notebook_share_recipients r
                  where r.share_id = s.id and r.revoked_at is null);
$$;

-- "Update shared copy": replace the snapshot with the note as it is now.
create or replace function public.notebook_share_update_snapshot(p_id uuid, p_title text, p_body text)
returns void
language plpgsql security definer set search_path = ''
as $$
declare
    me uuid := public.ex_uid();
    v_body text := public.ns_clean_body(p_body);
    found text;
begin
    if not exists (select 1 from public.notebook_shares where id = p_id and owner_id = me) then
        raise exception 'That shared note is not available.';
    end if;
    if btrim(coalesce(p_title, '')) = '' then raise exception 'That note has no title.'; end if;
    found := public.ex_phi_check(p_title || ' ' || public.ns_plain(v_body));
    if found is not null then
        raise exception 'Not updated: this note looks like it contains %. Shared notes must be hypothetical; remove anything that could identify a real person.', found;
    end if;
    perform public.social_rate(me, 'notebook_share', 30, interval '1 hour', 'shares');
    update public.notebook_shares
    set title = left(btrim(p_title), 300), body = v_body, updated_at = now()
    where id = p_id;
end $$;

-- Unshare: one recipient, or everyone (p_recipient null). Copies they
-- already saved stay theirs; only the shared snapshot goes.
create or replace function public.notebook_share_revoke(p_id uuid, p_recipient uuid)
returns void
language plpgsql security definer set search_path = ''
as $$
declare me uuid := public.ex_uid();
begin
    if not exists (select 1 from public.notebook_shares where id = p_id and owner_id = me) then
        raise exception 'That shared note is not available.';
    end if;
    update public.notebook_share_recipients set revoked_at = now()
    where share_id = p_id and revoked_at is null
      and (p_recipient is null or recipient_id = p_recipient);
end $$;


-- ---------------------------------------------------------------------
-- 4. Receiving
-- ---------------------------------------------------------------------
create or replace function public.notebook_share_list_received()
returns setof jsonb
language plpgsql stable security definer set search_path = ''
as $$
declare me uuid := public.ex_uid();
begin
    return query
    select public.ns_row(s, me, false) || jsonb_build_object('shared_at', r.created_at)
    from public.notebook_share_recipients r
    join public.notebook_shares s on s.id = r.share_id
    where r.recipient_id = me and r.revoked_at is null
      and public.fr_are_friends(s.owner_id, me) and public.social_active(s.owner_id)
    order by greatest(s.updated_at, r.created_at) desc;
end $$;

create or replace function public.notebook_share_get(p_id uuid)
returns jsonb
language plpgsql security definer set search_path = ''
as $$
declare
    me uuid := public.ex_uid();
    s public.notebook_shares;
begin
    if not public.ns_can_read(p_id, me) then
        raise exception 'This shared note is no longer available.';
    end if;
    select * into s from public.notebook_shares where id = p_id;
    update public.notebook_share_recipients set opened_at = coalesce(opened_at, now())
    where share_id = p_id and recipient_id = me;
    return public.ns_row(s, me, true);
end $$;

-- "Save a copy to my notebook": the snapshot, for the app to save as a new
-- local note (which then syncs like any other). Refused once access ends.
create or replace function public.notebook_share_save_copy(p_id uuid)
returns jsonb
language plpgsql stable security definer set search_path = ''
as $$
declare
    me uuid := public.ex_uid();
    s public.notebook_shares;
begin
    if not public.ns_can_read(p_id, me) then
        raise exception 'This shared note is no longer available.';
    end if;
    select * into s from public.notebook_shares where id = p_id;
    return public.ns_row(s, me, true);
end $$;


-- ---------------------------------------------------------------------
-- 5. Account deletion (called through social_purge_user, migration 040)
-- ---------------------------------------------------------------------
create or replace function public.notebook_share_purge_user(p_user uuid)
returns integer
language plpgsql security definer set search_path = ''
as $$
declare n integer := 0; m integer := 0;
begin
    delete from public.notebook_shares where owner_id = p_user;          -- and their recipients
    get diagnostics n = row_count;
    delete from public.notebook_share_recipients where recipient_id = p_user;
    get diagnostics m = row_count;
    return n + m;
end $$;


-- ---------------------------------------------------------------------
-- 6. Who may call what
-- ---------------------------------------------------------------------
do $$
declare fn text;
begin
    foreach fn in array array[
        'public.ns_clean_body(text)', 'public.ns_plain(text)',
        'public.ns_can_read(uuid, uuid)',
        'public.ns_row(public.notebook_shares, uuid, boolean)',
        'public.ns_friendship_ended()', 'public.notebook_share_purge_user(uuid)'] loop
        execute format('revoke execute on function %s from public, anon, authenticated', fn);
    end loop;
    foreach fn in array array[
        'public.notebook_share_create(jsonb, uuid[])', 'public.notebook_share_manage(text)',
        'public.notebook_share_my_items()',
        'public.notebook_share_update_snapshot(uuid, text, text)',
        'public.notebook_share_revoke(uuid, uuid)', 'public.notebook_share_list_received()',
        'public.notebook_share_get(uuid)', 'public.notebook_share_save_copy(uuid)'] loop
        execute format('revoke execute on function %s from public, anon', fn);
        execute format('grant execute on function %s to authenticated', fn);
    end loop;
end $$;
grant execute on function public.notebook_share_purge_user(uuid) to service_role;

commit;

notify pgrst, 'reload schema';

-- =====================================================================
-- Check: select to_regprocedure('public.notebook_share_get(uuid)') is not null;  -- true
-- =====================================================================
