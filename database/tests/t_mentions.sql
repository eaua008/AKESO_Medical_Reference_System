-- LOCAL TEST DATABASE ONLY. Never run this on the real Supabase project: it creates
-- test users and a 't' schema. See claude/friends-sharing-groups-design.md, Testing.

-- @mention handles for group members (migration 046)
delete from t.results where suite = 'mentions';
do $$
declare
    x text := substr(md5(random()::text), 1, 5);
    own uuid := t.mk_user('mno' || x);
    priv uuid := t.mk_user('mnp' || x);
    out uuid := t.mk_user('mnx' || x);
    g uuid; r jsonb; me jsonb;
begin
    update public.profiles set visibility = 'private' where id = priv;
    perform t.as_user(own);
    g := public.group_create('Mentions ' || x, '', 'public', '', null);
    perform t.as_user(priv); perform public.group_join_public(g);
    perform t.as_user(own);
    r := public.group_get(g);
    me := (select m from jsonb_array_elements(r -> 'members_list') m where (m ->> 'id')::uuid = priv);
    perform t.ok('mentions', me ->> 'handle' is null, 'a private profile still hides its handle in the member list');
    perform t.ok('mentions', me ->> 'mention' = 'mnp' || x, 'but a fellow member gets its mention handle', me::text);
    perform public.group_send_message(g, 'hi @mnp' || x);
    perform t.ok('mentions', exists (select 1 from public.notifications
                                     where user_id = priv and kind = 'group_mention'),
                 'mentioning that handle notifies them');
    perform t.as_user(out);
    r := public.group_get(g);
    perform t.ok('mentions', not (r ? 'members_list'), 'a non-member gets no member list, so no handles', r::text);
end $$;
select ok, label, case when not ok then detail end as detail from t.results where suite = 'mentions' order by id;
