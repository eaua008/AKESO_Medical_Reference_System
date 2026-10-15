"""Keeps the Study Notebook the same on every computer you sign in on.

The notebook still works from akeso_notebook.db on this computer (fast,
and usable offline). NotebookSync copies it to and from the account's
notebook in Supabase (migration 011):

  1. download what changed in the cloud since the last sync, and merge it:
       - something new or untouched here  -> take the cloud copy,
       - edited both here and elsewhere  -> the most recent edit wins
         (by its "last edited" time), the other edit is replaced,
       - deleted elsewhere                -> deleted here too;
  2. upload what changed here (deletions included);
  3. pictures pasted into notes travel with them: uploaded to the private
     notebook-images bucket, and downloaded into this computer's
     akeso_notebook_images folder when a note needs them.

Notes refer to pictures by their full path on this computer
(file:///C:/Users/<you>/AppData/...). That path differs per computer, so
uploads replace it with "akeso-image:<file name>" and downloads put this
computer's path back in.

Times: the notebook stores local times without a zone ("2026-10-04T19:20:05").
They are sent as UTC and turned back into this computer's local time.
"""

import json
import mimetypes
import re
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Callable, Optional

from app.repositories.local_notebook_store import LocalNotebookStore
from app.repositories.notebook_cloud_repository import NotebookCloudRepository

LAST_PULL = "cloud_last_pull"
OVERLAP = timedelta(minutes=5)          # re-read a little, never miss a late commit
PORTABLE = "akeso-image:"
_LOCAL_IMAGE = re.compile(
    r"file:///[^\"'<>]*?akeso_notebook_images/([0-9A-Za-z_-]{6,64}\.[A-Za-z0-9]{2,5})")
_PORTABLE_IMAGE = re.compile(r"akeso-image:([0-9A-Za-z_-]{6,64}\.[A-Za-z0-9]{2,5})")


@dataclass
class SyncResult:
    downloaded: int = 0          # notes / cases / subjects changed here by the cloud
    uploaded: int = 0
    images_up: int = 0
    images_down: int = 0

    @property
    def changed_here(self) -> bool:
        return self.downloaded > 0 or self.images_down > 0


# ------------------------------------------------------------------ times

def to_utc(local: Optional[str]) -> Optional[str]:
    """'2026-10-04T19:20:05' (this computer's time) -> UTC ISO string."""
    if not local:
        return None
    moment = datetime.fromisoformat(local)
    if moment.tzinfo is None:
        moment = moment.astimezone()                # local zone
    return moment.astimezone(timezone.utc).isoformat(timespec="seconds")


def to_local(stamp: Optional[str]) -> Optional[str]:
    """Server timestamp -> this computer's local time, as the notebook stores it."""
    if not stamp:
        return None
    moment = datetime.fromisoformat(stamp.replace("Z", "+00:00"))
    if moment.tzinfo is None:
        moment = moment.replace(tzinfo=timezone.utc)
    return moment.astimezone().replace(tzinfo=None).isoformat(timespec="seconds")


def _moment(local: Optional[str]) -> datetime:
    if not local:
        return datetime.min.replace(tzinfo=timezone.utc)
    moment = datetime.fromisoformat(local)
    return (moment.astimezone() if moment.tzinfo is None else moment).astimezone(timezone.utc)


# ---------------------------------------------------------------- service

