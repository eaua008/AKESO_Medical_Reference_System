-- =====================================================================
-- Akeso 008: member profiles for Clinical Exchange
-- Run AFTER 007_poll_option_comments.sql (Supabase -> SQL Editor -> Run).
-- Safe to run again.
--
-- What it adds
--   * Profile visibility: public (everyone signed in) / members (verified
--     students and educators only) / private (name only). The old
--     is_public switch is kept in step automatically.
--   * Per-section switches: photo, stats, activity, last active (school and
--     program already existed).
--   * ex_profile(handle): the full profile page (stats, poll accuracy,
--     badges, topics, recent posts and replies). Anonymous posts and replies
--     are NEVER counted or listed, so anonymity cannot be undone.
--   * Following people: notified when someone you follow posts.
--   * Reporting a profile; moderators can make it private or clear the bio.
--   * Profile photos visible to others only when the owner allows it.
-- =====================================================================

-- ---------------------------------------------------------------------
-- 1. Profile columns
-- ---------------------------------------------------------------------
alter table public.profiles
    add column if not exists visibility       text    not null default 'private',
    add column if not exists show_photo       boolean not null default false,
    add column if not exists show_stats       boolean not null default true,
    add column if not exists show_activity    boolean not null default true,
    add column if not exists show_last_active boolean not null default true;

do $$
begin
    if not exists (select 1 from pg_constraint where conname = 'profiles_visibility_check') then
        alter table public.profiles add constraint profiles_visibility_check
            check (visibility in ('public', 'members', 'private'));
    end if;
end $$;

-- Existing public profiles stay public.
update public.profiles set visibility = 'public' where is_public and visibility = 'private';

-- Keep is_public and visibility in step, whichever one an app changes.
create or replace function public.profiles_sync_visibility()
returns trigger
language plpgsql set search_path = ''
as $$
begin
    if tg_op = 'INSERT' then
        if new.visibility = 'private' and new.is_public then new.visibility := 'public'; end if;
    elsif new.visibility is distinct from old.visibility then
        null;                                   -- visibility wins
    elsif new.is_public is distinct from old.is_public then
        new.visibility := case when new.is_public then 'public' else 'private' end;
    end if;
    new.is_public := new.visibility <> 'private';
    return new;
end $$;

drop trigger if exists profiles_sync_visibility on public.profiles;
create trigger profiles_sync_visibility before insert or update on public.profiles
    for each row execute function public.profiles_sync_visibility();

-- The app may change the new switches on its own row.
grant update (visibility, show_photo, show_stats, show_activity, show_last_active)
    on public.profiles to authenticated;

-- ---------------------------------------------------------------------
-- 2. Who may open whose profile
-- ---------------------------------------------------------------------
create or replace function public.ex_profile_access(p_target uuid, p_viewer uuid)
returns text            -- null = allowed, otherwise the reason it isn't
language sql stable security definer set search_path = ''
as $$
    select case
        when p.id is null or p.deletion_scheduled_for is not null then 'This profile is not available.'
        when p.id = p_viewer or public.ex_is_mod(p_viewer) then null
        when p.visibility = 'public' then null
        when p.visibility = 'members' and (
                exists (select 1 from public.profiles v where v.id = p_viewer
                        and v.school_email_verified_at is not null)
             or exists (select 1 from public.user_roles r where r.user_id = p_viewer
                        and r.role::text in ('educator', 'admin'))) then null
        when p.visibility = 'members' then
            'Only verified students and educators can see this profile. Verify your school email in Account Settings.'
        else 'This profile is private.'
    end
    from (select 1) one left join public.profiles p on p.id = p_target;
$$;

