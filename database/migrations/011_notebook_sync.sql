-- =====================================================================
-- 011_notebook_sync.sql  -  the Study Notebook follows your account
-- =====================================================================
-- Run AFTER 010_hidden_posts_author_admin.sql. Safe to run more than once.
--
-- Before: notes, symptom cases, interaction cases and subjects lived only
-- in akeso_notebook.db on one computer. Now the app keeps that file (so
-- the notebook still works offline) and copies changes to these tables;
-- signing in on another computer brings the notebook along.
--
--   notebook_subjects   the subject folders
--   notebook_items      notes and case studies
--   storage bucket "notebook-images"   pictures pasted into notes,
--                                      at <user id>/<file name>
--
-- Private: row-level security lets each person read and write ONLY their
-- own rows and pictures. Not even admins or educators can read them
-- through the app. Deleting an account deletes its rows (cascade).
-- Deletions are kept as a date (deleted_at), so a note deleted on one
-- computer also disappears on the others.
-- =====================================================================

create table if not exists public.notebook_subjects (
    owner        uuid        not null default auth.uid()
                             references auth.users (id) on delete cascade,
    id           text        not null check (char_length(id) between 1 and 64),
    name         text        not null check (char_length(btrim(name)) between 1 and 120),
    created_at   timestamptz not null default now(),
    updated_at   timestamptz not null default now(),
    deleted_at   timestamptz,
    server_updated_at timestamptz not null default now(),
    primary key (owner, id)
);

create table if not exists public.notebook_items (
    owner        uuid        not null default auth.uid()
                             references auth.users (id) on delete cascade,
    id           text        not null check (char_length(id) between 1 and 64),
    kind         text        not null check (kind in ('note', 'symptom_case', 'interaction_case')),
    title        text        not null check (char_length(btrim(title)) between 1 and 300),
    subject_id   text        not null default '',
    tags         jsonb       not null default '[]',
    body         text        not null default '' check (char_length(body) <= 2000000),
    case_data    jsonb       not null default '{}',
    workspace    text        not null default '' check (char_length(workspace) <= 200000),
    pinned       boolean     not null default false,
    created_at   timestamptz not null default now(),
    updated_at   timestamptz not null default now(),
    deleted_at   timestamptz,
    server_updated_at timestamptz not null default now(),
    primary key (owner, id)
);

create index if not exists notebook_subjects_pull_idx
    on public.notebook_subjects (owner, server_updated_at);
create index if not exists notebook_items_pull_idx
    on public.notebook_items (owner, server_updated_at);

-- When the server last saw a change: what "give me what changed since
-- my last sync" compares against (the device clocks may disagree).
create or replace function public.notebook_touch()
returns trigger
language plpgsql
set search_path = ''
as $$
begin
    new.server_updated_at := now();
    new.owner := auth.uid();                 -- never someone else's row
    return new;
end $$;

drop trigger if exists notebook_subjects_touch on public.notebook_subjects;
create trigger notebook_subjects_touch before insert or update on public.notebook_subjects
    for each row execute function public.notebook_touch();
drop trigger if exists notebook_items_touch on public.notebook_items;
create trigger notebook_items_touch before insert or update on public.notebook_items
    for each row execute function public.notebook_touch();

-- ------------------------------------------------------------- privacy
alter table public.notebook_subjects enable row level security;
alter table public.notebook_items enable row level security;

drop policy if exists "notebook subjects: own" on public.notebook_subjects;
create policy "notebook subjects: own" on public.notebook_subjects
    for all to authenticated
    using (owner = (select auth.uid())) with check (owner = (select auth.uid()));

drop policy if exists "notebook items: own" on public.notebook_items;
create policy "notebook items: own" on public.notebook_items
    for all to authenticated
    using (owner = (select auth.uid())) with check (owner = (select auth.uid()));

revoke all on public.notebook_subjects, public.notebook_items from anon;
grant select, insert, update on public.notebook_subjects, public.notebook_items to authenticated;

-- -------------------------------------------------------------- pictures
insert into storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
values ('notebook-images', 'notebook-images', false, 10485760,
        array['image/png', 'image/jpeg', 'image/gif', 'image/bmp', 'image/webp'])
on conflict (id) do update set public = false, file_size_limit = excluded.file_size_limit,
                               allowed_mime_types = excluded.allowed_mime_types;

drop policy if exists "notebook images: own read" on storage.objects;
create policy "notebook images: own read" on storage.objects
    for select to authenticated
    using (bucket_id = 'notebook-images'
           and (storage.foldername(name))[1] = (select auth.uid())::text);

drop policy if exists "notebook images: own write" on storage.objects;
create policy "notebook images: own write" on storage.objects
    for insert to authenticated
    with check (bucket_id = 'notebook-images'
                and (storage.foldername(name))[1] = (select auth.uid())::text);

drop policy if exists "notebook images: own update" on storage.objects;
create policy "notebook images: own update" on storage.objects
    for update to authenticated
    using (bucket_id = 'notebook-images'
           and (storage.foldername(name))[1] = (select auth.uid())::text);

notify pgrst, 'reload schema';
