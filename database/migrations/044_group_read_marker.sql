-- =====================================================================
-- Akeso migration 044: "new messages" marker in study group chats
-- =====================================================================
-- Run AFTER 042_study_groups.sql. Safe to run again.
--
-- 042 already remembers, per member, the last message they have seen
-- (study_group_members.last_read_id) and counts unread messages for the
-- group list. But opening a group marked everything read in the same call,
-- so the app could never show WHERE the new messages start.
--
-- group_messages_after now also returns "last_read": the last message id
-- this member had seen BEFORE the call. The app draws a "New messages"
-- divider after it and scrolls there. Nothing else changes (same
-- arguments, same fields as before, plus one).
-- =====================================================================

begin;

create or replace function public.group_messages_after(p_group uuid, p_after bigint default null,
                                                       p_limit integer default 50)
returns jsonb
language plpgsql security definer set search_path = ''
as $$
declare
    me uuid := public.ex_uid();
    staff boolean;
    out_rows jsonb;
    newest bigint;
    previous bigint;
    n integer := least(greatest(coalesce(p_limit, 50), 1), 100);
begin
    if public.sg_role(p_group, me) is null then
        raise exception 'That study group is not available.';
    end if;
    staff := public.sg_is_staff(p_group, me);
    select last_read_id into previous from public.study_group_members
    where group_id = p_group and user_id = me;
    if p_after is null then
        select coalesce(jsonb_agg(public.sg_message_row(m, me, staff) order by m.id), '[]'::jsonb),
               max(m.id)
          into out_rows, newest
          from (select * from public.study_group_messages where group_id = p_group
                order by id desc limit n) m;
    else
        select coalesce(jsonb_agg(public.sg_message_row(m, me, staff) order by m.id), '[]'::jsonb),
               max(m.id)
          into out_rows, newest
          from (select * from public.study_group_messages where group_id = p_group and id > p_after
                order by id limit n) m;
    end if;
    if newest is not null then
        update public.study_group_members set last_read_id = greatest(last_read_id, newest)
        where group_id = p_group and user_id = me;
    end if;
    return jsonb_build_object('messages', out_rows, 'more', jsonb_array_length(out_rows) >= n,
                              'last_read', coalesce(previous, 0));
end $$;

commit;

notify pgrst, 'reload schema';
