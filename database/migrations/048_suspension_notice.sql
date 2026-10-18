-- =====================================================================
-- Akeso migration 048: show a suspended person the admin's reason
-- =====================================================================
-- Run AFTER 047. Safe to run again. Adds a function and a small log table.
--
-- Supabase Auth refuses to sign a suspended account in, so the app has no
-- session to read the reason with. suspension_notice() answers the one
-- question the sign-in screen has after Supabase said "banned":
--
--     "what reason did the admin write?"
--
-- and only when the caller also knows the account's password (checked
-- against the stored bcrypt hash), so it cannot be used to find out which
-- emails are suspended or what was written about them. A wrong password,
-- an account that is not suspended, or an unknown email all answer the
-- same: null. Five tries an hour per email, the wrong ones count too.
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

create or replace function public.suspension_notice(p_login text, p_password text)
returns jsonb
language plpgsql security definer set search_path = ''
as $$
declare
    k text := lower(btrim(coalesce(p_login, '')));
    u record;
begin
    if k = '' or coalesce(p_password, '') = '' or char_length(k) > 254 then
        return null;
    end if;
    delete from public.suspension_notice_log where at < now() - interval '1 day';
    if (select count(*) from public.suspension_notice_log
        where login_key = k and at > now() - interval '1 hour') >= 5 then
        return null;
    end if;
    insert into public.suspension_notice_log (login_key) values (k);

    select pr.suspended_at, pr.suspended_reason, au.encrypted_password
    into u
    from auth.users au
    join public.profiles pr on pr.id = au.id
    where lower(au.email) = k;

    if not found or u.suspended_at is null
       or u.encrypted_password is null
       or extensions.crypt(p_password, u.encrypted_password) <> u.encrypted_password then
        return null;
    end if;
    return jsonb_build_object('reason', coalesce(u.suspended_reason, ''));
end $$;

-- Google sign-in has no password to prove anything with. For that (and for a
-- remembered session) the app sends this computer's random device key: a 32-letter
-- secret kept in a file on the computer and registered to the account at its
-- earlier sign-ins. Nobody else has it, so it proves "this is that account's
-- computer". Newest sign-in on that computer wins.
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
    select pr.suspended_at, pr.suspended_reason into u
    from public.user_devices d
    join public.profiles pr on pr.id = d.user_id
    where d.device_key = p_device_key
    order by d.last_seen desc
    limit 1;
    if not found or u.suspended_at is null then
        return null;
    end if;
    return jsonb_build_object('reason', coalesce(u.suspended_reason, ''));
end $$;

revoke execute on function public.suspension_notice_device(text) from public;
grant execute on function public.suspension_notice_device(text) to anon, authenticated;

revoke execute on function public.suspension_notice(text, text) from public;
grant execute on function public.suspension_notice(text, text) to anon, authenticated;

commit;

notify pgrst, 'reload schema';
