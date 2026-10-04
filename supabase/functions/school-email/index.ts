// =====================================================================
// Edge Function: school-email
// ---------------------------------------------------------------------
// Gives an account the "Verified student" badge by proving it can read
// mail at a school address. Supabase Auth only verifies the sign-in
// email, so this second address is checked here.
//
//   POST { "action": "send",   "email": "juan@school.edu.ph" }
//   POST { "action": "verify", "code":  "123456" }
//
// Privacy: the address is used once to send the code and is never
// stored. Only its domain ("school.edu.ph") is kept, on the profile,
// once the code is correct. The code itself is stored only as a hash.
//
// Secrets (Dashboard > Edge Functions > Secrets):
//   SMTP_HOSTNAME   smtp.gmail.com
//   SMTP_PORT       465            (587 and 25 are blocked on Supabase)
//   SMTP_USERNAME   the Gmail address that sends the codes
//   SMTP_PASSWORD   a Google "app password" for that address, not the real one
//   SMTP_FROM       Akeso <that same address>
//   SCHOOL_EMAIL_SUFFIXES  optional, default ".edu.ph,.edu"
// SUPABASE_URL and the project's keys are provided by Supabase
// automatically (legacy or new-style, both work: see envKey).
//
// Deploy with "Verify JWT" OFF (Dashboard > Edge Functions > school-email
// > Details, or: supabase functions deploy school-email --no-verify-jwt).
// The built-in check only understands the legacy key format and answers
// 401 before this code runs on projects using the new keys; this function
// checks the signed-in user itself (auth.getUser below).
// =====================================================================

import { createClient } from "npm:@supabase/supabase-js@2";
import nodemailer from "npm:nodemailer@6";

const CODE_TTL_MINUTES = 15;
const MAX_ATTEMPTS = 5;
const RESEND_AFTER_SECONDS = 60;
const MAX_SENDS_PER_DAY = 5;
const EMAIL_PATTERN = /^[^@\s]+@([a-z0-9-]+\.)+[a-z]{2,}$/i;

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

const url = Deno.env.get("SUPABASE_URL")!;
const anonKey = envKey("SUPABASE_ANON_KEY", "SUPABASE_PUBLISHABLE_KEYS");
const serviceKey = envKey("SUPABASE_SERVICE_ROLE_KEY", "SUPABASE_SECRET_KEYS");
const suffixes = (Deno.env.get("SCHOOL_EMAIL_SUFFIXES") ?? ".edu.ph,.edu")
  .split(",").map((s) => s.trim().toLowerCase()).filter(Boolean);

const admin = createClient(url, serviceKey, { auth: { persistSession: false } });

function reply(status: number, body: Record<string, unknown>): Response {
  return new Response(JSON.stringify(body), {
    status,
    headers: { "Content-Type": "application/json" },
  });
}

async function sha256(text: string): Promise<string> {
  const bytes = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(text));
  return Array.from(new Uint8Array(bytes)).map((b) => b.toString(16).padStart(2, "0")).join("");
}

function sixDigits(): string {
  // Rejection sampling, so every code from 000000 to 999999 is equally likely.
  const buf = new Uint32Array(1);
  let n: number;
  do {
    crypto.getRandomValues(buf);
    n = buf[0];
  } while (n >= 4_294_000_000);
  return String(n % 1_000_000).padStart(6, "0");
}

function sameText(a: string, b: string): boolean {
  if (a.length !== b.length) return false;
  let diff = 0;
  for (let i = 0; i < a.length; i++) diff |= a.charCodeAt(i) ^ b.charCodeAt(i);
  return diff === 0;
}

async function sendMail(to: string, code: string): Promise<void> {
  const transport = nodemailer.createTransport({
    host: Deno.env.get("SMTP_HOSTNAME")!,
    port: Number(Deno.env.get("SMTP_PORT") ?? "465"),
    secure: true,
    auth: {
      user: Deno.env.get("SMTP_USERNAME")!,
      pass: Deno.env.get("SMTP_PASSWORD")!,
    },
  });
  await transport.sendMail({
    from: Deno.env.get("SMTP_FROM") ?? Deno.env.get("SMTP_USERNAME")!,
    to,
    subject: "Your Akeso student verification code",
    text:
      `Your Akeso verification code is ${code}.\n\n` +
      `It expires in ${CODE_TTL_MINUTES} minutes. If you did not ask for this, ` +
      `you can ignore this email: nothing happens unless the code is entered in Akeso.`,
  });
}

