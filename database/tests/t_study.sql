-- LOCAL TEST DATABASE ONLY. Never run this on the real Supabase project: it creates
-- test users and a 't' schema.

-- Study Hub, part 1 (migration 050)
delete from t.results where suite = 'study';
drop table if exists t.study_ids;
create table t.study_ids (k text primary key, v text);
grant all on t.study_ids to anon, authenticated;

do $$
declare
    x text := substr(md5(random()::text), 1, 5);
    stu uuid := t.mk_user('sstu' || x);
    other uuid := t.mk_user('soth' || x);
    edu uuid := t.mk_user('sedu' || x, 'educator');
    adm uuid := t.mk_user('sadm' || x, 'admin');
    deck uuid; v jsonb; n int;
begin
    insert into t.study_ids values ('stu', stu), ('other', other), ('edu', edu), ('adm', adm);
    perform t.ok('study', (select count(*) from public.study_subjects
                           where id in ('anatomy', 'pathology', 'pharmacology', 'microbiology')) = 4,
                 'the four subjects are there');

    -- educators save drafts, cannot publish
    perform t.as_user(edu);
    deck := public.admin_save_deck(jsonb_build_object(
        'title', 'Antibiotics ' || x, 'subject_id', 'pharmacology',
        'cards', jsonb_build_array(
            jsonb_build_object('type', 'basic', 'front', 'Drug class of amoxicillin?', 'back', 'Penicillin'),
            jsonb_build_object('type', 'mcq', 'front', 'Which is a macrolide?',
                               'choices', jsonb_build_array(
                                   jsonb_build_object('text', 'Azithromycin', 'correct', true, 'rationale', 'A macrolide.'),
                                   jsonb_build_object('text', 'Amoxicillin', 'correct', false, 'rationale', 'A penicillin.'))),
            jsonb_build_object('type', 'cloze', 'cloze_text', 'Amoxicillin is a {{c1::penicillin}}.'))));
    insert into t.study_ids values ('deck', deck);
    perform t.ok('study', (select status from public.decks where id = deck) = 'draft', 'an educator''s deck is a draft');
    perform t.ok('study', (select count(*) from public.cards where deck_id = deck) = 3, 'its three cards are saved');
    perform t.err('study', format('select public.admin_set_deck_status(%L, ''published'')', deck),
                  'Only admins', 'an educator cannot publish');
    perform t.err('study', format('select public.admin_save_deck(%L)', jsonb_build_object(
        'title', 'Bad', 'cards', jsonb_build_array(jsonb_build_object('type', 'mcq', 'front', 'Q?',
            'choices', jsonb_build_array(jsonb_build_object('text', 'A', 'correct', false),
                                         jsonb_build_object('text', 'B', 'correct', false)))))),
                  'at least one choice', 'an MCQ with no correct choice is refused');
    perform t.err('study', format('select public.admin_save_deck(%L)', jsonb_build_object(
        'title', 'Bad', 'cards', jsonb_build_array(jsonb_build_object('type', 'cloze', 'cloze_text', 'no blanks')))),
                  '{{blank}}', 'a cloze with no blank is refused');

    -- students cannot use the staff functions
    perform t.as_user(stu);
    perform t.err('study', 'select public.admin_list_decks()', 'Only educators and admins', 'a student cannot list official drafts');

    -- admins publish; that changes content_version and is in the audit trail
    perform t.as_user(adm);
    select version into n from public.content_version where id = 1;
    perform public.admin_set_deck_status(deck, 'published');
    perform t.ok('study', (select version from public.content_version where id = 1) = n + 1,
                 'publishing bumps content_version');
    perform t.ok('study', exists (select 1 from public.admin_audit_log
                                  where target_id = deck::text and action = 'publish'), 'publishing is logged');

    -- once published, an educator can no longer edit it
    perform t.as_user(edu);
    perform t.err('study', format('select public.admin_save_deck(%L)', jsonb_build_object('id', deck, 'title', 'Changed')),
                  'Ask an admin', 'an educator cannot edit a published deck');

    -- an admin removes a card: it is deleted softly
    perform t.as_user(adm);
    v := public.admin_get_deck(deck);
    perform public.admin_save_deck(jsonb_build_object('id', deck, 'title', 'Antibiotics ' || x,
        'subject_id', 'pharmacology', 'cards', jsonb_build_array(v -> 'cards' -> 0, v -> 'cards' -> 1)));
    perform t.ok('study', (select count(*) from public.cards where deck_id = deck and deleted_at is not null) = 1,
                 'a card left out is soft-deleted');

    -- reports
    perform t.as_user(stu);
    perform public.report_card((v -> 'cards' -> 0 ->> 'id'), 'wrong', 'Not a penicillin?');
    perform public.report_card('auto:medicine:amoxicillin:class', 'typo', '');
    perform t.as_user(edu);
    perform t.ok('study', jsonb_array_length(public.admin_list_card_reports()) >= 2, 'staff see open card reports');
