"""Google sign-in for a desktop app: the loopback redirect.

A web app receives the OAuth callback at its own URL. A desktop app has no
URL, so it opens a tiny HTTP listener on this machine, sends the user to the
browser, and waits for the browser to be redirected back to that listener.

The full round trip:

    1. The repository asks Supabase for a Google authorize URL.
    2. This listener starts on 127.0.0.1:8123.
    3. The system browser opens that URL; the user signs in with Google.
    4. Google -> Supabase -> redirect to http://localhost:8123/callback?code=...
    5. This listener reads the code and hands it back to the app.
    6. The repository exchanges the code for a session.

Why PKCE and not the implicit flow: the implicit flow returns tokens in the
URL fragment (#access_token=...). Browsers never send the fragment to the
server, so this listener would never see it. PKCE returns ?code= in the query
string, which it can read.

Why an intercepted code is useless: exchanging it needs the PKCE code
verifier, which never leaves this process. A code copied out of the browser
history cannot be redeemed anywhere else.
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Optional
from urllib.parse import parse_qs, urlparse

from PySide6.QtCore import QThread, Signal

# Must match the Redirect URL added in Supabase -> Authentication ->
# URL Configuration, or Supabase will refuse to redirect here.
#
# 127.0.0.1 on BOTH sides, deliberately not "localhost". On Windows,
# localhost often resolves to the IPv6 address ::1 first, while this
# listener binds IPv4 only — the browser would knock on a door nobody is
# listening at. Using the literal address removes the ambiguity.
CALLBACK_HOST = "127.0.0.1"
CALLBACK_PORT = 8123
CALLBACK_PATH = "/callback"
REDIRECT_URL = f"http://{CALLBACK_HOST}:{CALLBACK_PORT}{CALLBACK_PATH}"

# How long to wait for the user to finish in the browser before giving up.
#
# This is only a backstop. The app cannot detect the browser tab being
# closed — it is simply listening for a redirect that may never come — so
# the user can cancel at any time from the button. This covers someone who
# walks away without cancelling.
#
# Not shorter: choosing an account, typing a password and approving a 2FA
# prompt on a phone routinely takes well over 30 seconds.
TIMEOUT_SECONDS = 120


_SUCCESS_PAGE = b"""<!doctype html>
<html><head><meta charset="utf-8"><title>Akeso</title>
<style>
 body{background:#0D0D13;color:#F3F4F6;font-family:system-ui,sans-serif;
      display:flex;align-items:center;justify-content:center;height:100vh;margin:0}
 .card{background:#14141C;border:1px solid #2A2A38;border-radius:14px;
       padding:36px 44px;text-align:center}
 h1{font-size:20px;margin:0 0 8px} p{color:#9CA3AF;margin:0}
</style></head><body><div class="card">
<h1>Signed in to Akeso</h1>
<p>You can close this tab and return to the app.</p>
</div></body></html>"""

_FAILURE_PAGE = b"""<!doctype html>
<html><head><meta charset="utf-8"><title>Akeso</title>
<style>
 body{background:#0D0D13;color:#F3F4F6;font-family:system-ui,sans-serif;
      display:flex;align-items:center;justify-content:center;height:100vh;margin:0}
 .card{background:#14141C;border:1px solid #FB7185;border-radius:14px;
       padding:36px 44px;text-align:center}
 h1{font-size:20px;margin:0 0 8px} p{color:#9CA3AF;margin:0}
</style></head><body><div class="card">
<h1>Sign-in was not completed</h1>
<p>Close this tab and try again from the app.</p>
</div></body></html>"""


class _CallbackHandler(BaseHTTPRequestHandler):
    """Handles exactly the one redirect request, then stores the result."""

    # Set by the server before handling; read back by the listener thread.
    result_code: Optional[str] = None
    result_error: Optional[str] = None

    def do_GET(self) -> None:  # noqa: N802 — name fixed by BaseHTTPRequestHandler
        parsed = urlparse(self.path)

        if parsed.path != CALLBACK_PATH:
            # Browsers also ask for /favicon.ico. Answer it without treating
            # it as the callback, or it would end the wait prematurely.
            self.send_response(404)
            self.end_headers()
            return

        params = parse_qs(parsed.query)
        code = params.get("code", [None])[0]
        error = params.get("error_description", params.get("error", [None]))[0]

        if code:
            type(self).result_code = code
            self._respond(200, _SUCCESS_PAGE)
        else:
            type(self).result_error = error or "No authorisation code returned."
            self._respond(400, _FAILURE_PAGE)

    def _respond(self, status: int, body: bytes) -> None:
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        # The page holds nothing sensitive, but there is no reason for a
        # browser to keep it.
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args) -> None:  # noqa: A002
        # Silence the default per-request stderr logging. It would print the
        # full callback URL — including the authorisation code — to the
        # console.
        return


class OAuthCallbackListener(QThread):
    """Waits for the browser redirect on a background thread.

    Runs off the UI thread because the wait lasts as long as the user takes
    in the browser. On the UI thread, the whole window would freeze for that
    time.
    """

    code_received = Signal(str)
    failed = Signal(str)
    # Seconds left before the backstop timeout. Emitted once per poll so the
    # button can show a live countdown next to Cancel.
    tick = Signal(int)
    server_error = Signal(str)     # the redirect carried an error instead of a code

    def run(self) -> None:
        _CallbackHandler.result_code = None
        _CallbackHandler.result_error = None

        try:
            # 127.0.0.1, never 0.0.0.0. Binding to all interfaces would let
            # any machine on the same network hit this listener.
            server = HTTPServer((CALLBACK_HOST, CALLBACK_PORT), _CallbackHandler)
        except OSError:
            self.failed.emit(
                f"Port {CALLBACK_PORT} is already in use. Close any other copy "
                "of Akeso and try again."
            )
            return

        server.timeout = 1.0  # poll interval, so the loop can notice timeouts
        waited = 0.0

        try:
            while (
                    _CallbackHandler.result_code is None
                    and _CallbackHandler.result_error is None
                    and waited < TIMEOUT_SECONDS
                    and not self.isInterruptionRequested()
            ):
                # Emitted from this worker thread; Qt queues it across to the
                # UI thread automatically, so the button updates safely.
                self.tick.emit(max(0, int(TIMEOUT_SECONDS - waited)))
                server.handle_request()
                waited += server.timeout
        finally:
            server.server_close()

        if _CallbackHandler.result_code:
            self.code_received.emit(_CallbackHandler.result_code)
        elif _CallbackHandler.result_error:
            # From Supabase (e.g. "User is banned"): raw server text, so the
            # controller decides what to show rather than showing it as-is.
            self.server_error.emit(_CallbackHandler.result_error)
        elif self.isInterruptionRequested():
            self.failed.emit("Google sign-in was cancelled.")
        else:
            self.failed.emit(
                "Google sign-in timed out. Try again when you're ready."
            )