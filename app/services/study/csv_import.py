"""Bulk import of cards from a CSV file (Content Management -> Decks).

Columns (a header row is required; extra columns are ignored):

    type          basic | mcq | cloze        (label3d comes later)
    front         the question (basic, mcq)
    back          the answer (basic)
    choices_json  mcq only: [{"text": "...", "correct": true, "rationale": "..."}, ...]
    cloze_text    cloze only: "Amoxicillin is a {{c1::penicillin}}."
    tags          optional, separated by ; or ,

Every row is checked with the same rules as the card editor; bad rows are
reported with their line number and are not imported.
"""

import csv
import io
import json
from dataclasses import dataclass, field

from app.models.study import Card, CardType, Choice

COLUMNS = ("type", "front", "back", "choices_json", "cloze_text", "tags")
MAX_ROWS = 2000


@dataclass
class ImportResult:
    cards: list[Card] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)       # "Line 4: ..."

    @property
    def summary(self) -> str:
        bad = len(self.errors)
        return (f"{len(self.cards)} card{'s' if len(self.cards) != 1 else ''} ready"
                + (f", {bad} row{'s' if bad != 1 else ''} with problems (not imported)" if bad else ""))


def parse_csv(text: str, deck_id: str = "") -> ImportResult:
    result = ImportResult()
    text = (text or "").lstrip("﻿")
    if not text.strip():
        result.errors.append("The file is empty.")
        return result
    reader = csv.DictReader(io.StringIO(text))
    header = [h.strip().lower() for h in (reader.fieldnames or [])]
    if "type" not in header:
        result.errors.append("The first row must name the columns: type, front, back, choices_json, "
                             "cloze_text, tags.")
        return result
    reader.fieldnames = header
    for number, row in enumerate(reader, start=2):
        if number - 1 > MAX_ROWS:
            result.errors.append(f"Only the first {MAX_ROWS} rows were read.")
            break
        row = {k: (v or "").strip() for k, v in row.items() if k}
        if not any(row.values()):
            continue
        try:
            kind = CardType((row.get("type") or "basic").lower())
        except ValueError:
            result.errors.append(f"Line {number}: unknown type “{row.get('type')}” "
                                 "(use basic, mcq or cloze).")
            continue
        if kind == CardType.LABEL3D:
            result.errors.append(f"Line {number}: 3D label cards can't be imported yet.")
            continue
        card = Card("", deck_id, type=kind, front=row.get("front", ""), back=row.get("back", ""),
                    cloze_text=row.get("cloze_text", ""),
                    tags=[t.strip() for t in row.get("tags", "").replace(";", ",").split(",") if t.strip()])
        if kind == CardType.MCQ:
            try:
                raw = json.loads(row.get("choices_json") or "[]")
                if not isinstance(raw, list):
                    raise ValueError
                card.choices = [Choice.from_json(c) for c in raw if isinstance(c, dict)]
            except (ValueError, TypeError):
                result.errors.append(f"Line {number}: choices_json is not a valid list of choices.")
                continue
        problems = card.problems()
        if problems:
            result.errors.append(f"Line {number}: {problems[0]}")
            continue
        result.cards.append(card)
    return result