-- Author lines: the @handle (which opens the profile) shows unless the
-- profile is private or the post is anonymous.
create or replace function public.ex_author(p_author uuid, p_anon boolean, p_viewer uuid)
returns jsonb
language sql stable security definer set search_path = ''
as $$
    select case
        when p_anon and p_viewer <> p_author and not public.ex_is_mod(p_viewer) then
            jsonb_build_object('name', 'Anonymous student', 'anonymous', true)
        else jsonb_build_object(
            'name', coalesce(nullif(p.display_name, ''), 'Akeso student'),
            'anonymous', p_anon,
            'handle', case when p.visibility <> 'private' and not p_anon then p.handle end,
            'program', case when p.show_program and not p_anon then p.program end,
            'verified_domain', case when not p_anon and p.school_email_verified_at is not null
                                    then p.school_email_domain end,
            'role', case when not p_anon then (select r.role::text from public.user_roles r
                                               where r.user_id = p_author) end,
            'is_me', p_viewer = p_author)
        end
    from public.profiles p where p.id = p_author;
$$;

-- ---------------------------------------------------------------------
-- 3. Following people
-- ---------------------------------------------------------------------
create table if not exists public.exchange_user_follows (
    follower_id  uuid not null references auth.users (id) on delete cascade,
    followee_id  uuid not null references auth.users (id) on delete cascade,
    created_at   timestamptz not null default now(),
    primary key (follower_id, followee_id),
    check (follower_id <> followee_id)
);
create index if not exists exchange_user_follows_followee_idx
    on public.exchange_user_follows (followee_id);
alter table public.exchange_user_follows enable row level security;
revoke all on public.exchange_user_follows from anon, authenticated;

alter table public.notifications drop constraint if exists notifications_kind_check;
alter table public.notifications add constraint notifications_kind_check
    check (kind in ('reply', 'best_answer', 'verified', 'reveal', 'moderation', 'mention',
                    'new_post'));

create or replace function public.ex_follow_user(p_handle text, p_on boolean)
returns boolean
language plpgsql security definer set search_path = ''
as $$
declare
    me uuid := public.ex_uid();
    target uuid;
    denied text;
begin
    select id into target from public.profiles where lower(handle) = lower(p_handle);
    denied := public.ex_profile_access(target, me);
    if denied is not null then raise exception '%', denied; end if;
    if target = me then raise exception 'You can''t follow yourself.'; end if;
    if p_on then
        insert into public.exchange_user_follows (follower_id, followee_id) values (me, target)
        on conflict do nothing;
    else
        delete from public.exchange_user_follows where follower_id = me and followee_id = target;
    end if;
    return p_on;
end $$;

-- New (non-anonymous) post -> tell the author's followers.
create or replace function public.ex_notify_followers()
returns trigger
language plpgsql security definer set search_path = ''
as $$
declare
    who text;
    targets uuid[];
begin
    if new.is_anonymous or new.status <> 'open' then return new; end if;
    select array_agg(follower_id) into targets
    from public.exchange_user_follows where followee_id = new.author_id;
    if targets is null then return new; end if;
    select coalesce(nullif(display_name, ''), 'Someone') into who
    from public.profiles where id = new.author_id;
    perform public.ex_notify(targets, 'new_post', new.id, null,
        who || ' posted ' || case when new.kind = 'case' then 'a new case' else 'a question' end
        || ': “' || public.ex_short(new.title) || '”', new.author_id);
    return new;
end $$;

drop trigger if exists exchange_posts_notify_followers on public.exchange_posts;
create trigger exchange_posts_notify_followers after insert on public.exchange_posts
    for each row execute function public.ex_notify_followers();

-- ---------------------------------------------------------------------
-- 4. The profile page
-- ---------------------------------------------------------------------
create or replace function public.ex_profile(p_handle text)
returns jsonb
language plpgsql stable security definer set search_path = ''
as $$
declare
    me uuid := public.ex_uid();
    pr public.profiles;
    denied text;
    full_view boolean;                    -- the owner or a moderator sees every section
    see_stats boolean;
    see_activity boolean;
    v_posts int; v_cases int; v_questions int; v_replies int;
    v_best int; v_verified int; v_helpful int;
    v_poll_total int; v_poll_right int;
    badges jsonb := '[]'::jsonb;
    top_topic record;
    result jsonb;
