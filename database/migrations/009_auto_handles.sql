-- =====================================================================
-- 009_auto_handles.sql  -  @handles are given automatically
-- =====================================================================
-- Run AFTER 008_member_profiles.sql. Safe to run more than once.
--
-- Before: every user had to type and claim an @handle in Account
-- Settings before anyone could open their Clinical Exchange profile.
-- Now:
--   * every profile gets a handle made from its display name when it is
--     created ("Juan Dela Cruz" -> @juan_dela_cruz; if taken,
--     @juan_dela_cruz4821),
--   * existing profiles without one get one now,
--   * users can no longer change it, so links to a profile never break.
-- =====================================================================

-- ---------------------------------------------------------------------
-- 1. Make a free handle from a name
-- ---------------------------------------------------------------------
create or replace function public.make_handle(p_name text, p_self uuid default null)
returns text
language plpgsql volatile security definer set search_path = ''
as $$
declare
    base      text;
    candidate text;
    tries     int := 0;
begin
    -- lowercase, strip common accents (Mapúa -> mapua, Niño -> nino),
    -- anything else that isn't a-z / 0-9 becomes one underscore
    base := lower(coalesce(p_name, ''));
    base := translate(base, 'áàâäãåéèêëíìîïóòôöõúùûüñçý',
                            'aaaaaaeeeeiiiiooooouuuuncy');
    base := regexp_replace(base, '[^a-z0-9]+', '_', 'g');
    base := btrim(left(btrim(base, '_'), 16), '_');
    if length(base) < 3 then
        base := 'member';
    end if;

    candidate := base;
    loop
        exit when not exists (
            select 1 from public.profiles p
            where lower(p.handle) = candidate
              and (p_self is null or p.id <> p_self));
        tries := tries + 1;
        if tries > 50 then                      -- practically never
            candidate := 'member' || substr(md5(random()::text), 1, 10);
            exit;
        end if;
        candidate := base || (1000 + floor(random() * 9000))::int::text;   -- <= 20 chars
    end loop;
    return candidate;
end $$;

revoke execute on function public.make_handle(text, uuid) from public, anon, authenticated;


-- ---------------------------------------------------------------------
-- 2. New profiles (and any that lose theirs) get one automatically
-- ---------------------------------------------------------------------
create or replace function public.profiles_auto_handle()
returns trigger
language plpgsql security definer set search_path = ''
as $$
begin
    if new.handle is null or btrim(new.handle) = '' then
        new.handle := public.make_handle(new.display_name, new.id);
    end if;
    return new;
end $$;

revoke execute on function public.profiles_auto_handle() from public, anon, authenticated;

drop trigger if exists profiles_auto_handle on public.profiles;
create trigger profiles_auto_handle before insert or update of handle on public.profiles
    for each row execute function public.profiles_auto_handle();


-- ---------------------------------------------------------------------
-- 3. Existing profiles without a handle
-- ---------------------------------------------------------------------
do $$
declare
    r record;
begin
    for r in select id, display_name from public.profiles
             where handle is null or btrim(handle) = ''
             order by created_at
    loop
        update public.profiles
           set handle = public.make_handle(r.display_name, r.id)
         where id = r.id;
    end loop;
end $$;


-- ---------------------------------------------------------------------
-- 4. Users can't change their handle any more
-- ---------------------------------------------------------------------
revoke update (handle) on public.profiles from authenticated;
