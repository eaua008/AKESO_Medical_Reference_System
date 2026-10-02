"""The account's data kept on this computer (the local SQLite stores).

Bookmarks, saved cases, medications, the Study Notebook and search history live in local
SQLite files, and every row carries an "owner" (the account's email). This
class works across all of them without knowing their tables in detail:

  * export(owner)             every row that belongs to the account
  * erase(owner)              remove those rows (account deletion)
  * rename_owner(old, new)    after an email change, so the notes follow
  * schedule_cache_clear()    wipe the downloaded reference copies at the
                              next start (they re-download on their own)

"Belongs to" means: a row with owner = ?, a child row whose foreign key
points at such a row (medication intake logs), or a notebook setting
stored in meta under "<setting>:<owner>".
"""

import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Callable, Iterator, Optional

from app.repositories.cached_medicine_repository import default_medicine_cache_path
from app.repositories.cached_safety_repository import default_safety_cache_path
from app.repositories.cached_symptom_repository import default_symptom_cache_path
from app.repositories.local_bookmark_store import default_bookmark_path
from app.repositories.local_case_store import default_case_path
from app.repositories.local_disease_cache import default_cache_path
from app.repositories.local_history_store import default_history_path
from app.repositories.local_medication_store import default_medication_path
from app.repositories.local_notebook_store import default_notebook_path

PERSONAL_STORES: dict[str, Callable[[], Path]] = {
    "bookmarks": default_bookmark_path,
    "saved_cases": default_case_path,
    "medications": default_medication_path,
    "notebook": default_notebook_path,
    "search_history": default_history_path,
}
CACHE_FILES: list[Callable[[], Path]] = [
    default_cache_path, default_symptom_cache_path,
    default_medicine_cache_path, default_safety_cache_path,
]
IMAGE_FOLDER = "akeso_notebook_images"
CLEAR_FLAG = "akeso_clear_caches.flag"


@contextmanager
def _open(path: Path) -> Iterator[sqlite3.Connection]:
    """Commit on success, roll back on error, and always close the file."""
    db = sqlite3.connect(path, timeout=5)
    db.row_factory = sqlite3.Row
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def _tables(db: sqlite3.Connection) -> list[str]:
    return [r[0] for r in db.execute(
        "SELECT name FROM sqlite_master WHERE type = 'table' AND name NOT LIKE 'sqlite_%'")]


def _columns(db: sqlite3.Connection, table: str) -> list[str]:
    return [r[1] for r in db.execute(f'PRAGMA table_info("{table}")')]


def _children(db: sqlite3.Connection, owned: set[str]) -> list[tuple[str, str, str, str]]:
    """(child table, its column, parent table, parent column) for tables
    without an owner column that point at an owned table."""
    links = []
    for table in _tables(db):
        if table in owned:
            continue
        for fk in db.execute(f'PRAGMA foreign_key_list("{table}")'):
            parent, column, parent_column = fk[2], fk[3], fk[4] or "id"
            if parent in owned:
                links.append((table, column, parent, parent_column))
    return links


