"""Study Hub: flashcards, decks and spaced-repetition state (migration 050).

    Subject          Anatomy, Pathology, Pharmacology, Microbiology
    Deck             a set of cards: official, personal, auto (made on this
                     computer from the encyclopedia) or shared
    Card             basic | mcq | cloze | label3d
    Choice           one answer of a multiple-choice card
    CardState        where one card is in a person's review schedule
    ReviewLogEntry   one rating; the history every state can be rebuilt from
    StudySettings    new cards a day, reviews a day, learning steps

A card is reviewed under its card_key: the card's id for real cards, and a
stable "auto:<kind>:<entry>:<template>" key for the cards made from the
encyclopedia, so their history survives content edits.
"""

import uuid
from dataclasses import dataclass, field, replace
from datetime import datetime
from enum import Enum
from typing import Optional


class CardType(str, Enum):
    BASIC = "basic"
    MCQ = "mcq"
    CLOZE = "cloze"
    LABEL3D = "label3d"


class CardStateKind(str, Enum):
    NEW = "new"
    LEARNING = "learning"
    REVIEW = "review"
    RELEARNING = "relearning"
    SUSPENDED = "suspended"


class Rating(int, Enum):
    AGAIN = 1
    HARD = 2
    GOOD = 3
    EASY = 4


class Origin(str, Enum):
    OFFICIAL = "official"
    PERSONAL = "personal"
    AUTO = "auto"            # never stored on the server: made from the encyclopedia
    SHARED = "shared"        # Phase 5


ORIGIN_LABELS = {Origin.OFFICIAL: "Official", Origin.AUTO: "Auto",
                 Origin.PERSONAL: "Student-made", Origin.SHARED: "Shared"}
TYPE_LABELS = {CardType.BASIC: "Basic", CardType.MCQ: "Multiple choice",
               CardType.CLOZE: "Fill in the blank", CardType.LABEL3D: "3D label"}
TEXT_MAX = 2000
RATIONALE_MAX = 600
CHOICES_MAX = 6
DISCLAIMER = "Akeso is a study tool, not medical advice."


def new_id() -> str:
    return str(uuid.uuid4())


@dataclass
class Subject:
    id: str
    name: str
    icon: str = ""
    position: int = 0


@dataclass
class Choice:
    text: str
    correct: bool = False
    rationale: str = ""

    def to_json(self) -> dict:
        return {"text": self.text, "correct": self.correct, "rationale": self.rationale}

    @classmethod
    def from_json(cls, raw: dict) -> "Choice":
        return cls(text=str(raw.get("text") or ""), correct=bool(raw.get("correct")),
                   rationale=str(raw.get("rationale") or ""))


@dataclass
class Card:
    id: str
    deck_id: str
    type: CardType = CardType.BASIC
    front: str = ""
    back: str = ""
    choices: list[Choice] = field(default_factory=list)
    cloze_text: str = ""
    part_ids: list[str] = field(default_factory=list)
    source_kind: Optional[str] = None       # disease | symptom | medicine | article | body_part
    source_id: Optional[str] = None
    tags: list[str] = field(default_factory=list)
    position: int = 0
    key: str = ""                           # card_key; "" = the card id
    updated_at: str = ""
    deleted_at: Optional[str] = None
    # Teaching fields (auto cards fill them; own/official cards may)
    answer_short: str = ""                  # one line, shown big on the back
    explanation: str = ""                   # "Why": taken from the source text
    distinguish: str = ""                   # "Don't confuse with: X: feature" (one per line)
    hint: str = ""
    difficulty: str = ""                    # basic | clinical | advanced
    family: str = ""                        # template id, e.g. dz_picture
    source_ref: dict = field(default_factory=dict)    # {kind, id, field, title?, url?}
    content_hash: str = ""

    @property
    def card_key(self) -> str:
        return self.key or self.id

    @property
    def is_auto(self) -> bool:
        return self.card_key.startswith(("auto:", "auto2:"))

    def problems(self) -> list[str]:
        """What is wrong with the card, in plain words (empty when it is fine).
        The same rules the database checks (migration 050)."""
        out: list[str] = []
        if len(self.front) > TEXT_MAX or len(self.back) > TEXT_MAX or len(self.cloze_text) > TEXT_MAX:
            out.append("Keep each side under 2,000 letters.")
        if self.type == CardType.BASIC:
            if not self.front.strip():
                out.append("Write the front (the question).")
            if not self.back.strip():
                out.append("Write the back (the answer).")
        elif self.type == CardType.MCQ:
            if not self.front.strip():
                out.append("Write the question.")
            filled = [c for c in self.choices if c.text.strip()]
            if len(filled) < 2:
                out.append("Add at least two choices.")
            if len(self.choices) > CHOICES_MAX:
                out.append("Use up to six choices.")
            if not any(c.correct for c in filled):
                out.append("Mark at least one choice as correct.")
            if any(len(c.rationale) > RATIONALE_MAX for c in self.choices):
                out.append("Keep each explanation under 600 letters.")
            texts = [c.text.strip().lower() for c in filled]
            if len(texts) != len(set(texts)):
                out.append("Two choices say the same thing.")
        elif self.type == CardType.CLOZE:
            from app.services.study.cloze import blanks
            if not blanks(self.cloze_text):
                out.append("Make at least one blank: select a word and press Make blank.")
        elif self.type == CardType.LABEL3D:
            if not self.part_ids:
                out.append("Pick at least one body part.")
        # the teaching fields (same limits as migration 051)
        if len(self.answer_short) > 300:
            out.append("Keep the short answer under 300 letters.")
        if len(self.explanation) > TEXT_MAX or len(self.distinguish) > TEXT_MAX:
            out.append("Keep Why and Don't confuse with under 2,000 letters each.")
        if len(self.hint) > 200:
            out.append("Keep the hint under 200 letters.")
        if self.difficulty and self.difficulty not in DIFFICULTIES:
            out.append("Pick basic, clinical or advanced.")
        return out

    def to_row(self) -> dict:
        return {"id": self.id, "deck_id": self.deck_id, "type": self.type.value,
                "front": self.front, "back": self.back,
                "choices": [c.to_json() for c in self.choices],
                "cloze_text": self.cloze_text, "part_ids": list(self.part_ids),
                "source_kind": self.source_kind, "source_id": self.source_id,
                "tags": list(self.tags), "position": self.position,
                "answer_short": self.answer_short, "explanation": self.explanation,
                "distinguish": self.distinguish, "hint": self.hint, "difficulty": self.difficulty,
                "family": self.family, "source_ref": dict(self.source_ref),
                "content_hash": self.content_hash}

    @classmethod
    def from_row(cls, raw: dict) -> "Card":
        try:
            kind = CardType(raw.get("type") or "basic")
        except ValueError:
            kind = CardType.BASIC
        return cls(id=str(raw.get("id") or ""), deck_id=str(raw.get("deck_id") or ""), type=kind,
                   front=raw.get("front") or "", back=raw.get("back") or "",
                   choices=[Choice.from_json(c) for c in (raw.get("choices") or [])
                            if isinstance(c, dict)],
                   cloze_text=raw.get("cloze_text") or "",
                   part_ids=[str(p) for p in (raw.get("part_ids") or [])],
                   source_kind=raw.get("source_kind") or None,
                   source_id=raw.get("source_id") or None,
                   tags=[str(t) for t in (raw.get("tags") or [])],
                   position=int(raw.get("position") or 0),
                   updated_at=str(raw.get("updated_at") or ""),
                   deleted_at=raw.get("deleted_at") or None,
                   answer_short=raw.get("answer_short") or "", explanation=raw.get("explanation") or "",
                   distinguish=raw.get("distinguish") or "", hint=raw.get("hint") or "",
                   difficulty=raw.get("difficulty") or "", family=raw.get("family") or "",
                   source_ref=dict(raw.get("source_ref") or {}),
                   content_hash=raw.get("content_hash") or "")


