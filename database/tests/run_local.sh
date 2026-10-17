#!/bin/bash
# LOCAL TEST DATABASE ONLY. Rebuilds a throwaway Postgres database with the
# Supabase stand-ins, migrations 002-017 and 040-047 (each new one twice),
# then runs the SQL test suites. Needs PostgreSQL 16+ (psql) and a server
# you can reach as postgres on localhost (set PGPORT, default 55432).
set -e
export PGCLIENTENCODING=UTF8          # migrations contain “curly quotes” and ·
PSQL=${PSQL:-psql}
PORT=${PGPORT:-55432}
DB="-p $PORT -U postgres -h localhost"
HERE=$(cd "$(dirname "$0")" && pwd)
MIG="$HERE/../migrations"
"$PSQL" $DB -d postgres -q -c "drop database if exists akeso_test" -c "create database akeso_test"
"$PSQL" $DB -d akeso_test -q -v ON_ERROR_STOP=1 -f "$HERE/supabase_stub.sql" -f "$HERE/reference_stub.sql"
for n in 002 003 004 005 006 007 008 009 010 011 012 013 014 015 016 017; do
    "$PSQL" $DB -d akeso_test -q -v ON_ERROR_STOP=1 -f "$(ls "$MIG"/${n}_*.sql | head -1)" > /dev/null
done
for m in 040_friends 041_notebook_sharing 042_study_groups 043_change_handle 044_group_read_marker 045_group_images 046_group_mention_handles 047_admin_version_announcement_delete; do
    "$PSQL" $DB -d akeso_test -q -v ON_ERROR_STOP=1 -f "$MIG/$m.sql" > /dev/null
    "$PSQL" $DB -d akeso_test -q -v ON_ERROR_STOP=1 -f "$MIG/$m.sql" > /dev/null   # safe to re-run
done
"$PSQL" $DB -d akeso_test -q -v ON_ERROR_STOP=1 -f "$HERE/t_harness.sql"
for t in friends sharing groups handles readmarker images mentions admin47; do "$PSQL" $DB -d akeso_test -q -f "$HERE/t_$t.sql" > /dev/null; done
"$PSQL" $DB -d akeso_test -tA -c "select suite, count(*) filter (where ok) || '/' || count(*) from t.results group by suite"
"$PSQL" $DB -d akeso_test -tA -c "select suite, label, detail from t.results where not ok"
