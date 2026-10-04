"""Hide hover pop-ups (tooltips) that only repeat what is already on screen.

Many buttons carry a tooltip with their own label ("Notifications" on the
Notifications button). Those boxes add nothing and get in the way, so one
app-wide filter drops a tooltip whenever it says the same as the text the
widget is showing. Tooltips that add something still appear:

  * icon-only buttons (the shrunk sidebar, the header icons),
  * shortened text ("Acute Coronary Syn…" shows the full name),
  * explanations ("Hide it to see what's behind (H)").

Installed once in main.py.
"""

import re

from PySide6.QtCore import QEvent, QObject
from PySide6.QtWidgets import QAbstractButton, QApplication, QLabel, QWidget

_TRIM = " \t\r\n›→↗…:·"


def _normal(text: str) -> str:
    text = re.sub(r"<[^>]+>", " ", text or "")        # rich-text labels
    text = text.replace("&&", "&")
    text = re.sub(r"\s+", " ", text).strip(_TRIM)
    return text.lower()


def shown_text(widget: QWidget) -> str:
    """The text a widget is actually displaying (elided text stays elided)."""
    if isinstance(widget, QAbstractButton):
        return widget.text()
    if isinstance(widget, QLabel):
        return QLabel.text(widget)                       # not ElidedLabel's full text
    return ""


def is_redundant(widget: QWidget) -> bool:
    tip = _normal(widget.toolTip())
    shown = _normal(shown_text(widget))
    return bool(tip) and tip == shown


class RedundantTooltipFilter(QObject):
    def eventFilter(self, watched: QObject, event: QEvent) -> bool:  # noqa: N802
        if event.type() == QEvent.Type.ToolTip and isinstance(watched, QWidget):
            if is_redundant(watched):
                return True                                # swallow: no pop-up
        return False


_filter = None


def install() -> None:
    global _filter
    app = QApplication.instance()
    if app is not None and _filter is None:
        _filter = RedundantTooltipFilter(app)
        app.installEventFilter(_filter)
