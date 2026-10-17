-- LOCAL TEST DATABASE ONLY. Never run this on the real Supabase project: it creates
-- test users and a 't' schema. See claude/friends-sharing-groups-design.md, Testing.

create table if not exists public.body_systems (id text primary key, name text);
create table if not exists public.diseases (id text primary key, name text, scientific_name text, body_system_id text, is_published boolean default true, updated_at timestamptz default now());
create table if not exists public.symptoms (id text primary key, name text, body_system_id text, is_published boolean default true, updated_at timestamptz default now());
create table if not exists public.medicines (id text primary key, name text, generic_name text, is_published boolean default true, updated_at timestamptz default now());
create table if not exists public.content_version (id int primary key, version bigint default 1, updated_at timestamptz default now());
insert into public.content_version values (1, 1, now()) on conflict do nothing;
