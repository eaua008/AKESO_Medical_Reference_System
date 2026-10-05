-- =====================================================================
-- Akeso migration 004: Admin Control Panel
-- =====================================================================
-- Run once in the Supabase SQL editor, AFTER 002_accounts.sql (it uses
-- profiles, user_roles, is_admin() and mfa_satisfied()). Safe to run again.
--
-- What this adds
--
--   User Management
--     profiles.suspended_at / suspended_reason
--     admin_users()            every account: role, status, last sign-in
--     admin_user_detail()      one account: profile basics + recent activity
--     admin_set_role()         student / educator / admin
--     admin_set_suspended()    suspend or reactivate (also blocks sign-in)
--     admin_delete_user()      delete an account for good
--
--   Content Management
--     admin_list_diseases() / _symptoms() / _medicines()   incl. archived
--     admin_get_disease() / _symptom() / _medicine()       one entry, all parts
--     admin_save_disease() / _symptom() / _medicine()      create or edit
--     admin_set_published()    archive (hide) or restore an entry
--     admin_body_systems()     for the body-system pickers
--
--   admin_audit_log + admin_audit()   who changed what, append-only
--
-- Security model
--
--   Only admins can call these, and the check happens HERE, in the
--   database (ad_me), not in the app: anyone can edit the app's Python.
--   An admin with two-factor turned on must have passed it (aal2).
--
--   Private health data is out of reach on purpose: nothing here reads
--   the medication vault, symptom-checker cases or notebook contents.
--
--   Content is never hard-deleted from here. "Delete" archives the entry
--   (is_published = false): the app stops showing it, links to it stay
--   intact, and it can be restored. Every save bumps content_version, so
--   every running app downloads the change on its next sync.
-- =====================================================================

begin;

-- ---------------------------------------------------------------------
-- 1. Suspension (on the profile; the app also checks it at sign-in)
-- ---------------------------------------------------------------------
alter table public.profiles add column if not exists suspended_at timestamptz;
alter table public.profiles add column if not exists suspended_reason text not null default '';
do $$ begin
    alter table public.profiles add constraint profiles_suspended_reason_len
        check (char_length(suspended_reason) <= 300);
exception when duplicate_object then null; end $$;
-- Users can read their own profile (002 grants select), so the app can tell
-- a suspended user why. They cannot change these columns: 002 grants
-- update on a fixed list of columns only.


-- ---------------------------------------------------------------------
-- 2. Audit log
-- ---------------------------------------------------------------------
create table if not exists public.admin_audit_log (
    id            bigint generated always as identity primary key,
    actor_id      uuid references auth.users (id) on delete set null,
    actor_label   text not null default '',
    action        text not null,      -- create, update, archive, restore, role,
                                      -- suspend, reactivate, delete_user
    target_kind   text not null,      -- disease, symptom, medicine, user
    target_id     text not null,
    target_label  text not null default '',
    detail        jsonb not null default '{}'::jsonb,
    created_at    timestamptz not null default now()
);
create index if not exists admin_audit_log_created_idx
    on public.admin_audit_log (created_at desc);

alter table public.admin_audit_log enable row level security;
revoke all on public.admin_audit_log from anon, authenticated;


-- ---------------------------------------------------------------------
-- 3. Helpers (not callable from the app)
-- ---------------------------------------------------------------------
-- The caller's id, if they are an admin who has passed two-factor.
create or replace function public.ad_me()
returns uuid
language plpgsql stable security definer set search_path = ''
as $$
declare uid uuid := auth.uid();
begin
    if uid is null then raise exception 'Not signed in.'; end if;
    if not public.mfa_satisfied() then raise exception 'Two-factor check required.'; end if;
    if not public.is_admin() then raise exception 'Only admins can do that.'; end if;
    return uid;
end $$;

create or replace function public.ad_log(
    p_action text, p_kind text, p_id text, p_label text,
    p_detail jsonb default '{}'::jsonb)
returns void
language plpgsql security definer set search_path = ''
as $$
declare
    uid uuid := auth.uid();
    v_actor text;
begin
    select coalesce(nullif(p.display_name, ''), u.email, '') into v_actor
    from auth.users u left join public.profiles p on p.id = u.id
    where u.id = uid;
    insert into public.admin_audit_log
        (actor_id, actor_label, action, target_kind, target_id, target_label, detail)
    values (uid, coalesce(v_actor, ''), p_action, p_kind, p_id,
            left(coalesce(p_label, ''), 200), coalesce(p_detail, '{}'::jsonb));
end $$;

-- Every running app compares this number and re-downloads when it changes.
create or replace function public.ad_bump()
returns void
language sql security definer set search_path = ''
as $$
    update public.content_version set version = version + 1, updated_at = now() where id = 1;
$$;