end $$;

-- ------------------------------------------------ as the student, through RLS
set role authenticated;
select t.as_user((select v::uuid from t.study_ids where k = 'stu'));
do $$
declare
    stu uuid := (select v::uuid from t.study_ids where k = 'stu');
    official uuid := (select v::uuid from t.study_ids where k = 'deck');
    mine uuid; n int;
begin
    perform t.ok('study', exists (select 1 from public.decks where id = official), 'a student sees the published deck');
    perform t.ok('study', (select count(*) from public.cards where deck_id = official and deleted_at is null) = 2,
                 'and its cards');
    insert into public.decks (title, origin, owner_id) values ('My cards', 'personal', stu) returning id into mine;
    insert into t.study_ids values ('mine', mine);
    insert into public.cards (deck_id, type, front, back) values (mine, 'basic', 'Front', 'Back');
    perform t.ok('study', (select count(*) from public.cards where deck_id = mine) = 1, 'a student adds a card to their deck');
    begin
        insert into public.cards (deck_id, type, front, back) values (official, 'basic', 'Sneaky', 'Edit');
        perform t.ok('study', false, 'a student cannot add to an official deck');
    exception when others then
        perform t.ok('study', true, 'a student cannot add to an official deck');
    end;
    begin
        insert into public.decks (title, origin, owner_id, status) values ('Fake', 'official', null, 'published');
        perform t.ok('study', false, 'a student cannot make an official deck');
    exception when others then
        perform t.ok('study', true, 'a student cannot make an official deck');
    end;
    update public.decks set title = 'Renamed' where id = official;
    get diagnostics n = row_count;
    perform t.ok('study', n = 0, 'a student cannot rename an official deck');

    -- states, history (idempotent by client_id) and settings
    insert into public.card_states (user_id, card_key, state, due, interval_days)
    values (stu, 'auto:medicine:amoxicillin:class', 'review', now() + interval '3 days', 3);
    insert into public.review_log (user_id, card_key, rating, reviewed_at, client_id)
    values (stu, 'auto:medicine:amoxicillin:class', 3, now(), '00000000-0000-0000-0000-0000000000a1')
    on conflict (client_id) do nothing;
    insert into public.review_log (user_id, card_key, rating, reviewed_at, client_id)
    values (stu, 'auto:medicine:amoxicillin:class', 3, now(), '00000000-0000-0000-0000-0000000000a1')
    on conflict (client_id) do nothing;
    perform t.ok('study', (select count(*) from public.review_log
                           where client_id = '00000000-0000-0000-0000-0000000000a1') = 1,
                 'uploading the same review twice keeps one row');
    insert into public.study_settings (user_id, new_per_day) values (stu, 15)
    on conflict (user_id) do update set new_per_day = 15;
    perform t.ok('study', (select new_per_day from public.study_settings where user_id = stu) = 15, 'settings are saved');
    begin
        update public.review_log set rating = 1 where user_id = stu;
        perform t.ok('study', false, 'review history cannot be changed');
    exception when insufficient_privilege then
        perform t.ok('study', true, 'review history cannot be changed');
    end;
    begin
        perform count(*) from public.card_reports;
        perform t.ok('study', false, 'reports are not readable directly');
    exception when insufficient_privilege then
        perform t.ok('study', true, 'reports are not readable directly');
    end;
end $$;

-- ------------------------------------------------ another student sees nothing of it
select t.as_user((select v::uuid from t.study_ids where k = 'other'));
do $$
declare mine uuid := (select v::uuid from t.study_ids where k = 'mine');
begin
    perform t.ok('study', not exists (select 1 from public.decks where id = mine), 'another student cannot see my deck');
    perform t.ok('study', not exists (select 1 from public.cards where deck_id = mine), 'or its cards');
    perform t.ok('study', (select count(*) from public.card_states) = 0, 'or my progress');
    perform t.ok('study', (select count(*) from public.review_log) = 0, 'or my review history');
end $$;

-- ------------------------------------------------ educators cannot see students' progress either
select t.as_user((select v::uuid from t.study_ids where k = 'edu'));
do $$ begin
    perform t.ok('study', (select count(*) from public.card_states) = 0, 'an educator cannot read students'' progress');
    perform t.ok('study', (select count(*) from public.review_log) = 0, 'or their review history');
end $$;
reset role;

set role anon;
do $$ begin
    perform t.ok('study', (select count(*) from public.study_subjects) >= 4, 'subjects are readable signed out');
    begin perform count(*) from public.decks; perform t.ok('study', false, 'decks need sign-in');
    exception when insufficient_privilege then perform t.ok('study', true, 'decks need sign-in'); end;
end $$;
reset role;

select ok, label, case when not ok then detail end as detail from t.results where suite = 'study' order by id;
