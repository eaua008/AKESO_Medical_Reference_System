"""Which computer this is, for the Devices list in Account > Security.

The device key is a random id created the first time Akeso runs on this
computer and kept in a small file next to the local caches. It identifies
an installation, not a person, and contains nothing about the hardware.

The same file remembers which email each account last used here, so a
changed email can take the account's local data along (see
LocalAccountData.adopt).
"""

import json
import platform
import secrets
from pathlib import Path
from typing import Optional

from app.repositories.local_disease_cache import default_cache_path

APP_VERSION = "1.0.0"


def identity_path() -> Path:
    return default_cache_path().with_name("akeso_device.json")


def _read(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def _write(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(".tmp")
    temp.write_text(json.dumps(data, indent=2), encoding="utf-8")
    temp.replace(path)          # atomic: never a half-written file


def device_key(path: Optional[Path] = None) -> str:
    path = path or identity_path()
    data = _read(path)
    key = data.get("device_key")
    if not isinstance(key, str) or not 16 <= len(key) <= 64:
        key = secrets.token_hex(16)
        data["device_key"] = key
        _write(path, data)
    return key


def device_name() -> str:
    """The computer's own name, as Windows shows it (e.g. EIJKIM-PC)."""
    return (platform.node() or "This computer")[:80]


def platform_label() -> str:
    system = platform.system() or "Unknown system"
    release = platform.release()
    return f"{system} {release}".strip()[:80]


def last_email_for(user_id: str, path: Optional[Path] = None) -> Optional[str]:
    return _read(path or identity_path()).get("accounts", {}).get(user_id)


def remember_email(user_id: str, email: str, path: Optional[Path] = None) -> None:
    path = path or identity_path()
    data = _read(path)
    data.setdefault("accounts", {})[user_id] = email
    data.setdefault("device_key", secrets.token_hex(16))
    _write(path, data)


def forget_account(user_id: str, path: Optional[Path] = None) -> None:
    path = path or identity_path()
    data = _read(path)
    if data.get("accounts", {}).pop(user_id, None) is not None:
        _write(path, data)
