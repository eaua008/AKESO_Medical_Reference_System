-- LOCAL TEST DATABASE ONLY. Never run this on the real Supabase project: it creates
-- test users and a 't' schema. See claude/friends-sharing-groups-design.md, Testing.

-- Notebook sharing (migration 041)
delete from t.results where suite = 'sharing';
do $$
declare
    ann uuid := t.mk_user('ann_s');
    ben uuid := t.mk_user('ben_s');
    cy  uuid := t.mk_user('cy_s');
    r jsonb; sid uuid; n int;
begin
    -- ann and ben are friends; cy is not
    perform t.as_user(ann); perform public.friend_request('ben_s');
    perform t.as_user(ben); perform public.friend_respond(ann, true);

    perform t.as_user(ann);
    r := public.notebook_share_create(jsonb_build_object(
            'source_item_id', 'item1', 'kind', 'note', 'title', 'Cardio notes',
            'body', '<p>Heart failure basics</p><img src="file:///C:/x.png"><script>x</script>'),
         array[ben]);
    sid := (r ->> 'share_id')::uuid;
    perform t.ok('sharing', (r ->> 'shared_with')::int = 1, 'share to a friend', r::text);
    perform t.ok('sharing', (select body from public.notebook_shares where id = sid)
                 like '%[image not shared]%' and (select body from public.notebook_shares where id = sid)
                 not like '%<img%' and (select body from public.notebook_shares where id = sid)
                 not like '%script%', 'server strips pictures and scripts');
    perform t.ok('sharing', exists (select 1 from public.notifications where user_id = ben
                 and kind = 'notebook_shared' and ref_id = sid::text), 'recipient notified');
    perform t.ok('sharing', 'item1' in (select public.notebook_share_my_items()), 'owner sees badge item');

    perform t.err('sharing', format('select public.notebook_share_create(%L::jsonb, array[%L]::uuid[])',
        '{"source_item_id":"item2","title":"x","body":"hi"}', cy), 'only share notes with your friends',
        'share to a non-friend refused');
    perform t.err('sharing', format('select public.notebook_share_create(%L::jsonb, array[%L]::uuid[])',
        '{"source_item_id":"item3","title":"Case","body":"<p>Call 09171234567</p>"}', ben),
        'phone number', 'PHI guard blocks the share');

    -- recipient reads it
    perform t.as_user(ben);
    perform t.ok('sharing', (select count(*) from public.notebook_share_list_received()) = 1, 'received list');
    r := public.notebook_share_get(sid);
    perform t.ok('sharing', r ->> 'title' = 'Cardio notes' and r ->> 'source_item_id' is null,
                 'recipient reads snapshot, owner item id hidden', r::text);
    r := public.notebook_share_save_copy(sid);
    perform t.ok('sharing', r ->> 'body' like '%Heart failure%', 'save copy returns the text');
    perform t.err('sharing', format('select public.notebook_share_update_snapshot(%L, ''x'', ''y'')', sid),
                  'not available', 'recipient cannot update the snapshot');
    -- a stranger cannot read it
    perform t.as_user(cy);
    perform t.err('sharing', format('select public.notebook_share_get(%L)', sid), 'no longer available',
                  'non-recipient refused');

    -- snapshot update
    perform t.as_user(ann);
    perform public.notebook_share_update_snapshot(sid, 'Cardio notes v2', '<p>Updated</p>');
    perform t.as_user(ben);
    perform t.ok('sharing', public.notebook_share_get(sid) ->> 'body' = '<p>Updated</p>', 'recipient sees update');

    -- manage shows recipient
    perform t.as_user(ann);
    r := public.notebook_share_manage('item1');
    perform t.ok('sharing', jsonb_array_length(r -> 'recipients') = 1, 'manage lists recipients', r::text);

    -- unfriend: access gone immediately, revoked by trigger
    perform public.friend_remove(ben);
    perform t.as_user(ben);
    perform t.err('sharing', format('select public.notebook_share_get(%L)', sid), 'no longer available',
                  'access gone after unfriending');
    perform t.ok('sharing', (select count(*) from public.notebook_share_list_received()) = 0,
                 'received list empty after unfriending');
    perform t.ok('sharing', (select revoked_at is not null from public.notebook_share_recipients
                             where share_id = sid and recipient_id = ben), 'recipient row revoked');

    -- befriend again, reshare, then unshare explicitly
    perform t.as_user(ann); perform public.friend_request('ben_s');
    perform t.as_user(ben); perform public.friend_respond(ann, true);
    perform t.as_user(ann);
    perform public.notebook_share_create('{"source_item_id":"item1","title":"Cardio","body":"<p>a</p>"}', array[ben]);
    perform t.as_user(ben);
    perform t.ok('sharing', (select count(*) from public.notebook_share_list_received()) = 1, 'reshare works');
    perform t.as_user(ann);
    perform public.notebook_share_revoke(sid, null);
    perform t.as_user(ben);
    perform t.ok('sharing', (select count(*) from public.notebook_share_list_received()) = 0, 'unshare works');

    -- blocking also ends access
    perform t.as_user(ann);
    perform public.notebook_share_create('{"source_item_id":"item1","title":"Cardio","body":"<p>a</p>"}', array[ben]);
    perform t.as_user(ben);
    perform public.friend_block(ann);
    perform t.err('sharing', format('select public.notebook_share_get(%L)', sid), 'no longer available',
                  'access gone after blocking');
    perform public.friend_unblock(ann);

    -- rate limit 30/hour
    perform t.as_user(ann); perform public.friend_request('ben_s');
    perform t.as_user(ben); perform public.friend_respond(ann, true);
    perform t.as_user(ann);
    begin
        for i in 1..40 loop
            perform public.notebook_share_create(jsonb_build_object('source_item_id', 'r' || i,
                'title', 'n' || i, 'body', 'x'), array[ben]);
        end loop;
        perform t.ok('sharing', false, 'share rate limit');
    exception when others then
        perform t.ok('sharing', sqlerrm like 'Slow down%', 'share rate limit', sqlerrm);
    end;

    -- purge removes shares made and received
    select count(*) into n from public.notebook_shares where owner_id = ann;
    perform t.ok('sharing', n >= 1, 'ann has shares before purge');
    perform public.social_purge_user(ann);
    perform t.ok('sharing', not exists (select 1 from public.notebook_shares where owner_id = ann)
                 and not exists (select 1 from public.friendships where user_a = ann or user_b = ann),
                 'purge removes shares and friendships');
end $$;

set role authenticated;
do $$ begin
    begin perform count(*) from public.notebook_shares; perform t.ok('sharing', false, 'RLS: shares table refused');
    exception when insufficient_privilege then perform t.ok('sharing', true, 'RLS: shares table refused'); end;
    begin perform count(*) from public.notebook_share_recipients; perform t.ok('sharing', false, 'RLS: recipients refused');
    exception when insufficient_privilege then perform t.ok('sharing', true, 'RLS: recipients refused'); end;
end $$;
reset role;
select ok, label, case when not ok then detail end as detail from t.results where suite = 'sharing' order by id;
