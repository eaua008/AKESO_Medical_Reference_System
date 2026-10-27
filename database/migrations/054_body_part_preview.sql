-- =====================================================================
-- Akeso migration 054: admins preview body part drafts in the Explorer
-- =====================================================================
-- Run AFTER 052_body_part_info.sql (and 053 for the B1 text). Safe to run
-- again. Adds one function; no table changes.
--
--   admin_body_parts_preview   every body_part_info row, drafts included,
--                              for an admin who has passed two-factor. The
--                              Explorer shows drafts to admins (marked
--                              "Draft") so the text can be checked in place
--                              before it is published. Everyone else still
--                              reads published rows only (052's policy).
-- =====================================================================

begin;

create or replace function public.admin_body_parts_preview()
returns jsonb
language plpgsql stable security definer set search_path = ''
as $$
declare me uuid := public.ad_me();
begin
    return coalesce((select jsonb_agg(to_jsonb(b) order by b.key)
                     from public.body_part_info b), '[]'::jsonb);
end $$;

revoke execute on function public.admin_body_parts_preview() from public, anon;
grant execute on function public.admin_body_parts_preview() to authenticated;

commit;
