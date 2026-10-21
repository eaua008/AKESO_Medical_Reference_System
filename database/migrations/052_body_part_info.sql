-- =====================================================================
-- Akeso migration 052: body part descriptions (Body System Explorer)
-- =====================================================================
-- Run AFTER 051_flashcard_teaching_fields.sql. Safe to run again.
-- See docs/body-part-descriptions-plan.md.
--
--   body_part_info       one description per concept (a part name with
--                        left/right removed, e.g. 'femur') or per group
--                        ('group:<id>'), covering both sides. Plain text
--                        for everyone, a "For students" level, clinical
--                        notes linked to disease pages, an exam tip and
--                        the sources it was written from.
--   status               draft -> reviewed -> published. Everyone can read
--                        published rows; drafts are for admins only.
--   admin functions      list, get, save, set status. Each one checks for
--                        an admin, writes to the audit log, and bumps
--                        content_version whenever published text changes,
--                        so running apps re-download it like the
--                        encyclopedia.
-- Content batches (053_body_parts_01.sql, ...) upsert rows as drafts.
-- =====================================================================

begin;

-- ---------------------------------------------------------------------
-- 1. Table
-- ---------------------------------------------------------------------
create table if not exists public.body_part_info (
    key            text primary key,
    kind           text not null default 'part',
    fma_ids        text[] not null default '{}',
    layer          text not null default '',
    system         text not null default '',
    display_name   text not null,
    aliases        text[] not null default '{}',
    name_tl        text not null default '',
    summary_plain  text not null default '',
    function_plain text not null default '',
    description    text not null default '',
    location       text not null default '',
    details        jsonb not null default '{}'::jsonb,
    clinical       jsonb not null default '[]'::jsonb,
    exam_tip       text not null default '',
    sources        jsonb not null default '[]'::jsonb,
    status         text not null default 'draft',
    reviewed_by    uuid references auth.users (id) on delete set null,
    created_at     timestamptz not null default now(),
    updated_at     timestamptz not null default now(),
    constraint body_part_info_kind check (kind in ('part', 'group')),
    constraint body_part_info_key check (
        (kind = 'part' and key ~ '^[a-z0-9][a-z0-9 ,()''-]*$')
        or (kind = 'group' and key ~ '^group:[A-Za-z0-9_]+$')),
    constraint body_part_info_layer check (layer in ('', 'bone', 'muscle', 'organ', 'vessel', 'nerve', 'skin')),
    constraint body_part_info_status check (status in ('draft', 'reviewed', 'published')),
    constraint body_part_info_name check (btrim(display_name) <> '' and length(display_name) <= 120),
    constraint body_part_info_details check (jsonb_typeof(details) = 'object'),
    constraint body_part_info_clinical check (jsonb_typeof(clinical) = 'array'),
    constraint body_part_info_sources check (jsonb_typeof(sources) = 'array')
);

-- "Which entry covers this FMA id?" (the Explorer looks parts up by FMA id).
create index if not exists body_part_info_fma_idx on public.body_part_info using gin (fma_ids);

-- ---------------------------------------------------------------------
-- 2. Who can read it
-- ---------------------------------------------------------------------
alter table public.body_part_info enable row level security;
revoke all on public.body_part_info from anon, authenticated;
grant select on public.body_part_info to anon, authenticated;
-- Writes only through the admin functions below.

drop policy if exists "body parts: read published" on public.body_part_info;
create policy "body parts: read published" on public.body_part_info
    for select to anon, authenticated using (status = 'published');

-- ---------------------------------------------------------------------
-- 3. Helpers (not callable from the app)
-- ---------------------------------------------------------------------
-- A JSON array of strings -> a clean text[] (trimmed, no blanks, no repeats).
create or replace function public.bp_text_array(p jsonb)
returns text[]
language sql immutable set search_path = ''
as $$
    select coalesce(array_agg(v order by o), '{}')
    from (select distinct on (lower(btrim(v))) btrim(v) as v, o
          from jsonb_array_elements_text(
                   case when jsonb_typeof(p) = 'array' then p else '[]'::jsonb end)
               with ordinality as t(v, o)
          where btrim(v) <> ''
          order by lower(btrim(v)), o) s;
