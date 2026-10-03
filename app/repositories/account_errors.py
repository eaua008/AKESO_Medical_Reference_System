"""One error type for the whole Account module, with readable messages.

Upper layers catch AccountError and show its text. Supabase, PostgREST,
Storage and Edge Function exceptions never leave the repositories.
"""


class AccountError(Exception):
    """Something the user should be told about, already in plain words."""


# Messages raised by our own SQL functions are already written for people;
# pass them through. Everything else is mapped or summarised.
_OWN_MESSAGES = (
    "Type DELETE to confirm.",
    "Too many wrong attempts. Try again in 15 minutes.",
    "You are the only admin. Make someone else an admin first.",
    "Akeso needs at least one admin.",
    "Two-factor check required.",
    "Two-factor status does not match.",
    "Not signed in.",
    "Invalid device key.",
)


def friendly(exc: BaseException) -> str:
    message = getattr(exc, "message", None) or str(exc)
    # P0001 = "raise exception" in one of Akeso's own SQL functions: those
    # messages are written for people already.
    if getattr(exc, "code", None) == "P0001" and message:
        return message
    for own in _OWN_MESSAGES:
        if own in message:
            return own
    text = message.lower()
    if "session" in text and ("missing" in text or "ended" in text or "expired" in text):
        return "Your session has ended. Please sign in again."
    if "jwt expired" in text:
        return "Your session has ended. Please sign in again."
    if "duplicate key" in text and "handle" in text:
        return "That handle is already taken."
    if "profiles_handle_check" in text:
        return "Handles use 3–20 lowercase letters, numbers or underscores."
    if "permission denied" in text or "row-level security" in text:
        return "Akeso's database refused that change. Is migration 002 installed?"
    if "could not find the function" in text or "schema cache" in text:
        return "The account tables are missing. Run database/migrations/002_accounts.sql."
    if "same password" in text or "should be different" in text:
        return "The new password must be different from the current one."
    if "password" in text and ("weak" in text or "at least" in text):
        return "Supabase rejected that password as too weak."
    if "email" in text and ("already" in text or "exists" in text or "registered" in text):
        return "That email address is already used by another account."
    if "rate limit" in text or "too many" in text or "over_request_rate" in text:
        return "Too many attempts. Wait a minute and try again."
    if "invalid totp" in text or "invalid code" in text or "code" in text and "invalid" in text:
        return "That code is not right. Check the time on your phone and try again."
    if "mfa" in text and ("disabled" in text or "not enabled" in text):
        return "Two-factor sign-in is switched off in the Supabase dashboard (Auth > MFA)."
    if "reauthentication" in text or "nonce" in text:
        return ("Supabase asks for a recent sign-in before changing the password. "
                "Sign out, sign back in, then try again.")
    if "connect" in text or "timed out" in text or "network" in text or "name resolution" in text:
        return "Could not reach Akeso's server. Check your internet connection."
    return message if len(message) < 160 else "Something went wrong. Please try again."
