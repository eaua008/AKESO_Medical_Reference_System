"""The built-in reference browser: a web page inside a full-page sheet.

Opened from any "Open reference" link (see app/core/links.py). It looks and
slides like the inspect pages; the difference is that its body is a live web
page. A slim toolbar sits on top:

    [<] [>] [reload]  Title of the page            [copy] [Open in browser]
                      https://the.address/shown/here
    ====== loading bar ======

Privacy and safety:
  * An off-the-record profile: no cookies, history or cache are written to
    disk, so nothing a student browses here is kept on the computer.
  * Only http and https pages load. Other schemes are blocked.
  * Links that open a new window load here instead.
  * Downloads are not saved from here; the page can be opened in the real
    browser instead, where the student sees and controls the download.

QtWebEngine is heavy, so this module is imported only when the first link
is opened (DashboardShell._open_link).
"""

from PySide6.QtCore import QSize, Qt, QUrl, Signal
from PySide6.QtGui import QDesktopServices, QGuiApplication
from PySide6.QtWebEngineCore import (
    QWebEngineDownloadRequest, QWebEnginePage, QWebEngineProfile, QWebEngineSettings,
)
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import (
    QApplication, QFrame, QHBoxLayout, QProgressBar, QPushButton, QVBoxLayout, QWidget,
)

from app.core import lucide
from app.core.links import safe_url
from app.core.theme import Theme
from app.ui.views.account.account_widgets import Banner, button, label, refresh_icons, repolish


_PROFILE = None


def _shared_profile() -> QWebEngineProfile:
    """One off-the-record profile for the whole app run (no name = nothing
    written to disk). It belongs to the application, so it outlives every
    page that uses it: Qt warns if a profile goes before its pages."""
    global _PROFILE
    if _PROFILE is None:
        _PROFILE = QWebEngineProfile(QApplication.instance())
        settings = _PROFILE.settings()
        settings.setAttribute(QWebEngineSettings.WebAttribute.PluginsEnabled, False)
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessFileUrls,
                              False)
    return _PROFILE


class _Page(QWebEnginePage):
    """Keeps every navigation in this view, and only on the web."""

    blocked = Signal(str)

    def acceptNavigationRequest(self, url: QUrl, nav_type, is_main_frame: bool) -> bool:  # noqa: N802
        if url.scheme() in ("http", "https", "about", "data", "blob"):
            return True
        if is_main_frame:
            self.blocked.emit(url.toString())
        return False

    def javaScriptConsoleMessage(self, level, message, line, source) -> None:  # noqa: N802
        # The sites' own JavaScript logging (deprecation notices, blocked
        # trackers...). Qt prints it to the terminal by default; it is the
        # websites' noise, not Akeso's, so it is dropped.
        return

    def createWindow(self, _type) -> QWebEnginePage:  # noqa: N802
        # target="_blank" and window.open(): load in this same page.
        return self


