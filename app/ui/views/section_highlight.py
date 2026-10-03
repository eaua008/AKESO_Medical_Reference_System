"""A brief outline on the section you jumped to.

Clicking a rail link scrolls the page, but on a long monograph it isn't
always obvious which card you landed on. This outlines that card for a
couple of seconds, then removes it.

The outline is a widget-level stylesheet rather than a theme rule, so it
works on any section card whatever its object name, and it disappears
completely afterwards (setStyleSheet("") restores the app stylesheet).
"""

from typing import Optional

from PySide6.QtCore import QObject, QTimer
from PySide6.QtWidgets import QWidget

from app.core.theme import Theme


class SectionHighlighter(QObject):
    """Outlines one widget at a time."""

    DURATION_MS = 2200

    def __init__(self, parent: Optional[QObject] = None) -> None:
        super().__init__(parent)
        self._widget: Optional[QWidget] = None
        self._timer = QTimer(self)
        self._timer.setSingleShot(True)
        self._timer.timeout.connect(self.clear)

    def flash(self, widget: Optional[QWidget]) -> None:
        """Outline this widget now; any previous outline is removed first."""
        self.clear()
        if widget is None:
            return
        self._widget = widget
        name = widget.objectName()
        # Scope the rule to this object name so nested cards keep their look.
        selector = f"#{name}" if name else widget.metaObject().className()
        widget.setStyleSheet(
            f"{selector} {{ border: 2px solid {Theme.token('PRIMARY')}; }}"
        )
        self._timer.start(self.DURATION_MS)

    def clear(self) -> None:
        self._timer.stop()
        if self._widget is not None:
            # An empty stylesheet hands the widget back to the app stylesheet.
            self._widget.setStyleSheet("")
            self._widget = None