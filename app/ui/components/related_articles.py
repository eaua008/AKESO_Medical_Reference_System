"""The "Related health articles" list on a disease, symptom or medicine page.

Like PeerDiscussionList, the page drops one in and it fills itself: the
shell sets RelatedArticlesList.loader once, and each new list asks it for
the articles linked to its entry. Hidden while there are none, so pages
without articles look exactly as before.
"""

from typing import Callable, Optional

from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QWidget

from app.ui.views.account.account_widgets import icon_label, label


class _ArticleRow(QFrame):
    clicked = Signal(str)

    def __init__(self, article) -> None:
        super().__init__()
        self.setObjectName("acRow")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._id = article.id
        row = QHBoxLayout(self)
        row.setContentsMargins(12, 9, 12, 9)
        row.setSpacing(10)
        row.addWidget(icon_label("external-link" if article.is_external else "file-text", 16),
                      0, Qt.AlignmentFlag.AlignTop)
        text = QVBoxLayout()
        text.setSpacing(2)
        text.addWidget(label(article.title, "acRowTitle"))
        text.addWidget(label(" · ".join(x for x in (article.kind_label, article.category,
                                                          article.meta_line()) if x),
                             "acSmall"))
        row.addLayout(text, 1)

    def mouseReleaseEvent(self, event) -> None:  # noqa: N802
        if (event.button() == Qt.MouseButton.LeftButton
                and self.rect().contains(event.position().toPoint())):
            self.clicked.emit(self._id)
        super().mouseReleaseEvent(event)


class RelatedArticlesList(QWidget):
    loader: Optional[Callable[["RelatedArticlesList"], None]] = None

    article_requested = Signal(str)

    def __init__(self, kind: str, entry_id: str) -> None:
        super().__init__()
        self.setObjectName("panel")
        self.kind = kind
        self.entry_id = entry_id
        self._column = QVBoxLayout(self)
        self._column.setContentsMargins(0, 12, 0, 0)
        self._column.setSpacing(6)
        head = QHBoxLayout()
        head.setSpacing(8)
        head.addWidget(icon_label("layers", 16))
        head.addWidget(label("RELATED HEALTH ARTICLES", "acFieldLabel", wrap=False))
        head.addStretch(1)
        self._column.addLayout(head)
        self._rows: list[QWidget] = []
        self.hide()
        if RelatedArticlesList.loader is not None:
            QTimer.singleShot(0, lambda: RelatedArticlesList.loader and
                              RelatedArticlesList.loader(self))

    def show_articles(self, articles: list) -> None:
        for row in self._rows:
            self._column.removeWidget(row)
            row.deleteLater()
        self._rows = []
        for article in articles[:5]:
            row = _ArticleRow(article)
            row.clicked.connect(self.article_requested.emit)
            self._column.addWidget(row)
            self._rows.append(row)
        self.setVisible(bool(articles))
