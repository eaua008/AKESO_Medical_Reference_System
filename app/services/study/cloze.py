"""Fill-in-the-blank cards.

    "Amoxicillin is a {{c1::penicillin}} given {{c2::three times a day}}."
    "Amoxicillin is a {{penicillin}}."                (an unnumbered blank)
    "{{c1::Dengue::a virus}} is spread by mosquitoes"  (with a hint)

One card asks all its blanks at once: the question shows "[ … ]" (or
"[ hint ]") for each, the answer shows the full sentence with the blanks
marked.
"""

import html
import re
from dataclasses import dataclass

_BLANK = re.compile(r"\{\{(?:c(\d+)::)?(.+?)(?:::(.+?))?\}\}", re.S)
HIDDEN = "[ … ]"


@dataclass
class Blank:
    number: int                 # c1, c2... (0 when unnumbered)
    answer: str
    hint: str = ""


def blanks(text: str) -> list[Blank]:
    return [Blank(int(m.group(1) or 0), m.group(2).strip(), (m.group(3) or "").strip())
            for m in _BLANK.finditer(text or "") if m.group(2).strip()]


def question(text: str) -> str:
    """Plain text with every blank hidden."""
    def hide(m: re.Match) -> str:
        hint = (m.group(3) or "").strip()
        return f"[ {hint} ]" if hint else HIDDEN
    return _BLANK.sub(hide, text or "")


def answer(text: str) -> str:
    """Plain text with the blanks filled in."""
    return _BLANK.sub(lambda m: m.group(2).strip(), text or "")


def answer_html(text: str, mark: str = "b") -> str:
    """The full sentence, blanks filled and wrapped in <b> (or another tag), rest escaped."""
    out, last = [], 0
    for m in _BLANK.finditer(text or ""):
        out.append(html.escape(text[last:m.start()]))
        out.append(f"<{mark}>{html.escape(m.group(2).strip())}</{mark}>")
        last = m.end()
    out.append(html.escape((text or "")[last:]))
    return "".join(out).replace("\n", "<br>")


def question_html(text: str) -> str:
    out, last = [], 0
    for m in _BLANK.finditer(text or ""):
        out.append(html.escape(text[last:m.start()]))
        hint = (m.group(3) or "").strip()
        out.append(f"<b>{html.escape(f'[ {hint} ]' if hint else HIDDEN)}</b>")
        last = m.end()
    out.append(html.escape((text or "")[last:]))
    return "".join(out).replace("\n", "<br>")


def make_blank(text: str, start: int, end: int) -> str:
    """Wrap text[start:end] in the next numbered blank ({{cN::...}})."""
    start, end = sorted((max(0, start), min(len(text), end)))
    chosen = text[start:end]
    if not chosen.strip():
        return text
    lead = len(chosen) - len(chosen.lstrip())
    trail = len(chosen) - len(chosen.rstrip())
    start, end = start + lead, end - trail
    number = max([b.number for b in blanks(text)] + [0]) + 1
    return f"{text[:start]}{{{{c{number}::{text[start:end]}}}}}{text[end:]}"