begin
    select * into pr from public.profiles where lower(handle) = lower(p_handle);
    denied := public.ex_profile_access(pr.id, me);
    if denied is not null then raise exception '%', denied; end if;
    full_view := pr.id = me or public.ex_is_mod(me);
    see_stats := full_view or pr.show_stats;
    see_activity := full_view or pr.show_activity;

    result := jsonb_build_object(
        'id', pr.id,
        'handle', pr.handle,
        'display_name', coalesce(nullif(pr.display_name, ''), 'Akeso student'),
        'bio', pr.bio,
        'interests', to_jsonb(pr.interests),
        'role', (select role::text from public.user_roles where user_id = pr.id),
        'program', case when full_view or pr.show_program then pr.program end,
        'year_level', case when full_view or pr.show_program then pr.year_level end,
        'school', case when full_view or pr.show_school then pr.school end,
        'verified_domain', case when pr.school_email_verified_at is not null
                                then pr.school_email_domain end,
        'avatar_path', case when (full_view or pr.show_photo) then pr.avatar_path end,
        'member_since', pr.created_at,
        'last_active', case when full_view or pr.show_last_active
                            then (select u.last_sign_in_at from auth.users u where u.id = pr.id) end,
        'visibility', pr.visibility,
        'is_me', pr.id = me,
        'can_moderate', public.ex_is_mod(me),
        'following', exists (select 1 from public.exchange_user_follows
                             where follower_id = me and followee_id = pr.id),
        'followers', (select count(*) from public.exchange_user_follows where followee_id = pr.id),
        'shows', jsonb_build_object('stats', see_stats, 'activity', see_activity,
                                    'photo', full_view or pr.show_photo,
                                    'school', full_view or pr.show_school,
                                    'program', full_view or pr.show_program,
                                    'last_active', full_view or pr.show_last_active));

    if see_stats then
        -- Only non-anonymous, visible posts and replies count.
        select count(*), count(*) filter (where kind = 'case'), count(*) filter (where kind <> 'case'),
               coalesce(sum(score), 0)
          into v_posts, v_cases, v_questions, v_helpful
          from public.exchange_posts
         where author_id = pr.id and not is_anonymous and status in ('open', 'locked');
        select count(*), coalesce(sum(score), 0) + v_helpful,
               count(*) filter (where verified_at is not null)
          into v_replies, v_helpful, v_verified
          from public.exchange_replies
         where author_id = pr.id and not is_anonymous and status = 'open';
        select count(*) into v_best
          from public.exchange_posts p join public.exchange_replies r on r.id = p.best_reply_id
         where r.author_id = pr.id and not r.is_anonymous and r.status = 'open';
        -- Poll accuracy: votes on polls whose answer is revealed.
        select count(*), count(*) filter (where v.option_id = p.revealed_option_id)
          into v_poll_total, v_poll_right
          from public.exchange_poll_votes v join public.exchange_posts p on p.id = v.post_id
         where v.user_id = pr.id and p.revealed_option_id is not null
           and p.status in ('open', 'locked');

        -- Badges: plain milestones from the numbers above.
        if v_cases >= 1 then badges := badges || jsonb_build_object(
            'key', 'first_case', 'label', 'First case', 'detail', 'Posted a case for discussion'); end if;
        if v_best >= 1 then badges := badges || jsonb_build_object(
            'key', 'best_answer', 'label', 'Best answer', 'detail', 'Had a reply chosen as the best answer'); end if;
        if v_verified >= 10 then badges := badges || jsonb_build_object(
            'key', 'verified_10', 'label', '10 verified replies', 'detail', 'Ten replies verified by educators');
        elsif v_verified >= 1 then badges := badges || jsonb_build_object(
            'key', 'verified_1', 'label', 'Educator verified', 'detail', 'A reply verified by an educator'); end if;
        if v_helpful >= 25 then badges := badges || jsonb_build_object(
            'key', 'helpful_25', 'label', 'Very helpful', 'detail', '25+ helpful votes received');
        elsif v_helpful >= 10 then badges := badges || jsonb_build_object(
            'key', 'helpful_10', 'label', 'Helpful', 'detail', '10+ helpful votes received'); end if;
        if v_poll_total >= 5 and v_poll_right * 10 >= v_poll_total * 7 then
            badges := badges || jsonb_build_object(
            'key', 'sharp', 'label', 'Sharp diagnostician',
            'detail', '70%+ of revealed poll votes matched the intended answer'); end if;
        -- Go-to in a topic: 3+ best answers on posts with the same tag.
        select t.label, count(*) as n into top_topic
          from public.exchange_posts p
          join public.exchange_replies r on r.id = p.best_reply_id
          join public.exchange_post_tags t on t.post_id = p.id
         where r.author_id = pr.id and not r.is_anonymous
         group by t.label order by count(*) desc limit 1;
        if top_topic.n >= 3 then badges := badges || jsonb_build_object(
            'key', 'goto', 'label', 'Go-to in ' || top_topic.label,
            'detail', top_topic.n || ' best answers on ' || top_topic.label || ' posts'); end if;

        result := result || jsonb_build_object('stats', jsonb_build_object(
            'posts', v_posts, 'cases', v_cases, 'questions', v_questions, 'replies', v_replies,
            'best_answers', v_best, 'verified_answers', v_verified, 'helpful_votes', v_helpful,
            'poll_total', v_poll_total, 'poll_correct', v_poll_right), 'badges', badges);
    end if;

    if see_activity then
        result := result || jsonb_build_object(
            'topics', coalesce((
                select jsonb_agg(jsonb_build_object('kind', kind, 'id', ref_id, 'label', label, 'count', n)
                                 order by n desc, label)
                from (select t.kind, t.ref_id, t.label, count(*) as n
                        from public.exchange_post_tags t
                       where t.post_id in (
                             select id from public.exchange_posts
                              where author_id = pr.id and not is_anonymous and status in ('open', 'locked')
                             union
                             select r.post_id from public.exchange_replies r
                               join public.exchange_posts p on p.id = r.post_id
                              where r.author_id = pr.id and not r.is_anonymous and r.status = 'open'
                                and p.status in ('open', 'locked'))
                       group by t.kind, t.ref_id, t.label
                       order by count(*) desc limit 8) top), '[]'),
            'recent_posts', coalesce((
                select jsonb_agg(x order by (x ->> 'created_at') desc) from (
                    select jsonb_build_object('id', id, 'title', title, 'kind', kind,
                                              'created_at', created_at, 'reply_count', reply_count,
                                              'score', score, 'status', status) as x
                      from public.exchange_posts
                     where author_id = pr.id and not is_anonymous and status in ('open', 'locked')
                     order by created_at desc limit 15) q), '[]'),
            'recent_replies', coalesce((
                select jsonb_agg(x order by (x ->> 'created_at') desc) from (
                    select jsonb_build_object('id', r.id, 'post_id', r.post_id, 'post_title', p.title,
                                              'excerpt', public.ex_short(r.body, 160),
                                              'created_at', r.created_at, 'score', r.score,
                                              'is_best', p.best_reply_id = r.id,
                                              'verified', r.verified_at is not null) as x
                      from public.exchange_replies r join public.exchange_posts p on p.id = r.post_id
                     where r.author_id = pr.id and not r.is_anonymous and r.status = 'open'
                       and p.status in ('open', 'locked')
                     order by r.created_at desc limit 15) q), '[]'));
    end if;
    return result;
