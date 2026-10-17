-- LOCAL TEST DATABASE ONLY. Never run this on the real Supabase project: it creates
-- test users and a 't' schema. See claude/friends-sharing-groups-design.md, Testing.

-- "New messages" marker in group chats (migration 044)
delete from t.results where suite = 'readmarker';
do $$
declare
    x text := substr(md5(random()::text), 1, 5);
    own uuid := t.mk_user('rmo' || x);
    rdr uuid := t.mk_user('rmr' || x);
    g uuid; r jsonb; first_id bigint; last_id bigint;
begin
    perform t.as_user(own);
    g := public.group_create('Marker ' || x, '', 'public', '', null);
    perform t.as_user(rdr);
    perform public.group_join_public(g);
    perform t.as_user(own);
    for i in 1..3 loop perform public.group_send_message(g, 'old ' || i); end loop;
    perform t.as_user(rdr);
    r := public.group_messages_after(g, null, 50);
    perform t.ok('readmarker', (r ->> 'last_read')::bigint = 0, 'joined before any message: last_read is 0');
    last_id := (r -> 'messages' -> 2 ->> 'id')::bigint;
    perform t.ok('readmarker', (select count(*) from public.group_my_list() as v(value)) = 1
                 and (select (value ->> 'unread')::int from public.group_my_list() as v(value)) = 0,
                 'opening marks everything read');
    perform t.as_user(own);
    for i in 1..2 loop perform public.group_send_message(g, 'new ' || i); end loop;
    perform t.as_user(rdr);
    perform t.ok('readmarker', (select (value ->> 'unread')::int from public.group_my_list() as v(value)) = 2,
                 'two unread after the owner posts');
    r := public.group_messages_after(g, null, 50);
    perform t.ok('readmarker', (r ->> 'last_read')::bigint = last_id, 'last_read is the position BEFORE opening', r ->> 'last_read');
    perform t.ok('readmarker', jsonb_array_length(r -> 'messages') = 5, 'all five messages returned');
    r := public.group_messages_after(g, null, 50);
    perform t.ok('readmarker', (r ->> 'last_read')::bigint > last_id, 'second open: everything now counts as read');
    perform t.ok('readmarker', (select (value ->> 'unread')::int from public.group_my_list() as v(value)) = 0,
                 'unread back to zero');
end $$;
select ok, label, case when not ok then detail end as detail from t.results where suite = 'readmarker' order by id;
