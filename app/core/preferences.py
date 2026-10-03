"""App preferences for this computer: theme, sidebar, where Akeso opens.

A small JSON file next to the reference caches. These are choices about
this computer, not about the account, so they stay put when someone else
signs in on it (the same way a browser keeps its theme across accounts).
Per-account choices, such as whether search history is saved, live with
that account's data instead (see local_history_store.py).

Reading never fails: a missing or damaged file just means the defaults.
"""

import json
from dataclasses import asdict, dataclass, fields
from pathlib import Path
from typing import Optional

from app.repositories.local_disease_cache import default_cache_path

THEMES = ("light", "dark")
# Screens Akeso may open on after signing in (ids from the sidebar config).
START_TABS = (
    ("dashboard", "Dashboard Overview"),
    ("symptom-checker", "Symptom Checker"),
    ("drug-checker", "Drug Interaction Checker"),
    ("diseases", "Disease Encyclopedia"),
    ("notebook", "Study Notebook"),
    ("exchange", "Clinical Exchange"),
)


def default_preferences_path() -> Path:
    return default_cache_path().with_name("akeso_preferences.json")


@dataclass
class Preferences:
    theme: str = "dark"            # the app's built-in default (Theme._mode)
    sidebar_pinned: bool = False
    start_tab: str = "dashboard"

    def cleaned(self) -> "Preferences":
        """Replace anything unexpected (a hand-edited file) with the default."""
        default = Preferences()
        return Preferences(
            theme=self.theme if self.theme in THEMES else default.theme,
            sidebar_pinned=bool(self.sidebar_pinned),
            start_tab=(self.start_tab if self.start_tab in dict(START_TABS)
                       else default.start_tab),
        )


class PreferenceStore:
    def __init__(self, path: Optional[Path] = None) -> None:
        self._path = path or default_preferences_path()

    def load(self) -> Preferences:
        try:
            raw = json.loads(self._path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return Preferences()
        if not isinstance(raw, dict):
            return Preferences()
        known = {f.name for f in fields(Preferences)}
        return Preferences(**{k: v for k, v in raw.items() if k in known}).cleaned()

    def save(self, prefs: Preferences) -> None:
        """Best effort: a read-only folder must not crash the app."""
        try:
            self._path.parent.mkdir(parents=True, exist_ok=True)
            tmp = self._path.with_suffix(".tmp")
            tmp.write_text(json.dumps(asdict(prefs.cleaned()), indent=2), encoding="utf-8")
            tmp.replace(self._path)
        except OSError:
            pass

    def update(self, **changes) -> Preferences:
        """Change some fields and save; returns the new preferences."""
        prefs = self.load()
        for key, value in changes.items():
            setattr(prefs, key, value)
        prefs = prefs.cleaned()
        self.save(prefs)
        return prefs
