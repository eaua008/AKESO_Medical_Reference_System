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
// Akeso table (profiles, roles, devices, log, consents, activity, the
// synced Study Notebook), and the profile photo and notebook pictures are
// removed from storage here first.
//
// Friends, shared notes and study groups (migrations 040-042): before the
// account goes, social_purge_user() removes the person's friendships,
// notes they shared and notes shared with them, their group memberships,
// messages, shelf notes, invites and reports, and hands each group they
// own to its longest-standing moderator (or deletes it when there is
// none). The cascade would remove the rows anyway; calling it first makes
// the hand-over happen in a known order. Projects without those
// migrations skip this step. Redeploy this function after running them.
//
// Pictures in study group chats (migration 045) live in the private bucket
// group-attachments. After the accounts are handled, sweepGroupPictures()
// removes every picture file that no chat message points at any more:
// pictures of deleted groups and deleted accounts, of messages that were
// never sent (an upload that failed half way), and of anything else left
// over. Files younger than a day are left alone, so a picture being sent
// right now is never removed.
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

// Projects on the new API keys get SUPABASE_PUBLISHABLE_KEYS /
// SUPABASE_SECRET_KEYS (JSON, one entry per named key) instead of the
// legacy SUPABASE_ANON_KEY / SUPABASE_SERVICE_ROLE_KEY. Accept either.
function envKey(single: string, named: string): string {
  const direct = Deno.env.get(single);
  if (direct) return direct;
  const raw = Deno.env.get(named);
  if (raw) {
    try {
      const values = Object.values(JSON.parse(raw) as Record<string, string>);
      if (values.length > 0) return String(values[0]);
    } catch (_e) { /* not JSON: ignore */ }
  }
  return "";
}

const admin = createClient(
  Deno.env.get("SUPABASE_URL")!,
  envKey("SUPABASE_SERVICE_ROLE_KEY", "SUPABASE_SECRET_KEYS"),
  { auth: { persistSession: false } },
);

function reply(status: number, body: Record<string, unknown>): Response {
  return new Response(JSON.stringify(body), {
    status,
    headers: { "Content-Type": "application/json" },
  });
}

// The migration that defines a function hasn't been run on this project.
function isMissingFunction(error: { code?: string; message?: string }): boolean {
  const text = (error.message ?? "").toLowerCase();
  return error.code === "PGRST202" || error.code === "42883" ||
    text.includes("could not find the function") || text.includes("does not exist");
}

const IMAGE_BUCKET = "group-attachments";
const IMAGE_GRACE_MS = 24 * 60 * 60 * 1000;

// Remove picture files nothing refers to. Safe to run when migration 045 is
// not installed: the bucket or the column is missing, and it just returns.
async function sweepGroupPictures(): Promise<number> {
  const storage = admin.storage.from(IMAGE_BUCKET);
  const { data: groups, error } = await storage.list("", { limit: 1000 });
  if (error || !groups) return 0;
  let removed = 0;
  for (const group of groups) {
    const groupId = group.name;
    const { data: senders } = await storage.list(groupId, { limit: 1000 });
    const files: { path: string; created: number }[] = [];
    for (const sender of senders ?? []) {
      const { data: items } = await storage.list(`${groupId}/${sender.name}`, { limit: 1000 });
      for (const item of items ?? []) {
        files.push({
          path: `${groupId}/${sender.name}/${item.name}`,
          created: new Date(item.created_at ?? Date.now()).getTime(),
        });
      }
    }
    if (files.length === 0) continue;
    const { data: used, error: usedError } = await admin
      .from("study_group_messages")
      .select("attachment_path")
      .eq("group_id", groupId)
      .not("attachment_path", "is", null);
    if (usedError && !isMissingFunction(usedError)) {
      // A group id that isn't a uuid or a missing column: leave this folder alone.
      continue;
    }
    const inUse = new Set((used ?? []).map((row) => row.attachment_path as string));
    const stale = files
      .filter((f) => !inUse.has(f.path) && Date.now() - f.created > IMAGE_GRACE_MS)
      .map((f) => f.path);
    if (stale.length > 0) {
      await storage.remove(stale);
      removed += stale.length;
    }
  }
  return removed;
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
      for (const bucket of ["avatars", "notebook-images"]) {
        for (;;) {
          const { data: files } = await admin.storage.from(bucket).list(id, { limit: 1000 });
          if (!files || files.length === 0) break;
          await admin.storage.from(bucket).remove(files.map((f) => `${id}/${f.name}`));
          if (files.length < 1000) break;
        }
      }
      // Friends, shares and study groups first (migrations 040-042).
      const { error: socialError } = await admin.rpc("social_purge_user", { p_user: id });
      if (socialError && !isMissingFunction(socialError)) throw socialError;
      const { error: delError } = await admin.auth.admin.deleteUser(id);
      if (delError) throw delError;
      deleted += 1;
    } catch (_e) {
      failed.push(id);   // tried again tomorrow
    }
  }
  let pictures = 0;
  try {
    pictures = await sweepGroupPictures();
  } catch (_e) { /* pictures not set up, or storage busy: try again tomorrow */ }
  return reply(200, { checked: (due ?? []).length, deleted, failed: failed.length, pictures });
});