end $$;

-- ---------------------------------------------------------------------
-- 5. Reporting and moderating profiles
-- ---------------------------------------------------------------------
alter table public.exchange_reports drop constraint if exists exchange_reports_target_kind_check;
alter table public.exchange_reports add constraint exchange_reports_target_kind_check
    check (target_kind in ('post', 'reply', 'profile'));
alter table public.exchange_reports drop constraint if exists exchange_reports_reason_check;
alter table public.exchange_reports add constraint exchange_reports_reason_check
    check (reason in ('patient_data', 'misinformation', 'harassment', 'spam', 'off_topic',
                      'impersonation', 'other'));

create or replace function public.ex_report(p_kind text, p_id uuid, p_reason text, p_note text)
returns void
language plpgsql security definer set search_path = ''
as $$
declare me uuid := public.ex_uid();
begin
    perform public.ex_rate(me, 'report', 10, interval '1 hour');
    if p_kind = 'profile' then
        if p_id = me or public.ex_profile_access(p_id, me) is not null then
            raise exception 'That is not available.';
        end if;
    elsif not exists (select 1 from public.exchange_posts where p_kind = 'post' and id = p_id)
       and not exists (select 1 from public.exchange_replies where p_kind = 'reply' and id = p_id) then
        raise exception 'That is not available.';
    end if;
    insert into public.exchange_reports (reporter_id, target_kind, target_id, reason, note)
    values (me, p_kind, p_id, p_reason, left(coalesce(p_note, ''), 500))
    on conflict (reporter_id, target_kind, target_id) do update
        set reason = excluded.reason, note = excluded.note, status = 'open', created_at = now();