-- A JSON array of strings -> clean lines (trimmed, no blanks), in order.
create or replace function public.ad_lines(p jsonb)
returns table (pos integer, line text)
language sql immutable set search_path = ''
as $$
    select (row_number() over (order by o) - 1)::integer, btrim(v)
    from jsonb_array_elements_text(
             case when jsonb_typeof(p) = 'array' then p else '[]'::jsonb end)
         with ordinality as t(v, o)
    where btrim(v) <> '';
$$;

-- Shared checks for an entry's id and name.
create or replace function public.ad_check_entry(p_id text, p_name text, p_what text)
returns void
language plpgsql immutable set search_path = ''
as $$
begin
    if p_id is null or p_id !~ '^[a-z0-9_]{2,60}$' then
        raise exception 'The ID must be 2 to 60 lowercase letters, numbers or underscores.';
    end if;
    if coalesce(btrim(p_name), '') = '' then
        raise exception 'Give the % a name.', p_what;
    end if;
    if char_length(p_name) > 160 then
        raise exception 'Keep the name under 160 characters.';
    end if;
end $$;


-- ---------------------------------------------------------------------
-- 4. User Management
-- ---------------------------------------------------------------------
create or replace function public.admin_users()
returns jsonb
language plpgsql stable security definer set search_path = ''
as $$
declare me uuid := public.ad_me();
begin
    return coalesce((
        select jsonb_agg(jsonb_build_object(
            'id', u.id,
            'email', u.email,
            'display_name', coalesce(nullif(p.display_name, ''), split_part(u.email, '@', 1)),
            'handle', p.handle,
            'role', coalesce(r.role::text, 'student'),
            'created_at', u.created_at,
            'last_sign_in_at', u.last_sign_in_at,
            'suspended', p.suspended_at is not null,
            'suspended_reason', coalesce(p.suspended_reason, ''),
            'deletion_scheduled_for', p.deletion_scheduled_for,
            'registry_id', 'AK-' || lpad((abs(hashtext(u.id::text)) % 10000)::text, 4, '0'),
            'is_me', u.id = me
        ) order by u.created_at)
        from auth.users u
        left join public.profiles p on p.id = u.id
        left join public.user_roles r on r.user_id = u.id
    ), '[]'::jsonb);
end $$;

create or replace function public.admin_user_detail(p_user uuid)
returns jsonb
language plpgsql stable security definer set search_path = ''
as $$
declare
    me uuid := public.ad_me();
    v jsonb;
begin
    select jsonb_build_object(
        'id', u.id,
        'email', u.email,
        'display_name', coalesce(nullif(p.display_name, ''), split_part(u.email, '@', 1)),
        'handle', p.handle,
        'program', p.program,
        'school', p.school,
        'year_level', p.year_level,
        'school_email_domain', p.school_email_domain,
        'school_email_verified_at', p.school_email_verified_at,
        'role', coalesce(r.role::text, 'student'),
        'role_granted_at', r.granted_at,
        'role_granted_by', (select coalesce(nullif(gp.display_name, ''), gu.email)
                            from auth.users gu left join public.profiles gp on gp.id = gu.id
                            where gu.id = r.granted_by),
        'created_at', u.created_at,
        'last_sign_in_at', u.last_sign_in_at,
        'suspended', p.suspended_at is not null,
        'suspended_at', p.suspended_at,
        'suspended_reason', coalesce(p.suspended_reason, ''),
        'deletion_scheduled_for', p.deletion_scheduled_for,
        'device_count', (select count(*) from public.user_devices d where d.user_id = u.id),
        -- account activity only (sign-ins, password and role changes):
        -- never study or health data
        'recent_events', coalesce((
            select jsonb_agg(jsonb_build_object('kind', e.kind, 'device', e.device_name,
                                                'at', e.created_at) order by e.created_at desc)
            from (select * from public.security_events s where s.user_id = u.id
                  order by s.created_at desc limit 8) e), '[]'::jsonb),
        'registry_id', 'AK-' || lpad((abs(hashtext(u.id::text)) % 10000)::text, 4, '0'),
        'is_me', u.id = me)
    into v
    from auth.users u
    left join public.profiles p on p.id = u.id
    left join public.user_roles r on r.user_id = u.id
    where u.id = p_user;
    if v is null then raise exception 'That account no longer exists.'; end if;
    return v;
end $$;

create or replace function public.admin_set_role(p_user uuid, p_role text)
returns void
language plpgsql security definer set search_path = ''
as $$
declare
    me uuid := public.ad_me();
    v_old text;
    v_email text;
