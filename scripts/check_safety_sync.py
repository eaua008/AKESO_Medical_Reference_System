"""One-off check: download the drug-safety reference and show what arrived.

Run it from IntelliJ (right-click > Run 'check_safety_sync'). It uses the
same .env and the same cache file the app will use, so if this prints the
counts, the module's data layer works end to end.

Safe to run as often as you like: it only reads Supabase and rewrites the
local cache file, which the app rebuilds anyway.
"""

import sys
from pathlib import Path

# Let "import app..." work when this file is run directly.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.repositories.cached_safety_repository import (  # noqa: E402
    CachedSafetyRepository,
    default_safety_cache_path,
)


def main() -> None:
    repo = CachedSafetyRepository()
    print(f"Cache file: {default_safety_cache_path()}")

    changed = repo.sync(force=True)
    repo.reload()
    ref = repo.reference()

    print(f"Downloaded: {'yes' if changed else 'no'}")
    print(f"  conditions        {len(ref.conditions)}")
    print(f"  condition safety  {len(ref.condition_safety)}")
    print(f"  drug pairs        {len(ref.interactions)}")
    print(f"  rules             {len(ref.rules)}")
    for condition in ref.conditions:
        print(f"    - {condition.id:<18} {condition.label}")


if __name__ == "__main__":
    main()