$$;

-- Clinical lines: [{text, disease_id?}], with every disease_id checked.
create or replace function public.bp_clinical(p jsonb)
returns jsonb
language plpgsql stable set search_path = ''
as $$
declare
    e jsonb;
    v_text text;
    v_dis text;
    out jsonb := '[]'::jsonb;
begin
    for e in select x from jsonb_array_elements(
                 case when jsonb_typeof(p) = 'array' then p else '[]'::jsonb end) x loop
        v_text := btrim(coalesce(e ->> 'text', ''));
        v_dis := nullif(btrim(coalesce(e ->> 'disease_id', '')), '');
        continue when v_text = '';
        if v_dis is not null and not exists (select 1 from public.diseases where id = v_dis) then
            raise exception 'A clinical note links to a disease that does not exist.';
        end if;
        out := out || jsonb_build_array(
            case when v_dis is null then jsonb_build_object('text', v_text)
                 else jsonb_build_object('text', v_text, 'disease_id', v_dis) end);
    end loop;
    return out;
end $$;

-- Sources: [{title, url, licence}], https links only.
create or replace function public.bp_sources(p jsonb)
returns jsonb
language plpgsql immutable set search_path = ''
as $$
declare
    e jsonb;
    out jsonb := '[]'::jsonb;
begin
    for e in select x from jsonb_array_elements(
                 case when jsonb_typeof(p) = 'array' then p else '[]'::jsonb end) x loop
        continue when btrim(coalesce(e ->> 'title', '')) = '';
        if coalesce(e ->> 'url', '') !~ '^https://' then
            raise exception 'Every source needs a web link that starts with https://.';
        end if;
        out := out || jsonb_build_array(jsonb_build_object(
            'title', btrim(e ->> 'title'), 'url', btrim(e ->> 'url'),
            'licence', btrim(coalesce(e ->> 'licence', ''))));
    end loop;
    return out;
end $$;

-- ---------------------------------------------------------------------
-- 4. Admin functions
-- ---------------------------------------------------------------------
create or replace function public.admin_list_body_parts()
returns jsonb
language plpgsql stable security definer set search_path = ''
as $$
declare me uuid := public.ad_me();
begin
    return coalesce((
        select jsonb_agg(jsonb_build_object(
                   'key', b.key, 'kind', b.kind, 'display_name', b.display_name,
                   'layer', b.layer, 'system', b.system, 'status', b.status,
                   'has_text', b.summary_plain <> '' or b.description <> '',
                   'updated_at', b.updated_at)
               order by b.layer, lower(b.display_name))
        from public.body_part_info b), '[]'::jsonb);
end $$;

create or replace function public.admin_get_body_part(p_key text)
returns jsonb
language plpgsql stable security definer set search_path = ''
as $$
declare
    me uuid := public.ad_me();
    r jsonb;
begin
    select to_jsonb(b) into r from public.body_part_info b where b.key = p_key;
    if r is null then raise exception 'That body part has no description yet.'; end if;
    return r;
end $$;

-- Create or edit one entry. The status is kept (set it with
-- admin_set_body_part_status); editing published text re-publishes it.
create or replace function public.admin_save_body_part(p jsonb)
returns text
language plpgsql security definer set search_path = ''
as $$
declare
    me uuid := public.ad_me();
    v_key text := btrim(coalesce(p ->> 'key', ''));
    v_kind text := coalesce(nullif(btrim(p ->> 'kind'), ''), 'part');
    v_name text := btrim(coalesce(p ->> 'display_name', ''));
    v_new boolean;
    v_status text;