begin
    if p_role not in ('student', 'educator', 'admin') then
        raise exception 'Unknown role.';
    end if;
    select email into v_email from auth.users where id = p_user;
    if v_email is null then raise exception 'That account no longer exists.'; end if;
    select role::text into v_old from public.user_roles where user_id = p_user;
    if v_old is not distinct from p_role then return; end if;
    -- The user_roles trigger (002) stops the last admin being demoted and
    -- writes the change to that user's own activity log.
    insert into public.user_roles (user_id, role, granted_by, granted_at)
    values (p_user, p_role::public.app_role, me, now())
    on conflict (user_id) do update set role = excluded.role;
    perform public.ad_log('role', 'user', p_user::text, v_email,
                          jsonb_build_object('from', coalesce(v_old, 'student'), 'to', p_role));
end $$;

create or replace function public.admin_set_suspended(p_user uuid, p_suspend boolean,
                                                      p_reason text default '')
returns void
language plpgsql security definer set search_path = ''
as $$
declare
    me uuid := public.ad_me();
    v_email text;
begin
    if p_user = me then raise exception 'You cannot suspend your own account.'; end if;
    select email into v_email from auth.users where id = p_user;
    if v_email is null then raise exception 'That account no longer exists.'; end if;
    if p_suspend and exists (select 1 from public.user_roles
                             where user_id = p_user and role = 'admin') then
        raise exception 'Change this admin''s role first, then suspend the account.';
    end if;

    insert into public.profiles (id) values (p_user) on conflict (id) do nothing;
    update public.profiles
    set suspended_at = case when p_suspend then now() else null end,
        suspended_reason = case when p_suspend then left(coalesce(btrim(p_reason), ''), 300)
                                else '' end
    where id = p_user;

    -- Also stop sign-in and end their sessions at the source. Supabase Auth
    -- refuses banned users and they lose access within the hour (when
    -- their token expires). If a project does not allow these writes, the
    -- profile flag above still keeps them out of the app.
    begin
        update auth.users
        set banned_until = case when p_suspend then 'infinity'::timestamptz else null end
        where id = p_user;
        if p_suspend then
            delete from auth.sessions where user_id = p_user;
        end if;
    exception when insufficient_privilege or undefined_column then
        null;
    end;

    perform public.ad_log(case when p_suspend then 'suspend' else 'reactivate' end,
                          'user', p_user::text, v_email,
                          case when p_suspend and coalesce(btrim(p_reason), '') <> ''
                               then jsonb_build_object('reason', left(btrim(p_reason), 300))
                               else '{}'::jsonb end);
end $$;

create or replace function public.admin_delete_user(p_user uuid, p_confirm text)
returns text
language plpgsql security definer set search_path = ''
as $$
declare
    me uuid := public.ad_me();
    v_email text;
begin
    if coalesce(p_confirm, '') <> 'DELETE' then raise exception 'Type DELETE to confirm.'; end if;
    if p_user = me then
        raise exception 'Delete your own account from Account Settings instead.';
    end if;
    select email into v_email from auth.users where id = p_user;
    if v_email is null then raise exception 'That account no longer exists.'; end if;

    perform public.ad_log('delete_user', 'user', p_user::text, v_email);
    begin
        -- Cascades to the profile, role, devices, activity, posts and replies.
        -- (The user_roles trigger refuses if this is the last admin.)
        delete from auth.users where id = p_user;
        return 'deleted';
    exception when insufficient_privilege then
        -- Not allowed here: schedule it instead, and the deletion job
        -- (purge-deleted-accounts) removes the account on its next run.
        update public.profiles
        set deletion_requested_at = now(), deletion_scheduled_for = now()
        where id = p_user;
        return 'scheduled';
    end;
end $$;


-- ---------------------------------------------------------------------
-- 5. Content Management: lists (archived entries included)
-- ---------------------------------------------------------------------
create or replace function public.admin_body_systems()
returns jsonb
language plpgsql stable security definer set search_path = ''
as $$
begin
    perform public.ad_me();
    return coalesce((select jsonb_agg(jsonb_build_object('id', b.id, 'name', b.name)
                                      order by b.sort_order, b.name)
                     from public.body_systems b), '[]'::jsonb);
end $$;

create or replace function public.admin_list_diseases()
returns jsonb
language plpgsql stable security definer set search_path = ''
as $$
begin
    perform public.ad_me();
    return coalesce((
        select jsonb_agg(jsonb_build_object(
            'id', d.id, 'name', d.name, 'scientific_name', coalesce(d.scientific_name, ''),
            'body_system_id', d.body_system_id, 'body_system', coalesce(b.name, ''),
            'severity', d.severity, 'urgency', d.urgency,
            'published', d.is_published, 'updated_at', d.updated_at,
            'symptom_count', (select count(*) from public.disease_symptoms s
                              where s.disease_id = d.id),
            'primary_count', (select count(*) from public.disease_symptoms s
                              where s.disease_id = d.id and s.is_primary)
        ) order by d.updated_at desc)
        from public.diseases d
        left join public.body_systems b on b.id = d.body_system_id
    ), '[]'::jsonb);
end $$;