class LocalAccountData:
    def __init__(self, stores: Optional[dict[str, Callable[[], Path]]] = None,
                 images_dir: Optional[Path] = None) -> None:
        self._stores = stores or PERSONAL_STORES
        self._images_dir = images_dir or default_cache_path().with_name(IMAGE_FOLDER)

    def _open_stores(self):
        for name, path_fn in self._stores.items():
            path = path_fn()
            if path.exists():
                yield name, path

    # ------------------------------------------------------------- export

    def export(self, owner: str) -> dict[str, dict[str, list[dict]]]:
        result: dict[str, dict[str, list[dict]]] = {}
        for name, path in self._open_stores():
            with _open(path) as db:
                tables: dict[str, list[dict]] = {}
                owned = {t for t in _tables(db) if "owner" in _columns(db, t)}
                for table in sorted(owned):
                    rows = db.execute(f'SELECT * FROM "{table}" WHERE owner = ?', (owner,))
                    tables[table] = [dict(r) for r in rows]
                for child, column, parent, parent_column in _children(db, owned):
                    rows = db.execute(
                        f'SELECT * FROM "{child}" WHERE "{column}" IN '
                        f'(SELECT "{parent_column}" FROM "{parent}" WHERE owner = ?)', (owner,))
                    tables[child] = [dict(r) for r in rows]
                if "meta" in _tables(db):
                    rows = db.execute("SELECT key, value FROM meta WHERE key LIKE ?",
                                      (f"%:{owner}",))
                    settings = [dict(r) for r in rows]
                    if settings:
                        tables["settings"] = settings
                result[name] = tables
        return result

    def notebook_images(self, exported: dict) -> list[Path]:
        """Pictures pasted into this account's notes (they live in a folder)."""
        if not self._images_dir.exists():
            return []
        text = repr(exported.get("notebook", {}))
        return [p for p in self._images_dir.iterdir() if p.is_file() and p.name in text]

    # -------------------------------------------------------------- erase

    def erase(self, owner: str) -> int:
        """Delete every local row of this account. Returns rows removed."""
        exported = self.export(owner)
        images = self.notebook_images(exported)
        removed = 0
        for name, path in self._open_stores():
            with _open(path) as db:
                owned = {t for t in _tables(db) if "owner" in _columns(db, t)}
                for child, column, parent, parent_column in _children(db, owned):
                    removed += db.execute(
                        f'DELETE FROM "{child}" WHERE "{column}" IN '
                        f'(SELECT "{parent_column}" FROM "{parent}" WHERE owner = ?)',
                        (owner,)).rowcount
                for table in owned:
                    removed += db.execute(f'DELETE FROM "{table}" WHERE owner = ?',
                                          (owner,)).rowcount
                if "meta" in _tables(db):
                    db.execute("DELETE FROM meta WHERE key LIKE ?", (f"%:{owner}",))
        # Pictures are only removed when no other account's notes use them.
        others = repr(self._all_notebook_text(exclude=owner))
        for image in images:
            if image.name not in others:
                try:
                    image.unlink()
                except OSError:
                    pass
        return removed

    def _all_notebook_text(self, exclude: str) -> list:
        path = self._stores.get("notebook", default_notebook_path)()
        if not path.exists():
            return []
        with _open(path) as db:
            if "notebook_items" not in _tables(db):
                return []
            return [dict(r) for r in db.execute(
                "SELECT * FROM notebook_items WHERE owner <> ?", (exclude,))]

    # ------------------------------------------------------- email change

    def rename_owner(self, old: str, new: str) -> int:
        if not old or not new or old == new:
            return 0
        changed = 0
        for name, path in self._open_stores():
            with _open(path) as db:
                for table in _tables(db):
                    if "owner" in _columns(db, table):
                        changed += db.execute(f'UPDATE "{table}" SET owner = ? WHERE owner = ?',
                                              (new, old)).rowcount
                if "meta" in _tables(db):
                    for row in db.execute("SELECT key FROM meta WHERE key LIKE ?",
                                          (f"%:{old}",)).fetchall():
                        key = row[0]
                        db.execute("UPDATE OR REPLACE meta SET key = ? WHERE key = ?",
                                   (key[: -len(old)] + new, key))
        return changed

    # ------------------------------------------------------------- caches

    @staticmethod
    def schedule_cache_clear() -> None:
        flag = default_cache_path().with_name(CLEAR_FLAG)
        flag.parent.mkdir(parents=True, exist_ok=True)
        flag.write_text("clear downloaded reference copies at next start\n", encoding="utf-8")

    @staticmethod
    def cache_clear_pending() -> bool:
        return default_cache_path().with_name(CLEAR_FLAG).exists()

    @staticmethod
    def cache_size() -> int:
        total = 0
        for path_fn in CACHE_FILES:
            base = path_fn()
            for extra in ("", "-wal", "-shm"):
                file = Path(str(base) + extra)
                if file.exists():
                    total += file.stat().st_size
        return total


def apply_pending_cache_clear() -> bool:
    """Called by main.py before anything opens the caches. Returns True if
    the downloaded copies were removed (they re-download on first use)."""
    flag = default_cache_path().with_name(CLEAR_FLAG)
    if not flag.exists():
        return False
    for path_fn in CACHE_FILES:
        base = path_fn()
        for extra in ("", "-wal", "-shm"):
            file = Path(str(base) + extra)
            try:
                if file.exists():
                    file.unlink()
            except OSError:
                pass
    try:
        flag.unlink()
    except OSError:
        pass
    return True
