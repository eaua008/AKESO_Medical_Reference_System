-- LOCAL TEST DATABASE ONLY. Never run this on the real Supabase project: it creates
-- test users and a 't' schema. See claude/friends-sharing-groups-design.md, Testing.

-- Minimal stand-ins for the Supabase objects Akeso's migrations use, so the
-- real migration files run unchanged on a plain local Postgres.
-- auth.uid() / auth.jwt() read the same request.jwt.claims setting that
-- PostgREST sets, so "set role authenticated + set claims" behaves like a
-- signed-in API call.

do $$ begin
    if not exists (select 1 from pg_roles where rolname = 'anon') then create role anon nologin; end if;
    if not exists (select 1 from pg_roles where rolname = 'authenticated') then create role authenticated nologin; end if;
    if not exists (select 1 from pg_roles where rolname = 'service_role') then create role service_role nologin bypassrls; end if;
end $$;
grant usage on schema public to anon, authenticated, service_role;

create extension if not exists pgcrypto;
create schema if not exists extensions;
create or replace function extensions.crypt(text, text) returns text language sql as $$ select public.crypt($1, $2) $$;
create or replace function extensions.gen_salt(text) returns text language sql as $$ select public.gen_salt($1) $$;

create schema if not exists auth;
grant usage on schema auth to anon, authenticated, service_role;
create table if not exists auth.users (
    id uuid primary key default gen_random_uuid(),
    email text,
    encrypted_password text,
    raw_user_meta_data jsonb default '{}'::jsonb,
    email_change text default '',
    created_at timestamptz default now(),
    last_sign_in_at timestamptz,
    email_confirmed_at timestamptz,
    banned_until timestamptz
);
create table if not exists auth.sessions (
    id uuid primary key default gen_random_uuid(),
    user_id uuid references auth.users (id) on delete cascade,
    created_at timestamptz default now(),
    updated_at timestamptz default now(),
    user_agent text, ip inet, aal text, not_after timestamptz, refreshed_at timestamp
);
create table if not exists auth.mfa_factors (
    id uuid primary key default gen_random_uuid(),
    user_id uuid references auth.users (id) on delete cascade,
    status text
);
create table if not exists auth.identities (
    id uuid primary key default gen_random_uuid(),
    user_id uuid references auth.users (id) on delete cascade,
    provider text
);
create or replace function auth.jwt() returns jsonb language sql stable as $$
    select coalesce(nullif(current_setting('request.jwt.claims', true), ''), '{}')::jsonb $$;
create or replace function auth.uid() returns uuid language sql stable as $$
    select nullif(auth.jwt() ->> 'sub', '')::uuid $$;
create or replace function auth.role() returns text language sql stable as $$
    select auth.jwt() ->> 'role' $$;

create schema if not exists storage;
grant usage on schema storage to anon, authenticated, service_role;
create table if not exists storage.buckets (
    id text primary key, name text, public boolean default false,
    file_size_limit bigint, allowed_mime_types text[]);
create table if not exists storage.objects (
    id uuid primary key default gen_random_uuid(), bucket_id text, name text,
    owner uuid, created_at timestamptz default now());
alter table storage.objects enable row level security;
create or replace function storage.foldername(name text) returns text[] language sql immutable as $$
    select string_to_array(name, '/') $$;

-- Supabase grants these to signed-in users (the storage rules then decide).
grant select, insert, update, delete on storage.objects to authenticated;
grant select on storage.buckets to authenticated;
