"""Account > Profile: photo, name, handle, academic details, visibility."""

from typing import Optional

from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QComboBox, QFileDialog, QHBoxLayout, QLabel, QLineEdit, QPlainTextEdit, QVBoxLayout,
    QWidget,
)

from app.models.account import (
    INTEREST_OPTIONS, MAX_INTERESTS, PROGRAMS, YEAR_LEVELS, Profile, friendly_time,
)
from app.ui.components.fluid import ResponsiveGrid
from app.ui.views.account.account_widgets import (
    Card, ChipGroup, SwitchRow, button, field_block, label, pill, set_text,
)

HANDLE_CHECK_DELAY_MS = 450


class ProfileTab(QWidget):
    save_requested = Signal(dict)
    photo_chosen = Signal(str)
    photo_remove_requested = Signal()
    handle_check_requested = Signal(str)
    verify_school_requested = Signal()

    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("panel")
        self._profile: Optional[Profile] = None
        self._loading = False

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(16)

        self.grid = ResponsiveGrid(400, max_columns=2, spacing=16, steps=(2, 1))
        self.grid.set_cards([self._build_identity(), self._build_academic(),
                             self._build_badge(), self._build_visibility()])
        root.addWidget(self.grid)
        root.addWidget(self._build_save_bar())

        self._handle_timer = QTimer(self)
        self._handle_timer.setSingleShot(True)
        self._handle_timer.setInterval(HANDLE_CHECK_DELAY_MS)
        self._handle_timer.timeout.connect(self._check_handle)

    # -------------------------------------------------------------- cards

    def _build_identity(self) -> Card:
        card = Card("Photo and name", "How you appear in Akeso.", "user")
        photo_row = QHBoxLayout()
        photo_row.setSpacing(16)
        self.photo = QLabel()
        self.photo.setObjectName("panel")
        self.photo.setFixedSize(84, 84)
        photo_row.addWidget(self.photo)
        buttons = QVBoxLayout()
        buttons.setSpacing(6)
        self._change_photo = button("Change photo", "acGhost", "camera", self._pick_photo)
        self._remove_photo = button("Remove photo", "acLink",
                                    on_click=self.photo_remove_requested.emit)
        buttons.addWidget(self._change_photo, 0, Qt.AlignmentFlag.AlignLeft)
        buttons.addWidget(self._remove_photo, 0, Qt.AlignmentFlag.AlignLeft)
        buttons.addWidget(label("PNG or JPG. Cropped to a square; location data is removed.",
                                "acSmall"))
        photo_row.addLayout(buttons, 1)
        card.body.addLayout(photo_row)

        self.name = QLineEdit()
        self.name.setObjectName("acInput")
        self.name.setMaxLength(60)
        self.name.textEdited.connect(self._changed)
        card.body.addWidget(field_block("Display name", self.name))

        self.handle = QLineEdit()
        self.handle.setObjectName("acInput")
        self.handle.setMaxLength(21)
        self.handle.setPlaceholderText("@yourname")
        self.handle.textEdited.connect(self._handle_edited)
        self._handle_status = label("", "acSmall")
        self._handle_status.hide()
        card.body.addWidget(field_block("Handle", self.handle,
                                        "3–20 lowercase letters, numbers or underscores."))
        card.body.addWidget(self._handle_status)

        self.bio = QPlainTextEdit()
        self.bio.setObjectName("acInput")
        self.bio.setPlaceholderText("A line about you, e.g. “2nd-year nursing student "
                                    "who loves cardio”")
        self.bio.setFixedHeight(76)
        self.bio.textChanged.connect(self._bio_changed)
        self._bio_count = label("0 / 280", "acSmall", wrap=False)
        card.body.addWidget(field_block("Bio", self.bio))
        card.body.addWidget(self._bio_count, 0, Qt.AlignmentFlag.AlignRight)
        return card

    def _build_academic(self) -> Card:
        card = Card("Academic profile", "Your program and interests.", "graduation-cap")
        self.program = QComboBox()
        self.program.setObjectName("acInput")
        self.program.addItem("Not set", None)
        for key, text in PROGRAMS:
            self.program.addItem(text, key)
        self.program.currentIndexChanged.connect(self._changed)
        card.body.addWidget(field_block("Program", self.program))

        self.school = QLineEdit()
        self.school.setObjectName("acInput")
        self.school.setMaxLength(120)
        self.school.setPlaceholderText("e.g. University of Mindanao")
        self.school.textEdited.connect(self._changed)
        card.body.addWidget(field_block("School", self.school))

        self.year = QComboBox()
        self.year.setObjectName("acInput")
        self.year.addItem("Not set", None)
        for key, text in YEAR_LEVELS:
            self.year.addItem(text, key)
        self.year.currentIndexChanged.connect(self._changed)
        card.body.addWidget(field_block("Year level", self.year))

        self.interests = ChipGroup(MAX_INTERESTS)
        self.interests.changed.connect(self._changed)
        card.body.addWidget(field_block("Interest areas", self.interests,
                                        f"Pick up to {MAX_INTERESTS}."))
        return card

    def _build_badge(self) -> Card:
        card = Card("Verified student", "Prove you study at a school by confirming a code "
                    "sent to your school email.", "badge-check")
        self._badge_state = QHBoxLayout()
        self._badge_pill = pill("Not verified", "acPill")
        self._badge_state.addWidget(self._badge_pill)
        self._badge_state.addStretch(1)
        card.body.addLayout(self._badge_state)
        self._badge_note = label("", "acSmall")
        card.body.addWidget(self._badge_note)
        self._verify_button = button("Verify school email", "acGhost", "mail",
                                     self.verify_school_requested.emit)
        card.body.addWidget(self._verify_button, 0, Qt.AlignmentFlag.AlignLeft)
        card.body.addWidget(label("Only the school's domain (like school.edu.ph) is kept, "
                                  "never the address itself.", "acSmall"))
        card.body.addStretch(1)
        return card

    def _build_visibility(self) -> Card:
        card = Card("Visibility", "What other students can see once Clinical Exchange "
                    "shows profiles.", "eye")
        self.public = SwitchRow("Public profile", "Others can find you by your @handle.")
        self.show_school = SwitchRow("Show my school", "Hidden when off, even on a public "
                                     "profile.")
        self.show_program = SwitchRow("Show my program and year", "Hidden when off.")
        for row in (self.public, self.show_school, self.show_program):
            row.toggled.connect(self._changed)
            card.body.addWidget(row)
        self._preview = label("", "acSmall")
        card.body.addWidget(self._preview)
        card.body.addStretch(1)
        return card

    def _build_save_bar(self) -> QWidget:
        bar = QWidget()
        bar.setObjectName("panel")
        row = QHBoxLayout(bar)
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(10)
        self._status = label("", "acSmall")
        row.addWidget(self._status, 1)
        self._discard = button("Discard changes", "acGhost", on_click=self._discard_changes)
        self._save = button("Save profile", "acPrimary", "check", self._emit_save)
        row.addWidget(self._discard)
        row.addWidget(self._save)
        self._set_dirty(False)
        return bar

    def watch(self, viewport: QWidget) -> None:
        self.grid.watch(viewport)

    # --------------------------------------------------------------- data

    def show_profile(self, profile: Profile, photo: QPixmap) -> None:
        self._profile = profile
        self._loading = True
        self.name.setText(profile.display_name)
        self.handle.setText(f"@{profile.handle}" if profile.handle else "")
        self.bio.setPlainText(profile.bio)
        self.program.setCurrentIndex(max(0, self.program.findData(profile.program)))
        self.school.setText(profile.school or "")
        self.year.setCurrentIndex(max(0, self.year.findData(profile.year_level)))
        self.interests.set_options(INTEREST_OPTIONS, profile.interests)
        self.public.set_checked(profile.is_public)
        self.show_school.set_checked(profile.show_school)
        self.show_program.set_checked(profile.show_program)
        self._loading = False
        self.set_photo(photo, bool(profile.avatar_path))
        self._show_badge(profile)
        self._handle_status.hide()
        self._bio_count.setText(f"{len(profile.bio)} / 280")
        self._update_preview()
        self._set_dirty(False)

    def set_photo(self, photo: QPixmap, has_photo: bool) -> None:
        self.photo.setPixmap(photo)
        self._remove_photo.setVisible(has_photo)

    def _show_badge(self, profile: Profile) -> None:
        if profile.is_verified_student:
            self._badge_pill.setText(f"Verified · {profile.school_email_domain}")
            self._badge_pill.setObjectName("acPillGood")
            self._badge_note.setText(
                f"Verified {friendly_time(profile.school_email_verified_at, with_time=False)}.")
            set_text(self._verify_button, "Verify a different school email")
        else:
            self._badge_pill.setText("Not verified")
            self._badge_pill.setObjectName("acPill")
            self._badge_note.setText("Use an address ending in .edu.ph or .edu.")
            set_text(self._verify_button, "Verify school email")
        self._badge_pill.style().unpolish(self._badge_pill)
        self._badge_pill.style().polish(self._badge_pill)

    def changes(self) -> dict:
        return {
            "display_name": self.name.text(),
            "handle": self.handle.text().strip().lstrip("@").lower() or None,
            "bio": self.bio.toPlainText(),
            "program": self.program.currentData(),
            "school": self.school.text(),
            "year_level": self.year.currentData(),
            "interests": self.interests.selected(),
            "is_public": self.public.switch.isChecked(),
            "show_school": self.show_school.switch.isChecked(),
            "show_program": self.show_program.switch.isChecked(),
        }

    def set_busy(self, busy: bool, message: str = "") -> None:
        self._save.setEnabled(not busy and self._dirty)
        self._change_photo.setEnabled(not busy)
        self._status.setObjectName("acSmall")
        self._status.setText(message)
        self._status.style().polish(self._status)

    def show_error(self, message: str) -> None:
        self._status.setObjectName("acError")
        self._status.setText(message)
        self._status.style().unpolish(self._status)
        self._status.style().polish(self._status)
        self._save.setEnabled(self._dirty)
        self._change_photo.setEnabled(True)

    def show_saved(self, message: str = "Saved.") -> None:
        self._status.setObjectName("acOk")
        self._status.setText(message)
        self._status.style().unpolish(self._status)
        self._status.style().polish(self._status)

    def show_handle_status(self, handle: str, available: bool) -> None:
        current = self.handle.text().strip().lstrip("@").lower()
        if handle != current:
            return      # an older answer; the user has typed more since
        mine = self._profile is not None and (self._profile.handle or "") == handle
        if mine:
            self._handle_status.hide()
            return
        self._handle_status.setObjectName("acOk" if available else "acError")
        self._handle_status.setText(f"@{handle} is available." if available
                                    else f"@{handle} is taken or not allowed.")
        self._handle_status.show()
        self._handle_status.style().unpolish(self._handle_status)
        self._handle_status.style().polish(self._handle_status)

    # ------------------------------------------------------------- events

    def _pick_photo(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self, "Choose a profile photo", "", "Images (*.png *.jpg *.jpeg)")
        if path:
            self.photo_chosen.emit(path)

    def _handle_edited(self, _text: str) -> None:
        self._changed()
        self._handle_status.hide()
        self._handle_timer.start()

    def _check_handle(self) -> None:
        handle = self.handle.text().strip().lstrip("@").lower()
        if handle and (self._profile is None or handle != (self._profile.handle or "")):
            self.handle_check_requested.emit(handle)

    def _bio_changed(self) -> None:
        text = self.bio.toPlainText()
        if len(text) > 280:
            cursor = self.bio.textCursor()
            self.bio.setPlainText(text[:280])
            cursor.setPosition(280)
            self.bio.setTextCursor(cursor)
            text = text[:280]
        self._bio_count.setText(f"{len(text)} / 280")
        self._changed()

    def _changed(self, *_args) -> None:
        if self._loading or self._profile is None:
            return
        self._update_preview()
        self._set_dirty(True)

    def _set_dirty(self, dirty: bool) -> None:
        self._dirty = dirty
        self._save.setEnabled(dirty)
        self._discard.setVisible(dirty)
        if dirty:
            self._status.setObjectName("acSmall")
            self._status.setText("You have unsaved changes.")
            self._status.style().unpolish(self._status)
            self._status.style().polish(self._status)

    def _discard_changes(self) -> None:
        if self._profile is not None:
            self.show_profile(self._profile, self.photo.pixmap())
            self._status.setText("")

    def _emit_save(self) -> None:
        self._save.setEnabled(False)
        self.save_requested.emit(self.changes())

    def _update_preview(self) -> None:
        c = self.changes()
        if not c["is_public"]:
            self._preview.setText("Private: only you can see your profile.")
            return
        parts = [c["display_name"] or "Your name"]
        if c["handle"]:
            parts.append(f"@{c['handle']}")
        if c["show_program"] and c["program"]:
            parts.append(self.program.currentText())
        if c["show_school"] and c["school"]:
            parts.append(c["school"])
        self._preview.setText("Others will see: " + " · ".join(parts))
