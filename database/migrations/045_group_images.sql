-- =====================================================================
-- Akeso migration 045: pictures in study group chats
-- =====================================================================
-- Run AFTER 042_study_groups.sql (044 is not required). Safe to run again.
--
-- A group message can carry ONE picture (PNG or JPEG, up to 5 MB), with an
-- optional caption. The picture lives in a PRIVATE storage bucket,
-- group-attachments, at <group id>/<sender id>/<random id>.png or .jpg:
--
--   * only members of that group can read a picture (checked by the
--     database on every download; there are no public or shareable links);
--   * only a member can upload, and only into their own folder of their
--     own group; the bucket itself refuses anything over 5 MB or that
--     isn't PNG / JPEG;
--   * a picture of a hidden message can't be read by ordinary members any
--     more (only the sender and the group's owner and moderators);
--   * deleting a message's picture, or the whole group, is cleaned up by
--     the app and by the daily purge function (it removes pictures no
--     message points at).
--
-- The app removes metadata (camera, location) by re-encoding the picture
-- before upload, and asks the sender to confirm it shows no real patient.
-- The database can't look inside a picture, so the safety nets are the
-- confirmation, the caption's patient-data check, the report button and
-- hiding by moderators.
-- =====================================================================

begin;

alter table public.study_group_messages add column if not exists attachment_path text;
create unique index if not exists study_group_messages_attachment_key
    on public.study_group_messages (attachment_path) where attachment_path is not null;

-- A message needs text OR a picture (the text check from 042 required text).
alter table public.study_group_messages drop constraint if exists study_group_messages_body_check;
alter table public.study_group_messages drop constraint if exists study_group_messages_text_or_image;
alter table public.study_group_messages add constraint study_group_messages_text_or_image
    check (char_length(body) <= 2000
           and (attachment_path is not null or char_length(btrim(body)) >= 1));

insert into storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
values ('group-attachments', 'group-attachments', false, 5242880,
        array['image/png', 'image/jpeg'])
on conflict (id) do update set public = false, file_size_limit = excluded.file_size_limit,
                               allowed_mime_types = excluded.allowed_mime_types;


-- ---------------------------------------------------------------------
-- 1. Reading a path: <group>/<sender>/<id>.png|jpg
-- ---------------------------------------------------------------------
create or replace function public.sg_attach_group(p_path text)
returns uuid
language sql immutable set search_path = ''
as $$
    select case when p_path ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}/[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}/[0-9a-f]{32}\.(png|jpg)$'
                then split_part(p_path, '/', 1)::uuid end;
$$;

create or replace function public.sg_attach_user(p_path text)
returns uuid
language sql immutable set search_path = ''
as $$
    select case when public.sg_attach_group(p_path) is not null
                then split_part(p_path, '/', 2)::uuid end;
$$;

-- May this person read this picture right now?
create or replace function public.sg_attachment_visible(p_path text, p_viewer uuid)
returns boolean
language sql stable security definer set search_path = ''
as $$
    select public.sg_attach_group(p_path) is not null
       and public.sg_role(public.sg_attach_group(p_path), p_viewer) is not null
       and (public.sg_attach_user(p_path) = p_viewer
            or public.sg_is_staff(public.sg_attach_group(p_path), p_viewer)
            or not exists (select 1 from public.study_group_messages m
                           where m.attachment_path = p_path and m.status = 'hidden'));
$$;


-- ---------------------------------------------------------------------
-- 2. Storage rules (who may upload, read and delete)
-- ---------------------------------------------------------------------
-- Storage runs these as the signed-in user, so they must be callable. Each
-- answers only for the CALLER (auth.uid()), so they can't be used to find
-- out who is in which group.
create or replace function public.sg_img_can_read(p_path text)
returns boolean
language sql stable security definer set search_path = ''
as $$ select public.sg_attachment_visible(p_path, auth.uid()); $$;

create or replace function public.sg_img_can_upload(p_path text)
returns boolean
language sql stable security definer set search_path = ''
as $$
    select public.sg_attach_user(p_path) = auth.uid()
       and public.sg_role(public.sg_attach_group(p_path), auth.uid()) is not null;
$$;

create or replace function public.sg_img_can_delete(p_path text)
returns boolean
language sql stable security definer set search_path = ''
as $$
    select public.sg_attach_user(p_path) = auth.uid()
        or public.sg_is_staff(public.sg_attach_group(p_path), auth.uid());
$$;

drop policy if exists "group images: members upload" on storage.objects;
create policy "group images: members upload" on storage.objects
    for insert to authenticated
    with check (bucket_id = 'group-attachments' and public.sg_img_can_upload(name));

drop policy if exists "group images: members read" on storage.objects;
create policy "group images: members read" on storage.objects
    for select to authenticated
    using (bucket_id = 'group-attachments' and public.sg_img_can_read(name));

drop policy if exists "group images: sender or staff remove" on storage.objects;
create policy "group images: sender or staff remove" on storage.objects
    for delete to authenticated
    using (bucket_id = 'group-attachments' and public.sg_img_can_delete(name));


-- ---------------------------------------------------------------------
-- 3. Messages carry the picture's path (hidden ones don't give it away)
-- ---------------------------------------------------------------------
create or replace function public.sg_message_row(m public.study_group_messages, p_viewer uuid,
                                                 p_staff boolean)
returns jsonb
language sql stable security definer set search_path = ''
as $$
    select jsonb_build_object(
        'id', m.id, 'created_at', m.created_at, 'status', m.status,
        'author', public.sg_person(m.group_id, m.author_id, p_viewer),
        'body', case when m.status = 'open' or p_staff or m.author_id = p_viewer then m.body
                     else '' end,
        'attachment', case when m.status = 'open' or p_staff or m.author_id = p_viewer
                           then m.attachment_path end,
        'is_mine', m.author_id = p_viewer);
