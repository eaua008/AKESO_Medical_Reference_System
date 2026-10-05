-- =====================================================================
-- 012_public_profile_default.sql  -  new accounts start with a public
-- Clinical Exchange profile, with the personal details hidden
-- =====================================================================
-- Run AFTER 011_notebook_sync.sql. Safe to run more than once.
--
-- Before: new profiles were Private, so nobody could open them until the
-- person changed Account Settings > Profile. Now a NEW account starts:
--
--   Who can see my profile   Public (everyone signed in)
--   shown                    name, @handle, role, program and year, bio,
--                            interests, stats and badges, recent public
--                            posts and replies
--   hidden until switched on photo, school, "last active"
--   never shown              email address (it is never part of a
--                            profile), and anonymous posts
--
-- Everyone can still change any of this in Account Settings > Profile.
-- Existing accounts keep the choices they already have (see the end of
-- this file to change them too).
-- =====================================================================

alter table public.profiles
    alter column visibility       set default 'public',
    alter column show_photo       set default false,
    alter column show_school      set default false,
    alter column show_last_active set default false;

-- Optional, for the testers' accounts that already exist: uncomment and
-- run to give every STUDENT who is still Private the same new default.
-- (It overrides anyone who chose Private on purpose.)
--
-- update public.profiles p
--    set visibility = 'public', show_school = false, show_last_active = false
--  where p.visibility = 'private'
--    and exists (select 1 from public.user_roles r
--                where r.user_id = p.id and r.role = 'student');
