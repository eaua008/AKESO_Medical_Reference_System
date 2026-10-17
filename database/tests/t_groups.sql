-- LOCAL TEST DATABASE ONLY. Never run this on the real Supabase project: it creates
-- test users and a 't' schema. See claude/friends-sharing-groups-design.md, Testing.

-- Study groups (migration 042)
delete from t.results where suite = 'groups';
do $$
declare
    gus uuid := t.mk_user('gus_g');      -- owner
    hal uuid := t.mk_user('hal_g');      -- friend of gus
    ivy uuid := t.mk_user('ivy_g');      -- stranger
    jo  uuid := t.mk_user('jo_g');       -- will be blocked by gus
    edu uuid := t.mk_user('edu_g', 'educator');
    pub uuid; priv uuid; r jsonb; tok text; inv uuid; mid bigint; n int; x text;
begin
    perform t.as_user(gus);
    pub := public.group_create('Cardio Crew', 'Public cardiology group', 'public', 'Cardiology', 'cardio');
    priv := public.group_create('Night Owls', 'Private study', 'private', '', null);
    perform t.ok('groups', public.sg_role(pub, gus) = 'owner', 'creator is owner');
    perform t.err('groups', 'select public.group_create(''x'', '''', ''public'', '''', null)', 'at least 3',
                  'short name refused');

    -- browse lists public only
    perform t.as_user(ivy);
    perform t.ok('groups', (select count(*) from public.group_browse_public(null, null, null, 30, 0) as v(value)
                            where value ->> 'id' = priv::text) = 0
                 and (select count(*) from public.group_browse_public('cardio', null, null, 30, 0) as v(value)) = 1,
                 'browse shows public, never private');
    perform t.ok('groups', (select count(*) from public.group_browse_public(null, 'Cardiology', null, 30, 0) as v(value)) = 1
                 and (select count(*) from public.group_browse_public(null, null, 'cardio', 30, 0) as v(value)) = 1,
                 'browse filters by topic and body system');
    perform t.err('groups', format('select public.group_get(%L)', priv), 'not available',
                  'private group hidden from outsiders');
    perform public.group_join_public(pub);
    perform t.ok('groups', public.sg_role(pub, ivy) = 'member', 'public join');
    perform t.err('groups', format('select public.group_join_public(%L)', priv), 'not available',
                  'cannot join private directly');

    -- invite links
    perform t.as_user(ivy);
    perform t.err('groups', format('select public.group_invite_link_create(%L)', priv), 'Only the owner',
                  'non-member cannot make links');
    perform t.as_user(gus);
    r := public.group_invite_link_create(priv, null);
    tok := r ->> 'token';
    perform t.ok('groups', length(tok) = 64 and not exists (select 1 from public.study_group_invites
                 where token_hash = tok), 'token is 64 chars and stored only hashed');
    perform t.as_user(ivy);
    perform t.err('groups', 'select public.group_join_with_token(''deadbeef'')', 'not valid',
                  'wrong token refused');
    perform t.ok('groups', public.group_join_with_token(tok) = priv, 'valid token joins');
    perform public.group_leave(priv);
    -- regenerate: old token dies
    perform t.as_user(gus);
    r := public.group_invite_link_create(priv, 1);
    perform t.as_user(ivy);
    perform t.err('groups', format('select public.group_join_with_token(%L)', tok), 'not valid',
                  'regenerated link: old token refused');
    tok := r ->> 'token';
    update public.study_group_invites set expires_at = now() - interval '1 minute'
    where token_hash = public.sg_hash(tok);
    perform t.err('groups', format('select public.group_join_with_token(%L)', tok), 'not valid',
                  'expired token refused');
    perform t.as_user(gus);
    r := public.group_invite_link_create(priv, 24);
    tok := r ->> 'token';
    perform public.group_invite_link_revoke(priv);
    perform t.as_user(ivy);
    perform t.err('groups', format('select public.group_join_with_token(%L)', tok), 'not valid',
                  'revoked token refused');

    -- friend invites
    perform t.as_user(gus); perform public.friend_request('hal_g');
    perform t.as_user(hal); perform public.friend_respond(gus, true);
    perform t.as_user(gus);
    perform t.err('groups', format('select public.group_invite_friend(%L, %L)', priv, ivy), 'only invite your friends',
                  'invite a non-friend refused');
    perform public.group_invite_friend(priv, hal);
    perform t.ok('groups', exists (select 1 from public.notifications where user_id = hal
                 and kind = 'group_invite'), 'invitee notified');
    perform t.as_user(hal);
    r := (select value from public.group_my_invites() as v(value) limit 1);
    inv := (r ->> 'invite_id')::uuid;
    x := public.group_invite_respond(inv, true)::text;
    perform t.ok('groups', x = priv::text and public.sg_role(priv, hal) = 'member',
                 'friend invite accepted -> member');

    -- blocked pair cannot invite
    perform t.as_user(gus); perform public.friend_request('jo_g');
    perform t.as_user(jo);  perform public.friend_respond(gus, true);
    perform t.as_user(gus); perform public.group_invite_friend(pub, jo);
    perform t.as_user(jo);  perform public.friend_block(gus);
    perform t.ok('groups', (select count(*) from public.group_my_invites() as v(value)) = 0, 'block revokes pending invite');
    perform t.err('groups', format('select public.group_get(%L)', pub), 'not available',
                  'blocked person cannot open the blocker''s public group');
    perform t.ok('groups', (select count(*) from public.group_browse_public('cardio', null, null, 30, 0) as v(value)) = 0,
                 'blocker''s group left out of browse');
    perform public.friend_unblock(gus);

    -- roles
    perform t.as_user(gus);
    perform public.group_set_role(priv, hal, 'moderator');
    perform t.ok('groups', public.sg_role(priv, hal) = 'moderator', 'owner promotes moderator');
    perform t.as_user(hal);
    perform t.err('groups', format('select public.group_set_role(%L, %L, ''member'')', priv, gus),
                  'Only the owner', 'moderator cannot change roles');
    perform t.err('groups', format('select public.group_remove_member(%L, %L)', priv, gus),
                  'can''t remove', 'moderator cannot remove owner');

    -- chat
    perform t.as_user(ivy);
    perform t.err('groups', format('select public.group_send_message(%L, ''hi'')', priv), 'Join the group',
                  'non-member cannot post');
    perform t.as_user(gus);
    r := public.group_send_message(priv, 'Hello @hal_g, ready for cardio?');
    mid := (r ->> 'id')::bigint;
    perform t.ok('groups', exists (select 1 from public.notifications where user_id = hal
                 and kind = 'group_mention'), 'mention notifies member');
    perform t.err('groups', format('select public.group_send_message(%L, ''Mr. Santos, 09171234567'')', priv),
                  'Not sent', 'PHI guard on messages');
    perform t.err('groups', format('select public.group_send_message(%L, %L)', priv, repeat('a', 2001)),
                  '2,000', 'length cap');
    perform t.as_user(hal);
    r := public.group_messages_after(priv, null, 50);
    perform t.ok('groups', jsonb_array_length(r -> 'messages') = 1
                 and r -> 'messages' -> 0 -> 'author' ->> 'group_role' = 'owner',
                 'polling returns messages with role badge');
    r := public.group_messages_after(priv, mid, 50);
    perform t.ok('groups', jsonb_array_length(r -> 'messages') = 0, 'nothing new after the last id');
    perform t.as_user(gus);
    perform public.group_send_message(priv, 'second');
    perform t.as_user(hal);
    r := public.group_messages_after(priv, mid, 50);
    perform t.ok('groups', jsonb_array_length(r -> 'messages') = 1
                 and r -> 'messages' -> 0 ->> 'body' = 'second', 'only new messages fetched');
    -- rate limit 10 / minute
    begin
        for i in 1..12 loop perform public.group_send_message(priv, 'm' || i); end loop;
        perform t.ok('groups', false, 'message rate limit');
    exception when others then
        perform t.ok('groups', sqlerrm like 'Slow down%', 'message rate limit', sqlerrm);
    end;

    -- report and hide
    perform t.as_user(gus);
    perform public.group_join_public(pub);          -- already owner: no-op
    perform t.as_user(ivy);
    r := public.group_send_message(pub, 'spam spam');
    mid := (r ->> 'id')::bigint;
    perform t.as_user(gus);
    perform public.group_report(pub, 'message', mid::text, 'spam', '');
    perform t.as_user(edu);
    perform t.err('groups', format('select public.group_get(%L)', priv), 'not available',
                  'app educator cannot browse a private group');
    perform t.ok('groups', (select count(*) from public.group_report_queue() as v(value)) = 1, 'educator sees report queue');
    perform public.group_moderate(pub, 'message', mid::text, 'hide');
    perform t.ok('groups', (select status from public.study_group_messages where id = mid) = 'hidden',
                 'educator hides reported message');
    perform t.ok('groups', exists (select 1 from public.admin_audit_log where action = 'group_hide'),
                 'app moderation logged with ad_log');
    perform t.err('groups', format('select public.group_moderate(%L, ''message'', ''%s'', ''unhide'')', priv,
                  (select max(id) from public.study_group_messages where group_id = priv)),
                  'can''t moderate', 'educator cannot act on unreported content');
    perform t.as_user(hal);
    perform public.group_join_public(pub);
    r := public.group_messages_after(pub, null, 50);
    perform t.ok('groups', (select bool_and((m ->> 'body') = '') from jsonb_array_elements(r -> 'messages') m
                            where (m ->> 'id')::bigint = mid), 'hidden message text hidden from members');

    -- shared notes shelf
    perform t.as_user(hal);
    perform public.group_share_note(priv, '{"source_item_id":"n1","title":"ECG basics","body":"<p>PR interval</p><img src=x>"}');
    perform t.as_user(gus);
    r := (select value from public.group_notes_list(priv) as v(value) limit 1);
    perform t.ok('groups', r ->> 'title' = 'ECG basics', 'note on the shelf');
    r := public.group_note_get((r ->> 'id')::uuid);
    perform t.ok('groups', r ->> 'body' like '%[image not shared]%', 'shelf note text only');

    -- leave / owner handover / delete
    perform t.as_user(ivy);
    perform t.ok('groups', public.group_leave(pub) = 'left', 'member leaves');
    perform t.as_user(gus);
    x := public.group_leave(priv);
    perform t.ok('groups', x = 'transferred' and public.sg_role(priv, hal) = 'owner',
                 'owner leaving hands over to moderator', x);
    perform t.as_user(hal);
    perform public.group_delete(priv);
    perform t.ok('groups', not exists (select 1 from public.study_groups where id = priv)
                 and not exists (select 1 from public.study_group_messages where group_id = priv)
                 and not exists (select 1 from public.study_group_notes where group_id = priv),
                 'delete removes chat and notes');
