-- =====================================================================
-- Akeso 006: differential poll - the answer shows only after you vote
-- Run AFTER 003_clinical_exchange.sql (Supabase -> SQL Editor -> Run).
-- Safe to run again.
--
-- Before: once the author revealed the intended answer, everyone saw it
-- (and the vote counts), and nobody could vote any more.
-- Now:
--   * results, the intended answer and "Why" are sent only to people who
--     have voted (the author and moderators always see them);
--   * a student who has not voted yet can still cast one vote after the
--     reveal, and then sees the answer. Votes cast before the reveal stay
--     final, as before.
-- Only ex_post and ex_poll_vote change; grants carry over.
-- =====================================================================

create or replace function public.ex_post(p_id uuid)
returns jsonb
language plpgsql stable security definer set search_path = ''
as $$
declare
    me uuid := public.ex_uid();
    p public.exchange_posts;
    is_mod boolean := public.ex_is_mod(me);
    my_option uuid;
    show_results boolean;
    result jsonb;
begin
    select * into p from public.exchange_posts where id = p_id;
    if not found or not public.ex_can_see(p.status, p.author_id, me) then
        raise exception 'This post is not available.';
    end if;
    select option_id into my_option from public.exchange_poll_votes
    where post_id = p.id and user_id = me;
    -- Results, the intended answer and the explanation are for people who
    -- have voted (and the author / moderators). Before that, a student only
    -- sees the choices, even after the author revealed the answer.
    show_results := my_option is not null or p.author_id = me or is_mod;

    select jsonb_build_object(
        'id', p.id, 'kind', p.kind, 'title', p.title, 'body', p.body, 'question', p.question,
        'author', public.ex_author(p.author_id, p.is_anonymous, me),
        'is_anonymous', p.is_anonymous,
        'age_range', p.age_range, 'sex', p.sex, 'setting', p.setting, 'vitals', p.vitals,
        'case_data', p.case_data, 'source', p.source, 'status', p.status,
        'score', p.score, 'reply_count', p.reply_count,
        'created_at', p.created_at, 'edited_at', p.edited_at,
        'best_reply_id', p.best_reply_id,
        'voted', exists (select 1 from public.exchange_votes v where v.user_id = me
                         and v.target_kind = 'post' and v.target_id = p.id),
        'following', exists (select 1 from public.exchange_follows f
                             where f.user_id = me and f.post_id = p.id),
        'is_author', p.author_id = me, 'can_moderate', is_mod,
        'tags', coalesce((select jsonb_agg(jsonb_build_object('kind', t.kind, 'id', t.ref_id,
                                                              'label', t.label) order by t.kind, t.label)
                          from public.exchange_post_tags t where t.post_id = p.id), '[]'),
        'poll', case when not p.has_poll then null else jsonb_build_object(
            'my_option', my_option,
            'show_results', show_results,
            'revealed', p.revealed_option_id is not null,
            'revealed_option', case when show_results then p.revealed_option_id end,
            'explanation', case when show_results and p.revealed_option_id is not null
                                then p.reveal_explanation end,
            'total', case when show_results then (select count(*) from public.exchange_poll_votes
                                                  where post_id = p.id) end,
            'options', coalesce((select jsonb_agg(jsonb_build_object(
                    'id', o.id, 'label', o.label, 'disease_id', o.disease_id,
                    'by_author', o.by_author,
                    'suggested', not o.by_author,
                    'votes', case when show_results then (select count(*) from public.exchange_poll_votes v
                                                          where v.option_id = o.id) end)
                    order by o.by_author desc, o.created_at)
                from public.exchange_poll_options o
                where o.post_id = p.id and (o.status = 'active' or is_mod)), '[]')) end,
        'replies', coalesce((select jsonb_agg(jsonb_build_object(
                'id', r.id, 'parent_id', r.parent_id,
                'body', case when r.status = 'removed' and not is_mod then '' else r.body end,
                'status', r.status,
                'author', public.ex_author(r.author_id, r.is_anonymous, me),
                'score', r.score, 'created_at', r.created_at, 'edited_at', r.edited_at,
                'voted', exists (select 1 from public.exchange_votes v where v.user_id = me
                                 and v.target_kind = 'reply' and v.target_id = r.id),
                'is_best', r.id = p.best_reply_id,
                'verified', r.verified_at is not null,
                -- the poll badge: what they had voted when they wrote it, and now
                'voted_label', (select o.label from public.exchange_poll_options o
                                where o.id = r.poll_option_id),
                'current_label', (select o.label from public.exchange_poll_votes pv
                                  join public.exchange_poll_options o on o.id = pv.option_id
                                  where pv.post_id = p.id and pv.user_id = r.author_id),
                'is_mine', r.author_id = me)
                order by r.created_at)
            from public.exchange_replies r
            where r.post_id = p.id
              and (r.status = 'open' or is_mod or r.author_id = me
                   or (r.status = 'removed' and exists (select 1 from public.exchange_replies c
                                                        where c.parent_id = r.id)))), '[]'))
    into result;
    return result;
end $$;

create or replace function public.ex_poll_vote(p_post uuid, p_option uuid)
returns void
language plpgsql security definer set search_path = ''
as $$
declare
    me uuid := public.ex_uid();
    p public.exchange_posts;
begin
    select * into p from public.exchange_posts where id = p_post;
    if not found or not public.ex_can_see(p.status, p.author_id, me) then
        raise exception 'This post is not available.';
    end if;
    if p.author_id = me then raise exception 'You wrote this case, so you can''t vote on it.'; end if;
    if p.status <> 'open' then
        raise exception 'The poll is closed.';
    end if;
    -- After the reveal: one last vote for students who have not voted yet,
    -- which unlocks the answer for them. Votes cast before can't change.
    if p.revealed_option_id is not null and exists (
            select 1 from public.exchange_poll_votes where post_id = p_post and user_id = me) then
        raise exception 'The answer is revealed, so your vote is final.';
    end if;
    if p.revealed_option_id is not null and p_option is null then
        raise exception 'The answer is revealed. Pick a choice to see it.';
    end if;
    if p_option is null then
        delete from public.exchange_poll_votes where post_id = p_post and user_id = me;
        return;
    end if;
    if not exists (select 1 from public.exchange_poll_options
                   where id = p_option and post_id = p_post and status = 'active') then
        raise exception 'That choice is not in this poll.';
    end if;
    insert into public.exchange_poll_votes (post_id, user_id, option_id) values (p_post, me, p_option)
    on conflict (post_id, user_id) do update set option_id = excluded.option_id, voted_at = now();
    update public.exchange_posts set last_activity_at = now() where id = p_post;
end $$;

notify pgrst, 'reload schema';