create or replace function public.admin_list_symptoms()
returns jsonb
language plpgsql stable security definer set search_path = ''
as $$
begin
    perform public.ad_me();
    return coalesce((
        select jsonb_agg(jsonb_build_object(
            'id', s.id, 'name', s.name, 'scientific_name', s.scientific_name,
            'body_system_id', s.body_system_id, 'body_system', coalesce(b.name, ''),
            'is_red_flag', s.is_red_flag, 'diagnostic_weight', s.diagnostic_weight,
            'published', s.is_published, 'updated_at', s.updated_at,
            'disease_count', (select count(*) from public.disease_symptoms ds
                              where ds.symptom_id = s.id)
        ) order by s.updated_at desc)
        from public.symptoms s
        left join public.body_systems b on b.id = s.body_system_id
    ), '[]'::jsonb);
end $$;

create or replace function public.admin_list_medicines()
returns jsonb
language plpgsql stable security definer set search_path = ''
as $$
begin
    perform public.ad_me();
    return coalesce((
        select jsonb_agg(jsonb_build_object(
            'id', m.id, 'name', m.name,
            'generic_name', coalesce(nullif(m.international_generic_name, ''), m.generic_name, ''),
            'drug_class', coalesce(m.drug_class, ''), 'category', m.category,
            'black_box', coalesce(btrim(m.black_box_warning), '') <> '',
            'published', m.is_published, 'updated_at', m.updated_at,
            'disease_count', (select count(*) from public.disease_medicines dm
                              where dm.medicine_id = m.id)
        ) order by m.updated_at desc)
        from public.medicines m
    ), '[]'::jsonb);
end $$;


-- ---------------------------------------------------------------------
-- 6. Content Management: one entry with all its parts
-- ---------------------------------------------------------------------
create or replace function public.admin_get_disease(p_id text)
returns jsonb
language plpgsql stable security definer set search_path = ''
as $$
declare v jsonb;
begin
    perform public.ad_me();
    select to_jsonb(d) || jsonb_build_object(
        'causes', coalesce((select jsonb_agg(x.content order by x.position)
                            from public.disease_causes x where x.disease_id = d.id), '[]'),
        'risk_factors', coalesce((select jsonb_agg(x.content order by x.position)
                            from public.disease_risk_factors x where x.disease_id = d.id), '[]'),
        'recommended_tests', coalesce((select jsonb_agg(x.content order by x.position)
                            from public.disease_recommended_tests x where x.disease_id = d.id), '[]'),
        'treatments', coalesce((select jsonb_agg(x.content order by x.position)
                            from public.disease_treatments x where x.disease_id = d.id), '[]'),
        'home_care', coalesce((select jsonb_agg(x.content order by x.position)
                            from public.disease_home_care x where x.disease_id = d.id), '[]'),
        'emergency_signs', coalesce((select jsonb_agg(x.content order by x.position)
                            from public.disease_emergency_signs x where x.disease_id = d.id), '[]'),
        'prevention', coalesce((select jsonb_agg(jsonb_build_object(
                                    'tier', x.tier, 'content', x.content) order by x.position)
                            from public.disease_prevention x where x.disease_id = d.id), '[]'),
        'differentials', coalesce((select jsonb_agg(jsonb_build_object(
                                    'condition', x.condition,
                                    'distinguishing_feature', x.distinguishing_feature)
                                    order by x.position)
                            from public.disease_differentials x where x.disease_id = d.id), '[]'),
        'references', coalesce((select jsonb_agg(jsonb_build_object(
                                    'source_name', x.source_name, 'citation_text', x.citation_text,
                                    'url', coalesce(x.url, ''), 'is_mother_book', x.is_mother_book)
                                    order by x.position)
                            from public.clinical_references x where x.disease_id = d.id), '[]'),
        'symptoms', coalesce((select jsonb_agg(jsonb_build_object(
                                    'symptom_id', x.symptom_id, 'name', s.name,
                                    'typical_intensity', x.typical_intensity,
                                    'is_primary', x.is_primary,
                                    'weight_multiplier', x.weight_multiplier)
                                    order by x.is_primary desc, x.typical_intensity desc)
                            from public.disease_symptoms x
                            join public.symptoms s on s.id = x.symptom_id
                            where x.disease_id = d.id), '[]'),
        'medicines', coalesce((select jsonb_agg(jsonb_build_object(
                                    'medicine_id', x.medicine_id, 'name', m.name,
                                    'safety', x.safety, 'note', coalesce(x.note, ''))
                                    order by x.position)
                            from public.disease_medicines x
                            join public.medicines m on m.id = x.medicine_id
                            where x.disease_id = d.id), '[]'),
        'related', coalesce((select jsonb_agg(x.related_disease_id order by x.related_disease_id)
                            from public.disease_related x where x.disease_id = d.id), '[]'),
        'tags', coalesce((select jsonb_agg(x.tag order by x.tag)
                            from public.disease_tags x where x.disease_id = d.id), '[]'))
    into v
    from public.diseases d where d.id = p_id;
    if v is null then raise exception 'That disease no longer exists.'; end if;
    return v;
