"""The Body System Explorer's vessel and nerve colours, for this computer.

The user can recolour a whole kind (every artery green) or single vessels
(just the aorta orange). The 3D page reports every change; it is kept in a
small JSON file next to the preferences and sent back to the page the next
time the explorer opens.

Reading never fails: a missing or damaged file just means the textbook
colours (arteries red, veins blue).
"""

import json
import re
from pathlib import Path
from typing import Optional

from app.core.preferences import default_preferences_path

HEX = re.compile(r"^#[0-9a-f]{6}$")


def default_colours_path() -> Path:
    return default_preferences_path().with_name("akeso_anatomy_colours.json")


def _clean(raw) -> dict:
    """Only "#rrggbb" strings under short keys; anything else is dropped."""
    out = {"kinds": {}, "custom": {}}
    if not isinstance(raw, dict):
        return out
    for section in out:
        values = raw.get(section)
        if not isinstance(values, dict):
            continue
        for key, value in values.items():
            if (isinstance(key, str) and len(key) <= 64 and isinstance(value, str)
                    and HEX.match(value.lower())):
                out[section][key] = value.lower()
    return out


class AnatomyColourStore:
    def __init__(self, path: Optional[Path] = None) -> None:
        self._path = path or default_colours_path()

    def load(self) -> dict:
        try:
            return _clean(json.loads(self._path.read_text(encoding="utf-8")))
        except (OSError, ValueError):
            return _clean(None)

    def save(self, colours: dict) -> None:
        """Best effort: a read-only folder must not crash the app."""
        try:
            self._path.parent.mkdir(parents=True, exist_ok=True)
            tmp = self._path.with_suffix(".tmp")
            tmp.write_text(json.dumps(_clean(colours), indent=2), encoding="utf-8")
            tmp.replace(self._path)
        except OSError:
            pass
