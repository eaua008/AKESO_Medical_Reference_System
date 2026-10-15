-- =====================================================================
-- 016: delete notifications one at a time
-- ---------------------------------------------------------------------
-- The Notifications page gets a delete (trash) button on every row:
--
--   notif_delete(ids)          removes your own Clinical Exchange
--                              notifications (read or not)
--   hide_announcement(id)      takes an announcement off your
--                              Notifications page and dashboard (it
--                              also counts as read); others still see it
--   hide_read_announcements()  "Clear read" does the same for every
--                              announcement you have already opened
--
-- my_announcements() (migration 015) now leaves out the ones you hid.
-- Run once in the Supabase SQL Editor, after 015. Safe to run again.
-- =====================================================================

begin;

create or replace function public.notif_delete(p_ids bigint[])
returns void
language plpgsql security definer set search_path = ''
as $$
declare me uuid := public.ex_uid();
begin
    delete from public.notifications where user_id = me and id = any(coalesce(p_ids, '{}'));
end $$;

alter table public.announcement_dismissals
    add column if not exists hidden boolean not null default false;

create or replace function public.hide_announcement(p_id uuid)
returns void
language plpgsql security definer set search_path = ''
as $$
declare uid uuid := auth.uid();
begin
    if uid is null then raise exception 'Not signed in.'; end if;
    if not exists (select 1 from public.announcements where id = p_id) then return; end if;
    insert into public.announcement_dismissals (announcement_id, user_id, hidden)
    values (p_id, uid, true)
    on conflict (announcement_id, user_id) do update set hidden = true;
end $$;

create or replace function public.hide_read_announcements()
returns void
language plpgsql security definer set search_path = ''
as $$
declare uid uuid := auth.uid();
begin
    if uid is null then raise exception 'Not signed in.'; end if;
    update public.announcement_dismissals set hidden = true
    where user_id = uid and not hidden;
end $$;

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
          and not coalesce(d.hidden, false)
    ), '[]'::jsonb);
end $$;

do $$
declare fn text;
begin
    foreach fn in array array[
        'public.notif_delete(bigint[])', 'public.hide_announcement(uuid)',
        'public.hide_read_announcements()', 'public.my_announcements()'] loop
        execute format('revoke execute on function %s from public, anon', fn);
        execute format('grant execute on function %s to authenticated', fn);
    end loop;
end $$;

commit;

-- Check: should say true.
select to_regprocedure('public.notif_delete(bigint[])') is not null as ready;