end $$;

-- account deletion: owner with a moderator -> transfer; without -> delete
do $$
declare
    own uuid := t.mk_user('own_g'); m1 uuid := t.mk_user('mod_g'); mem uuid := t.mk_user('mem_g');
    g1 uuid; g2 uuid; r jsonb;
begin
    perform t.as_user(own);
    g1 := public.group_create('Keep me', '', 'public', '', null);
    g2 := public.group_create('Lose me', '', 'public', '', null);
    perform t.as_user(m1); perform public.group_join_public(g1);
    perform t.as_user(mem); perform public.group_join_public(g1); perform public.group_join_public(g2);
    perform t.as_user(own); perform public.group_set_role(g1, m1, 'moderator');
    perform public.group_send_message(g1, 'from the owner');
    r := public.social_purge_user(own);
    perform t.ok('groups', (r -> 'groups' ->> 'transferred')::int = 1 and (r -> 'groups' ->> 'deleted')::int = 1,
                 'purge: one transferred, one deleted', r::text);
    perform t.ok('groups', (select owner_id from public.study_groups where id = g1) = m1
                 and not exists (select 1 from public.study_groups where id = g2)
                 and not exists (select 1 from public.study_group_messages where author_id = own),
                 'purge result in tables');
end $$;

-- deleting the auth user directly (no purge call) still hands the group over
do $$
declare own uuid := t.mk_user('own2_g'); m1 uuid := t.mk_user('mod2_g'); g1 uuid;
begin
    perform t.as_user(own);
    g1 := public.group_create('Direct delete', '', 'public', '', null);
    perform t.as_user(m1); perform public.group_join_public(g1);
    perform t.as_user(own); perform public.group_set_role(g1, m1, 'moderator');
    delete from auth.users where id = own;
    perform t.ok('groups', (select owner_id from public.study_groups where id = g1) = m1
                 and public.sg_role(g1, m1) = 'owner', 'auth.users delete: trigger hands over');
end $$;

set role authenticated;
do $$ begin
    begin perform count(*) from public.study_group_messages; perform t.ok('groups', false, 'RLS: messages refused');
    exception when insufficient_privilege then perform t.ok('groups', true, 'RLS: messages refused'); end;
    begin perform count(*) from public.study_group_invites; perform t.ok('groups', false, 'RLS: invites refused');
    exception when insufficient_privilege then perform t.ok('groups', true, 'RLS: invites refused'); end;
    begin perform public.sg_add_member(gen_random_uuid(), gen_random_uuid(), 'owner');
          perform t.ok('groups', false, 'helpers not callable');
    exception when insufficient_privilege then perform t.ok('groups', true, 'helpers not callable'); end;
end $$;
reset role;
select ok, label, case when not ok then detail end as detail from t.results where suite = 'groups' order by id;
