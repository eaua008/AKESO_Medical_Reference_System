"""Pictures in a study group chat (migration 045): the "send this picture?"
dialog with its patient-privacy confirmation, and the full-size viewer."""

from typing import Optional

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QCheckBox, QLabel, QLineEdit, QScrollArea, QWidget

from app.models.social import MESSAGE_MAX
from app.ui.views.account.account_dialogs import AccountDialog
from app.ui.views.account.account_widgets import field_block, label


class PictureConfirmDialog(AccountDialog):
    """Shows the picture exactly as it will be sent and won't send it until
    the sender confirms it has no real patient information. The database
    can't look inside a picture, so this confirmation is the safeguard."""

    submitted = Signal(str)               # caption

    def __init__(self, data: bytes, size_text: str, caption: str = "",
                 parent: Optional[QWidget] = None) -> None:
        super().__init__("Send this picture?",
                         "Everyone in the group will see it. Camera and location details are "
                         "removed, and large pictures are shrunk before they are sent.",
                         "image", parent, width=560)
        pixmap = QPixmap()
        pixmap.loadFromData(data)
        self.preview = QLabel()
        self.preview.setObjectName("panel")
        self.preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        if not pixmap.isNull():
            self.preview.setPixmap(pixmap.scaled(480, 300, Qt.AspectRatioMode.KeepAspectRatio,
                                                 Qt.TransformationMode.SmoothTransformation))
        self.body.addWidget(self.preview)
        self.body.addWidget(label(size_text, "acSmall"))

        self.caption = QLineEdit()
        self.caption.setObjectName("acInput")
        self.caption.setMaxLength(MESSAGE_MAX)
        self.caption.setPlaceholderText("Add a caption (optional)")
        self.caption.setText(caption)
        self.caption.returnPressed.connect(self._submit)
        self.body.addWidget(field_block("Caption", self.caption))

        self.confirm = QCheckBox("This picture does not show a real patient: no face, name, "
                                 "wristband, record number or screen with patient details.")
        self.confirm.setObjectName("ccCheck")
        self.confirm.toggled.connect(lambda on: self.go.setEnabled(on))
        self.body.addWidget(self.confirm)
        self.body.addWidget(label("Moderators can see reported pictures. Teaching images should "
                                  "be your own drawings, textbooks you may share, or "
                                  "properly de-identified examples.", "acSmall"))
        self.add_button("Cancel", on_click=self.reject)
        self.go = self.add_button("Send picture", "acPrimary", "check", self._submit, default=True)
        self.go.setEnabled(False)

    def _submit(self) -> None:
        if not self.confirm.isChecked():
            self.show_error("Tick the box to confirm there's no real patient in the picture.")
            return
        self.set_busy(True)
        self.submitted.emit(self.caption.text().strip())


class PictureViewDialog(AccountDialog):
    """A picture at full size (scaled to fit the window; scrolls if larger)."""

    def __init__(self, pixmap: QPixmap, title: str = "Picture",
                 parent: Optional[QWidget] = None) -> None:
        super().__init__(title, "", "image", parent, width=940)
        picture = QLabel()
        picture.setObjectName("panel")
        picture.setAlignment(Qt.AlignmentFlag.AlignCenter)
        if pixmap.width() > 880 or pixmap.height() > 640:
            pixmap = pixmap.scaled(880, 640, Qt.AspectRatioMode.KeepAspectRatio,
                                   Qt.TransformationMode.SmoothTransformation)
        picture.setPixmap(pixmap)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.Shape.NoFrame)
        scroll.setMinimumHeight(min(pixmap.height() + 20, 660))
        scroll.setWidget(picture)
        self.body.addWidget(scroll)
        self.add_button("Close", "acPrimary", "", self.accept, default=True)
