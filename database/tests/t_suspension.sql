-- LOCAL TEST DATABASE ONLY. Never run this on the real Supabase project: it creates
-- test users and a 't' schema.

-- Migration 048: the reason a suspended person is shown
delete from t.results where suite = 'suspension';
do $$
declare
    x text := substr(md5(random()::text), 1, 5);
    u uuid := t.mk_user('sus' || x);
    e text := 'sus' || x || '@test.local';
    r jsonb;
begin
    update auth.users set encrypted_password = extensions.crypt('Correct-horse-1', extensions.gen_salt('bf')) where id = u;
    r := public.suspension_notice(e, 'Correct-horse-1');
    perform t.ok('suspension', r is null, 'an account that is not suspended gets nothing', r::text);
    update public.profiles set suspended_at = now(), suspended_reason = 'Shared exam answers in a group' where id = u;
    r := public.suspension_notice('  ' || upper(e) || ' ', 'Correct-horse-1');
    perform t.ok('suspension', r ->> 'reason' = 'Shared exam answers in a group', 'right password: the reason comes back', r::text);
    r := public.suspension_notice(e, 'wrong-password');
    perform t.ok('suspension', r is null, 'wrong password gets nothing', r::text);
    r := public.suspension_notice('nobody' || x || '@test.local', 'Correct-horse-1');
    perform t.ok('suspension', r is null, 'unknown email gets nothing', r::text);
    -- five tries an hour per email: the earlier ones above already used three for e
    perform public.suspension_notice(e, 'x1'); perform public.suspension_notice(e, 'x2');
    r := public.suspension_notice(e, 'Correct-horse-1');
    perform t.ok('suspension', r is null, 'after five tries an hour even the right password gets nothing', r::text);
    -- by this computer's key (Google sign-in has no password)
    insert into public.user_devices (user_id, device_key) values (u, 'devkey' || x || repeat('a', 20));
    r := public.suspension_notice_device('devkey' || x || repeat('a', 20));
    perform t.ok('suspension', r ->> 'reason' = 'Shared exam answers in a group', 'a registered computer gets the reason', r::text);
    r := public.suspension_notice_device('unknownkey' || x || repeat('b', 20));
    perform t.ok('suspension', r is null, 'an unknown computer key gets nothing', r::text);
    update public.profiles set suspended_at = null where id = u;
    r := public.suspension_notice_device('devkey' || x || repeat('a', 20));
    perform t.ok('suspension', r is null, 'a computer of an account that is not suspended gets nothing', r::text);
end $$;
select ok, label, case when not ok then detail end as detail from t.results where suite = 'suspension' order by id;
