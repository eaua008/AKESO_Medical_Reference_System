"""Remember me: keeps the sign-in between launches, safely.

When "Remember me" is ticked (password, Google or a new account), the
session's refresh token is saved to %LOCALAPPDATA%\\Akeso\\akeso_session.bin
so the next launch signs straight in instead of showing the sign-in screen.

  * Encrypted with Windows DPAPI (CryptProtectData): only the same Windows
    user on the same computer can decrypt it. Copying the file to another
    PC or account gives nothing usable. (On macOS / Linux, used only while
    developing, it is a file only your user can read.)
  * Never the password: Supabase refresh tokens can be revoked (Sign out,
    "Sign out all other devices", or an admin suspending the account) and
    they rotate: every refresh replaces the saved one.
  * Unticked "Remember me", or Sign out, deletes the file.
"""

import os
import sys
from pathlib import Path
from typing import Optional

from app.repositories.local_disease_cache import default_cache_path

MARKER = b"AKESO1"


def vault_path() -> Path:
    return default_cache_path().with_name("akeso_session.bin")


# ------------------------------------------------------------ Windows DPAPI

if sys.platform == "win32":
    import ctypes
    from ctypes import wintypes

    class _Blob(ctypes.Structure):
        _fields_ = [("cbData", wintypes.DWORD), ("pbData", ctypes.POINTER(ctypes.c_char))]

    _UI_FORBIDDEN = 0x1

    def _blob(data: bytes) -> tuple:
        buffer = ctypes.create_string_buffer(data, len(data))
        return _Blob(len(data), ctypes.cast(buffer, ctypes.POINTER(ctypes.c_char))), buffer

    def _take(blob: _Blob) -> bytes:
        try:
            return ctypes.string_at(blob.pbData, blob.cbData)
        finally:
            ctypes.windll.kernel32.LocalFree(blob.pbData)

    def _protect(data: bytes) -> bytes:
        source, _keep = _blob(data)
        out = _Blob()
        if not ctypes.windll.crypt32.CryptProtectData(
                ctypes.byref(source), ctypes.c_wchar_p("Akeso session"), None, None, None,
                _UI_FORBIDDEN, ctypes.byref(out)):
            raise OSError("Could not encrypt the saved session.")
        return _take(out)

    def _unprotect(data: bytes) -> bytes:
        source, _keep = _blob(data)
        out = _Blob()
        if not ctypes.windll.crypt32.CryptUnprotectData(
                ctypes.byref(source), None, None, None, None, _UI_FORBIDDEN, ctypes.byref(out)):
            raise OSError("Could not decrypt the saved session.")
        return _take(out)
else:
    def _protect(data: bytes) -> bytes:
        return data

    def _unprotect(data: bytes) -> bytes:
        return data


# ------------------------------------------------------------------ public

def save(refresh_token: str) -> None:
    if not refresh_token:
        return
    path = vault_path()
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        temp = path.with_suffix(".tmp")
        temp.write_bytes(MARKER + _protect(refresh_token.encode("utf-8")))
        if sys.platform != "win32":
            os.chmod(temp, 0o600)
        os.replace(temp, path)
    except OSError:
        pass                       # not remembered this time; nothing breaks


def load() -> Optional[str]:
    path = vault_path()
    try:
        raw = path.read_bytes()
        if not raw.startswith(MARKER):
            return None
        return _unprotect(raw[len(MARKER):]).decode("utf-8") or None
    except (OSError, UnicodeDecodeError):
        return None


def clear() -> None:
    try:
        vault_path().unlink()
    except FileNotFoundError:
        pass
    except OSError:
        pass