class ReferenceBrowser(QWidget):
    """Toolbar + web view. The sheet around it provides the X / Esc close."""

    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("panel")
        self._url = ""

        self._profile = _shared_profile()
        self._profile.downloadRequested.connect(self._download)

        column = QVBoxLayout(self)
        column.setContentsMargins(0, 0, 0, 0)
        column.setSpacing(0)
        column.addWidget(self._build_toolbar())

        self._progress = QProgressBar()
        self._progress.setObjectName("wbProgress")
        self._progress.setFixedHeight(3)
        self._progress.setTextVisible(False)
        self._progress.setRange(0, 100)
        self._progress.hide()
        column.addWidget(self._progress)

        self.banner = Banner()
        self.banner.action.connect(self.open_externally)
        holder = QWidget()
        holder.setObjectName("panel")
        banner_row = QVBoxLayout(holder)
        banner_row.setContentsMargins(16, 8, 16, 0)
        banner_row.addWidget(self.banner)
        column.addWidget(holder)
        self._banner_holder = holder
        holder.hide()

        self.view = QWebEngineView()
        self._page = _Page(self._profile, self.view)
        self.view.setPage(self._page)
        self._page.blocked.connect(
            lambda url: self._notice(f"That link ({url.split(':')[0]}:) can’t open here.",
                                     "warn", ""))
        self.view.titleChanged.connect(self._title_changed)
        self.view.urlChanged.connect(self._url_changed)
        self.view.loadStarted.connect(self._load_started)
        self.view.loadProgress.connect(self._progress.setValue)
        self.view.loadFinished.connect(self._load_finished)
        column.addWidget(self.view, 1)
        self.refresh_theme()

    # ------------------------------------------------------------ toolbar

    def _icon_button(self, icon: str, tip: str, slot) -> QPushButton:
        widget = QPushButton()
        widget.setObjectName("wbIconButton")
        widget.setFixedSize(32, 32)
        widget.setCursor(Qt.CursorShape.PointingHandCursor)
        widget.setToolTip(tip)
        widget.setAccessibleName(tip)
        widget.setProperty("wbIcon", icon)
        widget.clicked.connect(lambda _c=False: slot())
        return widget

    def _build_toolbar(self) -> QFrame:
        bar = QFrame()
        bar.setObjectName("wbToolbar")
        row = QHBoxLayout(bar)
        # Left margin clears the sheet's X tab, which overlaps this corner.
        row.setContentsMargins(16, 10, 16, 10)
        row.setSpacing(6)
        self._back = self._icon_button("chevron-left", "Back", lambda: self.view.back())
        self._forward = self._icon_button("chevron-right", "Forward",
                                          lambda: self.view.forward())
        self._reload = self._icon_button("refresh-cw", "Reload", self._reload_or_stop)
        for widget in (self._back, self._forward, self._reload):
            row.addWidget(widget)
        row.addSpacing(6)

        text = QVBoxLayout()
        text.setSpacing(0)
        self._title = label("", "acRowTitle", wrap=False)
        self._title.setMinimumWidth(60)
        self._address = label("", "acSmall", wrap=False)
        self._address.setMinimumWidth(60)
        self._address.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        text.addWidget(self._title)
        text.addWidget(self._address)
        row.addLayout(text, 1)

        self._lock = label("", "acSmall", wrap=False)
        row.addWidget(self._lock)
        row.addWidget(self._icon_button("copy", "Copy link", self._copy))
        row.addWidget(button("Open in browser", "acGhost", "external-link",
                             self.open_externally))
        return bar

    # ---------------------------------------------------------------- api

    def load(self, url: str, title: str = "") -> None:
        url = safe_url(url)
        if not url:
            return
        self._url = url
        self._banner_holder.hide()
        self._title.setText(title or "Loading…")
        self._address.setText(url)
        self.view.setUrl(QUrl(url))

    def stop(self) -> None:
        """The sheet closed: stop loading and silence any audio or video."""
        self.view.stop()
        self.view.setUrl(QUrl("about:blank"))

    def open_externally(self) -> None:
        if self._url:
            QDesktopServices.openUrl(QUrl(self._url))

    # ------------------------------------------------------------ private

    def _copy(self) -> None:
        if self._url:
            QGuiApplication.clipboard().setText(self._url)
            self._notice("Link copied.", "good", "")

    def _reload_or_stop(self) -> None:
        if self._progress.isVisible():
            self.view.stop()
        else:
            self.view.reload()

    def _title_changed(self, title: str) -> None:
        # Until the page sets a real <title>, Qt reports the address itself;
        # keep the reference's name showing instead of that.
        bare = self._url.split("://", 1)[-1]
        if title and not title.startswith(("http://", "https://")) and title != bare:
            self._title.setText(title)

    def _url_changed(self, url: QUrl) -> None:
        text = url.toString()
        if text and text != "about:blank":
            self._url = text
            self._address.setText(text)
            secure = url.scheme() == "https"
            self._lock.setText("Secure" if secure else "Not secure")
            self._lock.setToolTip("Encrypted connection (https)" if secure else
                                  "This page is not encrypted (http)")
        self._back.setEnabled(self.view.history().canGoBack())
        self._forward.setEnabled(self.view.history().canGoForward())

    def _load_started(self) -> None:
        self._progress.setValue(0)
        self._progress.show()
        self._reload.setProperty("wbIcon", "x")
        self._reload.setToolTip("Stop")
        self._paint_icons()

    def _load_finished(self, ok: bool) -> None:
        self._progress.hide()
        self._reload.setProperty("wbIcon", "refresh-cw")
        self._reload.setToolTip("Reload")
        self._paint_icons()
        self._back.setEnabled(self.view.history().canGoBack())
        self._forward.setEnabled(self.view.history().canGoForward())
        if not ok and self.view.url().toString() not in ("", "about:blank"):
            self._notice("This page didn’t load. You may be offline, or the site "
                         "doesn’t allow being shown inside other apps.", "warn",
                         "Open in browser")

    def _download(self, request: QWebEngineDownloadRequest) -> None:
        request.cancel()
        self._url = request.url().toString() or self._url
        self._notice("Files can’t be downloaded here. Open the link in your browser to "
                     "download it.", "info", "Open in browser")

    def _notice(self, text: str, tone: str, action: str) -> None:
        self.banner.show_message(text, tone, action)
        self._banner_holder.show()

    def _paint_icons(self) -> None:
        colour = Theme.token("TEXT_MUTED")
        for widget in self.findChildren(QPushButton):
            name = widget.property("wbIcon")
            if name:
                widget.setIcon(lucide.icon(name, 16, colour))
                widget.setIconSize(QSize(16, 16))

    def refresh_theme(self) -> None:
        bg = Theme.token("SURFACE")
        border = Theme.token("BORDER")
        self.setStyleSheet(f"""
            #wbToolbar {{ background-color: {bg}; border-bottom: 1px solid {border}; }}
            #wbIconButton {{ background: transparent; border: none; border-radius: 7px; }}
            #wbIconButton:hover {{ background-color: {Theme.token('SURFACE_ALT')}; }}
            #wbIconButton:disabled {{ background: transparent; }}
            #wbProgress {{ background: transparent; border: none; }}
            #wbProgress::chunk {{ background-color: {Theme.token('PRIMARY')}; }}
        """)
        self._paint_icons()
        refresh_icons(self)
        repolish(self)
