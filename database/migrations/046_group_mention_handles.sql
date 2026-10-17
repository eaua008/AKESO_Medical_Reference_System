-- =====================================================================
-- Akeso migration 046: @mention suggestions in study group chats
-- =====================================================================
-- Run AFTER 042_study_groups.sql. Safe to run again.
--
-- Typing @ in a group chat suggests the members to mention. Most accounts
-- keep their profile private (the default), and a private profile hides its
-- @handle everywhere, so the suggestions had nothing to offer for them
-- even though a mention (which notifies by handle) works for any member.
--
-- group_get now also gives each member's "mention" handle to the OTHER
-- MEMBERS OF THAT GROUP, for this one purpose. It is not shown anywhere
-- else, and nobody outside the group gets it. The handle is the plain
-- name-based one Akeso assigns; members of a group already see each
-- other's name, role and (if allowed) photo. The Privacy Notice says so.
-- =====================================================================

begin;

create or replace function public.group_get(p_group uuid)
returns jsonb
language plpgsql stable security definer set search_path = ''
as $$
declare
    me uuid := public.ex_uid();
    g public.study_groups;
    my_role text;
    link public.study_group_invites;
begin
    select * into g from public.study_groups where id = p_group;
    my_role := public.sg_role(p_group, me);
    if g.id is null or (my_role is null and (g.visibility <> 'public'
                                             or (g.owner_id is not null and public.fr_blocked(g.owner_id, me)))) then
        raise exception 'That study group is not available.';
    end if;
    if my_role is null then
        return public.sg_row(g, me) || jsonb_build_object('can_join',
            (select count(*) from public.study_group_members where group_id = g.id) < 50);
    end if;
    select * into link from public.study_group_invites
    where group_id = g.id and kind = 'link' and revoked_at is null
      and (expires_at is null or expires_at > now())
    order by created_at desc limit 1;
    return public.sg_row(g, me) || jsonb_build_object(
        'muted', (select muted from public.study_group_members where group_id = g.id and user_id = me),
        'members_list', coalesce((
            select jsonb_agg(public.sg_person(g.id, m.user_id, me)
                             || jsonb_build_object('joined_at', m.joined_at,
                                                   'blocked', public.fr_blocked(m.user_id, me),
                                                   -- what to type after @ to mention them
                                                   'mention', (select p.handle from public.profiles p
                                                               where p.id = m.user_id))
                             order by case m.role when 'owner' then 0 when 'moderator' then 1 else 2 end,
                                      m.joined_at)
            from public.study_group_members m where m.group_id = g.id), '[]'::jsonb),
        'invite_link', case when my_role in ('owner', 'moderator') and link.id is not null then
            jsonb_build_object('id', link.id, 'created_at', link.created_at,
                               'expires_at', link.expires_at, 'uses', link.uses) end,
        'pending_invites', case when my_role in ('owner', 'moderator') then coalesce((
            select jsonb_agg(public.fr_person(i.invitee_id, me) || jsonb_build_object('invite_id', i.id))
            from public.study_group_invites i
            where i.group_id = g.id and i.kind = 'friend' and i.answered_at is null
              and i.revoked_at is null), '[]'::jsonb) end);
end $$;

commit;

notify pgrst, 'reload schema';
