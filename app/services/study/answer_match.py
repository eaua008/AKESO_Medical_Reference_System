"""Type your answer: how close the typed words are to the card's answer.

    score("penicillin", "Penicillin (beta-lactam)")   -> 1.0 (brackets are extras)
    score("fever", "Fever and joint pain")            -> 0.33
    marks(typed, answer)  -> [(word, matched), ...] for highlighting both sides

Simple and predictable on purpose: lower case, punctuation and filler words
dropped, plurals and common endings folded ("infections" = "infection"). The
score is the share of the answer's words that were typed. It only pre-selects
Again or Good; the student always decides.
"""

import re

GOOD_FROM = 0.6
_WORD = re.compile(r"[A-Za-z0-9]+(?:[.'-][A-Za-z0-9]+)*")
_FILLER = {"a", "an", "the", "of", "and", "or", "to", "in", "on", "for", "with", "by", "is", "are",
           "it", "its", "as", "at", "be", "from", "that", "this"}


def stem(word: str) -> str:
    w = word.lower()
    for end in ("ies", "es", "s", "ing", "ed"):
        if len(w) > len(end) + 3 and w.endswith(end):
            return w[: -len(end)] + ("y" if end == "ies" else "")
    return w


def words(text: str) -> list[str]:
    return _WORD.findall(text or "")


def _key_words(text: str) -> set[str]:
    return {stem(w) for w in words(text) if w.lower() not in _FILLER}


def _core(answer: str) -> str:
    """The answer without its (bracketed extras), when something is left."""
    core = re.sub(r"\([^)]*\)", " ", answer or "")
    return core if _key_words(core) else answer


def score(typed: str, answer: str) -> float:
    want = _key_words(_core(answer))
    if not want or not typed.strip():
        return 0.0
    return len(want & _key_words(typed)) / len(want)


def suggested(typed: str, answer: str):
    """3 (Good) when most of the answer was typed, 1 (Again) when not, None when nothing was typed."""
    if not typed.strip() or not _key_words(answer):
        return None
    return 3 if score(typed, answer) >= GOOD_FROM else 1


def marks(text: str, other: str) -> list[tuple[str, bool]]:
    """Each word of text, and whether it also appears in other (filler words never count)."""
    theirs = _key_words(other)
    return [(w, w.lower() not in _FILLER and stem(w) in theirs) for w in words(text)]
