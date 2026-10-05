-- =====================================================================
-- 014: suspension that Supabase Auth can read
-- ---------------------------------------------------------------------
-- admin_set_suspended() (migration 004) banned users with
-- banned_until = 'infinity'. Supabase Auth (GoTrue, written in Go) cannot
-- turn 'infinity' into a date, so a suspended user's sign-in failed with
--   sql: Scan error on column index 1, name "banned_until" ...
-- shown on the sign-in screen: no suspension pop-up, and database
-- internals on display. This switches to 31 Dec 2999 (still "forever")
-- and fixes anyone already suspended.
--
-- Run once in the Supabase SQL Editor. Safe to run again.
-- =====================================================================

create or replace function public.admin_set_suspended(p_user uuid, p_suspend boolean,
                                                      p_reason text default '')
returns void
language plpgsql security definer set search_path = ''
as $$
declare
    me uuid := public.ad_me();
    v_email text;
begin
    if p_user = me then raise exception 'You cannot suspend your own account.'; end if;
    select email into v_email from auth.users where id = p_user;
    if v_email is null then raise exception 'That account no longer exists.'; end if;
    if p_suspend and exists (select 1 from public.user_roles
                             where user_id = p_user and role = 'admin') then
        raise exception 'Change this admin''s role first, then suspend the account.';
    end if;

    insert into public.profiles (id) values (p_user) on conflict (id) do nothing;
    update public.profiles
    set suspended_at = case when p_suspend then now() else null end,
        suspended_reason = case when p_suspend then left(coalesce(btrim(p_reason), ''), 300)
                                else '' end
    where id = p_user;

    -- Also stop sign-in and end their sessions at the source. Supabase Auth
    -- refuses banned users ("User is banned") and they lose access within
    -- the hour (when their token expires). A far-future date, NOT
    -- 'infinity': Supabase Auth is written in Go, which cannot read
    -- 'infinity' and failed every sign-in with a raw SQL error instead. If a project does not allow these writes, the
    -- profile flag above still keeps them out of the app.
    begin
        update auth.users
        set banned_until = case when p_suspend then '2999-12-31 00:00:00+00'::timestamptz else null end
        where id = p_user;
        if p_suspend then
            delete from auth.sessions where user_id = p_user;
        end if;
    exception when insufficient_privilege or undefined_column then
        null;
    end;

    perform public.ad_log(case when p_suspend then 'suspend' else 'reactivate' end,
                          'user', p_user::text, v_email,
                          case when p_suspend and coalesce(btrim(p_reason), '') <> ''
                               then jsonb_build_object('reason', left(btrim(p_reason), 300))
                               else '{}'::jsonb end);
end $$;

-- Accounts suspended with the old value.
update auth.users
set banned_until = '2999-12-31 00:00:00+00'::timestamptz
where banned_until = 'infinity'::timestamptz;

-- Check: should return 0.
select count(*) as still_infinity
from auth.users
where banned_until = 'infinity'::timestamptz;
