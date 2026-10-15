"""Serves the 3D body (assets/anatomy/) to the built-in browser engine.

Browsers refuse to load scripts and models straight from disk (file://)
for security, so the Body System Explorer page is served from a private
address instead: akeso://anatomy/anatomy.html. Only files inside
assets/anatomy/ can be reached this way, plus Qt's own qwebchannel.js
(the bridge between the page and Python).

register_scheme() must run before the QApplication is created (main.py);
install(profile) is called when the explorer is first opened.
"""

from PySide6.QtCore import QBuffer, QByteArray, QFile, QIODevice
from PySide6.QtWebEngineCore import (
    QWebEngineProfile, QWebEngineUrlRequestJob, QWebEngineUrlScheme, QWebEngineUrlSchemeHandler,
)

from app.core.assets import ASSETS_DIR

SCHEME = b"akeso"
ANATOMY_DIR = ASSETS_DIR / "anatomy"
TYPES = {
    ".html": b"text/html", ".js": b"text/javascript", ".json": b"application/json",
    ".glb": b"model/gltf-binary", ".css": b"text/css", ".png": b"image/png",
}


def register_scheme() -> None:
    """Tell the browser engine about akeso:// (before QApplication exists)."""
    scheme = QWebEngineUrlScheme(SCHEME)
    scheme.setSyntax(QWebEngineUrlScheme.Syntax.Host)
    scheme.setFlags(QWebEngineUrlScheme.Flag.SecureScheme
                    | QWebEngineUrlScheme.Flag.LocalScheme
                    | QWebEngineUrlScheme.Flag.LocalAccessAllowed
                    | QWebEngineUrlScheme.Flag.CorsEnabled
                    | QWebEngineUrlScheme.Flag.FetchApiAllowed)   # the page fetch()es the models
    QWebEngineUrlScheme.registerScheme(scheme)


class AnatomySchemeHandler(QWebEngineUrlSchemeHandler):
    def requestStarted(self, job: QWebEngineUrlRequestJob) -> None:  # noqa: N802
        url = job.requestUrl()
        if url.host() != "anatomy":
            job.fail(QWebEngineUrlRequestJob.Error.UrlNotFound)
            return
        name = url.path().lstrip("/") or "anatomy.html"
        data = self._read(name)
        if data is None:
            job.fail(QWebEngineUrlRequestJob.Error.UrlNotFound)
            return
        buffer = QBuffer(job)                    # freed with the request
        buffer.setData(QByteArray(data))
        buffer.open(QIODevice.OpenModeFlag.ReadOnly)
        suffix = "." + name.rsplit(".", 1)[-1].lower() if "." in name else ""
        job.reply(TYPES.get(suffix, b"application/octet-stream"), buffer)

    @staticmethod
    def _read(name: str):
        if name == "qwebchannel.js":             # ships inside Qt itself
            file = QFile(":/qtwebchannel/qwebchannel.js")
            if file.open(QIODevice.OpenModeFlag.ReadOnly):
                return bytes(file.readAll())
            return None
        path = (ANATOMY_DIR / name).resolve()
        # Nothing outside assets/anatomy/, whatever the page asks for.
        if ANATOMY_DIR.resolve() not in path.parents or not path.is_file():
            return None
        try:
            return path.read_bytes()
        except OSError:
            return None


_handler = None


def install(profile: QWebEngineProfile) -> None:
    global _handler
    if _handler is None:
        _handler = AnatomySchemeHandler(profile)
    if profile.urlSchemeHandler(SCHEME) is None:
        profile.installUrlSchemeHandler(SCHEME, _handler)


def models_present() -> bool:
    return all((ANATOMY_DIR / n).is_file() for n in
               ("anatomy.html", "anatomy.bundle.js", "parts.json", "regions.json", "skin.glb"))
