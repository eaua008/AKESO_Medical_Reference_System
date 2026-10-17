-- LOCAL TEST DATABASE ONLY. Never run this on the real Supabase project: it creates
-- test users and a 't' schema. See claude/friends-sharing-groups-design.md, Testing.

-- Migration 047: unknown handles, app version in the user list, deleting announcements
delete from t.results where suite = 'admin47';
do $$
declare
    x text := substr(md5(random()::text), 1, 5);
    adm uuid := t.mk_user('adm' || x, 'admin');
    stu uuid := t.mk_user('stu' || x);
    r jsonb; row jsonb; s1 text; s2 text; a uuid; n int;
begin
    -- friend request answers
    perform t.as_user(stu);
    r := public.friend_request('stu' || x || 'zz');
    perform t.ok('admin47', r ->> 'status' = 'not_found', 'unknown handle answers not_found', r::text);
    r := public.friend_request('stu' || x);
    perform t.ok('admin47', r ->> 'status' = 'self', 'own handle answers self', r::text);
    r := public.friend_requests();
    perform t.ok('admin47', jsonb_array_length(r -> 'sent') = 0, 'an unknown handle is not stored as sent', r::text);
    begin
        for i in 1..25 loop perform public.friend_request('nobody_' || i); end loop;
        perform t.ok('admin47', false, 'not_found tries still count toward the hourly limit');
    exception when others then
        perform t.ok('admin47', sqlerrm like 'Slow down%', 'not_found tries still count toward the hourly limit', sqlerrm);
    end;

    -- admin_users shows the version of the most recently used computer
    insert into public.user_devices (user_id, device_key, app_version, last_seen)
    values (stu, repeat('a', 20), '1.0.5', now() - interval '3 days'),
           (stu, repeat('b', 20), '1.0.7', now());
    perform t.as_user(adm);
    r := public.admin_users();
    row := (select e from jsonb_array_elements(r) e where (e ->> 'id')::uuid = stu);
    perform t.ok('admin47', row ->> 'app_version' = '1.0.7', 'newest device version is shown', row::text);
    row := (select e from jsonb_array_elements(r) e where (e ->> 'id')::uuid = adm);
    perform t.ok('admin47', row ->> 'app_version' = '', 'no device means an empty version', row::text);
    perform t.as_user(stu);
    perform t.err('admin47', 'select public.admin_users()', 'Only admins', 'students cannot list users');

    -- announcements: fingerprint and delete
    perform t.as_user(adm);
    a := public.admin_save_announcement(jsonb_build_object('title', 'Stamp ' || x, 'body', 'Body text',
                                                           'level', 'info', 'audience', 'everyone'));
    perform t.as_user(stu);
    s1 := public.announcements_stamp();
    perform t.ok('admin47', s1 <> '', 'stamp is set while announcements are live', s1);
    perform t.as_user(adm);
    perform public.admin_delete_announcement(a);
    perform t.as_user(stu);
    s2 := public.announcements_stamp();
    perform t.ok('admin47', s2 is distinct from s1, 'stamp changes after a delete');
    perform t.ok('admin47', not exists (select 1 from public.announcements where id = a), 'announcement is gone');
    select count(*) into n from public.admin_audit_log where action = 'announce_delete' and target_id = a::text;
    perform t.ok('admin47', n = 1, 'delete is written to the audit log');
    perform t.err('admin47', format('select public.admin_delete_announcement(%L)', a), 'Only admins',
                  'students cannot delete announcements');
end $$;
select ok, label, case when not ok then detail end as detail from t.results where suite = 'admin47' order by id;
