"""Where a clicked reference link goes.

Every screen that shows a link calls open_link(url, title) instead of
handing the link to the operating system. The dashboard shell listens and
opens it in the built-in reference browser (a full-page sheet, like the
inspect pages). If nothing is listening (a screen tested on its own, or the
login screen), the link opens in the computer's default browser as before.

Only plain web links (http, https) are ever opened. Anything else that
might come from the database, such as javascript: or file:, is dropped.
"""

from urllib.parse import urlparse

from PySide6.QtCore import QObject, QUrl, Signal
from PySide6.QtGui import QDesktopServices


def safe_url(url: str) -> str:
    url = (url or "").strip()
    parsed = urlparse(url)
    return url if parsed.scheme in ("http", "https") and parsed.netloc else ""


class LinkRouter(QObject):
    open_requested = Signal(str, str)      # url, title

    def __init__(self) -> None:
        super().__init__()
        self._listening = False

    def listen(self, handler) -> None:
        self.open_requested.connect(handler)
        self._listening = True

    def stop_listening(self, handler) -> None:
        try:
            self.open_requested.disconnect(handler)
        except (RuntimeError, TypeError):
            pass
        self._listening = False

    def open(self, url: str, title: str = "") -> bool:
        url = safe_url(url)
        if not url:
            return False
        if self._listening:
            self.open_requested.emit(url, title)
        else:
            QDesktopServices.openUrl(QUrl(url))
        return True


links = LinkRouter()


def open_link(url: str, title: str = "") -> bool:
    """Open a reference link (in the built-in browser when the app is running)."""
    return links.open(url, title)
