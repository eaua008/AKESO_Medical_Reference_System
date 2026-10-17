-- LOCAL TEST DATABASE ONLY. Never run this on the real Supabase project: it creates
-- test users and a 't' schema. See claude/friends-sharing-groups-design.md, Testing.

-- Test helpers (test database only).
create schema if not exists t;
create table if not exists t.results (id serial, suite text, label text, ok boolean, detail text);

create or replace function t.as_user(p uuid) returns void language sql as $$
    select set_config('request.jwt.claims',
        json_build_object('sub', p, 'role', 'authenticated', 'aal', 'aal1')::text, false);
$$;

create or replace function t.ok(p_suite text, p_cond boolean, p_label text, p_detail text default '')
returns void language plpgsql as $$
begin
    insert into t.results (suite, label, ok, detail) values (p_suite, p_label, coalesce(p_cond, false), p_detail);
end $$;

-- Run a statement and expect an error containing p_expect (or any error if null).
create or replace function t.err(p_suite text, p_sql text, p_expect text, p_label text)
returns void language plpgsql as $$
begin
    begin
        execute p_sql;
    exception when others then
        perform t.ok(p_suite, p_expect is null or position(lower(p_expect) in lower(sqlerrm)) > 0,
                     p_label, sqlerrm);
        return;
    end;
    perform t.ok(p_suite, false, p_label, 'no error');
end $$;

-- Make a user with a handle (the 002 trigger makes the profile and role).
create or replace function t.mk_user(p_handle text, p_role text default 'student') returns uuid
language plpgsql as $$
declare uid uuid := gen_random_uuid();
begin
    insert into auth.users (id, email, raw_user_meta_data)
    values (uid, p_handle || '@test.local', jsonb_build_object('display_name', initcap(p_handle)));
    update public.profiles set handle = p_handle, visibility = 'public' where id = uid;
    if p_role <> 'student' then
        alter table public.user_roles disable trigger user;
        update public.user_roles set role = p_role::public.app_role where user_id = uid;
        alter table public.user_roles enable trigger user;
    end if;
    return uid;
end $$;
grant usage on schema t to anon, authenticated;
grant all on all tables in schema t to anon, authenticated;
grant all on all sequences in schema t to anon, authenticated;
grant execute on all functions in schema t to anon, authenticated;