class NotebookSync:
    def __init__(self, owner: str, store: LocalNotebookStore,
                 cloud: NotebookCloudRepository, images_dir: Callable[[], Path]) -> None:
        self._owner = owner
        self._store = store
        self._cloud = cloud
        self._images_dir = images_dir

    def has_local_changes(self) -> bool:
        return self._store.has_pending(self._owner)

    def sync(self) -> SyncResult:
        """One full round. Runs on a background thread; raises AccountError
        (offline, signed out, migration missing) without changing anything
        that was not already finished."""
        result = SyncResult()
        self._pull(result)
        self._push(result)
        return result

    # ---------------------------------------------------------- download

    def _pull(self, result: SyncResult) -> None:
        last = self._store.get_setting(self._owner, LAST_PULL, None)
        since = None
        if last:
            since = (datetime.fromisoformat(last) - OVERLAP).isoformat()
        subjects = self._cloud.subjects_since(since)
        items = self._cloud.items_since(since)
        newest = last

        for row in subjects:
            newest = max(newest or "", row["server_updated_at"])
            remote = {"id": row["id"], "name": row["name"],
                      "created_at": to_local(row["created_at"]),
                      "updated_at": to_local(row["updated_at"]),
                      "deleted_at": to_local(row["deleted_at"])}
            if self._take(self._store.local_row(self._owner, "subjects", row["id"]), remote):
                self._store.put_remote_subject(self._owner, remote)
                result.downloaded += 1

        names: set[str] = set()
        for row in items:
            newest = max(newest or "", row["server_updated_at"])
            body = row.get("body") or ""
            names.update(_PORTABLE_IMAGE.findall(body))
            remote = {"id": row["id"], "kind": row["kind"], "title": row["title"],
                      "subject_id": row.get("subject_id") or "",
                      "tags": json.dumps(row.get("tags") or []),
                      "body": self._localise(body),
                      "case_data": json.dumps(row.get("case_data") or {}),
                      "workspace": row.get("workspace") or "",
                      "pinned": bool(row.get("pinned")),
                      "created_at": to_local(row["created_at"]),
                      "updated_at": to_local(row["updated_at"]),
                      "deleted_at": to_local(row["deleted_at"])}
            if self._take(self._store.local_row(self._owner, "items", row["id"]), remote):
                self._store.put_remote_item(self._owner, remote)
                result.downloaded += 1

        result.images_down = self._download_images(names)
        if newest and newest != last:
            self._store.set_setting(self._owner, LAST_PULL, newest)

    @staticmethod
    def _take(local: Optional[dict], remote: dict) -> bool:
        """Should the cloud copy replace what is on this computer?"""
        if local is None or local.get("synced"):
            return True                 # nothing here that is not in the cloud already
        # Changed here too and not uploaded yet: the most recent edit wins.
        remote_time = max(_moment(remote["updated_at"]), _moment(remote["deleted_at"]))
        local_time = max(_moment(local.get("updated_at")), _moment(local.get("deleted_at")))
        return remote_time > local_time

    def _localise(self, body: str) -> str:
        folder = self._images_dir()
        return _PORTABLE_IMAGE.sub(
            lambda m: (folder / m.group(1)).resolve().as_uri(), body)

    def _download_images(self, names: set[str]) -> int:
        if not names:
            return 0
        folder = self._images_dir()
        count = 0
        for name in sorted(names):
            target = folder / name
            if target.exists():
                continue
            data = self._cloud.download_image(name)
            if data:
                target.write_bytes(data)
                count += 1
        return count

    # ------------------------------------------------------------ upload

    def _push(self, result: SyncResult) -> None:
        subjects, items = self._store.pending(self._owner)
        if not subjects and not items:
            return

        if subjects:
            self._cloud.upsert("notebook_subjects", [
                {"id": s["id"], "name": s["name"], "created_at": to_utc(s["created_at"]),
                 "updated_at": to_utc(s["updated_at"]), "deleted_at": to_utc(s["deleted_at"])}
                for s in subjects])
            for s in subjects:
                self._store.mark_synced(self._owner, "subjects", s)
            result.uploaded += len(subjects)

        if items:
            names: set[str] = set()
            payload = []
            for i in items:
                names.update(_LOCAL_IMAGE.findall(i["body"] or ""))
                payload.append({
                    "id": i["id"], "kind": i["kind"], "title": i["title"],
                    "subject_id": i["subject_id"] or "",
                    "tags": json.loads(i["tags"] or "[]"),
                    "body": _LOCAL_IMAGE.sub(lambda m: PORTABLE + m.group(1), i["body"] or ""),
                    "case_data": json.loads(i["case_data"] or "{}"),
                    "workspace": i["workspace"] or "", "pinned": bool(i["pinned"]),
                    "created_at": to_utc(i["created_at"]), "updated_at": to_utc(i["updated_at"]),
                    "deleted_at": to_utc(i["deleted_at"])})
            # Pictures first, so another computer never gets a note whose
            # picture is not there yet.
            result.images_up = self._upload_images(names)
            self._cloud.upsert("notebook_items", payload)
            for i in items:
                self._store.mark_synced(self._owner, "items", i)
            result.uploaded += len(items)

    def _upload_images(self, names: set[str]) -> int:
        if not names:
            return 0
        folder = self._images_dir()
        present = self._cloud.image_names()
        count = 0
        for name in sorted(names - present):
            source = folder / name
            if not source.is_file():
                continue                       # picture removed from this computer
            kind = mimetypes.guess_type(name)[0] or "image/png"
            self._cloud.upload_image(name, source.read_bytes(), kind)
            count += 1
        return count