Deno.serve(async (req) => {
  if (req.method !== "POST") return reply(405, { error: "Use POST." });

  // Who is asking: the signed-in user's own token, checked by Supabase.
  const authHeader = req.headers.get("Authorization") ?? "";
  const asUser = createClient(url, anonKey, {
    global: { headers: { Authorization: authHeader } },
    auth: { persistSession: false },
  });
  const { data: userData, error: userError } = await asUser.auth.getUser();
  if (userError || !userData?.user) return reply(401, { error: "Please sign in again." });
  const userId = userData.user.id;

  // Same two-factor rule as the database: if 2FA is on, the session must have passed it.
  const { data: mfaOk } = await asUser.rpc("mfa_satisfied");
  if (mfaOk !== true) return reply(403, { error: "Two-factor check required." });

  let body: { action?: string; email?: string; code?: string };
  try {
    body = await req.json();
  } catch {
    return reply(400, { error: "Invalid request." });
  }

  // ------------------------------------------------------------ send a code
  if (body.action === "send") {
    const email = (body.email ?? "").trim().toLowerCase();
    if (!EMAIL_PATTERN.test(email)) return reply(400, { error: "Enter a valid email address." });
    const domain = email.split("@")[1];
    if (!suffixes.some((s) => domain.endsWith(s))) {
      return reply(400, { error: `Use your school email (ending in ${suffixes.join(" or ")}).` });
    }

    const { data: existing } = await admin
      .from("school_verifications").select("*").eq("user_id", userId).maybeSingle();
    const now = Date.now();
    let sentCount = 1;
    if (existing) {
      const last = new Date(existing.last_sent_at).getTime();
      if (now - last < RESEND_AFTER_SECONDS * 1000) {
        return reply(429, { error: "Wait a minute before asking for another code." });
      }
      const sameDay = now - last < 24 * 3600 * 1000;
      sentCount = sameDay ? existing.sent_count + 1 : 1;
      if (sentCount > MAX_SENDS_PER_DAY) {
        return reply(429, { error: "Too many codes today. Try again tomorrow." });
      }
    }

    const code = sixDigits();
    const { error: saveError } = await admin.from("school_verifications").upsert({
      user_id: userId,
      email_domain: domain,
      code_hash: await sha256(`${userId}:${code}`),
      expires_at: new Date(now + CODE_TTL_MINUTES * 60 * 1000).toISOString(),
      attempts: 0,
      sent_count: sentCount,
      last_sent_at: new Date(now).toISOString(),
    });
    if (saveError) return reply(500, { error: "Could not start verification." });

    try {
      await sendMail(email, code);
    } catch (_e) {
      return reply(502, { error: "The code could not be emailed. Try again later." });
    }
    return reply(200, { sent: true, domain, expires_in_minutes: CODE_TTL_MINUTES });
  }

  // ----------------------------------------------------------- check a code
  if (body.action === "verify") {
    const code = (body.code ?? "").replace(/\s/g, "");
    if (!/^\d{6}$/.test(code)) return reply(400, { error: "Enter the 6-digit code." });

    const { data: pending } = await admin
      .from("school_verifications").select("*").eq("user_id", userId).maybeSingle();
    if (!pending) return reply(400, { error: "Ask for a code first." });
    if (new Date(pending.expires_at).getTime() < Date.now()) {
      return reply(400, { error: "That code has expired. Ask for a new one." });
    }
    if (pending.attempts >= MAX_ATTEMPTS) {
      return reply(429, { error: "Too many wrong codes. Ask for a new one." });
    }

    const ok = sameText(await sha256(`${userId}:${code}`), pending.code_hash);
    if (!ok) {
      await admin.from("school_verifications")
        .update({ attempts: pending.attempts + 1 }).eq("user_id", userId);
      return reply(400, { error: "That code is not right." });
    }

    const verifiedAt = new Date().toISOString();
    const { error: badgeError } = await admin.from("profiles").update({
      school_email_domain: pending.email_domain,
      school_email_verified_at: verifiedAt,
    }).eq("id", userId);
    if (badgeError) return reply(500, { error: "Could not save the badge." });

    await admin.from("school_verifications").delete().eq("user_id", userId);
    await admin.from("security_events").insert({
      user_id: userId,
      kind: "school_email_verified",
      detail: { domain: pending.email_domain },
    });
    return reply(200, { verified: true, domain: pending.email_domain, verified_at: verifiedAt });
  }

  return reply(400, { error: "Unknown action." });
});
