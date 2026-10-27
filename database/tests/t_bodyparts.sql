-- LOCAL TEST DATABASE ONLY. Never run this on the real Supabase project: it creates
-- test users and a 't' schema.

-- Migrations 052 (body_part_info), 053 (B1 content, run twice by run_local.sh) and 054 (preview)
delete from t.results where suite = 'bodyparts';
drop table if exists t.bp_ids;
create table t.bp_ids (k text primary key, v text);
grant all on t.bp_ids to anon, authenticated;
insert into public.diseases (id, name) values ('dengue', 'Dengue') on conflict do nothing;

do $$
declare
    x text := substr(md5(random()::text), 1, 5);
    adm uuid := t.mk_user('bpa' || x, 'admin');
    stu uuid := t.mk_user('bps' || x);
    k text := 'test part ' || x;
    v0 bigint; v1 bigint; n int; r jsonb;
begin
    insert into t.bp_ids values ('adm', adm), ('stu', stu), ('draft', k), ('pub', k || ' pub');

    -- 053: the batch went in as drafts, and the second run changed nothing
    select count(*) into n from public.body_part_info where key not like 'test part %';
    perform t.ok('bodyparts', n = 54, 'batch 053 adds 54 entries', n::text);
    select count(*) into n from public.body_part_info
    where key not like 'test part %' and (status <> 'draft' or updated_at <> created_at);
    perform t.ok('bodyparts', n = 0, 'batch rows are drafts and the second run changed nothing', n::text);
    select count(*) into n from public.body_part_info
    where key not like 'test part %' and (jsonb_array_length(sources) = 0 or cardinality(fma_ids) = 0);
    perform t.ok('bodyparts', n = 0, 'every batch row has sources and FMA ids', n::text);

    -- admin save: a trimmed draft, logged
    perform t.as_user(adm);
    perform public.admin_save_body_part(jsonb_build_object(
        'key', k, 'kind', 'part', 'display_name', 'Test part', 'layer', 'bone',
        'fma_ids', jsonb_build_array('FMA1', 'FMA1', ' '), 'aliases', jsonb_build_array('tp'),
        'summary_plain', ' A test. ',
        'clinical', jsonb_build_array(jsonb_build_object('text', 'Line', 'disease_id', 'dengue'),
                                      jsonb_build_object('text', ' ')),
        'sources', '[]'::jsonb));
    select to_jsonb(b) into r from public.body_part_info b where key = k;
    perform t.ok('bodyparts', r ->> 'status' = 'draft' and r ->> 'summary_plain' = 'A test.',
                 'save creates a trimmed draft', r::text);
    perform t.ok('bodyparts', r -> 'fma_ids' = '["FMA1"]'::jsonb and jsonb_array_length(r -> 'clinical') = 1,
                 'blank and repeated items are dropped', r::text);
    select count(*) into n from public.admin_audit_log where target_kind = 'body_part' and target_id = k;
    perform t.ok('bodyparts', n = 1, 'save is written to the audit log');
    perform t.err('bodyparts', format('select public.admin_save_body_part(%L::jsonb)',
        jsonb_build_object('key', k, 'display_name', 'X', 'clinical',
            jsonb_build_array(jsonb_build_object('text', 'L', 'disease_id', 'no_such_disease')))),
        'does not exist', 'an unknown disease id is refused');
    perform t.err('bodyparts', format('select public.admin_save_body_part(%L::jsonb)',
        jsonb_build_object('key', k, 'display_name', 'X', 'sources',
            jsonb_build_array(jsonb_build_object('title', 'T', 'url', 'http://x.org')))),
        'https', 'a non-https source is refused');
    perform t.err('bodyparts', format('select public.admin_set_body_part_status(%L, %L)', k, 'published'),
        'at least one source', 'cannot publish without a source');
    perform t.ok('bodyparts', jsonb_array_length(public.admin_list_body_parts()) >= 55, 'admins list drafts too');

    -- publish: bumps content_version and records the reviewer; editing published text bumps again
    perform public.admin_save_body_part(jsonb_build_object('key', k || ' pub', 'display_name', 'Test part',
        'sources', jsonb_build_array(jsonb_build_object('title', 'T', 'url', 'https://example.org', 'licence', 'Public domain'))));
    select version into v0 from public.content_version where id = 1;
    perform public.admin_set_body_part_status(k || ' pub', 'published');
    select version into v1 from public.content_version where id = 1;
    perform t.ok('bodyparts', v1 = v0 + 1, 'publishing bumps content_version', v0 || ' -> ' || v1);
    perform t.ok('bodyparts', (select reviewed_by from public.body_part_info where key = k || ' pub') = adm,
                 'publishing records the reviewer');
    perform public.admin_save_body_part(jsonb_build_object('key', k || ' pub', 'display_name', 'Test part 2',
        'sources', jsonb_build_array(jsonb_build_object('title', 'T', 'url', 'https://example.org'))));
    select version into v0 from public.content_version where id = 1;
    perform t.ok('bodyparts', v0 = v1 + 1, 'editing a published entry bumps content_version');
    perform t.ok('bodyparts', (select status from public.body_part_info where key = k || ' pub') = 'published',
                 'editing keeps the status');

    -- 054: admins preview every row, drafts included
    r := public.admin_body_parts_preview();
    perform t.ok('bodyparts', jsonb_array_length(r) >= 56
                 and exists (select 1 from jsonb_array_elements(r) e where e ->> 'status' = 'draft'),
                 'admins preview drafts (054)', jsonb_array_length(r)::text);

    perform t.as_user(stu);
    perform t.err('bodyparts', 'select public.admin_body_parts_preview()', 'Only admins',
                  'students cannot preview drafts');
    perform t.err('bodyparts', format('select public.admin_save_body_part(%L::jsonb)',
        jsonb_build_object('key', k, 'display_name', 'X')), 'Only admins', 'students cannot save');
    perform t.err('bodyparts', format('select public.admin_set_body_part_status(%L, %L)', k, 'published'),
        'Only admins', 'students cannot publish');
end $$;

-- ------------------------------------------------ as a student, through RLS
set role authenticated;
select t.as_user((select v::uuid from t.bp_ids where k = 'stu'));
do $$
declare
    d text := (select v from t.bp_ids where k = 'draft');
    p text := (select v from t.bp_ids where k = 'pub');
begin
    perform t.ok('bodyparts', not exists (select 1 from public.body_part_info where key = d),
                 'students cannot see drafts');
    perform t.ok('bodyparts', not exists (select 1 from public.body_part_info where status <> 'published'),
                 'students see no batch drafts');
    perform t.ok('bodyparts', exists (select 1 from public.body_part_info where key = p),
                 'students can read published entries');
    begin update public.body_part_info set display_name = 'X' where key = p;
          perform t.ok('bodyparts', false, 'students cannot write the table directly');
    exception when insufficient_privilege then perform t.ok('bodyparts', true, 'students cannot write the table directly'); end;
end $$;
reset role;

set role anon;
do $$ begin
    perform t.ok('bodyparts', exists (select 1 from public.body_part_info
                                      where key = (select v from t.bp_ids where k = 'pub')),
                 'signed-out visitors can read published entries');
    perform t.ok('bodyparts', not exists (select 1 from public.body_part_info where status <> 'published'),
                 'signed-out visitors see no drafts');
end $$;
reset role;

-- tidy up so the 053 counts stay exact if this file is run again
delete from public.body_part_info where key like 'test part %';
select ok, label, case when not ok then detail end as detail from t.results where suite = 'bodyparts' order by id;
