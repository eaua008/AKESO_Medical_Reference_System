"""Akeso updates: is there a newer version, download it, install it.

Releases live on GitHub, in a public repository that holds ONLY the
installers (the code repository can stay private):

    https://github.com/eaua008/akeso-releases/releases

Each release is tagged with its version ("v1.0.1") and carries the Inno
Setup installer "Akeso-Setup-1.0.1.exe" (scripts/release.ps1 builds it and
its .sha256 file). Akeso asks GitHub for the latest release, compares the
version with its own, and on "Update now":

  1. downloads the installer into %LOCALAPPDATA%\\Akeso\\updates,
  2. checks its SHA-256 fingerprint against the one GitHub publishes for
     that file; a file that does not match (corrupted, or swapped by
     someone in the middle) is deleted and never run,
  3. runs it silently (/VERYSILENT ... /UPDATE). Inno Setup closes Akeso,
     replaces the program files and starts the new version. The user's
     notes, settings and "Remember me" live in %LOCALAPPDATA%\\Akeso and are
     not touched.

No keys or tokens: the releases repository is public and read-only to
everyone but its owner, which is what makes this safe to ship in the app.
"""

import hashlib
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Optional

import httpx

from app.core.device_identity import APP_VERSION

RELEASES_REPO = "eaua008/akeso-releases"
RELEASES_PAGE = f"https://github.com/{RELEASES_REPO}/releases"
LATEST_API = f"https://api.github.com/repos/{RELEASES_REPO}/releases/latest"
DOWNLOAD_PREFIX = f"https://github.com/{RELEASES_REPO}/releases/download/"
INSTALLER_NAME = re.compile(r"^Akeso-Setup-(\d+(?:\.\d+){1,3})\.exe$", re.IGNORECASE)
MAX_INSTALLER_BYTES = 2 * 1024 ** 3            # GitHub's own per-file limit


class UpdateError(Exception):
    """A message that can be shown to the user as-is."""


@dataclass(frozen=True)
class Release:
    version: str            # "1.0.1"
    notes: str              # the release description on GitHub
    url: str                # installer download URL (github.com/<repo>/releases/download/...)
    size: int               # bytes
    sha256: str             # lowercase hex
    file_name: str


# ------------------------------------------------------------- versions

def parse_version(text: str) -> tuple[int, ...]:
    """"v1.2.3" / "1.2" -> (1, 2, 3) / (1, 2, 0). Anything odd -> (0,)."""
    match = re.match(r"^\s*v?(\d+(?:\.\d+){0,3})", text or "")
    if not match:
        return (0,)
    parts = [int(p) for p in match.group(1).split(".")]
    while len(parts) < 3:
        parts.append(0)
    return tuple(parts)


def is_newer(latest: str, current: str = APP_VERSION) -> bool:
    return parse_version(latest) > parse_version(current)


# ----------------------------------------------------------- GitHub API

def _headers() -> dict:
    return {"Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": f"Akeso/{APP_VERSION}"}


def fetch_latest(timeout: float = 10.0) -> Optional[Release]:
    """The newest published release, or None if there is none yet.
    Raises UpdateError when GitHub cannot be reached or the release is
    incomplete (no installer or no checksum)."""
    try:
        response = httpx.get(LATEST_API, headers=_headers(), timeout=timeout,
                             follow_redirects=True)
    except httpx.HTTPError as exc:
        raise UpdateError("Could not reach GitHub to check for updates. "
                          "Check your internet connection.") from exc
    if response.status_code == 404:
        return None                                   # no release published yet
    if response.status_code == 403:
        raise UpdateError("GitHub is limiting update checks from this network. "
                          "Try again in an hour.")
    if response.status_code != 200:
        raise UpdateError(f"GitHub answered {response.status_code}. Try again later.")
    return release_from_json(response.json(), timeout)