begin
    if v_key = '' then raise exception 'The entry needs a key.'; end if;
    if v_name = '' then raise exception 'The entry needs a name.'; end if;
    select status into v_status from public.body_part_info where key = v_key;
    v_new := v_status is null;
    insert into public.body_part_info as b (
        key, kind, fma_ids, layer, system, display_name, aliases, name_tl,
        summary_plain, function_plain, description, location, details,
        clinical, exam_tip, sources, updated_at)
    values (
        v_key, v_kind, public.bp_text_array(p -> 'fma_ids'),
        coalesce(btrim(p ->> 'layer'), ''), coalesce(btrim(p ->> 'system'), ''),
        v_name, public.bp_text_array(p -> 'aliases'), coalesce(btrim(p ->> 'name_tl'), ''),
        coalesce(btrim(p ->> 'summary_plain'), ''), coalesce(btrim(p ->> 'function_plain'), ''),
        coalesce(btrim(p ->> 'description'), ''), coalesce(btrim(p ->> 'location'), ''),
        case when jsonb_typeof(p -> 'details') = 'object' then p -> 'details' else '{}'::jsonb end,
        public.bp_clinical(p -> 'clinical'), coalesce(btrim(p ->> 'exam_tip'), ''),
        public.bp_sources(p -> 'sources'), now())
    on conflict (key) do update set
        kind = excluded.kind, fma_ids = excluded.fma_ids, layer = excluded.layer,
        system = excluded.system, display_name = excluded.display_name,
        aliases = excluded.aliases, name_tl = excluded.name_tl,
        summary_plain = excluded.summary_plain, function_plain = excluded.function_plain,
        description = excluded.description, location = excluded.location,
        details = excluded.details, clinical = excluded.clinical,
        exam_tip = excluded.exam_tip, sources = excluded.sources, updated_at = now();
    if v_status = 'published' then perform public.ad_bump(); end if;
    perform public.ad_log(case when v_new then 'create' else 'update' end,
                          'body_part', v_key, v_name);
    return v_key;
end $$;

create or replace function public.admin_set_body_part_status(p_key text, p_status text)
returns void
language plpgsql security definer set search_path = ''
as $$
declare
    me uuid := public.ad_me();
    v_old text;
    v_name text;
begin
    if p_status not in ('draft', 'reviewed', 'published') then
        raise exception 'Unknown status.';
    end if;
    select status, display_name into v_old, v_name from public.body_part_info where key = p_key;
    if v_old is null then raise exception 'That entry no longer exists.'; end if;
    if p_status = 'published' and not exists (
        select 1 from public.body_part_info
        where key = p_key and jsonb_array_length(sources) > 0) then
        raise exception 'Add at least one source before publishing.';
    end if;
    update public.body_part_info
    set status = p_status,
        reviewed_by = case when p_status = 'draft' then reviewed_by else me end,
        updated_at = now()
    where key = p_key;
    if 'published' in (v_old, p_status) and v_old is distinct from p_status then
        perform public.ad_bump();
    end if;
    perform public.ad_log('status', 'body_part', p_key, v_name,
                          jsonb_build_object('from', v_old, 'to', p_status));
end $$;

-- ---------------------------------------------------------------------
-- 5. Who may call what
-- ---------------------------------------------------------------------
do $$
declare fn text;
begin
    foreach fn in array array[
        'public.bp_text_array(jsonb)', 'public.bp_clinical(jsonb)', 'public.bp_sources(jsonb)'] loop
        execute format('revoke execute on function %s from public, anon, authenticated', fn);
    end loop;
    -- Signed-in users may call these; each one checks for an admin itself.
    foreach fn in array array[
        'public.admin_list_body_parts()', 'public.admin_get_body_part(text)',
        'public.admin_save_body_part(jsonb)', 'public.admin_set_body_part_status(text, text)'] loop
        execute format('revoke execute on function %s from public, anon', fn);
        execute format('grant execute on function %s to authenticated', fn);
    end loop;
end $$;

commit;
