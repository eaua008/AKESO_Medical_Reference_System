from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class DashboardView(QWidget):
    """Placeholder shown after a successful login, signup, or guest entry.

    Intentionally blank — this is where the real application screens go
    once the auth flow is solid.
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        layout = QVBoxLayout(self)
        label = QLabel("Dashboard — coming soon")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setObjectName("cardSubtitle")
        layout.addWidget(label)