end $$;

create or replace function public.admin_get_symptom(p_id text)
returns jsonb
language plpgsql stable security definer set search_path = ''
as $$
declare v jsonb;
begin
    perform public.ad_me();
    select to_jsonb(s) || jsonb_build_object(
        'causes', coalesce((select jsonb_agg(x.content order by x.position)
                            from public.symptom_causes x where x.symptom_id = s.id), '[]'),
        'red_flags', coalesce((select jsonb_agg(x.content order by x.position)
                            from public.symptom_red_flags x where x.symptom_id = s.id), '[]'),
        'references', coalesce((select jsonb_agg(jsonb_build_object(
                                    'source_name', x.source_name, 'citation_text', x.citation_text,
                                    'url', coalesce(x.url, ''), 'is_mother_book', x.is_mother_book)
                                    order by x.position)
                            from public.symptom_references x where x.symptom_id = s.id), '[]'))
    into v
    from public.symptoms s where s.id = p_id;
    if v is null then raise exception 'That symptom no longer exists.'; end if;
    return v;
end $$;

create or replace function public.admin_get_medicine(p_id text)
returns jsonb
language plpgsql stable security definer set search_path = ''
as $$
declare v jsonb;
begin
    perform public.ad_me();
    select to_jsonb(m) || jsonb_build_object(
        'facts', coalesce((select jsonb_object_agg(f.kind, f.lines) from (
                              select x.kind, jsonb_agg(x.content order by x.position) as lines
                              from public.medicine_facts x where x.medicine_id = m.id
                              group by x.kind) f), '{}'),
        'references', coalesce((select jsonb_agg(jsonb_build_object(
                                    'source_name', x.source_name, 'citation_text', x.citation_text,
                                    'url', coalesce(x.url, ''), 'is_mother_book', x.is_mother_book)
                                    order by x.position)
                            from public.medicine_references x where x.medicine_id = m.id), '[]'))
    into v
    from public.medicines m where m.id = p_id;
    if v is null then raise exception 'That medicine no longer exists.'; end if;
    return v;
end $$;


-- ---------------------------------------------------------------------
-- 7. Content Management: saving
-- ---------------------------------------------------------------------
-- Replace an entry's ordered text list (disease_causes, symptom_red_flags, ...)
create or replace function public.ad_replace_lines(p_table text, p_fk text, p_id text,
                                                   p_lines jsonb)
returns void
language plpgsql security definer set search_path = ''
as $$
begin
    execute format('delete from public.%I where %I = $1', p_table, p_fk) using p_id;
    execute format('insert into public.%I (%I, position, content) '
                   'select $1, pos, line from public.ad_lines($2)', p_table, p_fk)
        using p_id, p_lines;
end $$;

-- References: [{source_name, citation_text, url, is_mother_book}, ...]
create or replace function public.ad_reference_rows(p jsonb)
returns table (pos integer, source_name text, citation_text text, url text,
               is_mother_book boolean)
language sql immutable set search_path = ''
as $$
    select (row_number() over (order by o) - 1)::integer,
           btrim(r ->> 'source_name'), btrim(coalesce(r ->> 'citation_text', '')),
           btrim(coalesce(r ->> 'url', '')), coalesce((r ->> 'is_mother_book')::boolean, false)
    from jsonb_array_elements(case when jsonb_typeof(p) = 'array' then p else '[]'::jsonb end)
         with ordinality as t(r, o)
    where coalesce(btrim(r ->> 'source_name'), '') <> '';
$$;

create or replace function public.admin_save_disease(p jsonb, p_new boolean)
returns text
language plpgsql security definer set search_path = ''
as $$
declare
    me uuid := public.ad_me();
    v_id text := lower(btrim(coalesce(p ->> 'id', '')));
    v_name text := btrim(coalesce(p ->> 'name', ''));
    v_body text := nullif(btrim(coalesce(p ->> 'body_system_id', '')), '');
    t text;
