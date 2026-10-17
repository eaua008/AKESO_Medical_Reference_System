-- LOCAL TEST DATABASE ONLY. Never run this on the real Supabase project: it creates
-- test users and a 't' schema. See claude/friends-sharing-groups-design.md, Testing.

-- Friends (migration 040)
delete from t.results where suite = 'friends';
do $$
declare
    alice uuid := t.mk_user('alice_t');
    bob   uuid := t.mk_user('bob_t');
    cara  uuid := t.mk_user('cara_t');
    r jsonb; s text; n int;
begin
    -- real and blocked handles answer the same; an unknown one says not_found (047)
    perform t.as_user(alice);
    r := public.friend_request('@bob_t');
    perform t.ok('friends', r ->> 'status' = 'sent', 'request to real handle says sent', r::text);
    r := public.friend_request('nobody_here_xyz');
    perform t.ok('friends', r ->> 'status' = 'not_found', 'request to unknown handle says not_found (047)', r::text);
    r := public.friend_requests();
    perform t.ok('friends', jsonb_array_length(r -> 'sent') = 1
                 and not (r::text like '%' || bob::text || '%'),
                 'sent list echoes typed handles only, no ids', r::text);
    select count(*) into n from public.notifications where user_id = bob and kind = 'friend_request';
    perform t.ok('friends', n = 1, 'bob notified of the request');

    -- decline
    perform t.as_user(bob);
    r := public.friend_requests();
    perform t.ok('friends', jsonb_array_length(r -> 'incoming') = 1
                 and (r -> 'incoming' -> 0 ->> 'id')::uuid = alice, 'bob sees incoming from alice');
    perform public.friend_respond(alice, false);
    perform t.ok('friends', not public.fr_are_friends(alice, bob), 'decline: not friends');
    select count(*) into n from public.notifications where user_id = alice and kind = 'friend_accepted';
    perform t.ok('friends', n = 0, 'decline sends no notification');

    -- request again, accept
    perform t.as_user(alice);
    perform public.friend_request('bob_t');
    perform t.as_user(bob);
    perform public.friend_respond(alice, true);
    perform t.ok('friends', public.fr_are_friends(alice, bob), 'accept: friends');
    select count(*) into n from public.notifications where user_id = alice and kind = 'friend_accepted';
    perform t.ok('friends', n = 1, 'alice notified of acceptance');
    perform t.as_user(alice);
    perform t.ok('friends', (select count(*) from public.friend_list()) = 1, 'alice lists 1 friend');
    perform t.ok('friends', public.friend_status('bob_t') = 'friends', 'status friends');
    r := public.friend_requests();
    perform t.ok('friends', not (r -> 'sent')::text like '%bob_t%', 'accepted request leaves Sent', r::text);

    -- mutual request auto-accepts
    perform t.as_user(cara);
    perform public.friend_request('alice_t');
    perform t.as_user(alice);
    r := public.friend_request('cara_t');
    perform t.ok('friends', r ->> 'status' = 'accepted', 'asking someone who asked you accepts');

    -- unfriend
    perform public.friend_remove(cara);
    perform t.ok('friends', not public.fr_are_friends(alice, cara), 'unfriend works');

    -- block: cara blocks alice; alice's request is silently dropped
    perform t.as_user(cara);
    perform public.friend_block(alice);
    perform t.as_user(alice);
    select count(*) into n from public.notifications where user_id = cara and kind = 'friend_request';
    r := public.friend_request('cara_t');
    perform t.ok('friends', r ->> 'status' = 'sent', 'blocked requester still sees "sent"');
    perform t.ok('friends', (select count(*) from public.notifications
                             where user_id = cara and kind = 'friend_request') = n,
                 'blocker gets no notification');
    perform t.ok('friends', public.friend_status('cara_t') = 'none', 'blocked person sees none');
    perform t.as_user(cara);
    perform t.ok('friends', public.friend_status('alice_t') = 'blocked', 'blocker sees blocked');
    perform t.ok('friends', (select count(*) from public.friend_blocked_list()) = 1, 'blocked list');
    -- both block; one unblock keeps the block
    perform t.as_user(alice);
    perform public.friend_block(cara);
    perform t.as_user(cara);
    perform public.friend_unblock(alice);
    perform t.ok('friends', public.fr_blocked(alice, cara), 'still blocked while alice blocks');
    perform t.as_user(alice);
    perform public.friend_unblock(cara);
    perform t.ok('friends', not public.fr_blocked(alice, cara)
                 and not exists (select 1 from public.friendships
                                 where user_a = least(alice, cara) and user_b = greatest(alice, cara)),
                 'both unblocked: row gone, no friendship restored');
    -- blocking a friend ends the friendship
    perform t.as_user(bob);
    perform public.friend_block(alice);
    perform t.ok('friends', not public.fr_are_friends(alice, bob), 'blocking ends friendship');
    perform public.friend_unblock(alice);

    -- cancel a sent request
    perform t.as_user(alice);
    perform public.friend_request('bob_t');
    r := public.friend_requests();
    perform public.friend_cancel((select (e ->> 'request_id')::bigint from jsonb_array_elements(r -> 'sent') e where e ->> 'handle' = 'bob_t'));
    perform t.ok('friends', not exists (select 1 from public.friendships
                 where user_a = least(alice, bob) and user_b = greatest(alice, bob)),
                 'cancel removes pending');

    -- rate limit: 20 per hour (alice has used some already)
    begin
        for i in 1..25 loop perform public.friend_request('ghost_' || i); end loop;
        perform t.ok('friends', false, 'rate limit refuses the 21st request');
    exception when others then
        perform t.ok('friends', sqlerrm like 'Slow down%', 'rate limit refuses the 21st request', sqlerrm);
    end;
    perform t.err('friends', 'select public.friend_request(''x'')', 'Enter a handle', 'bad handle format refused');
end $$;

-- pending cap: 50 waiting requests
do $$
declare d uuid := t.mk_user('dave_t');
begin
    perform t.as_user(d);
    insert into public.friend_outbox (sender_id, handle) select d, 'cap_' || g from generate_series(1, 50) g;
    perform t.err('friends', 'select public.friend_request(''another_one'')', '50 requests waiting',
                  'cap of 50 pending outgoing');
end $$;

-- direct table access refused, functions allowed
set role authenticated;
do $$ begin
    begin perform count(*) from public.friendships;
          perform t.ok('friends', false, 'RLS: table read refused');
    exception when insufficient_privilege then perform t.ok('friends', true, 'RLS: table read refused'); end;
    begin insert into public.friendships (user_a, user_b, status) values (gen_random_uuid(), gen_random_uuid(), 'accepted');
          perform t.ok('friends', false, 'RLS: table write refused');
    exception when insufficient_privilege then perform t.ok('friends', true, 'RLS: table write refused'); end;
    begin perform public.social_purge_user(gen_random_uuid());
          perform t.ok('friends', false, 'purge not callable by users');
    exception when insufficient_privilege then perform t.ok('friends', true, 'purge not callable by users'); end;
end $$;
reset role;
set role anon;
do $$ begin
    begin perform public.friend_list(); perform t.ok('friends', false, 'anon cannot call friend_list');
    exception when insufficient_privilege then perform t.ok('friends', true, 'anon cannot call friend_list'); end;
end $$;
reset role;

select ok, label, case when not ok then detail end as detail from t.results where suite = 'friends' order by id;
