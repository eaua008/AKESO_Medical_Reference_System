"""Where Akeso's own files are, in development and in the packaged .exe.

Running from IntelliJ (python main.py), everything sits in the project
folder. In the packaged app (PyInstaller), the files that ship with Akeso
(assets/, data/, the bundled .env) are unpacked next to the program, in the
folder PyInstaller reports as sys._MEIPASS, and the .exe itself is
sys.executable.

Files Akeso writes (caches, notes, preferences) never go here: they live in
%LOCALAPPDATA%\\Akeso (see local_disease_cache.default_cache_path), because
an installed program's folder is read-only for normal users.
"""

import sys
from pathlib import Path


def is_frozen() -> bool:
    """True inside the packaged .exe."""
    return bool(getattr(sys, "frozen", False))


def resource_root() -> Path:
    """The folder holding assets/, data/ and the bundled .env."""
    if is_frozen():
        return Path(getattr(sys, "_MEIPASS", Path(sys.executable).parent))
    # app/core/paths.py -> app/core -> app -> <project root>
    return Path(__file__).resolve().parents[2]


def app_dir() -> Path:
    """The folder of the .exe (packaged) or the project (development)."""
    return Path(sys.executable).parent if is_frozen() else resource_root()


def resource(*parts: str) -> Path:
    return resource_root().joinpath(*parts)
