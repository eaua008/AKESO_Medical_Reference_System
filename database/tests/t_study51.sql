-- LOCAL TEST DATABASE ONLY.
-- Migration 051: teaching fields on cards, "hinted" on reviews
delete from t.results where suite = 'study51';
do $$
declare
    x text := substr(md5(random()::text), 1, 5);
    edu uuid := t.mk_user('t51e' || x, 'educator');
    stu uuid := t.mk_user('t51s' || x);
    deck uuid; v jsonb;
begin
    perform t.as_user(edu);
    deck := public.admin_save_deck(jsonb_build_object('title', 'Teach ' || x, 'cards', jsonb_build_array(
        jsonb_build_object('type', 'basic', 'front', 'Q?', 'back', 'A', 'answer_short', 'A',
                           'explanation', 'Because.', 'distinguish', 'X: y', 'hint', 'Starts with A',
                           'difficulty', 'clinical'))));
    v := public.admin_get_deck(deck);
    perform t.ok('study51', v -> 'cards' -> 0 ->> 'explanation' = 'Because.', 'teaching fields are saved and read back', v::text);
    perform t.ok('study51', v -> 'cards' -> 0 ->> 'difficulty' = 'clinical', 'difficulty too');
    perform t.err('study51', format('select public.admin_save_deck(%L)', jsonb_build_object('title', 'Bad',
        'cards', jsonb_build_array(jsonb_build_object('type', 'basic', 'front', 'Q', 'back', 'A', 'difficulty', 'impossible')))),
        'cards_difficulty_check', 'an unknown difficulty is refused');
    perform t.as_user(stu);
    insert into public.review_log (user_id, card_key, rating, reviewed_at, client_id, hinted)
    values (stu, 'auto2:x', 3, now(), gen_random_uuid(), true);
    perform t.ok('study51', exists (select 1 from public.review_log where user_id = stu and hinted), 'hinted is stored');
end $$;
select ok, label, case when not ok then detail end as detail from t.results where suite = 'study51' order by id;
