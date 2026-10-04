"""The "Recent peer case discussions" list on a disease, symptom or medicine page.

Display only. The page puts one of these where its discussion list goes;
the shell asks Clinical Exchange for posts tagged with that entry and hands
them to show_posts(). Clicking a post emits post_requested(post_id).

    loading   "Looking for discussions..."
    posts     one row per post: kind, title, author, replies, last activity
    empty     "No peer discussions are linked to this entry yet."
    message   signed out, offline, or the board could not be read
"""

from datetime import datetime

from typing import Callable, Optional

from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QWidget

from app.ui.views.account.account_widgets import icon_label, label

SHOWN = 5


def _ago(value) -> str:
    if not isinstance(value, datetime):
        return ""
    now = datetime.now(value.tzinfo) if value.tzinfo else datetime.now()
    seconds = max(0, int((now - value).total_seconds()))
    if seconds < 60:
        return "just now"
    if seconds < 3600:
        return f"{seconds // 60}m ago"
    if seconds < 86400:
        return f"{seconds // 3600}h ago"
    if seconds < 7 * 86400:
        return f"{seconds // 86400}d ago"
    return value.astimezone().strftime("%b %d, %Y").replace(" 0", " ")


class _PostRow(QFrame):
    clicked = Signal(str)

    def __init__(self, post) -> None:
        super().__init__()
        self.setObjectName("acRow")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._id = post.id
        row = QHBoxLayout(self)
        row.setContentsMargins(12, 9, 12, 9)
        row.setSpacing(10)
        row.addWidget(icon_label("message-circle", 16), 0, Qt.AlignmentFlag.AlignTop)

        text = QVBoxLayout()
        text.setSpacing(2)
        title = label(post.title or "Untitled post", "acRowTitle")
        text.addWidget(title)
        author = post.author
        who = "Anonymous" if author is None or author.anonymous else author.name
        parts = [post.kind.title(), who,
                 f"{post.reply_count} repl{'y' if post.reply_count == 1 else 'ies'}"]
        if post.age_range or post.sex:
            parts.insert(1, " ".join(x for x in (post.age_range, post.sex) if x))
        if post.revealed:
            parts.append("answer revealed")
        text.addWidget(label(" · ".join(parts), "acSmall"))
        row.addLayout(text, 1)

        when = _ago(post.last_activity_at or post.created_at)
        if when:
            row.addWidget(label(when, "acSmall", wrap=False), 0, Qt.AlignmentFlag.AlignTop)

    def mouseReleaseEvent(self, event) -> None:  # noqa: N802
        if (event.button() == Qt.MouseButton.LeftButton
                and self.rect().contains(event.position().toPoint())):
            self.clicked.emit(self._id)
        super().mouseReleaseEvent(event)


class PeerDiscussionList(QWidget):
    """Pages rebuild this list every time they draw an entry, so the list
    asks for its own posts: the shell sets PeerDiscussionList.loader once,
    and every new list calls it right after it is made."""

    loader: Optional[Callable[["PeerDiscussionList"], None]] = None

    post_requested = Signal(str)          # post id
    count_changed = Signal(int)           # for the page's "N cases" chip
    see_all_requested = Signal()          # the board, filtered to this entry

    def __init__(self, kind: str, entry_id: str, empty_name: str = "") -> None:
        super().__init__()
        self.setObjectName("panel")
        self.kind = kind                  # "disease", "symptom" or "medicine"
        self.entry_id = entry_id
        self._column = QVBoxLayout(self)
        self._column.setContentsMargins(0, 4, 0, 0)
        self._column.setSpacing(6)
        self._message = label("", "acMuted")
        self._message.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._column.addWidget(self._message)
        self._more = label("", "acSmall")
        self._more.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._more.hide()
        self._column.addWidget(self._more)
        self._column.addStretch(1)       # rows keep their size; spare room goes below
        self._rows: list[QWidget] = []
        self.show_message("No peer discussions are linked to this entry yet.")
        if PeerDiscussionList.loader is not None:
            # After the page has finished building, not in the middle of it.
            QTimer.singleShot(0, lambda: PeerDiscussionList.loader and
                              PeerDiscussionList.loader(self))

    def _clear(self) -> None:
        for row in self._rows:
            self._column.removeWidget(row)
            row.deleteLater()
        self._rows = []
        self._more.hide()

    def show_loading(self) -> None:
        self.show_message("Looking for discussions…")

    def show_message(self, text: str) -> None:
        self._clear()
        self._message.setText(text)
        self._message.show()

    def show_posts(self, posts: list) -> None:
        self._clear()
        self.count_changed.emit(len(posts))
        if not posts:
            self.show_message("No peer discussions are linked to this entry yet. "
                              "Present a case to start one.")
            return
        self._message.hide()
        for index, post in enumerate(posts[:SHOWN]):
            row = _PostRow(post)
            row.clicked.connect(self.post_requested.emit)
            self._column.insertWidget(index, row)
            self._rows.append(row)
        if len(posts) > SHOWN:
            self._more.setText(f"Showing the {SHOWN} most recent of {len(posts)}. "
                               "See the rest in Clinical Exchange (filter by this tag).")
            self._more.show()
