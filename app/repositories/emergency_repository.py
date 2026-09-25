"""Loads the Emergency Guide from a JSON file shipped with the app.

Why bundled instead of Supabase + cache like the encyclopedia: this is the one
screen that has to work on a brand-new install with no internet. The
encyclopedia cache is empty until the first sync; this file is on disk from
the moment the app is installed.

The service only calls load(). A Supabase-backed repository with the same
method could replace this later without the service or view changing, the
same way CachedDiseaseRepository slotted in behind DiseaseService.
"""

import json
from pathlib import Path
from typing import Optional

from app.models.emergency import EmergencyGuide, EmergencyProtocol, Hotline

DEFAULT_DATA_PATH = Path(__file__).resolve().parents[2] / "data" / "emergency_ph.json"

class EmergencyDataError(Exception):
    """The bundled file is missing or malformed."""


class BundledEmergencyRepository:
    """Reads app/data/emergency_ph.json into model objects."""

    def __init__(self, path: Optional[Path] = None) -> None:
        self._path = path or DEFAULT_DATA_PATH
        self._guide: Optional[EmergencyGuide] = None

    def load(self) -> EmergencyGuide:
        """Parse once, then reuse. The file never changes while the app runs."""
        if self._guide is None:
            self._guide = self._parse(self._read())
        return self._guide

    # ------------------------------------------------------------ internals

    def _read(self) -> dict:
        try:
            with self._path.open(encoding="utf-8") as handle:
                return json.load(handle)
        except FileNotFoundError as exc:
            raise EmergencyDataError(f"Emergency data not found: {self._path}") from exc
        except json.JSONDecodeError as exc:
            raise EmergencyDataError(f"Emergency data is not valid JSON: {exc}") from exc

    @staticmethod
    def _hotline(raw: dict) -> Hotline:
        return Hotline(
            name=raw["name"],
            number=raw["number"],
            description=raw.get("description", ""),
            alt_numbers=tuple(raw.get("alt_numbers", [])),
        )

    @staticmethod
    def _protocol(raw: dict) -> EmergencyProtocol:
        return EmergencyProtocol(
            id=raw["id"],
            title=raw["title"],
            local_name=raw.get("local_name", ""),
            urgency=raw.get("urgency", "urgent"),
            keywords=tuple(raw.get("keywords", [])),
            warning_signs=tuple(raw.get("warning_signs", [])),
            steps=tuple(raw["steps"]),
            avoid=tuple(raw.get("avoid", [])),
            call_when=raw.get("call_when", ""),
            source=raw.get("source", ""),
        )

    def _parse(self, data: dict) -> EmergencyGuide:
        try:
            return EmergencyGuide(
                region=data.get("region", ""),
                featured_hotline=self._hotline(data["featured_hotline"]),
                hotlines=tuple(self._hotline(h) for h in data.get("hotlines", [])),
                call_tips=tuple(data.get("call_tips", [])),
                local_note=data.get("local_note", ""),
                protocols=tuple(self._protocol(p) for p in data.get("protocols", [])),
            )
        except KeyError as exc:
            # A missing required field should fail loudly here, not show up
            # later as a half-empty card on screen.
            raise EmergencyDataError(f"Emergency data is missing field {exc}") from exc