-- =====================================================================
-- Akeso 005: Health Articles
--
-- Two kinds of article, in one list:
--   written    an article written by the Akeso team in Content Management
--              (title, summary, body, author, last reviewed date, references)
--   external   a curated link to a trusted source (WHO, DOH, MedlinePlus...):
--              title, summary, source and URL; it opens in the app's
--              built-in reference browser
--
-- Either kind can be linked to diseases, symptoms and medicines. The
-- article shows those links, and each linked encyclopedia page lists its
-- related articles.
--
-- Who can do what:
--   * everyone (signed in or not) reads PUBLISHED articles, through RLS
--   * only admins (after two-factor) create, edit, archive and restore,
--     through the admin_* functions below; every change is in the audit
--     trail (migration 004)
--
-- Run after 004_admin.sql. Safe to run again.
-- =====================================================================

begin;

-- ---------------------------------------------------------------------
-- 1. Tables
-- ---------------------------------------------------------------------
create table if not exists public.health_articles (
    id            text primary key check (id ~ '^[a-z0-9_]{2,60}$'),
    name          text not null check (char_length(name) between 1 and 160),   -- the title
    kind          text not null default 'written' check (kind in ('written', 'external')),
    category      text not null default 'General' check (char_length(category) <= 60),
    summary       text not null default '' check (char_length(summary) <= 600),
    body          text not null default '' check (char_length(body) <= 60000),
    url           text not null default '' check (url = '' or url ~ '^https?://'),
    source_name   text not null default '' check (char_length(source_name) <= 160),
    author_name   text not null default '' check (char_length(author_name) <= 120),
    reviewed_on   date,
    is_published  boolean not null default false,
    created_at    timestamptz not null default now(),
    updated_at    timestamptz not null default now(),
    -- A written article needs a body; a link needs its address.
    constraint health_articles_content check (
        (kind = 'written' and btrim(body) <> '') or (kind = 'external' and url <> ''))
);

create table if not exists public.health_article_references (
    article_id     text not null references public.health_articles (id) on delete cascade,
    position       integer not null,
    source_name    text not null,
    citation_text  text not null default '',
    url            text not null default '',
    is_mother_book boolean not null default false,
    primary key (article_id, position)
);

create table if not exists public.health_article_links (
    article_id  text not null references public.health_articles (id) on delete cascade,
    kind        text not null check (kind in ('disease', 'symptom', 'medicine')),
    ref_id      text not null,
    primary key (article_id, kind, ref_id)
);
create index if not exists health_article_links_ref_idx
    on public.health_article_links (kind, ref_id);


-- ---------------------------------------------------------------------
-- 2. Row-level security: read published, write only through functions
-- ---------------------------------------------------------------------
alter table public.health_articles           enable row level security;
alter table public.health_article_references enable row level security;
alter table public.health_article_links      enable row level security;

revoke all on public.health_articles, public.health_article_references,
              public.health_article_links from anon, authenticated;
grant select on public.health_articles, public.health_article_references,
                public.health_article_links to anon, authenticated;

drop policy if exists "articles: read published" on public.health_articles;
create policy "articles: read published" on public.health_articles
    for select to anon, authenticated using (is_published);

drop policy if exists "article refs: read published" on public.health_article_references;
create policy "article refs: read published" on public.health_article_references
    for select to anon, authenticated
    using (exists (select 1 from public.health_articles a
                   where a.id = article_id and a.is_published));

drop policy if exists "article links: read published" on public.health_article_links;
create policy "article links: read published" on public.health_article_links
    for select to anon, authenticated
    using (exists (select 1 from public.health_articles a
                   where a.id = article_id and a.is_published));


-- ---------------------------------------------------------------------
-- 3. Content Management: list, read, save
-- ---------------------------------------------------------------------
create or replace function public.admin_list_articles()
returns jsonb
language plpgsql stable security definer set search_path = ''
as $$
begin
    perform public.ad_me();
    return coalesce((
        select jsonb_agg(jsonb_build_object(
            'id', a.id, 'name', a.name, 'kind', a.kind, 'category', a.category,
            'source_name', a.source_name, 'published', a.is_published,
            'updated_at', a.updated_at,
            'link_count', (select count(*) from public.health_article_links l
                           where l.article_id = a.id)
        ) order by a.updated_at desc)
        from public.health_articles a
    ), '[]'::jsonb);
end $$;

create or replace function public.admin_get_article(p_id text)
returns jsonb
language plpgsql stable security definer set search_path = ''
as $$
declare v jsonb;
begin
    perform public.ad_me();
    select to_jsonb(a) || jsonb_build_object(
        'links', coalesce((select jsonb_agg(jsonb_build_object('kind', l.kind, 'ref_id', l.ref_id)
                                            order by l.kind, l.ref_id)
                           from public.health_article_links l where l.article_id = a.id), '[]'),
        'references', coalesce((select jsonb_agg(jsonb_build_object(
                                    'source_name', x.source_name, 'citation_text', x.citation_text,
                                    'url', x.url, 'is_mother_book', x.is_mother_book)
                                    order by x.position)
                                from public.health_article_references x
                                where x.article_id = a.id), '[]'))
    into v
    from public.health_articles a where a.id = p_id;
    if v is null then raise exception 'That article no longer exists.'; end if;
    return v;
