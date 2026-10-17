"""Shared plumbing for the Friends, sharing and Study Groups controllers.

Every request runs in the background (core/background.py) with the busy
state set before it starts, so a second click can't send it twice.
"""

from typing import Callable, Optional

from PySide6.QtCore import QObject

from app.core.background import call_in_background

NOT_INSTALLED = "isn't set up on Akeso's server yet"


def is_not_installed(message: str) -> bool:
    """The error says the feature's migration (040-042) hasn't been run."""
    return NOT_INSTALLED in (message or "")


def run(owner: QObject, call: Callable, on_done: Optional[Callable] = None,
        on_error: Optional[Callable[[str], None]] = None) -> None:
    call_in_background(call, on_done, on_error, owner=owner)