$$;


-- ---------------------------------------------------------------------
-- 4. Sending a message with a picture
-- ---------------------------------------------------------------------
-- The app uploads the picture first (storage rules above), then calls this
-- with its path. Same limits as text messages, plus 10 pictures an hour.
create or replace function public.group_send_image(p_group uuid, p_caption text, p_path text)
returns jsonb
language plpgsql security definer set search_path = ''
as $$
declare
    me uuid := public.ex_uid();
    clean text := btrim(coalesce(p_caption, ''));
    found text;
    msg public.study_group_messages;
    gname text;
    target uuid;
begin
    if public.sg_role(p_group, me) is null then raise exception 'Join the group to post in it.'; end if;
    if public.sg_attach_group(p_path) is distinct from p_group
       or public.sg_attach_user(p_path) is distinct from me then
        raise exception 'That picture can''t be sent. Try again.';
    end if;
    if not exists (select 1 from storage.objects where bucket_id = 'group-attachments' and name = p_path) then
        raise exception 'The picture didn''t upload. Try again.';
    end if;
    if char_length(clean) > 2000 then raise exception 'Keep messages under 2,000 characters.'; end if;
    found := public.ex_phi_check(clean);
    if found is not null then
        raise exception 'Not sent: the caption looks like it contains %. Cases must be hypothetical; remove anything that could identify a real person.', found;
    end if;
    if (select count(*) from public.study_group_messages
        where author_id = me and created_at > now() - interval '1 minute') >= 10 then
        raise exception 'Slow down: at most 10 messages a minute.';
    end if;
    if (select count(*) from public.study_group_messages
        where author_id = me and created_at > now() - interval '1 hour') >= 120 then
        raise exception 'Slow down: at most 120 messages an hour.';
    end if;
    perform public.social_rate(me, 'group_image', 10, interval '1 hour', 'pictures');
    insert into public.study_group_messages (group_id, author_id, body, attachment_path)
    values (p_group, me, clean, p_path) returning * into msg;
    update public.study_group_members set last_read_id = msg.id where group_id = p_group and user_id = me;

    select name into gname from public.study_groups where id = p_group;
    for target in
        select distinct m.user_id
        from regexp_matches(clean, '@([A-Za-z0-9_]{3,20})', 'g') as h(parts)
        join public.profiles p on lower(p.handle) = lower(h.parts[1])
        join public.study_group_members m on m.group_id = p_group and m.user_id = p.id
        where m.user_id <> me and not m.muted and not public.fr_blocked(m.user_id, me)
        limit 10
    loop
        perform public.social_notify(target, 'group_mention', 'group', p_group::text,
            public.social_name(me) || ' mentioned you in “' || public.ex_short(gname, 40) || '”: '
            || public.ex_short(clean, 120));
    end loop;
    return public.sg_message_row(msg, me, public.sg_is_staff(p_group, me));
end $$;

-- Reported pictures: the moderators' queue shows the caption, with "(picture)".
create or replace function public.group_report_queue()
returns setof jsonb
language plpgsql stable security definer set search_path = ''
as $$
declare me uuid := public.ex_uid();
begin
    if not public.ex_is_mod(me) then raise exception 'Only educators and admins can moderate.'; end if;
    return query
    select jsonb_build_object(
        'group_id', r.group_id, 'group_name', g.name, 'target_kind', r.target_kind,
        'target_id', r.target_id, 'reports', count(*), 'reasons', jsonb_agg(distinct r.reason),
        'notes', jsonb_agg(r.note) filter (where r.note <> ''), 'first_reported', min(r.created_at),
        'excerpt', public.ex_short(coalesce(
            (select case when m.attachment_path is not null then '(picture) ' else '' end || m.body
               from public.study_group_messages m where r.target_kind = 'message'
                                                    and m.id::text = r.target_id),
            (select n.title || ': ' || public.ns_plain(n.body) from public.study_group_notes n
              where r.target_kind = 'note' and n.id::text = r.target_id), ''), 300),
        'author', public.fr_person(coalesce(
            (select m.author_id from public.study_group_messages m where r.target_kind = 'message'
                                                                   and m.id::text = r.target_id),
            (select n.owner_id from public.study_group_notes n where r.target_kind = 'note'
                                                              and n.id::text = r.target_id)), me))
    from public.study_group_reports r join public.study_groups g on g.id = r.group_id
    where r.status = 'open'
    group by r.group_id, g.name, r.target_kind, r.target_id
    order by count(*) desc, min(r.created_at);
end $$;


-- ---------------------------------------------------------------------
-- 5. Who may call what
-- ---------------------------------------------------------------------
do $$
declare fn text;
begin
    -- the storage rules call these as the signed-in user (they answer for the caller only)
    foreach fn in array array['public.sg_attach_group(text)', 'public.sg_attach_user(text)',
                              'public.sg_img_can_read(text)', 'public.sg_img_can_upload(text)',
                              'public.sg_img_can_delete(text)'] loop
        execute format('revoke execute on function %s from public, anon', fn);
        execute format('grant execute on function %s to authenticated', fn);
    end loop;
    execute 'revoke execute on function public.sg_attachment_visible(text, uuid) from public, anon, authenticated';
    foreach fn in array array['public.group_send_image(uuid, text, text)'] loop
        execute format('revoke execute on function %s from public, anon', fn);
        execute format('grant execute on function %s to authenticated', fn);
    end loop;
end $$;

commit;

notify pgrst, 'reload schema';