begin
    perform public.ad_check_entry(v_id, v_name, 'disease');
    if coalesce(btrim(p ->> 'description'), '') = '' then
        raise exception 'Write a clinical summary (description) for the disease.';
    end if;
    if v_body is not null and not exists (select 1 from public.body_systems where id = v_body) then
        raise exception 'Unknown body system.';
    end if;

    if p_new then
        if exists (select 1 from public.diseases where id = v_id) then
            raise exception 'A disease with the ID "%" already exists.', v_id;
        end if;
        insert into public.diseases (id, name, description) values (v_id, v_name, '');
    elsif not exists (select 1 from public.diseases where id = v_id) then
        raise exception 'That disease no longer exists.';
    end if;

    update public.diseases set
        name = v_name,
        scientific_name = nullif(btrim(coalesce(p ->> 'scientific_name', '')), ''),
        description = btrim(p ->> 'description'),
        body_system_id = v_body,
        severity = coalesce(nullif(p ->> 'severity', ''), 'Moderate')::public.severity_level,
        urgency = nullif(p ->> 'urgency', '')::public.urgency_level,
        urgency_criteria = nullif(btrim(coalesce(p ->> 'urgency_criteria', '')), ''),
        contagious = coalesce((p ->> 'contagious')::boolean, false),
        onset_progression = nullif(btrim(coalesce(p ->> 'onset_progression', '')), ''),
        pathophysiology = nullif(btrim(coalesce(p ->> 'pathophysiology', '')), ''),
        clinicopathologic_correlation =
            nullif(btrim(coalesce(p ->> 'clinicopathologic_correlation', '')), ''),
        follow_up_monitoring = nullif(btrim(coalesce(p ->> 'follow_up_monitoring', '')), ''),
        source_attribution = nullif(btrim(coalesce(p ->> 'source_attribution', '')), ''),
        is_published = coalesce((p ->> 'is_published')::boolean, true),
        updated_at = now()
    where id = v_id;

    foreach t in array array['causes', 'risk_factors', 'recommended_tests', 'treatments',
                             'home_care', 'emergency_signs'] loop
        perform public.ad_replace_lines('disease_' || t, 'disease_id', v_id, p -> t);
    end loop;

    delete from public.disease_prevention where disease_id = v_id;
    insert into public.disease_prevention (disease_id, position, content, tier)
    select v_id, (row_number() over (order by o) - 1)::integer, btrim(r ->> 'content'),
           nullif(r ->> 'tier', '')::public.prevention_tier
    from jsonb_array_elements(coalesce(p -> 'prevention', '[]')) with ordinality as x(r, o)
    where coalesce(btrim(r ->> 'content'), '') <> '';

    delete from public.disease_differentials where disease_id = v_id;
    insert into public.disease_differentials (disease_id, position, condition, distinguishing_feature)
    select v_id, (row_number() over (order by o) - 1)::integer, btrim(r ->> 'condition'),
           btrim(coalesce(r ->> 'distinguishing_feature', ''))
    from jsonb_array_elements(coalesce(p -> 'differentials', '[]')) with ordinality as x(r, o)
    where coalesce(btrim(r ->> 'condition'), '') <> '';

    delete from public.clinical_references where disease_id = v_id;
    insert into public.clinical_references
        (id, disease_id, position, source_name, citation_text, url, is_mother_book)
    select 'ref_' || v_id || '_' || (r.pos + 1), v_id, r.pos, r.source_name, r.citation_text,
           nullif(r.url, ''), r.is_mother_book
    from public.ad_reference_rows(p -> 'references') r;

    -- Links: unknown ids are skipped, duplicates keep the first row.
    delete from public.disease_symptoms where disease_id = v_id;
    insert into public.disease_symptoms
        (disease_id, symptom_id, typical_intensity, is_primary, weight_multiplier)
    select distinct on (r ->> 'symptom_id') v_id, r ->> 'symptom_id',
           least(10, greatest(1, coalesce((r ->> 'typical_intensity')::integer, 5)))::smallint,
           coalesce((r ->> 'is_primary')::boolean, false),
           least(5, greatest(0.1, coalesce((r ->> 'weight_multiplier')::numeric, 1.0)))
    from jsonb_array_elements(coalesce(p -> 'symptoms', '[]')) with ordinality as x(r, o)
    join public.symptoms s on s.id = r ->> 'symptom_id'
    order by r ->> 'symptom_id', o;

    delete from public.disease_medicines where disease_id = v_id;
    insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
    select distinct on (r ->> 'medicine_id') v_id, r ->> 'medicine_id',
           (o - 1)::integer, coalesce(nullif(r ->> 'safety', ''), 'safe')::public.condition_safety,
           nullif(btrim(coalesce(r ->> 'note', '')), '')
    from jsonb_array_elements(coalesce(p -> 'medicines', '[]')) with ordinality as x(r, o)
    join public.medicines m on m.id = r ->> 'medicine_id'
    order by r ->> 'medicine_id', o;

    delete from public.disease_related where disease_id = v_id;
    insert into public.disease_related (disease_id, related_disease_id)
    select distinct v_id, r.v
    from jsonb_array_elements_text(coalesce(p -> 'related', '[]')) as r(v)
    join public.diseases d on d.id = r.v
    where r.v <> v_id;

    delete from public.disease_tags where disease_id = v_id;
    insert into public.disease_tags (disease_id, tag)
    select distinct v_id, l.line from public.ad_lines(p -> 'tags') l;

    perform public.ad_bump();
    perform public.ad_log(case when p_new then 'create' else 'update' end,
                          'disease', v_id, v_name);
    return v_id;
