-- =====================================================================
-- 013_author_photos.sql  -  profile photos next to names on posts and
-- replies in Clinical Exchange
-- =====================================================================
-- Run AFTER 012_public_profile_default.sql. Safe to run more than once.
--
-- ex_author (how an author appears to a viewer) now also sends the
-- author's photo path, ONLY when all of these hold:
--   * the post / reply is not anonymous (anonymous ones never show a
--     photo, not even to moderators, who still see the real name),
--   * the author has a photo and turned on "Show my photo",
--   * the viewer may open the author's profile (public, or members-only
--     and the viewer is verified / an educator / an admin).
-- You always see your own photo. Everyone else gets the initial of the
-- name in a circle, drawn by the app.
-- =====================================================================

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
            'avatar_path', case
                when p.avatar_path is null then null
                when p_viewer = p_author then p.avatar_path
                when p_anon then null
                when p.show_photo and public.ex_profile_access(p_author, p_viewer) is null
                    then p.avatar_path
                end,
            'is_me', p_viewer = p_author)
        end
    from public.profiles p where p.id = p_author;
$$;

revoke execute on function public.ex_author(uuid, boolean, uuid) from public, anon, authenticated;

notify pgrst, 'reload schema';
