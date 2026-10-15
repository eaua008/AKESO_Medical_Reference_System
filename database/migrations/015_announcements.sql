-- =====================================================================
-- 015: announcements from the Akeso admins
-- ---------------------------------------------------------------------
-- An admin writes an announcement (Admin > Announcements). Everyone it is
-- meant for (everyone, students only or educators only) gets it as a
-- pop-up on the dashboard at their next sign-in. Once they close it, it
-- does not pop up again for that account, but it stays listed on the
-- dashboard until it ends.
--
--   announcements              what was announced, to whom, from / until
--   announcement_dismissals    who has already closed which one
--
-- Neither table can be read or written directly by the app: everything
-- goes through the functions below, which decide what each person may
-- see (row-level security on, and no policies at all).
--
--   my_announcements()            the signed-in user's live announcements
--   dismiss_announcement(id)      "Got it"
--   admin_list_announcements()    every announcement, with how many closed it
--   admin_save_announcement(p)    create or edit (admins only)
--   admin_end_announcement(id)    stop showing it now (admins only)
--
-- Run once in the Supabase SQL Editor, after 004. Safe to run again.
-- =====================================================================

begin;

create table if not exists public.announcements (
    id          uuid primary key default gen_random_uuid(),
    title       text not null check (char_length(btrim(title)) between 1 and 120),
    body        text not null check (char_length(btrim(body)) between 1 and 4000),
    level       text not null default 'info'
                check (level in ('info', 'important', 'critical')),
    audience    text not null default 'everyone'
                check (audience in ('everyone', 'student', 'educator')),
    link_url    text check (link_url is null or link_url ~ '^https?://[^\s]+$'),
    link_label  text check (link_label is null or char_length(link_label) <= 40),
    starts_at   timestamptz not null default now(),
    ends_at     timestamptz,
    ended_at    timestamptz,                    -- ended early by an admin
    created_by  uuid references auth.users (id) on delete set null,
    created_at  timestamptz not null default now(),
    updated_at  timestamptz not null default now(),
    check (ends_at is null or ends_at > starts_at)
);

create table if not exists public.announcement_dismissals (
    announcement_id uuid not null references public.announcements (id) on delete cascade,
    user_id         uuid not null references auth.users (id) on delete cascade,
    dismissed_at    timestamptz not null default now(),
    primary key (announcement_id, user_id)
);

create index if not exists announcements_live_idx
    on public.announcements (starts_at desc) where ended_at is null;
create index if not exists announcement_dismissals_user_idx
    on public.announcement_dismissals (user_id);

alter table public.announcements enable row level security;
alter table public.announcement_dismissals enable row level security;
revoke all on public.announcements from anon, authenticated;
revoke all on public.announcement_dismissals from anon, authenticated;


-- ---------------------------------------------------------------------
-- What one row looks like to the app.
-- ---------------------------------------------------------------------
create or replace function public.an_row(a public.announcements)
returns jsonb
language sql stable security definer set search_path = ''
as $$
    select jsonb_build_object(
        'id', a.id, 'title', a.title, 'body', a.body, 'level', a.level,
        'audience', a.audience, 'link_url', a.link_url, 'link_label', a.link_label,
        'starts_at', a.starts_at, 'ends_at', a.ends_at, 'ended_at', a.ended_at,
        'created_at', a.created_at, 'updated_at', a.updated_at);
$$;


-- ---------------------------------------------------------------------
-- Everyone (signed in)
-- ---------------------------------------------------------------------
create or replace function public.my_announcements()
returns jsonb
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
        select jsonb_agg(public.an_row(a) || jsonb_build_object(
                   'dismissed', d.user_id is not null)
               order by case a.level when 'critical' then 0 when 'important' then 1 else 2 end,
                        a.starts_at desc)
        from public.announcements a
        left join public.announcement_dismissals d
               on d.announcement_id = a.id and d.user_id = uid
        where a.ended_at is null
          and a.starts_at <= now()
          and (a.ends_at is null or a.ends_at > now())
          and (a.audience = 'everyone' or a.audience = v_role)
    ), '[]'::jsonb);
end $$;

create or replace function public.dismiss_announcement(p_id uuid)
returns void
language plpgsql security definer set search_path = ''
as $$
declare uid uuid := auth.uid();
begin
    if uid is null then raise exception 'Not signed in.'; end if;
    if not exists (select 1 from public.announcements where id = p_id) then
        return;                                   -- deleted meanwhile: nothing to do
    end if;
    insert into public.announcement_dismissals (announcement_id, user_id)
    values (p_id, uid)
    on conflict do nothing;
end $$;


