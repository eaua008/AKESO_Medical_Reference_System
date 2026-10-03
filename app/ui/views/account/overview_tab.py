"""Account > Overview: completeness, security at a glance, study activity."""

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget

from app.models.account import (
    ACTIVITY_FIELDS, AccountSnapshot, ActivitySummary, CompletenessItem, Device, friendly_time,
)
from app.ui.components.fluid import ResponsiveGrid
from app.ui.views.account.account_widgets import (
    ActivityBars, Card, ChecklistRow, ProgressRing, StatTile, button, label, pill,
)

STAT_ICONS = {
    "diseases_viewed": "book-open", "symptoms_viewed": "activity",
    "medicines_viewed": "pill", "notebook_edits": "notebook-pen",
    "checker_runs": "stethoscope", "interaction_checks": "arrow-left-right",
}


class OverviewTab(QWidget):
    go_to_tab = Signal(str)
    refresh_requested = Signal()

    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("panel")
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(16)

        self.grid = ResponsiveGrid(380, max_columns=2, spacing=16, steps=(2, 1))
        self.grid.set_cards([self._build_completeness(), self._build_security()])
        root.addWidget(self.grid)
        root.addWidget(self._build_activity())

    # -------------------------------------------------------------- cards

    def _build_completeness(self) -> Card:
        card = Card("Profile completeness", "Finish setting up your account.", "badge-check")
        top = QHBoxLayout()
        top.setSpacing(16)
        self.ring = ProgressRing(76)
        top.addWidget(self.ring, 0, Qt.AlignmentFlag.AlignTop)
        self._checklist = QVBoxLayout()
        self._checklist.setSpacing(0)
        top.addLayout(self._checklist, 1)
        card.body.addLayout(top)
        return card

    def _build_security(self) -> Card:
        card = Card("Security at a glance", "How well your account is protected.", "shield-check")
        self._security_rows = QVBoxLayout()
        self._security_rows.setSpacing(8)
        card.body.addLayout(self._security_rows)
        card.body.addStretch(1)
        card.body.addWidget(button("Open security settings", "acGhost", "shield",
                                   on_click=lambda: self.go_to_tab.emit("security")),
                            0, Qt.AlignmentFlag.AlignLeft)
        return card

    def _build_activity(self) -> Card:
        card = Card("Your study activity", "Private to you. Counted on this account, "
                    "across every computer you use.", "trending-up")
        self._activity_off = label(
            "Study activity tracking is off. Turn it on in Privacy & data to see your "
            "streak and weekly totals here.", "acMuted")
        card.body.addWidget(self._activity_off)

        self._activity_on = QWidget()
        self._activity_on.setObjectName("panel")
        body = QVBoxLayout(self._activity_on)
        body.setContentsMargins(0, 0, 0, 0)
        body.setSpacing(12)
        streak_row = QHBoxLayout()
        streak_row.setSpacing(10)
        self._streak = label("", "acCardTitle", wrap=False)
        self._streak_note = label("", "acSmall")
        streak_row.addWidget(pill("\U0001F525 Streak", "acPillWarn"))
        streak_row.addWidget(self._streak)
        streak_row.addWidget(self._streak_note, 1)
        body.addLayout(streak_row)
        self.bars = ActivityBars()
        body.addWidget(self.bars)
        body.addWidget(label("THIS WEEK", "acFieldLabel", wrap=False))
        self._tiles: dict[str, StatTile] = {}
        tiles = []
        for key, caption in ACTIVITY_FIELDS:
            tile = StatTile(caption, STAT_ICONS.get(key, ""))
            self._tiles[key] = tile
            tiles.append(tile)
        self.tile_grid = ResponsiveGrid(170, max_columns=6, spacing=10, steps=(6, 3, 2))
        self.tile_grid.set_cards(tiles)
        body.addWidget(self.tile_grid)
        self._all_time = label("", "acSmall")
        body.addWidget(self._all_time)
        card.body.addWidget(self._activity_on)
        return card

    def watch(self, viewport: QWidget) -> None:
        self.grid.watch(viewport)
        self.tile_grid.watch(viewport)

    # --------------------------------------------------------------- data

    def show_snapshot(self, snapshot: AccountSnapshot, percent: int,
                      items: list[CompletenessItem], devices: list[Device]) -> None:
        self.ring.set_value(percent)
        _clear(self._checklist)
        for item in items:
            row = ChecklistRow(item)
            row.fix.connect(self.go_to_tab.emit)
            self._checklist.addWidget(row)

        _clear(self._security_rows)
        mfa = snapshot.mfa
        rows = [
            ("Two-factor sign-in", ("On", "acPillGood") if mfa.enabled else ("Off", "acPillWarn")),
            ("Password", ("Set", "acPillGood") if snapshot.has_password
             else ("Google sign-in only", "acPill")),
            ("Signed-in computers", (str(sum(1 for d in devices if d.is_active is not False)),
                                     "acPill")),
        ]
        current = next((d for d in devices if d.is_current), None)
        for caption, (value, style) in rows:
            line = QHBoxLayout()
            line.addWidget(label(caption, "acValue"), 1)
            line.addWidget(pill(value, style))
            self._security_rows.addLayout(line)
        if current is not None:
            self._security_rows.addWidget(label(
                f"This computer: {current.device_name}, first used "
                f"{friendly_time(current.first_seen, with_time=False)}.", "acSmall"))
        if snapshot.profile.deletion_pending:
            self._security_rows.addWidget(label(
                "Your account is scheduled for deletion. See Privacy & data.", "acError"))

        tracking = snapshot.profile.track_study_activity
        self._activity_off.setVisible(not tracking)
        self._activity_on.setVisible(tracking)

    def show_activity(self, summary: ActivitySummary) -> None:
        days = summary.streak
        self._streak.setText(f"{days} day{'s' if days != 1 else ''}")
        self._streak_note.setText(
            "Study on any day to keep it going." if days else
            "Open any entry or run a checker today to start a streak.")
        self.bars.set_days(summary.last_14_days)
        for key, tile in self._tiles.items():
            tile.set_number(int(summary.week.get(key, 0)))
        total = sum(int(v) for v in summary.all_time.values())
        self._all_time.setText(
            f"All time: {total:,} activities on {summary.active_days_30} of the last 30 days.")


def _clear(layout) -> None:
    while layout.count():
        item = layout.takeAt(0)
        if item.widget():
            item.widget().deleteLater()
        elif item.layout():
            _clear(item.layout())
