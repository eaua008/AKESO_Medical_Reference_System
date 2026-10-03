"""Moderation queue (educators and admins): reported posts and replies."""

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QFrame, QHBoxLayout, QScrollArea, QVBoxLayout, QWidget

from app.models.exchange import REPORT_REASONS, STATUS_LABELS, ModItem, time_ago
from app.ui.views.account.account_widgets import Banner, button, label, pill, refresh_icons
from app.ui.views.exchange.exchange_widgets import AuthorLine, clear_layout, flow

REASON_TEXT = dict(REPORT_REASONS)


class ModQueueView(QWidget):
    back_requested = Signal()
    refresh_requested = Signal()
    item_action = Signal(str, object)        # open | hide | lock | remove | dismiss, ModItem

    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("panel")
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        page = QWidget()
        page.setObjectName("panel")
        self._page = QVBoxLayout(page)
        self._page.setContentsMargins(30, 18, 30, 30)
        self._page.setSpacing(12)
        top = QHBoxLayout()
        top.addWidget(button("Back to the feed", "acLink", "arrow-left", self.back_requested.emit))
        top.addStretch(1)
        top.addWidget(button("Refresh", "acLink", on_click=self.refresh_requested.emit))
        self._page.addLayout(top)
        self._page.addWidget(label("Moderation queue", "acTitle"))
        self._page.addWidget(label("Reported posts and replies, most reported first. You see the "
                                   "real author even on anonymous posts; keep it confidential. "
                                   "Every action is logged.", "acSubtitle"))
        self.banner = Banner()
        self.banner.action.connect(self.banner.hide)
        self._page.addWidget(self.banner)
        self._list = QVBoxLayout()
        self._list.setSpacing(10)
        self._page.addLayout(self._list)
        self._page.addStretch(1)
        scroll.setWidget(page)
        outer.addWidget(scroll)

    def show_items(self, items: list[ModItem]) -> None:
        clear_layout(self._list)
        if not items:
            self._list.addWidget(label("Nothing to review. The queue is empty.", "acMuted"))
        for item in items:
            self._list.addWidget(self._row(item))

    def show_error(self, message: str) -> None:
        clear_layout(self._list)
        self._list.addWidget(label(message, "acError"))

    def _row(self, item: ModItem) -> QFrame:
        frame = QFrame()
        frame.setObjectName("acCard")
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(16, 14, 16, 14)
        layout.setSpacing(8)
        top = QHBoxLayout()
        top.addWidget(pill("Post" if item.target_kind == "post" else "Reply", "acPill"))
        top.addWidget(pill(f"{item.reports} report{'s' if item.reports != 1 else ''}",
                           "acPillDanger"))
        if item.status != "open":
            top.addWidget(pill(STATUS_LABELS.get(item.status, item.status), "acPillWarn"))
        top.addStretch(1)
        top.addWidget(label(f"first reported {time_ago(item.first_reported)}", "acSmall",
                            wrap=False))
        layout.addLayout(top)
        layout.addWidget(label(item.title if item.target_kind == "post"
                               else f"Reply on “{item.title}”", "exPostTitle"))
        if item.excerpt:
            layout.addWidget(label(item.excerpt, "acMuted"))
        layout.addWidget(AuthorLine(item.author))
        layout.addWidget(flow([pill(REASON_TEXT.get(r, r), "acPillWarn") for r in item.reasons]))
        for note in item.notes[:3]:
            layout.addWidget(label(f"“{note}”", "acSmall"))
        actions = QHBoxLayout()
        actions.addWidget(button("Open", "acGhost", on_click=lambda: self.item_action.emit("open", item)))
        actions.addWidget(button("Hide", "acGhost", on_click=lambda: self.item_action.emit("hide", item)))
        if item.target_kind == "post":
            actions.addWidget(button("Lock", "acGhost", on_click=lambda: self.item_action.emit("lock", item)))
        actions.addWidget(button("Remove", "acDanger", on_click=lambda: self.item_action.emit("remove", item)))
        actions.addStretch(1)
        actions.addWidget(button("Dismiss reports", "acLink",
                                 on_click=lambda: self.item_action.emit("dismiss", item)))
        layout.addLayout(actions)
        return frame

    def refresh_theme(self) -> None:
        refresh_icons(self)