DIFFICULTIES = ("basic", "clinical", "advanced")
RETIRED_PREFIX = "auto:"        # the first generation of auto cards: hidden, history kept


@dataclass
class Deck:
    id: str
    title: str
    description: str = ""
    subject_id: str = ""
    origin: Origin = Origin.PERSONAL
    owner_id: Optional[str] = None
    owner_name: str = ""
    status: str = "draft"
    visibility: str = "private"
    updated_at: str = ""
    deleted_at: Optional[str] = None
    group: str = ""                          # auto decks: "Antibiotics", "Cardiovascular"
    source: Optional[tuple[str, str]] = None  # auto deck of one entry: (kind, id)

    @property
    def label(self) -> str:
        return ORIGIN_LABELS[self.origin]

    @property
    def editable(self) -> bool:
        return self.origin == Origin.PERSONAL

    def to_row(self) -> dict:
        return {"id": self.id, "title": self.title, "description": self.description,
                "subject_id": self.subject_id or None, "origin": self.origin.value
                if self.origin != Origin.AUTO else "personal",
                "visibility": self.visibility}

    @classmethod
    def from_row(cls, raw: dict) -> "Deck":
        try:
            origin = Origin(raw.get("origin") or "personal")
        except ValueError:
            origin = Origin.PERSONAL
        return cls(id=str(raw.get("id") or ""), title=raw.get("title") or "",
                   description=raw.get("description") or "",
                   subject_id=raw.get("subject_id") or "", origin=origin,
                   owner_id=raw.get("owner_id") or None, status=raw.get("status") or "draft",
                   visibility=raw.get("visibility") or "private",
                   updated_at=str(raw.get("updated_at") or ""),
                   deleted_at=raw.get("deleted_at") or None)


@dataclass
class CardState:
    card_key: str
    state: CardStateKind = CardStateKind.NEW
    due: Optional[datetime] = None
    interval_days: float = 0.0
    ease: float = 2.5
    reps: int = 0
    lapses: int = 0
    step: int = 0
    last_rating: Optional[int] = None
    last_review: Optional[datetime] = None

    def copy(self, **changes) -> "CardState":
        return replace(self, **changes)

    @property
    def is_new(self) -> bool:
        return self.state == CardStateKind.NEW

    @property
    def is_mature(self) -> bool:
        return self.state == CardStateKind.REVIEW and self.interval_days >= 21


@dataclass
class ReviewLogEntry:
    card_key: str
    rating: int
    reviewed_at: datetime
    client_id: str = field(default_factory=new_id)
    elapsed_ms: int = 0
    state_before: str = "new"
    interval_before: float = 0.0
    interval_after: float = 0.0
    ease_after: float = 2.5
    synced: bool = False
    hinted: bool = False                  # the hint was shown before answering


@dataclass
class StudySettings:
    new_per_day: int = 20
    max_reviews: int = 200
    learning_steps: list[int] = field(default_factory=lambda: [1, 10])     # minutes
    relearn_steps: list[int] = field(default_factory=lambda: [10])
    graduating_days: float = 1.0
    easy_days: float = 4.0
    start_ease: float = 2.5
    min_ease: float = 1.3
    day_starts_at_hour: int = 4                                            # like Anki
    type_answer: bool = False             # type the answer before flipping
    difficulties: list[str] = field(default_factory=list)                 # [] = all
    families: list[str] = field(default_factory=list)                     # [] = all templates
