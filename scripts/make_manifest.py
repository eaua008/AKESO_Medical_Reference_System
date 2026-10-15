"""Write the file list that Settings > Updates > Check files compares with.

    .venv\\Scripts\\python scripts\\make_manifest.py 1.0.4

Run after PyInstaller and before Inno Setup (scripts/release.ps1 does it).
It lists every file in dist\\Akeso with its size and SHA-256 fingerprint and
saves the list as dist\\Akeso\\_internal\\akeso_manifest.json, so it ships
inside the installer. See app/services/repair.py.
"""

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist" / "Akeso"
MANIFEST = DIST / "_internal" / "akeso_manifest.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    version = sys.argv[1] if len(sys.argv) > 1 else ""
    if not (DIST / "_internal").is_dir():
        print(f"Not found: {DIST}. Build the app with PyInstaller first.")
        return 1
    files = {}
    for path in sorted(DIST.rglob("*")):
        if path.is_file() and path != MANIFEST:
            relative = path.relative_to(DIST).as_posix()
            files[relative] = [path.stat().st_size, sha256(path)]
    MANIFEST.write_text(json.dumps({"version": version, "files": files}, indent=0),
                        encoding="utf-8")
    size = sum(s for s, _h in files.values()) / 1048576
    print(f"   {len(files)} files ({size:.0f} MB) listed in {MANIFEST.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