end $$;

create or replace function public.admin_save_symptom(p jsonb, p_new boolean)
returns text
language plpgsql security definer set search_path = ''
as $$
declare
    me uuid := public.ad_me();
    v_id text := lower(btrim(coalesce(p ->> 'id', '')));
    v_name text := btrim(coalesce(p ->> 'name', ''));
    v_body text := nullif(btrim(coalesce(p ->> 'body_system_id', '')), '');
begin
    perform public.ad_check_entry(v_id, v_name, 'symptom');
    if v_body is not null and not exists (select 1 from public.body_systems where id = v_body) then
        raise exception 'Unknown body system.';
    end if;
    if p_new then
        if exists (select 1 from public.symptoms where id = v_id) then
            raise exception 'A symptom with the ID "%" already exists.', v_id;
        end if;
        insert into public.symptoms (id, name) values (v_id, v_name);
    elsif not exists (select 1 from public.symptoms where id = v_id) then
        raise exception 'That symptom no longer exists.';
    end if;

    update public.symptoms set
        name = v_name,
        scientific_name = btrim(coalesce(p ->> 'scientific_name', '')),
        description = nullif(btrim(coalesce(p ->> 'description', '')), ''),
        body_system_id = v_body,
        is_red_flag = coalesce((p ->> 'is_red_flag')::boolean, false),
        diagnostic_weight = least(10, greatest(1, coalesce((p ->> 'diagnostic_weight')::integer, 5))),
        weight_rationale = btrim(coalesce(p ->> 'weight_rationale', '')),
        tags = coalesce((select array_agg(distinct l.line) from public.ad_lines(p -> 'tags') l),
                        '{}'),
        source_attribution = btrim(coalesce(p ->> 'source_attribution', '')),
        is_published = coalesce((p ->> 'is_published')::boolean, true),
        updated_at = now()
    where id = v_id;

    perform public.ad_replace_lines('symptom_causes', 'symptom_id', v_id, p -> 'causes');
    perform public.ad_replace_lines('symptom_red_flags', 'symptom_id', v_id, p -> 'red_flags');

    delete from public.symptom_references where symptom_id = v_id;
    insert into public.symptom_references
        (symptom_id, source_name, citation_text, url, is_mother_book, position)
    select v_id, r.source_name, r.citation_text, r.url, r.is_mother_book, r.pos
    from public.ad_reference_rows(p -> 'references') r;

    perform public.ad_bump();
    perform public.ad_log(case when p_new then 'create' else 'update' end,
                          'symptom', v_id, v_name);
    return v_id;
end $$;

create or replace function public.admin_save_medicine(p jsonb, p_new boolean)
returns text
language plpgsql security definer set search_path = ''
as $$
declare
    me uuid := public.ad_me();
    v_id text := lower(btrim(coalesce(p ->> 'id', '')));
    v_name text := btrim(coalesce(p ->> 'name', ''));
    v_kind text;
begin
    perform public.ad_check_entry(v_id, v_name, 'medicine');
    if p_new then
        if exists (select 1 from public.medicines where id = v_id) then
            raise exception 'A medicine with the ID "%" already exists.', v_id;
        end if;
        insert into public.medicines (id, name) values (v_id, v_name);
    elsif not exists (select 1 from public.medicines where id = v_id) then
        raise exception 'That medicine no longer exists.';
    end if;

    update public.medicines set
        name = v_name,
        generic_name = nullif(btrim(coalesce(p ->> 'generic_name', '')), ''),
        international_generic_name = btrim(coalesce(p ->> 'international_generic_name', '')),
        trade_name = nullif(btrim(coalesce(p ->> 'trade_name', '')), ''),
        drug_class = nullif(btrim(coalesce(p ->> 'drug_class', '')), ''),
        category = coalesce(nullif(p ->> 'category', ''), 'Prescription')::public.medicine_category,
        description = nullif(btrim(coalesce(p ->> 'description', '')), ''),
        dosage_text = btrim(coalesce(p ->> 'dosage_text', '')),
        storage = btrim(coalesce(p ->> 'storage', '')),
        black_box_warning = nullif(btrim(coalesce(p ->> 'black_box_warning', '')), ''),
        source_attribution = btrim(coalesce(p ->> 'source_attribution', '')),
        is_published = coalesce((p ->> 'is_published')::boolean, true),
        updated_at = now()
    where id = v_id;

    -- The app reads these kinds from medicine_facts.
    delete from public.medicine_facts where medicine_id = v_id;
    foreach v_kind in array array['brand_ph', 'brand_intl', 'indication', 'adverse',
                                  'contraindication', 'interaction'] loop
        insert into public.medicine_facts (medicine_id, kind, content, position)
        select v_id, v_kind, l.line, l.pos from public.ad_lines(p -> 'facts' -> v_kind) l;
    end loop;
    -- Brand names are also kept in medicine_brands, for anything reading that table.
    delete from public.medicine_brands where medicine_id = v_id;
    insert into public.medicine_brands (medicine_id, market, position, brand_name)
    select v_id, 'philippine'::public.brand_market, l.pos, l.line from public.ad_lines(p -> 'facts' -> 'brand_ph') l
    union all
    select v_id, 'international'::public.brand_market, l.pos, l.line from public.ad_lines(p -> 'facts' -> 'brand_intl') l;

    delete from public.medicine_references where medicine_id = v_id;
    insert into public.medicine_references
        (medicine_id, source_name, citation_text, url, is_mother_book, position)
    select v_id, r.source_name, r.citation_text, r.url, r.is_mother_book, r.pos
    from public.ad_reference_rows(p -> 'references') r;

    perform public.ad_bump();
    perform public.ad_log(case when p_new then 'create' else 'update' end,
                          'medicine', v_id, v_name);
    return v_id;
