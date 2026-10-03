"""Clinical Exchange page: the feed or the moderation queue, with one post
sliding in over them in the shell's sheet (stacked if there is none)."""

from PySide6.QtWidgets import QStackedWidget, QVBoxLayout, QWidget

from app.ui.views.exchange.feed_view import FeedView
from app.ui.views.exchange.mod_queue_view import ModQueueView
from app.ui.views.exchange.post_view import PostView


class ExchangePage(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("panel")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self.stack = QStackedWidget()
        self.feed = FeedView()
        self.post = PostView()
        self.queue = ModQueueView()
        for view in (self.feed, self.post, self.queue):
            self.stack.addWidget(view)
        layout.addWidget(self.stack)
        self._sheet = None

    def attach_sheet(self, sheet) -> None:
        self._sheet = sheet
        self.stack.removeWidget(self.post)
        sheet.adopt(self.post, self.post.back_requested)

    def current_view(self) -> QWidget:
        """The screen the user is looking at (for banners)."""
        if self._sheet is not None and self._sheet.is_open:
            return self.post
        return self.stack.currentWidget()

    def _close_sheet(self) -> None:
        if self._sheet is not None:
            self._sheet.close_sheet()

    def show_feed(self) -> None:
        self._close_sheet()
        self.stack.setCurrentWidget(self.feed)

    def show_post(self) -> None:
        if self._sheet is not None:
            self._sheet.open_sheet()
        else:
            self.stack.setCurrentWidget(self.post)

    def show_queue(self) -> None:
        self._close_sheet()
        self.stack.setCurrentWidget(self.queue)

    def refresh_theme(self) -> None:
        for view in (self.feed, self.post, self.queue):
            view.refresh_theme()
