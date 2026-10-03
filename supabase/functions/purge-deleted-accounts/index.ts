// =====================================================================
// Edge Function: purge-deleted-accounts
// ---------------------------------------------------------------------
// Runs once a day from Supabase Cron. Deletes every account whose
// 30-day deletion window has ended.
//
// Why a function and not SQL: removing a sign-in account needs the
// service-role key (auth.admin.deleteUser). The app only ever has the
// publishable key, so it can ask for deletion (request_account_deletion)
// but can never carry it out. Deleting the auth user cascades to every
// Akeso table (profiles, roles, devices, log, consents, activity), and
// the profile photo is removed from storage here first.
//
// Deploy with "Verify JWT" OFF: Supabase Cron calls it with a shared
// secret instead of a user's sign-in token.
//
// Secrets (Dashboard > Edge Functions > Secrets):
//   PURGE_CRON_SECRET   a long random string; the cron job sends the same
//                       value in the x-cron-secret header
// SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY are provided automatically.
// =====================================================================

import { createClient } from "npm:@supabase/supabase-js@2";

const BATCH = 50;

const admin = createClient(
  Deno.env.get("SUPABASE_URL")!,
  Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!,
  { auth: { persistSession: false } },
);

function reply(status: number, body: Record<string, unknown>): Response {
  return new Response(JSON.stringify(body), {
    status,
    headers: { "Content-Type": "application/json" },
  });
}

function sameText(a: string, b: string): boolean {
  if (a.length !== b.length) return false;
  let diff = 0;
  for (let i = 0; i < a.length; i++) diff |= a.charCodeAt(i) ^ b.charCodeAt(i);
  return diff === 0;
}

Deno.serve(async (req) => {
  const expected = Deno.env.get("PURGE_CRON_SECRET") ?? "";
  const given = req.headers.get("x-cron-secret") ?? "";
  // No secret configured means the function refuses to run at all.
  if (expected.length < 24 || !sameText(given, expected)) {
    return reply(401, { error: "Not allowed." });
  }

  const { data: due, error } = await admin
    .from("profiles")
    .select("id")
    .lte("deletion_scheduled_for", new Date().toISOString())
    .not("deletion_scheduled_for", "is", null)
    .limit(BATCH);
  if (error) return reply(500, { error: "Could not read the deletion list." });

  let deleted = 0;
  const failed: string[] = [];
  for (const row of due ?? []) {
    const id = row.id as string;
    try {
      // Photos first: storage objects are not removed by the cascade.
      const { data: files } = await admin.storage.from("avatars").list(id);
      if (files && files.length > 0) {
        await admin.storage.from("avatars").remove(files.map((f) => `${id}/${f.name}`));
      }
      const { error: delError } = await admin.auth.admin.deleteUser(id);
      if (delError) throw delError;
      deleted += 1;
    } catch (_e) {
      failed.push(id);   // tried again tomorrow
    }
  }
  return reply(200, { checked: (due ?? []).length, deleted, failed: failed.length });
});