end $$;

-- p_action: hide | unhide | lock | unlock | remove (posts, replies)
--           make_private | clear_bio (profiles)
create or replace function public.ex_moderate(p_kind text, p_id uuid, p_action text, p_reason text)
returns void
language plpgsql security definer set search_path = ''
as $$
declare
    me uuid := public.ex_uid();
    author uuid;
    post uuid;
    v_title text;
    new_status text;
begin
    if not public.ex_is_mod(me) then raise exception 'Only educators and admins can moderate.'; end if;
    if p_kind = 'profile' then
        if p_action = 'make_private' then
            update public.profiles set visibility = 'private' where id = p_id returning id into author;
        elsif p_action = 'clear_bio' then
            update public.profiles set bio = '' where id = p_id returning id into author;
        else
            raise exception 'Unknown action.';
        end if;
        if author is null then raise exception 'That is not available.'; end if;
        insert into public.exchange_mod_log (moderator_id, action, target_kind, target_id, reason)
        values (me, p_action, p_kind, p_id, left(coalesce(p_reason, ''), 300));
        update public.exchange_reports set status = 'resolved', handled_by = me, handled_at = now()
        where target_kind = 'profile' and target_id = p_id and status = 'open';
        perform public.ex_notify(array[author], 'moderation', null, null,
            'A moderator ' || case p_action when 'make_private' then 'made your profile private'
                else 'cleared your profile bio' end
            || case when coalesce(p_reason, '') <> '' then ': ' || left(p_reason, 120) else '' end, me);
        return;
    end if;

    new_status := case p_action when 'hide' then 'hidden' when 'unhide' then 'open'
                                when 'lock' then 'locked' when 'unlock' then 'open'
                                when 'remove' then 'removed' end;
    if new_status is null then raise exception 'Unknown action.'; end if;
    if p_kind = 'post' then
        update public.exchange_posts set status = new_status where id = p_id
        returning author_id, id, exchange_posts.title into author, post, v_title;
    elsif p_kind = 'reply' then
        if p_action in ('lock', 'unlock') then raise exception 'Replies can''t be locked.'; end if;
        update public.exchange_replies set status = new_status where id = p_id
        returning author_id, post_id into author, post;
        select p.title into v_title from public.exchange_posts p where p.id = post;
    end if;
    if author is null then raise exception 'That is not available.'; end if;

    insert into public.exchange_mod_log (moderator_id, action, target_kind, target_id, reason)
    values (me, p_action, p_kind, p_id, left(coalesce(p_reason, ''), 300));
    update public.exchange_reports set status = 'resolved', handled_by = me, handled_at = now()
    where target_kind = p_kind and target_id = p_id and status = 'open';
    if p_action in ('hide', 'lock', 'remove') then
        perform public.ex_notify(array[author], 'moderation', case when p_action = 'remove'
                and p_kind = 'post' then null else post end, null,
            'A moderator ' || case p_action when 'hide' then 'hid' when 'lock' then 'locked'
                else 'removed' end || ' your ' || p_kind || ' on “' || public.ex_short(v_title) || '”'
            || case when coalesce(p_reason, '') <> '' then ': ' || left(p_reason, 120) else '' end, me);
    end if;
end $$;