end $$;

create or replace function public.admin_save_article(p jsonb, p_new boolean)
returns text
language plpgsql security definer set search_path = ''
as $$
declare
    me uuid := public.ad_me();
    v_id text := lower(btrim(coalesce(p ->> 'id', '')));
    v_name text := btrim(coalesce(p ->> 'name', ''));
    v_kind text := coalesce(p ->> 'kind', 'written');
    v_url text := btrim(coalesce(p ->> 'url', ''));
    v_body text := btrim(coalesce(p ->> 'body', ''));
    v_reviewed date;
begin
    perform public.ad_check_entry(v_id, v_name, 'article');
    if v_kind not in ('written', 'external') then
        raise exception 'Choose whether this is a written article or an external link.';
    end if;
    if v_url <> '' and v_url !~ '^https?://' then
        raise exception 'The link must start with http:// or https://.';
    end if;
    if v_kind = 'external' and v_url = '' then
        raise exception 'An external article needs its link.';
    end if;
    if v_kind = 'written' and v_body = '' then
        raise exception 'Write the article text.';
    end if;
    begin
        v_reviewed := nullif(btrim(coalesce(p ->> 'reviewed_on', '')), '')::date;
    exception when others then
        raise exception 'Write the review date as YYYY-MM-DD.';
    end;

    if p_new then
        if exists (select 1 from public.health_articles where id = v_id) then
            raise exception 'An article with the ID "%" already exists.', v_id;
        end if;
        insert into public.health_articles (id, name, kind, body, url)
        values (v_id, v_name, v_kind, v_body, v_url);
    elsif not exists (select 1 from public.health_articles where id = v_id) then
        raise exception 'That article no longer exists.';
    end if;

    update public.health_articles set
        name = v_name,
        kind = v_kind,
        category = coalesce(nullif(btrim(coalesce(p ->> 'category', '')), ''), 'General'),
        summary = btrim(coalesce(p ->> 'summary', '')),
        body = v_body,
        url = v_url,
        source_name = btrim(coalesce(p ->> 'source_name', '')),
        author_name = btrim(coalesce(p ->> 'author_name', '')),
        reviewed_on = v_reviewed,
        is_published = coalesce((p ->> 'is_published')::boolean, false),
        updated_at = now()
    where id = v_id;

    delete from public.health_article_links where article_id = v_id;
    insert into public.health_article_links (article_id, kind, ref_id)
    select distinct v_id, l ->> 'kind', l ->> 'ref_id'
    from jsonb_array_elements(case when jsonb_typeof(p -> 'links') = 'array'
                                   then p -> 'links' else '[]'::jsonb end) as l
    where l ->> 'kind' in ('disease', 'symptom', 'medicine')
      and coalesce(l ->> 'ref_id', '') <> '';

    delete from public.health_article_references where article_id = v_id;
    insert into public.health_article_references
        (article_id, source_name, citation_text, url, is_mother_book, position)
    select v_id, r.source_name, r.citation_text, r.url, r.is_mother_book, r.pos
    from public.ad_reference_rows(p -> 'references') r;

    perform public.ad_log(case when p_new then 'create' else 'update' end,
                          'article', v_id, v_name);
    return v_id;
end $$;

-- Archive / restore now knows about articles too (same signature as 004).
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
                           when 'medicine' then 'medicines'
                           when 'article' then 'health_articles' end;
    if v_table is null then raise exception 'Unknown content type.'; end if;
    execute format('update public.%I set is_published = $1, updated_at = now() '
                   'where id = $2 returning name', v_table)
        into v_name using p_published, p_id;
    if v_name is null then raise exception 'That entry no longer exists.'; end if;
    -- Articles are read live, not from the synced encyclopedia copy.
    if p_kind <> 'article' then
        perform public.ad_bump();
    end if;
    perform public.ad_log(case when p_published then 'restore' else 'archive' end,
                          p_kind, p_id, v_name);
end $$;


-- ---------------------------------------------------------------------
-- 4. Who may call what
-- ---------------------------------------------------------------------
do $$
declare fn text;
begin
    foreach fn in array array[
        'public.admin_list_articles()', 'public.admin_get_article(text)',
        'public.admin_save_article(jsonb, boolean)',
        'public.admin_set_published(text, text, boolean)'] loop
        execute format('revoke execute on function %s from public, anon', fn);
        execute format('grant execute on function %s to authenticated', fn);
    end loop;
end $$;

commit;

-- =====================================================================
-- Checks:
--   select count(*) from public.health_articles;              -- 0 at first
--   select public.admin_list_articles();   -- as owner: "Only admins..." is expected
-- =====================================================================