end $$;

-- Archive (hide from the app) or restore. Nothing is deleted.
create or replace function public.admin_set_published(p_kind text, p_id text, p_published boolean)
returns void
language plpgsql security definer set search_path = ''
as $$
declare
    me uuid := public.ad_me();
    v_table text;
    v_name text;
begin
    v_table := case p_kind when 'disease' then 'diseases' when 'symptom' then 'symptoms'
                           when 'medicine' then 'medicines' end;
    if v_table is null then raise exception 'Unknown content type.'; end if;
    execute format('update public.%I set is_published = $1, updated_at = now() '
                   'where id = $2 returning name', v_table)
        into v_name using p_published, p_id;
    if v_name is null then raise exception 'That entry no longer exists.'; end if;
    perform public.ad_bump();
    perform public.ad_log(case when p_published then 'restore' else 'archive' end,
                          p_kind, p_id, v_name);
end $$;


-- ---------------------------------------------------------------------
-- 8. Audit trail
-- ---------------------------------------------------------------------
create or replace function public.admin_audit(p_limit integer default 100,
                                              p_before bigint default null)
returns jsonb
language plpgsql stable security definer set search_path = ''
as $$
begin
    perform public.ad_me();
    return jsonb_build_object(
        'total', (select count(*) from public.admin_audit_log),
        'items', coalesce((
            select jsonb_agg(to_jsonb(a) order by a.id desc)
            from (select * from public.admin_audit_log l
                  where p_before is null or l.id < p_before
                  order by l.id desc limit least(greatest(coalesce(p_limit, 100), 1), 500)) a
        ), '[]'::jsonb));
end $$;


-- ---------------------------------------------------------------------
-- 9. Who may call what
-- ---------------------------------------------------------------------
do $$
declare fn text;
begin
    foreach fn in array array[
        'public.ad_me()', 'public.ad_log(text, text, text, text, jsonb)', 'public.ad_bump()',
        'public.ad_lines(jsonb)', 'public.ad_check_entry(text, text, text)',
        'public.ad_replace_lines(text, text, text, jsonb)', 'public.ad_reference_rows(jsonb)'] loop
        execute format('revoke execute on function %s from public, anon, authenticated', fn);
    end loop;
    -- Signed-in users may call these; each one checks for an admin itself.
    foreach fn in array array[
        'public.admin_users()', 'public.admin_user_detail(uuid)',
        'public.admin_set_role(uuid, text)', 'public.admin_set_suspended(uuid, boolean, text)',
        'public.admin_delete_user(uuid, text)', 'public.admin_body_systems()',
        'public.admin_list_diseases()', 'public.admin_list_symptoms()',
        'public.admin_list_medicines()', 'public.admin_get_disease(text)',
        'public.admin_get_symptom(text)', 'public.admin_get_medicine(text)',
        'public.admin_save_disease(jsonb, boolean)', 'public.admin_save_symptom(jsonb, boolean)',
        'public.admin_save_medicine(jsonb, boolean)',
        'public.admin_set_published(text, text, boolean)', 'public.admin_audit(integer, bigint)'] loop
        execute format('revoke execute on function %s from public, anon', fn);
        execute format('grant execute on function %s to authenticated', fn);
    end loop;
end $$;

commit;

-- =====================================================================
-- Checks (in the SQL editor these run as the owner, so ad_me() refuses:
-- try them from the app instead). Counts that should work here:
--   select count(*) from public.admin_audit_log;      -- 0 at first
--   select id, suspended_at from public.profiles limit 5;
-- Make someone an admin (only from here, or by another admin in the app):
--   update public.user_roles set role = 'admin' where user_id = '<their id>';
-- =====================================================================
