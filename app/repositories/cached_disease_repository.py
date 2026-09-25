"""Cache-first disease repository.

This is the payoff of the repository layer. It has the SAME method names as
SupabaseDiseaseRepository, so DiseaseService, the controllers and every view
work unchanged — they cannot tell the data now comes from local disk.

Reads never touch the network:

    reload(), all_diseases(), get_disease()   ->  local SQLite copy

The network is used only by sync(), which the app runs on a background
thread:

    1. Read one number from Supabase: content_version.
    2. Same as the local copy's version?  Done. Nothing downloads.
    3. Different, or no local copy yet?   Download everything in ~11
       requests and swap it in atomically.

That is also what makes the app work offline. With no network, sync()
fails quietly and the last downloaded copy keeps serving every read.
"""

from typing import Callable, Optional

from app.models.disease import BodySystem, Disease
from app.repositories.local_disease_cache import LocalDiseaseCache
from app.repositories.supabase_disease_repository import (
    DiseaseRepositoryError,
    SupabaseDiseaseRepository,
)


class CachedDiseaseRepository:
    """Serves reads from the local copy; refreshes it from Supabase."""

    def __init__(
            self,
            cache: Optional[LocalDiseaseCache] = None,
            remote_factory: Optional[Callable[[], SupabaseDiseaseRepository]] = None,
    ) -> None:
        self._cache = cache or LocalDiseaseCache()
        # A factory, not an instance. sync() runs on a worker thread and
        # builds its own remote client there, so no network client is ever
        # shared between threads. Also lets tests pass a fake remote.
        self._remote_factory = remote_factory or SupabaseDiseaseRepository
        self._diseases: list[Disease] = []
        self._body_systems: list[BodySystem] = []
        self._loaded = False

    # --------------------------------------------------------------- reads

    def _ensure_loaded(self) -> None:
        if not self._loaded:
            self.reload()

    def reload(self) -> None:
        """Re-read the local copy into memory. Disk only, so it is fast.

        Called on the UI thread — including after a sync has written a newer
        copy, which is how fresh data reaches the screen.
        """
        self._diseases = self._cache.load_diseases()
        self._body_systems = self._cache.load_body_systems()
        self._loaded = True

    def all_diseases(self) -> list[Disease]:
        self._ensure_loaded()
        return list(self._diseases)

    def all_body_systems(self) -> list[BodySystem]:
        self._ensure_loaded()
        return list(self._body_systems)

    def get_body_system(self, system_id: str) -> Optional[BodySystem]:
        self._ensure_loaded()
        return next((s for s in self._body_systems if s.id == system_id), None)

    def get_disease(self, disease_id: str) -> Optional[Disease]:
        """Already fully hydrated in the local copy — no round trips."""
        self._ensure_loaded()
        return next((d for d in self._diseases if d.id == disease_id), None)

    def count(self) -> int:
        self._ensure_loaded()
        return len(self._diseases)

    def is_empty(self) -> bool:
        """True before the first successful sync on this machine."""
        return self._cache.is_empty()

    def stats(self) -> dict[str, int]:
        """Counts as of the last sync, falling back to a live query.

        The fallback only happens before the first sync, when there is no
        local copy to count.
        """
        cached = self._cache.stats()
        if cached is not None:
            return cached
        return self._remote_factory().stats()

    # ---------------------------------------------------------------- sync

    def sync(self, force: bool = False) -> bool:
        """Bring the local copy up to date. Returns True if it changed.

        Runs on a background thread. It writes to disk only and never
        touches the in-memory lists above — those belong to the UI thread,
        which picks up the new copy by calling reload() afterwards.

        Raises DiseaseRepositoryError on network failure. The caller treats
        that as "stay on the copy we have", not as a crash.
        """
        remote = self._remote_factory()

        remote_version = remote.content_version()
        local_version = self._cache.version()

        # Nothing to do when versions match and a copy exists. The is_empty
        # check covers a cache that was cleared but kept its version number.
        if not force and remote_version == local_version and not self._cache.is_empty():
            return False

        diseases, body_systems = remote.fetch_all_hydrated()
        stats = remote.stats()
        self._cache.replace_all(diseases, body_systems, remote_version, stats)
        return True

    def clear_cache(self) -> None:
        self._cache.clear()
        self._loaded = False