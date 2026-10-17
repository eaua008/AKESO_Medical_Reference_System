-- LOCAL TEST DATABASE ONLY. Never run this on the real Supabase project: it creates
-- test users and a 't' schema. See claude/friends-sharing-groups-design.md, Testing.

-- Pictures in group chats (migration 045)
delete from t.results where suite = 'images';
do $$
declare
    x text := substr(md5(random()::text), 1, 5);
    own uuid := t.mk_user('imo' || x);
    mem uuid := t.mk_user('imm' || x);
    out uuid := t.mk_user('imx' || x);
    g uuid; p_own text; p_mem text; p_bad text; p_cap text; r jsonb; n int; mid bigint;
begin
    perform t.as_user(own);
    g := public.group_create('Images ' || x, '', 'public', '', null);
    perform t.as_user(mem); perform public.group_join_public(g);
    p_own := g || '/' || own || '/' || md5('a' || x) || '.png';
    p_mem := g || '/' || mem || '/' || md5('b' || x) || '.jpg';
    p_bad := g || '/' || own || '/' || md5('c' || x) || '.gif';
    p_cap := g || '/' || mem || '/' || md5('e' || x) || '.png';

    -- uploads (storage rules), as the signed-in user
    perform t.as_user(mem);
    execute 'set role authenticated';
    begin
        insert into storage.objects (bucket_id, name, owner) values ('group-attachments', p_mem, mem);
        perform t.ok('images', true, 'member uploads into their own folder');
    exception when others then
        perform t.ok('images', false, 'member uploads into their own folder', sqlerrm);
    end;
    begin
        insert into storage.objects (bucket_id, name, owner) values ('group-attachments', p_own, mem);
        perform t.ok('images', false, 'upload into someone else''s folder refused');
    exception when others then
        perform t.ok('images', true, 'upload into someone else''s folder refused');
    end;
    execute 'reset role';
    perform t.as_user(out);
    execute 'set role authenticated';
    begin
        insert into storage.objects (bucket_id, name, owner)
        values ('group-attachments', g || '/' || out || '/' || md5('d' || x) || '.png', out);
        perform t.ok('images', false, 'non-member upload refused');
    exception when others then
        perform t.ok('images', true, 'non-member upload refused');
    end;
    begin
        insert into storage.objects (bucket_id, name, owner) values ('group-attachments', 'loose.png', out);
        perform t.ok('images', false, 'upload with a bad path refused');
    exception when others then
        perform t.ok('images', true, 'upload with a bad path refused');
    end;
    execute 'reset role';
    -- the owner's own picture
    perform t.as_user(own);
    execute 'set role authenticated';
    insert into storage.objects (bucket_id, name, owner) values ('group-attachments', p_own, own);
    execute 'reset role';

    -- sending
    perform t.as_user(mem);
    perform t.err('images', format('select public.group_send_image(%L, ''x'', %L)', g, p_own),
                  'can''t be sent', 'sending someone else''s path refused');
    perform t.err('images', format('select public.group_send_image(%L, ''x'', %L)', g, p_bad),
                  'can''t be sent', 'a path that isn''t png/jpg refused');
    perform t.err('images', format('select public.group_send_image(%L, ''x'', %L)', g,
                  g || '/' || mem || '/' || md5('zzz') || '.png'),
                  'didn''t upload', 'path with no uploaded file refused');
    perform t.err('images', format('select public.group_send_image(%L, %L, %L)', g,
                  'Mr. Cruz 09171234567', p_mem), 'Not sent', 'PHI guard on the caption');
    r := public.group_send_image(g, 'ECG strip, hypothetical', p_mem);
    mid := (r ->> 'id')::bigint;
    perform t.ok('images', r ->> 'attachment' = p_mem and r ->> 'body' = 'ECG strip, hypothetical',
                 'image message sent', r::text);
    perform t.err('images', format('select public.group_send_image(%L, '''', %L)', g, p_mem),
                  'duplicate', 'the same picture can''t be sent twice');
    execute 'set role authenticated';
    insert into storage.objects (bucket_id, name, owner) values ('group-attachments', p_cap, mem);
    execute 'reset role';
    r := public.group_send_image(g, '', p_cap);
    perform t.ok('images', r ->> 'body' = '' and r ->> 'attachment' is not null, 'picture with no caption');

    -- who can read it
    perform t.as_user(own);
    execute 'set role authenticated';
    select count(*) into n from storage.objects where bucket_id = 'group-attachments' and name = p_mem;
    execute 'reset role';
    perform t.ok('images', n = 1, 'another member can read it');
    perform t.as_user(out);
    execute 'set role authenticated';
    select count(*) into n from storage.objects where bucket_id = 'group-attachments' and name = p_mem;
    execute 'reset role';
    perform t.ok('images', n = 0, 'a non-member cannot read it');

    -- hidden message: ordinary members lose the picture; sender and staff keep it
    perform t.as_user(own);
    perform public.group_report(g, 'message', mid::text, 'other', '');
    perform public.group_moderate(g, 'message', mid::text, 'hide');
    perform t.as_user(mem);
    perform t.ok('images', (select (m ->> 'attachment') = p_mem
                            from jsonb_array_elements(public.group_messages_after(g, null, 50) -> 'messages') m
                            where (m ->> 'id')::bigint = mid), 'sender still sees their hidden picture');
    perform t.as_user(own);
    execute 'set role authenticated';
    select count(*) into n from storage.objects where bucket_id = 'group-attachments' and name = p_mem;
    execute 'reset role';
    perform t.ok('images', n = 1, 'owner (staff) can still read a hidden picture');
    perform t.as_user(out);
    perform public.group_join_public(g);
    execute 'set role authenticated';
    select count(*) into n from storage.objects where bucket_id = 'group-attachments' and name = p_mem;
    execute 'reset role';
    perform t.ok('images', n = 0, 'an ordinary member cannot read a hidden picture');
    perform t.ok('images', (select (m ->> 'attachment') is null
                            from jsonb_array_elements(public.group_messages_after(g, null, 50) -> 'messages') m
                            where (m ->> 'id')::bigint = mid), 'hidden message gives no picture path');

    -- deleting files: sender or staff only
    execute 'set role authenticated';
    delete from storage.objects where bucket_id = 'group-attachments' and name = p_mem;
    get diagnostics n = row_count;
    execute 'reset role';
    perform t.ok('images', n = 0, 'an ordinary member cannot delete another''s picture');
    perform t.as_user(own);
    execute 'set role authenticated';
    delete from storage.objects where bucket_id = 'group-attachments' and name = p_mem;
    get diagnostics n = row_count;
    execute 'reset role';
    perform t.ok('images', n = 1, 'the owner can delete it');

    -- rate limit: 10 pictures an hour (two were sent above)
    perform t.as_user(mem);
    begin
        for i in 1..12 loop
            execute 'set role authenticated';
            insert into storage.objects (bucket_id, name, owner)
            values ('group-attachments', g || '/' || mem || '/' || md5('r' || i || x) || '.png', mem);
            execute 'reset role';
            perform public.group_send_image(g, '', g || '/' || mem || '/' || md5('r' || i || x) || '.png');
        end loop;
        perform t.ok('images', false, 'picture rate limit');
    exception when others then
        perform t.ok('images', sqlerrm like 'Slow down%', 'picture rate limit', sqlerrm);
    end;
end $$;

-- the helpers that reveal membership stay closed to signed-in users
set role authenticated;
do $$ begin
    begin
        perform public.sg_role(gen_random_uuid(), gen_random_uuid());
        perform t.ok('images', false, 'sg_role not callable');
    exception when insufficient_privilege then
        perform t.ok('images', true, 'sg_role not callable');
    end;
    begin
        perform public.sg_attachment_visible('x', gen_random_uuid());
        perform t.ok('images', false, 'sg_attachment_visible not callable');
    exception when insufficient_privilege then
        perform t.ok('images', true, 'sg_attachment_visible not callable');
    end;
end $$;
reset role;
select ok, label, case when not ok then detail end as detail from t.results where suite = 'images' order by id;
