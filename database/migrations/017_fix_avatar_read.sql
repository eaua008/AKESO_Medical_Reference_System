-- =====================================================================
-- 017_fix_avatar_read.sql  -  other people can now actually load a
-- profile photo that its owner chose to show
-- =====================================================================
-- Run AFTER 016_delete_notifications.sql. Safe to run more than once.
--
-- The bug: the storage rule "avatars: read shown" (migration 008) looked
-- the photo's owner up in public.profiles AS THE VIEWER. But profiles can
-- only be read by their owner ("own profile: read"), so for anyone else
-- the lookup found nothing and the download was refused. ex_author and
-- ex_profile correctly sent the photo path, the app tried to download
-- it, storage said no, and everyone saw the initial instead.
--
-- The fix: the check runs in a SECURITY DEFINER function, which can read
-- the owner's settings without opening profiles to anyone. It allows the
-- same people the app already shows the photo to:
--   * the owner turned on "Show my photo", the account is not being
--     deleted, and
--   * the viewer may open the owner's profile (ex_profile_access: public,
--     or members-only and the viewer is verified / an educator / admin).
-- Nothing else about the bucket changes: it stays private, and only the
-- owner can upload, replace or remove their photo.
-- =====================================================================

create or replace function public.avatar_readable(p_folder text)
returns boolean
language plpgsql stable security definer set search_path = ''
as $$
declare
    owner uuid;
begin
    begin
        owner := p_folder::uuid;              -- folders are named after the account id
    exception when invalid_text_representation then
        return false;
    end;
    return exists (
        select 1 from public.profiles p
        where p.id = owner
          and p.show_photo
          and p.deletion_scheduled_for is null
          and public.ex_profile_access(owner, auth.uid()) is null);
end $$;

revoke execute on function public.avatar_readable(text) from public, anon;
grant execute on function public.avatar_readable(text) to authenticated;

drop policy if exists "avatars: read shown" on storage.objects;
create policy "avatars: read shown" on storage.objects
    for select to authenticated
    using (bucket_id = 'avatars'
           and public.avatar_readable((storage.foldername(name))[1]));

notify pgrst, 'reload schema';