def release_from_json(data: dict, timeout: float = 10.0) -> Release:
    """Pick the installer and its fingerprint out of GitHub's answer."""
    if data.get("draft") or data.get("prerelease"):
        raise UpdateError("The latest release is not published yet.")
    version = ".".join(str(n) for n in parse_version(data.get("tag_name", "")))
    assets = data.get("assets") or []
    installer = None
    for asset in assets:
        match = INSTALLER_NAME.match(asset.get("name", ""))
        if match:
            installer = asset
            break
    if installer is None:
        raise UpdateError(f"Release {version} has no Akeso-Setup installer attached.")
    url = installer.get("browser_download_url", "")
    if not url.startswith(DOWNLOAD_PREFIX):
        raise UpdateError("The update's download address is not Akeso's release page.")
    size = int(installer.get("size") or 0)
    if not 0 < size <= MAX_INSTALLER_BYTES:
        raise UpdateError("The update's installer has an unexpected size.")

    # GitHub computes a SHA-256 for every uploaded file ("digest"). Older
    # uploads may lack it; then use the .sha256 file published beside it.
    sha = ""
    digest = installer.get("digest") or ""
    if digest.lower().startswith("sha256:"):
        sha = digest.split(":", 1)[1]
    if not sha:
        side = next((a for a in assets
                     if a.get("name", "").lower() == installer["name"].lower() + ".sha256"),
                    None)
        if side is not None:
            sha = _read_checksum_file(side.get("browser_download_url", ""), timeout)
    sha = sha.strip().lower()
    if not re.fullmatch(r"[0-9a-f]{64}", sha):
        raise UpdateError(f"Release {version} has no checksum, so it cannot be "
                          "verified. Download it from the releases page instead.")
    return Release(version=version, notes=(data.get("body") or "").strip(), url=url,
                   size=size, sha256=sha, file_name=installer["name"])


def _read_checksum_file(url: str, timeout: float) -> str:
    if not url.startswith(DOWNLOAD_PREFIX):
        return ""
    try:
        response = httpx.get(url, headers=_headers(), timeout=timeout, follow_redirects=True)
        response.raise_for_status()
    except httpx.HTTPError:
        return ""
    # "abc123...  Akeso-Setup-1.0.1.exe" or just the hash.
    first = response.text.strip().split()
    return first[0] if first else ""


# ------------------------------------------------------- download / run

def updates_dir() -> Path:
    from app.repositories.local_disease_cache import default_cache_path
    return default_cache_path().parent / "updates"


def download(release: Release, progress: Callable[[int, int], None],
             cancelled: Callable[[], bool]) -> Path:
    """Download and verify the installer. Returns its path. Raises
    UpdateError (the partial file is deleted)."""
    folder = updates_dir()
    folder.mkdir(parents=True, exist_ok=True)
    final = folder / release.file_name
    part = final.with_name(final.name + ".part")
    digest = hashlib.sha256()
    done = 0
    try:
        with httpx.stream("GET", release.url, headers=_headers(), timeout=30.0,
                          follow_redirects=True) as response:
            response.raise_for_status()
            with open(part, "wb") as out:
                for chunk in response.iter_bytes(256 * 1024):
                    if cancelled():
                        raise UpdateError("Update cancelled.")
                    done += len(chunk)
                    if done > release.size:
                        raise UpdateError("The download is bigger than the release says. "
                                          "It was deleted.")
                    out.write(chunk)
                    digest.update(chunk)
                    progress(done, release.size)
        if done != release.size:
            raise UpdateError("The download was cut off. Try again.")
        if digest.hexdigest() != release.sha256:
            raise UpdateError("The downloaded installer does not match its fingerprint, so "
                              "it was deleted and not run. Try again later.")
        os.replace(part, final)
        return final
    except httpx.HTTPError as exc:
        raise UpdateError("The download failed. Check your internet connection.") from exc
    except OSError as exc:
        raise UpdateError(f"Could not save the update: {exc.strerror or exc}") from exc
    finally:
        try:
            part.unlink(missing_ok=True)
        except OSError:
            pass


def launch_installer(path: Path) -> None:
    """Start the installer silently, detached from Akeso (which then quits).
    /UPDATE tells installer\\akeso.iss to start Akeso again when done."""
    if sys.platform != "win32":
        raise UpdateError("Updates install on Windows only.")
    flags = 0x00000008 | 0x00000200            # DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP
    try:
        subprocess.Popen([str(path), "/VERYSILENT", "/SUPPRESSMSGBOXES", "/NORESTART",
                          "/CLOSEAPPLICATIONS", "/UPDATE"],
                         creationflags=flags, close_fds=True)
    except OSError as exc:
        raise UpdateError(f"Could not start the installer: {exc.strerror or exc}") from exc


def clean_up_downloads() -> None:
    """Delete installers left from earlier updates (run at start-up)."""
    folder = updates_dir()
    if not folder.is_dir():
        return
    for item in folder.iterdir():
        if item.is_file() and item.name.lower().startswith("akeso-setup-"):
            try:
                item.unlink()
            except OSError:
                pass                     # still running (the update just finished)
