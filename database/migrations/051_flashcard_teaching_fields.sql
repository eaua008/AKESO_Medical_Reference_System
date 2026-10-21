-- =====================================================================
-- Akeso migration 051: flashcards that teach (Study Hub)
-- =====================================================================
-- Run AFTER 050. Safe to run again (adds columns, replaces functions).
--
--   cards       answer_short, explanation, distinguish, hint, difficulty:
--               the back of a card in sections (Answer, Why, Don't confuse
--               with) and a hint, for your own decks and official decks.
--               (Auto cards are made on each computer and are not stored.)
--   review_log  hinted: whether the hint was shown before answering
--
-- admin_save_deck / admin_get_deck read and write the new fields.
-- =====================================================================

begin;

alter table public.cards add column if not exists answer_short text not null default '';
alter table public.cards add column if not exists explanation  text not null default '';
alter table public.cards add column if not exists distinguish  text not null default '';
alter table public.cards add column if not exists hint         text not null default '';
alter table public.cards add column if not exists difficulty   text not null default '';
alter table public.review_log add column if not exists hinted boolean not null default false;

do $$
begin
    if not exists (select 1 from pg_constraint where conname = 'cards_teaching_lengths') then
        alter table public.cards add constraint cards_teaching_lengths check (
            char_length(answer_short) <= 300 and char_length(explanation) <= 2000
            and char_length(distinguish) <= 2000 and char_length(hint) <= 200);
    end if;
    if not exists (select 1 from pg_constraint where conname = 'cards_difficulty_check') then
        alter table public.cards add constraint cards_difficulty_check
            check (difficulty in ('', 'basic', 'clinical', 'advanced'));
    end if;
end $$;

create or replace function public.st_card_json(c public.cards)
returns jsonb
language sql stable security definer set search_path = ''
as $$
    select jsonb_build_object(
        'id', c.id, 'type', c.type, 'front', c.front, 'back', c.back,
        'choices', c.choices, 'cloze_text', c.cloze_text, 'part_ids', to_jsonb(c.part_ids),
        'source_kind', c.source_kind, 'source_id', c.source_id, 'tags', to_jsonb(c.tags),
        'position', c.position, 'updated_at', c.updated_at,
        'answer_short', c.answer_short, 'explanation', c.explanation,
        'distinguish', c.distinguish, 'hint', c.hint, 'difficulty', c.difficulty);
$$;
revoke execute on function public.st_card_json(public.cards) from public, anon, authenticated;

-- Same as 050, plus the five teaching fields.
create or replace function public.admin_save_deck(p jsonb)
returns uuid
language plpgsql security definer set search_path = ''
as $$
declare
    me uuid := public.st_staff();
    v_id uuid := nullif(p ->> 'id', '')::uuid;
    v_title text := btrim(coalesce(p ->> 'title', ''));
    v_status text;
    v_new boolean := false;
    v_keep uuid[] := '{}';
    c jsonb;
    v_card uuid;
    pos integer := 0;
begin
    if v_title = '' then raise exception 'Give the deck a title.'; end if;
    if char_length(v_title) > 120 then raise exception 'Keep the title under 120 letters.'; end if;
    if jsonb_typeof(coalesce(p -> 'cards', '[]'::jsonb)) <> 'array' then
        raise exception 'The cards could not be read.';
    end if;
    if jsonb_array_length(coalesce(p -> 'cards', '[]'::jsonb)) > 2000 then
        raise exception 'A deck can hold up to 2,000 cards.';
    end if;

    if v_id is null or not exists (select 1 from public.decks where id = v_id) then
        v_new := true;
        insert into public.decks (id, title, origin, owner_id, status, created_by, updated_by)
        values (coalesce(v_id, gen_random_uuid()), v_title, 'official', null, 'draft', me, me)
        returning id into v_id;
    else
        select status into v_status from public.decks
        where id = v_id and origin = 'official' and deleted_at is null;
        if v_status is null then raise exception 'That deck no longer exists.'; end if;
        if v_status = 'published' and not public.is_admin() then
            raise exception 'This deck is published. Ask an admin to unpublish it before editing.';
        end if;
    end if;

    update public.decks set
        title = v_title,
        description = left(btrim(coalesce(p ->> 'description', '')), 1000),
        subject_id = nullif(p ->> 'subject_id', ''),
        updated_by = me,
        updated_at = now()
    where id = v_id;

    for c in select * from jsonb_array_elements(coalesce(p -> 'cards', '[]'::jsonb)) loop
        pos := pos + 1;
        v_card := nullif(c ->> 'id', '')::uuid;
        if v_card is not null and exists (select 1 from public.cards where id = v_card and deck_id = v_id) then
            update public.cards set
                type = c ->> 'type', front = coalesce(c ->> 'front', ''),
                back = coalesce(c ->> 'back', ''),
                choices = coalesce(c -> 'choices', '[]'::jsonb),
                cloze_text = coalesce(c ->> 'cloze_text', ''),
                part_ids = coalesce((select array_agg(x) from jsonb_array_elements_text(c -> 'part_ids') x), '{}'),
                source_kind = nullif(c ->> 'source_kind', ''), source_id = nullif(c ->> 'source_id', ''),
                tags = coalesce((select array_agg(x) from jsonb_array_elements_text(c -> 'tags') x), '{}'),
                answer_short = coalesce(c ->> 'answer_short', ''), explanation = coalesce(c ->> 'explanation', ''),
                distinguish = coalesce(c ->> 'distinguish', ''), hint = coalesce(c ->> 'hint', ''),
                difficulty = coalesce(c ->> 'difficulty', ''),
                position = pos, deleted_at = null, updated_at = now()
            where id = v_card;
        else
            insert into public.cards (id, deck_id, type, front, back, choices, cloze_text, part_ids,
                                      source_kind, source_id, tags, position,
                                      answer_short, explanation, distinguish, hint, difficulty)
            values (coalesce(v_card, gen_random_uuid()), v_id, c ->> 'type', coalesce(c ->> 'front', ''),
                    coalesce(c ->> 'back', ''), coalesce(c -> 'choices', '[]'::jsonb),
                    coalesce(c ->> 'cloze_text', ''),
                    coalesce((select array_agg(x) from jsonb_array_elements_text(c -> 'part_ids') x), '{}'),
                    nullif(c ->> 'source_kind', ''), nullif(c ->> 'source_id', ''),
                    coalesce((select array_agg(x) from jsonb_array_elements_text(c -> 'tags') x), '{}'), pos,
                    coalesce(c ->> 'answer_short', ''), coalesce(c ->> 'explanation', ''),
                    coalesce(c ->> 'distinguish', ''), coalesce(c ->> 'hint', ''), coalesce(c ->> 'difficulty', ''))
            returning id into v_card;
        end if;
        v_keep := v_keep || v_card;
    end loop;

    update public.cards set deleted_at = now(), updated_at = now()
    where deck_id = v_id and deleted_at is null and not (id = any (v_keep));

    if v_status = 'published' then
        perform public.ad_bump();
    end if;
    perform public.ad_log(case when v_new then 'create' else 'update' end, 'deck', v_id::text, v_title);
    return v_id;
end $$;

revoke execute on function public.admin_save_deck(jsonb) from public, anon;
grant execute on function public.admin_save_deck(jsonb) to authenticated;

commit;

notify pgrst, 'reload schema';