-- Open reports, posts/replies as before plus reported profiles.
create or replace function public.ex_mod_queue()
returns setof jsonb
language plpgsql stable security definer set search_path = ''
as $$
declare me uuid := public.ex_uid();
begin
    if not public.ex_is_mod(me) then raise exception 'Only educators and admins can moderate.'; end if;
    return query
    select q.item from (
        select jsonb_build_object(
            'target_kind', r.target_kind, 'target_id', r.target_id,
            'reports', count(*), 'reasons', jsonb_agg(distinct r.reason),
            'notes', jsonb_agg(r.note) filter (where r.note <> ''),
            'first_reported', min(r.created_at),
            'post_id', coalesce(p.id, rp.post_id),
            'title', coalesce(p.title, pp.title),
            'excerpt', public.ex_short(coalesce(rp.body, p.body, ''), 200),
            'status', coalesce(rp.status, p.status),
            'author', public.ex_author(coalesce(p.author_id, rp.author_id),
                                       coalesce(p.is_anonymous, rp.is_anonymous), me)) as item,
            count(*) as n, min(r.created_at) as first_at
        from public.exchange_reports r
        left join public.exchange_posts p on r.target_kind = 'post' and p.id = r.target_id
        left join public.exchange_replies rp on r.target_kind = 'reply' and rp.id = r.target_id
        left join public.exchange_posts pp on pp.id = rp.post_id
        where r.status = 'open' and r.target_kind in ('post', 'reply')
          and (p.id is not null or rp.id is not null)
        group by r.target_kind, r.target_id, p.id, p.title, p.body, p.status, p.author_id,
                 p.is_anonymous, rp.post_id, rp.body, rp.status, rp.author_id, rp.is_anonymous, pp.title
        union all
        select jsonb_build_object(
            'target_kind', 'profile', 'target_id', r.target_id,
            'reports', count(*), 'reasons', jsonb_agg(distinct r.reason),
            'notes', jsonb_agg(r.note) filter (where r.note <> ''),
            'first_reported', min(r.created_at),
            'post_id', null,
            'title', coalesce(nullif(pr.display_name, ''), 'Akeso student')
                     || coalesce(' (@' || pr.handle || ')', ''),
            'handle', pr.handle,
            'excerpt', public.ex_short(pr.bio, 200),
            'status', pr.visibility,
            'author', public.ex_author(pr.id, false, me)),
            count(*), min(r.created_at)
        from public.exchange_reports r
        join public.profiles pr on pr.id = r.target_id
        where r.status = 'open' and r.target_kind = 'profile'
        group by r.target_id, pr.id, pr.display_name, pr.handle, pr.bio, pr.visibility
    ) q
    order by q.n desc, q.first_at;
end $$;

-- ---------------------------------------------------------------------
-- 6. Profile photos others may see (only when the owner allows it)
-- ---------------------------------------------------------------------
drop policy if exists "avatars: read shown" on storage.objects;
create policy "avatars: read shown" on storage.objects
    for select to authenticated
    using (bucket_id = 'avatars' and exists (
        select 1 from public.profiles p
        where p.id::text = (storage.foldername(name))[1]
          and p.show_photo and p.visibility <> 'private'
          and p.deletion_scheduled_for is null));

-- ---------------------------------------------------------------------
-- 7. Grants
-- ---------------------------------------------------------------------
do $$
declare fn text;
begin
    foreach fn in array array['public.ex_profile_access(uuid, uuid)',
                              'public.ex_notify_followers()',
                              'public.profiles_sync_visibility()'] loop
        execute format('revoke execute on function %s from public, anon, authenticated', fn);
    end loop;
    foreach fn in array array['public.ex_profile(text)', 'public.ex_follow_user(text, boolean)',
                              'public.ex_report(text, uuid, text, text)',
                              'public.ex_moderate(text, uuid, text, text)',
                              'public.ex_mod_queue()'] loop
        execute format('revoke execute on function %s from public, anon', fn);
        execute format('grant execute on function %s to authenticated', fn);
    end loop;
end $$;

notify pgrst, 'reload schema';
