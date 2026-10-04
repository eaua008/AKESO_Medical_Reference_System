"""One remembered search: what was opened from the search box, and when."""

from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone

# The kinds a search result can be (see search_service.SearchResult.kind),
# in the order the History filters show them.
KIND_LABELS = {
    "disease": "Disease",
    "symptom": "Symptom",
    "medicine": "Medicine",
    "protocol": "First aid",
    "article": "Article",
    "module": "Module",
}
FILTERS = [("all", "All"), ("disease", "Diseases"), ("symptom", "Symptoms"),
           ("medicine", "Medicines"), ("protocol", "First aid"), ("article", "Articles"),
           ("module", "Modules")]


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="microseconds")


@dataclass
class HistoryEntry:
    id: int
    kind: str
    target_id: str
    title: str
    subtitle: str
    icon: str
    query: str
    searched_at: str        # ISO 8601, UTC
    times: int = 1

    @property
    def kind_label(self) -> str:
        return KIND_LABELS.get(self.kind, self.kind.title())

    @property
    def when(self) -> datetime:
        try:
            value = datetime.fromisoformat(self.searched_at)
        except ValueError:
            return datetime.now(timezone.utc)
        return value if value.tzinfo else value.replace(tzinfo=timezone.utc)

    def time_text(self) -> str:
        return self.when.astimezone().strftime("%I:%M %p").lstrip("0")

    def day_label(self, today: date | None = None) -> str:
        """"Today", "Yesterday", or a date, for the group headings."""
        today = today or date.today()
        day = self.when.astimezone().date()
        if day == today:
            return "Today"
        if day == today - timedelta(days=1):
            return "Yesterday"
        text = day.strftime("%A, %b %d").replace(" 0", " ")
        return text if day.year == today.year else f"{text}, {day.year}"
