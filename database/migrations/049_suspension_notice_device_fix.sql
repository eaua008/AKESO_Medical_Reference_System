-- =====================================================================
-- Akeso migration 049: the suspension reason, found by computer
-- =====================================================================
-- Run AFTER 048. Safe to run again. Self-contained: it also creates what 048
-- creates if that was run in an older form.
--
-- Fix: when two accounts have signed in on the same computer, the lookup took
-- the account used most recently there, which might not be the suspended one.
-- It now takes the most recently used SUSPENDED account on that computer, so
-- a suspended person sees their reason even on a shared computer.
-- =====================================================================

begin;

create table if not exists public.suspension_notice_log (
    id        bigint generated always as identity primary key,
    login_key text not null,
    at        timestamptz not null default now()
);
create index if not exists suspension_notice_log_key_idx
    on public.suspension_notice_log (login_key, at desc);
alter table public.suspension_notice_log enable row level security;
revoke all on public.suspension_notice_log from anon, authenticated;

create or replace function public.suspension_notice_device(p_device_key text)
returns jsonb
language plpgsql security definer set search_path = ''
as $$
declare
    k text := 'dev:' || md5(coalesce(p_device_key, ''));
    u record;
begin
    if p_device_key is null or char_length(p_device_key) not between 16 and 64 then
        return null;
    end if;
    if (select count(*) from public.suspension_notice_log
        where login_key = k and at > now() - interval '1 hour') >= 20 then
        return null;
    end if;
    insert into public.suspension_notice_log (login_key) values (k);
    select pr.suspended_reason into u
    from public.user_devices d
    join public.profiles pr on pr.id = d.user_id
    where d.device_key = p_device_key and pr.suspended_at is not null
    order by d.last_seen desc
    limit 1;
    if not found then
        return null;
    end if;
    return jsonb_build_object('reason', coalesce(u.suspended_reason, ''));
end $$;

revoke execute on function public.suspension_notice_device(text) from public;
grant execute on function public.suspension_notice_device(text) to anon, authenticated;

commit;

notify pgrst, 'reload schema';
