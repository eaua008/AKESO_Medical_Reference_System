-- LOCAL TEST DATABASE ONLY. Never run this on the real Supabase project: it creates
-- test users and a 't' schema. See claude/friends-sharing-groups-design.md, Testing.

-- Changing the @handle (migration 043)
delete from t.results where suite = 'handles';
do $$
declare
    x text := substr(md5(random()::text), 1, 5);
    hana uuid := t.mk_user('hana' || x);
    ivo uuid := t.mk_user('ivo' || x);
    r text; j jsonb;
begin
    perform t.as_user(hana);
    perform t.ok('handles', public.handle_check('Bad Handle!') like 'Use 3 to 20%', 'format checked');
    perform t.ok('handles', public.handle_check('admin_x' || x) like '%reserved%', 'reserved word refused');
    perform t.ok('handles', public.handle_check('IVO' || x) = 'That handle is taken.', 'taken (any case) refused');
    perform t.ok('handles', public.handle_check('hana_new' || x) is null, 'free handle passes');
    j := public.handle_change_info();
    perform t.ok('handles', j ->> 'next_change_at' is null, 'first change allowed now');
    r := public.change_handle('@Hana_New' || x);
    perform t.ok('handles', r = 'hana_new' || x
                 and (select handle from public.profiles where id = hana) = r, 'handle changed, cleaned');
    perform t.ok('handles', exists (select 1 from public.security_events where user_id = hana
                 and kind = 'profile_updated' and detail ->> 'to' = r), 'change logged in security events');
    perform t.err('handles', 'select public.change_handle(''hana_again' || x || ''')',
                  'once every 30 days', 'second change within 30 days refused');
    perform t.ok('handles', public.handle_change_info() ->> 'next_change_at' is not null, 'next change date given');
    perform t.ok('handles', public.change_handle('hana_new' || x) = 'hana_new' || x, 'same handle is a no-op');
    -- the old handle is held for its owner
    perform t.as_user(ivo);
    perform t.ok('handles', public.handle_check('hana' || x) = 'That handle is taken.',
                 'released handle reserved for 30 days');
    update public.handle_history set changed_at = now() - interval '31 days' where user_id = hana;
    perform t.ok('handles', public.handle_check('hana' || x) is null, 'free again after 30 days');
    perform t.as_user(hana);
    perform t.ok('handles', public.handle_change_info() ->> 'next_change_at' is null, 'cooldown over after 30 days');
end $$;

-- direct writes still refused (009's lock stays)
set role authenticated;
do $$ begin
    begin
        perform set_config('request.jwt.claims', json_build_object('sub',
            (select id from public.profiles where handle like 'hana_new%' limit 1), 'role', 'authenticated')::text, false);
        update public.profiles set handle = 'sneaky_' || substr(md5(random()::text), 1, 5)
         where id = auth.uid();
        perform t.ok('handles', false, 'direct handle update refused');
    exception when insufficient_privilege then perform t.ok('handles', true, 'direct handle update refused'); end;
    begin perform count(*) from public.handle_history; perform t.ok('handles', false, 'history table refused');
    exception when insufficient_privilege then perform t.ok('handles', true, 'history table refused'); end;
end $$;
reset role;
select ok, label, case when not ok then detail end as detail from t.results where suite = 'handles' order by id;
