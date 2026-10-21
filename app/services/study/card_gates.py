"""Quality gates every auto card must pass (and helpers they share).

    * the answer must not appear in the question
    * no answer with more than 6 items
    * nothing empty; the front at most ~220 characters
    * multiple choice: exactly one correct, 2-4 distractors, no duplicate or
      near-duplicate choices (bracketed synonyms count), and no distractor
      that is actually true for this entry
    * near-identical cards of one entry are kept once
    * at most N cards per entry, best templates first
"""

import re
from typing import Iterable

from app.models.study import Card, CardType
from app.services.study import cloze

FRONT_MAX = 220
ITEMS_MAX = 6
_BRACKETS = re.compile(r"\(([^)]*)\)")


def norm(text: str) -> str:
    """Lower case, brackets removed, punctuation to spaces."""
    text = _BRACKETS.sub(" ", (text or "").lower())
    return " ".join(re.sub(r"[^a-z0-9]+", " ", text).split())


def forms(text: str) -> set[str]:
    """The text and its bracketed synonyms, normalised: 'Joint pain (arthralgia)' ->
    {'joint pain', 'arthralgia'}."""
    out = {norm(text)}
    for inner in _BRACKETS.findall(text or ""):
        for part in re.split(r"[,;/]| or ", inner):
            n = norm(part)
            if n and n not in ("e g", "eg", "i e"):
                out.add(n)
    return {f for f in out if f}


def overlaps(a: str, b: str) -> bool:
    return bool(forms(a) & forms(b))


_STOP = {"about", "after", "other", "their", "there", "these", "those", "which", "while", "without",
         "within", "severe", "sudden", "signs", "lying", "always", "never", "usually", "being"}


# Plain-language words that name the same finding (wording, not medical facts),
# so "Palpitations" and "a racing heartbeat" count as the same thing.
_SAME = {"palpi": "heart", "heart": "heart", "racin": "heart", "dyspn": "breat", "breat": "breat",
         "edema": "swell", "oedem": "swell", "swell": "swell", "synco": "faint", "faint": "faint",
         "hemop": "cough", "haemo": "bleed", "bleed": "bleed", "blood": "bleed", "hemat": "bleed",
         "melen": "stool", "stool": "stool", "jaund": "yello", "yello": "yello", "seizu": "convu",
         "convu": "convu", "letha": "drows", "drows": "drows", "confu": "confu"}


def stems(text: str) -> set[str]:
    """First five letters of each meaningful word (bracketed synonyms included),
    with common plain-language equivalents folded together."""
    words = " ".join(forms(text)).split()
    return {_SAME.get(w[:5], w[:5]) for w in words if len(w) >= 5 and w not in _STOP}


def similar(a: str, b: str) -> bool:
    """Same thing in other words, roughly: they share a meaningful word stem
    ("Leg swelling" ~ "Swelling of the legs", "Breathlessness" ~ "Shortness of breath")."""
    return overlaps(a, b) or bool(stems(a) & stems(b))


def _contains_words(haystack: str, needle: str) -> bool:
    return bool(needle) and re.search(rf"(^| ){re.escape(needle)}( |$)", haystack) is not None


def front_text(card: Card) -> str:
    return cloze.question(card.cloze_text) if card.type == CardType.CLOZE else card.front


def answer_text(card: Card) -> str:
    if card.type == CardType.MCQ:
        right = [c.text for c in card.choices if c.correct]
        return right[0] if len(right) == 1 else ""
    return card.answer_short or card.back


def item_count(text: str) -> int:
    parts = [p for p in re.split(r"[\n;•]", text or "") if p.strip()]
    return len(parts)


def problems(card: Card, forbidden: Iterable[str] = ()) -> list[str]:
    """Why a card fails the gates ([] = it passes). forbidden: texts that are
    true for this entry, so no distractor may match them."""
    out: list[str] = []
    front = front_text(card).strip()
    answer = answer_text(card).strip()
    if not front:
        out.append("empty front")
    if not answer:
        out.append("empty answer")
    if len(front) > FRONT_MAX:
        out.append("front too long")
    if card.type != CardType.CLOZE and answer:
        question = norm(front)
        if any(_contains_words(question, f) for f in forms(answer) if len(f) > 3):
            out.append("answer appears in the question")
    if item_count(card.answer_short or "") > ITEMS_MAX:
        out.append("answer has more than 6 items")
    if card.type == CardType.MCQ:
        correct = [c for c in card.choices if c.correct]
        wrong = [c for c in card.choices if not c.correct]
        if len(correct) != 1:
            out.append("not exactly one correct choice")
        if not 2 <= len(wrong) <= 4:
            out.append("needs 2 to 4 distractors")
        texts = [c.text for c in card.choices]
        for i in range(len(texts)):
            if not texts[i].strip():
                out.append("empty choice")
            for j in range(i + 1, len(texts)):
                if overlaps(texts[i], texts[j]):
                    out.append("duplicate choices")
        bad = [f for f in forbidden if f]
        for choice in wrong:
            if any(overlaps(choice.text, f) for f in bad):
                out.append("a distractor is true for this entry")
    out.extend(card.problems())
    return out


def dedupe(cards: list[Card]) -> list[Card]:
    seen: set[tuple] = set()
    out = []
    for card in cards:
        key = (card.source_kind, card.source_id, norm(answer_text(card)), card.type)
        if key in seen:
            continue
        seen.add(key)
        out.append(card)
    return out


def cap(cards: list[Card], limit: int, priority: list[str]) -> list[Card]:
    order = {family: i for i, family in enumerate(priority)}
    ranked = sorted(enumerate(cards), key=lambda pair: (order.get(pair[1].family, len(order)), pair[0]))
    keep = {id(card) for _i, card in ranked[:limit]}
    return [card for card in cards if id(card) in keep]


def first_sentence(text: str, limit: int = 260) -> str:
    text = " ".join((text or "").split())
    if not text:
        return ""
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z])", text)
    sentence = parts[0]
    return sentence if len(sentence) <= limit else ""


def sentences(text: str) -> list[str]:
    text = " ".join((text or "").split())
    return [s for s in re.split(r"(?<=[.!?])\s+(?=[A-Z])", text) if s]


def lower_first(text: str) -> str:
    if len(text) > 1 and text[1].isupper():
        return text                      # an abbreviation: keep it
    return text[:1].lower() + text[1:]


def joined(items: list[str]) -> str:
    items = [i for i in items if i]
    if len(items) <= 1:
        return "".join(items)
    return ", ".join(items[:-1]) + " and " + items[-1]


__all__ = ["problems", "dedupe", "cap", "norm", "forms", "overlaps", "first_sentence", "sentences",
           "lower_first", "joined"]