-- ---------------------------------------------------------------------
-- Admins (ad_me() and ad_log() are from migration 004)
-- ---------------------------------------------------------------------
create or replace function public.admin_list_announcements()
returns jsonb
language plpgsql stable security definer set search_path = ''
as $$
begin
    perform public.ad_me();
    return coalesce((
        select jsonb_agg(public.an_row(a) || jsonb_build_object(
                   'author', coalesce(nullif(p.display_name, ''), u.email, 'Deleted account'),
                   'dismiss_count', (select count(*) from public.announcement_dismissals d
                                     where d.announcement_id = a.id))
               order by a.created_at desc)
        from public.announcements a
        left join auth.users u on u.id = a.created_by
        left join public.profiles p on p.id = a.created_by
    ), '[]'::jsonb);
end $$;

create or replace function public.admin_save_announcement(p jsonb)
returns uuid
language plpgsql security definer set search_path = ''
as $$
declare
    me uuid := public.ad_me();
    v_id uuid := nullif(p->>'id', '')::uuid;
    v_title text := btrim(coalesce(p->>'title', ''));
    v_body text := btrim(coalesce(p->>'body', ''));
    v_level text := coalesce(nullif(p->>'level', ''), 'info');
    v_audience text := coalesce(nullif(p->>'audience', ''), 'everyone');
    v_url text := nullif(btrim(coalesce(p->>'link_url', '')), '');
    v_label text := nullif(btrim(coalesce(p->>'link_label', '')), '');
    v_starts timestamptz := coalesce(nullif(p->>'starts_at', '')::timestamptz, now());
    v_ends timestamptz := nullif(p->>'ends_at', '')::timestamptz;
    v_reshow boolean := coalesce((p->>'reshow')::boolean, false);
begin
    if char_length(v_title) not between 1 and 120 then
        raise exception 'The title must be 1 to 120 characters.';
    end if;
    if char_length(v_body) not between 1 and 4000 then
        raise exception 'The message must be 1 to 4000 characters.';
    end if;
    if v_level not in ('info', 'important', 'critical') then
        raise exception 'Unknown importance level.';
    end if;
    if v_audience not in ('everyone', 'student', 'educator') then
        raise exception 'Unknown audience.';
    end if;
    if v_url is not null and v_url !~ '^https?://[^\s]+$' then
        raise exception 'The link must start with http:// or https://.';
    end if;
    if v_label is not null and v_url is null then
        v_label := null;                          -- a button with nowhere to go
    end if;
    if v_ends is not null and v_ends <= v_starts then
        raise exception 'The end date must be after the start.';
    end if;

    if v_id is null then
        insert into public.announcements
            (title, body, level, audience, link_url, link_label, starts_at, ends_at,
             created_by)
        values (v_title, v_body, v_level, v_audience, v_url, left(v_label, 40), v_starts,
                v_ends, me)
        returning id into v_id;
        -- The author has read it already: no pop-up for them.
        insert into public.announcement_dismissals (announcement_id, user_id)
        values (v_id, me) on conflict do nothing;
        perform public.ad_log('announce', 'announcement', v_id::text, v_title,
                              jsonb_build_object('audience', v_audience, 'level', v_level));
    else
        update public.announcements
        set title = v_title, body = v_body, level = v_level, audience = v_audience,
            link_url = v_url, link_label = left(v_label, 40), starts_at = v_starts,
            ends_at = v_ends, updated_at = now()
        where id = v_id;
        if not found then raise exception 'That announcement no longer exists.'; end if;
        if v_reshow then
            -- Pop up again for everyone who already closed it (except the editor).
            delete from public.announcement_dismissals
            where announcement_id = v_id and user_id <> me;
        end if;
        perform public.ad_log('announce_edit', 'announcement', v_id::text, v_title,
                              jsonb_build_object('reshow', v_reshow));
    end if;
    return v_id;
end $$;

create or replace function public.admin_end_announcement(p_id uuid)
returns void
language plpgsql security definer set search_path = ''
as $$
declare v_title text;
begin
    perform public.ad_me();
    update public.announcements set ended_at = now(), updated_at = now()
    where id = p_id and ended_at is null
    returning title into v_title;
    if v_title is not null then
        perform public.ad_log('announce_end', 'announcement', p_id::text, v_title);
    end if;
end $$;


-- ---------------------------------------------------------------------
-- Who may call what
-- ---------------------------------------------------------------------
revoke execute on function public.an_row(public.announcements) from public, anon, authenticated;
do $$
declare fn text;
begin
    foreach fn in array array[
        'public.my_announcements()', 'public.dismiss_announcement(uuid)',
        'public.admin_list_announcements()', 'public.admin_save_announcement(jsonb)',
        'public.admin_end_announcement(uuid)'] loop
        execute format('revoke execute on function %s from public, anon', fn);
        execute format('grant execute on function %s to authenticated', fn);
    end loop;
end $$;

commit;

-- Check: both should say true.
select to_regclass('public.announcements') is not null as announcements_ready,
       to_regprocedure('public.my_announcements()') is not null as functions_ready;
