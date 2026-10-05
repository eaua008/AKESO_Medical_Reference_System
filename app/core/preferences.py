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


# Display size, in percent of normal. Applied when Akeso starts (Qt scales
# every widget, font and icon by it), so a change needs a restart.
UI_SCALES = (80, 90, 100, 110, 125)
# Encyclopedia cards per row; 0 means "as many as fit".
CARD_COLUMNS = (0, 2, 3, 4, 5)


def _theme_ids() -> set:
    from app.core.theme_presets import PRESETS
    return set(PRESETS)


def default_preferences_path() -> Path:
    return default_cache_path().with_name("akeso_preferences.json")


@dataclass
class Preferences:
    theme: str = "dark"            # the app's built-in default (Theme._mode)
    sidebar_pinned: bool = False
    start_tab: str = "dashboard"
    ui_scale: int = 90             # a little smaller than Qt's default
    color_theme: str = "akeso"     # Settings > Appearance (app/core/theme_presets.py)
    cards_per_row: int = 0
    # The window's normal ("restore down") size and place, [x, y, w, h] in
    # screen pixels, and whether it was maximised when Akeso closed.
    window_rect: Optional[list] = None
    window_maximized: bool = False

    def cleaned(self) -> "Preferences":
        """Replace anything unexpected (a hand-edited file) with the default."""
        default = Preferences()
        return Preferences(
            theme=self.theme if self.theme in THEMES else default.theme,
            sidebar_pinned=bool(self.sidebar_pinned),
            start_tab=(self.start_tab if self.start_tab in dict(START_TABS)
                       else default.start_tab),
            ui_scale=self.ui_scale if self.ui_scale in UI_SCALES else default.ui_scale,
            cards_per_row=(self.cards_per_row if self.cards_per_row in CARD_COLUMNS
                           else default.cards_per_row),
            color_theme=(self.color_theme if self.color_theme in _theme_ids()
                         else default.color_theme),
            window_rect=_clean_rect(self.window_rect),
            window_maximized=bool(self.window_maximized),
        )


def _clean_rect(value) -> Optional[list]:
    """[x, y, w, h] of whole numbers and a usable size, or None."""
    if not isinstance(value, (list, tuple)) or len(value) != 4:
        return None
    if not all(isinstance(n, int) and not isinstance(n, bool) for n in value):
        return None
    x, y, w, h = value
    if w < 600 or h < 400 or w > 20000 or h > 20000:
        return None
    return [x, y, w, h]


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
