-- =====================================================================
-- Akeso 007: comments on poll choices
-- Run AFTER 006_poll_answer_after_vote.sql (Supabase -> SQL Editor -> Run).
-- Safe to run again.
--
-- Every choice in a differential poll (the author's and suggested ones)
-- gets its own comment thread. A comment is an ordinary reply tagged with
-- the choice it is about, so votes, "Reply", reporting, moderation,
-- anonymity, the PHI guard, rate limits and notifications all work the
-- same as in the main discussion.
-- =====================================================================

alter table public.exchange_replies
    add column if not exists about_option_id uuid
        references public.exchange_poll_options (id) on delete set null;
create index if not exists exchange_replies_option_idx
    on public.exchange_replies (about_option_id) where about_option_id is not null;

-- Write a comment on one choice (answers to it use ex_reply with a parent).
create or replace function public.ex_option_comment(p_post uuid, p_option uuid, p_body text,
                                                    p_anonymous boolean default false)
returns uuid
language plpgsql security definer set search_path = ''
as $$
declare
    me uuid := public.ex_uid();
    p public.exchange_posts;
    option_label text;
    found_phi text;
    new_id uuid;
    my_option uuid;
    who text;
    targets uuid[];
begin
    select * into p from public.exchange_posts where id = p_post;
    if not found or not public.ex_can_see(p.status, p.author_id, me) then
        raise exception 'This post is not available.';
    end if;
    if p.status <> 'open' then raise exception 'This post is locked; no new replies.'; end if;
    perform public.ex_rate(me, 'reply', 30, interval '1 hour');
    select label into option_label from public.exchange_poll_options
    where id = p_option and post_id = p_post and status = 'active';
    if option_label is null then raise exception 'That choice is not in this poll.'; end if;
    found_phi := public.ex_phi_check(p_body);
    if found_phi is not null then
        raise exception 'This looks like it contains %. Cases must be hypothetical: remove anything that could identify a real person.', found_phi;
    end if;
    select option_id into my_option from public.exchange_poll_votes
    where post_id = p_post and user_id = me;

    insert into public.exchange_replies (post_id, parent_id, author_id, body, is_anonymous,
                                         poll_option_id, about_option_id)
    values (p_post, null, me, trim(p_body), coalesce(p_anonymous, false), my_option, p_option)
    returning id into new_id;

    update public.exchange_posts
    set reply_count = reply_count + 1, last_activity_at = now() where id = p_post;
    insert into public.exchange_follows (user_id, post_id) values (me, p_post)
    on conflict do nothing;

    who := case when p_anonymous then 'An anonymous student'
                else coalesce((select nullif(display_name, '') from public.profiles where id = me),
                              'Someone') end;
    select array_agg(user_id) into targets from public.exchange_follows where post_id = p_post;
    -- whoever suggested this choice hears about it too
    targets := targets || (select suggested_by from public.exchange_poll_options where id = p_option);
    perform public.ex_notify(targets, 'reply', p_post, new_id,
        who || ' commented on “' || public.ex_short(option_label) || '” in “'
            || public.ex_short(p.title) || '”', me);
    return new_id;
end $$;

-- ex_post: each reply says which choice it is about ('option_id'), and
-- each choice says how many comments it has ('comments').
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
                    -- comments written about this choice (007)
                    'comments', (select count(*) from public.exchange_replies c
                                 where c.about_option_id = o.id and c.parent_id is null
                                   and (c.status = 'open' or is_mod or c.author_id = me)),
                    'suggested', not o.by_author,
                    'votes', case when show_results then (select count(*) from public.exchange_poll_votes v
                                                          where v.option_id = o.id) end)
                    order by o.by_author desc, o.created_at)
                from public.exchange_poll_options o
                where o.post_id = p.id and (o.status = 'active' or is_mod)), '[]')) end,
        'replies', coalesce((select jsonb_agg(jsonb_build_object(
                'id', r.id, 'parent_id', r.parent_id,
                'option_id', r.about_option_id,
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

do $$
begin
    revoke execute on function public.ex_option_comment(uuid, uuid, text, boolean) from public, anon;
    grant execute on function public.ex_option_comment(uuid, uuid, text, boolean) to authenticated;
end $$;

notify pgrst, 'reload schema';
