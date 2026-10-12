"""Repair Akeso: find program files that are missing or damaged, and put
them back by reinstalling the same version.

Why: an update can leave the install half-replaced (a file in use, an
antivirus quarantine, a cut-off copy). One tester's 1.0.1 -> 1.0.3 update
lost the 3D vessel file, so Blood vessels said "Couldn't load this layer".

How:
  * scripts/make_manifest.py runs during every release and writes
    _internal/akeso_manifest.json: every file of the install with its size
    and SHA-256 fingerprint.
  * check_files() compares the installed files with that list.
  * Repair downloads the installer of THIS version from GitHub (verified
    exactly like an update, see updater.py) and runs it silently. Inno
    Setup copies every file again; notes, settings and "Remember me" live
    in %LOCALAPPDATA%\\Akeso and are not touched.
"""

import hashlib
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Optional

import httpx

from app.core.device_identity import APP_VERSION
from app.core.paths import is_frozen, resource_root
from app.services import updater
from app.services.updater import Release, UpdateError

MANIFEST_NAME = "akeso_manifest.json"
TAG_API = f"https://api.github.com/repos/{updater.RELEASES_REPO}/releases/tags/v{{version}}"


class RepairError(Exception):
    """A message that can be shown to the user as-is."""


@dataclass
class FileReport:
    checked: int = 0
    missing: list[str] = field(default_factory=list)
    damaged: list[str] = field(default_factory=list)
    has_manifest: bool = True

    @property
    def ok(self) -> bool:
        return self.has_manifest and not self.missing and not self.damaged

    @property
    def problems(self) -> list[str]:
        return self.missing + self.damaged


def install_dir() -> Path:
    """The folder holding Akeso.exe (the installed copy)."""
    return Path(sys.executable).resolve().parent


def manifest_path() -> Path:
    return resource_root() / MANIFEST_NAME            # _internal\akeso_manifest.json


def _sha256(path: Path, cancelled: Callable[[], bool]) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        while True:
            if cancelled():
                raise RepairError("The file check was stopped.")
            chunk = handle.read(1024 * 1024)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def check_files(progress: Callable[[int, int], None] = lambda _d, _t: None,
                cancelled: Callable[[], bool] = lambda: False) -> FileReport:
    """Compare the installed files with the release's manifest."""
    if not is_frozen():
        raise RepairError("The file check works on the installed Akeso only. This copy "
                          "is running from the project folder.")
    path = manifest_path()
    if not path.is_file():
        # Releases before the manifest existed: nothing to compare with,
        # but Repair (a reinstall) still works.
        return FileReport(has_manifest=False)
    try:
        data = json.loads(path.read_text("utf-8"))
        files: dict = data["files"]
    except (OSError, ValueError, KeyError, TypeError):
        report = FileReport()
        report.damaged.append(MANIFEST_NAME)
        return report
    root = install_dir()
    report = FileReport()
    total = len(files)
    for index, (relative, (size, sha)) in enumerate(sorted(files.items()), 1):
        target = root / Path(relative)
        try:
            if not target.is_file():
                report.missing.append(relative)
            elif target.stat().st_size != size or _sha256(target, cancelled) != sha:
                report.damaged.append(relative)
        except OSError:
            report.damaged.append(relative)              # unreadable counts as damaged
        report.checked = index
        progress(index, total)
    return report


def release_for_this_version(timeout: float = 10.0) -> Release:
    """The GitHub release of the version that is installed now."""
    url = TAG_API.format(version=APP_VERSION)
    try:
        response = httpx.get(url, headers=updater._headers(), timeout=timeout,
                             follow_redirects=True)
    except httpx.HTTPError as exc:
        raise RepairError("Could not reach GitHub to download the repair. "
                          "Check your internet connection.") from exc
    if response.status_code == 404:
        raise RepairError(f"Akeso {APP_VERSION} is no longer on the releases page. "
                          "Update to the newest version instead.")
    if response.status_code == 403:
        raise RepairError("GitHub is limiting downloads from this network. Try again in an hour.")
    if response.status_code != 200:
        raise RepairError("GitHub could not be reached right now. Try again later.")
    try:
        return updater.release_from_json(response.json(), timeout)
    except UpdateError as exc:
        raise RepairError(str(exc)) from exc
    except ValueError as exc:
        raise RepairError("GitHub sent an unexpected answer. Try again later.") from exc


def summary(report: Optional[FileReport]) -> str:
    """One line for Settings."""
    if report is None:
        return ""
    if not report.has_manifest:
        return ("This version can't check its files (it was built before the check "
                "existed). Repair Akeso still reinstalls every file.")
    if report.ok:
        return f"All {report.checked} Akeso files are present and intact."
    count = len(report.problems)
    names = ", ".join(Path(p).name for p in report.problems[:3])
    more = f" and {count - 3} more" if count > 3 else ""
    return (f"{count} file{'s are' if count != 1 else ' is'} missing or damaged "
            f"({names}{more}). Repair Akeso puts them back.")
