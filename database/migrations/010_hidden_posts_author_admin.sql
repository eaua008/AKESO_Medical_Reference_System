-- =====================================================================
-- 010_hidden_posts_author_admin.sql  -  hidden / removed content is seen
-- only by its author and admins
-- =====================================================================
-- Run AFTER 009_auto_handles.sql. Safe to run more than once.
--
-- Before: a post or reply that a moderator hid or removed was still shown
-- (with a red "Hidden by a moderator" / "Removed by a moderator" pill) to
-- every educator and admin. Now:
--   * posts:   open / locked -> everyone; hidden / removed -> the author
--              and admins only (educators no longer see them in the feed or
--              open them),
--   * replies, option comments and poll suggestions: the same rule,
--   * educators still moderate: Moderation queue, hide, remove, verify.
--     Unhiding / restoring something that is already hidden is done by an
--     admin (or from the Admin panel).
-- =====================================================================

create or replace function public.ex_is_admin(p_user uuid)
returns boolean
language sql stable security definer set search_path = ''
as $$
    select exists (select 1 from public.user_roles r
                   where r.user_id = p_user and r.role = 'admin');
$$;

-- Can this viewer see this post at all?
create or replace function public.ex_can_see(p_status text, p_author uuid, p_viewer uuid)
returns boolean
language sql stable security definer set search_path = ''
as $$
    select p_status in ('open', 'locked')
        or p_author = p_viewer
        or public.ex_is_admin(p_viewer);
$$;

-- ex_post (latest version from 007) with the same rule for replies,
-- option comments and suggested choices.
create or replace function public.ex_post(p_id uuid)
returns jsonb
language plpgsql stable security definer set search_path = ''
as $$
declare
    me uuid := public.ex_uid();
    p public.exchange_posts;
    is_mod boolean := public.ex_is_mod(me);
    -- hidden / removed replies and suggestions: their author and admins only (010)
    is_admin boolean := public.ex_is_admin(me);
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
                                   and (c.status = 'open' or is_admin or c.author_id = me)),
                    'suggested', not o.by_author,
                    'votes', case when show_results then (select count(*) from public.exchange_poll_votes v
                                                          where v.option_id = o.id) end)
                    order by o.by_author desc, o.created_at)
                from public.exchange_poll_options o
                where o.post_id = p.id and (o.status = 'active' or is_admin)), '[]')) end,
        'replies', coalesce((select jsonb_agg(jsonb_build_object(
                'id', r.id, 'parent_id', r.parent_id,
                'option_id', r.about_option_id,
                'body', case when r.status = 'removed' and not is_admin then '' else r.body end,
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
              and (r.status = 'open' or is_admin or r.author_id = me
                   or (r.status = 'removed' and exists (select 1 from public.exchange_replies c
                                                        where c.parent_id = r.id)))), '[]'))
    into result;
    return result;
end $$;

do $$
begin
    -- internal helpers, like ex_is_mod: not callable from the app
    revoke execute on function public.ex_is_admin(uuid) from public, anon, authenticated;
    revoke execute on function public.ex_can_see(text, uuid, uuid) from public, anon, authenticated;
    revoke execute on function public.ex_post(uuid) from public, anon;
    grant execute on function public.ex_post(uuid) to authenticated;
end $$;

notify pgrst, 'reload schema';
