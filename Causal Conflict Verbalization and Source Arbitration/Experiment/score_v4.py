#!/usr/bin/env python3
"""Deterministic scoring for the v4 study. Standard library only.

Status: not yet validated against human coding. `sample_for_coding.py` produces
that validation. Until it exists, every label here is a heuristic, except numeric
exact match, which is checkable arithmetic.

Outcome hierarchy
  Primary    answer_source(): the final number equals y_I or y_T.
  Secondary  classify_attempt(): which problem the solve segment works on.
  Secondary  is_refusal(), classify_verdict(), stated_reliable_source().

Differences from the v3 harness functions
  * Answer extraction reports HOW it found the number, so the share that relied on
    a fallback can be reported per arm.
  * Literal "#### <answer>" templates and markdown "#### Heading" lines are handled.
  * Comparison is numeric, so "18.00" equals "18".
  * Entities use word boundaries and a stoplist applied to capitalised words too.
  * A conflict verdict ("cannot determine if they agree") is not a refusal to solve.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from typing import Optional, Set, Tuple

# A number not glued to a preceding word character, digit or decimal point. A sign
# counts only when it isn't a subtraction such as "10-5" or "10 - 5".
_NUM = re.compile(r"(?<![\w.,])(?:(?<![\d)\]]\s)[+-])?\$?\d[\d,]*(?:\.\d+)?(?![\w])")
_TEMPLATE = re.compile(r"</?answer>|\*\*|\\boxed|[{}$`]|\\\(|\\\)|\\\[|\\\]", re.I)


def _clean_number(raw: str) -> str:
    return raw.replace("$", "").replace(",", "").rstrip(".")


def numbers_in(text: str) -> list:
    """All numbers in reading order, as plain strings."""
    return [_clean_number(m.group(0)) for m in _NUM.finditer(text)]


def extract_answer(text: str) -> Tuple[Optional[str], str]:
    """Return (answer, method).

    method is one of:
      hash_direct           number immediately follows the last '####'
      hash_tail             '####' is followed by words, then a number
      hash_no_number        words after '####' but no number (answer is None)
      fallback_last_number  no usable '####'; last number in the output
      none                  no number anywhere
    """
    if "####" in text:
        tail = text[text.rfind("####") + 4 :]
        stripped = _TEMPLATE.sub(" ", tail).strip()
        if stripped:
            nums = numbers_in(stripped)
            if nums:
                first = _NUM.match(stripped)
                return (nums[0], "hash_direct") if first else (nums[-1], "hash_tail")
            return None, "hash_no_number"
        # A bare "#### <answer>" with nothing after it: the template was copied and
        # the output ended, so anything earlier is only a fallback.
    nums = numbers_in(text)
    if nums:
        return nums[-1], "fallback_last_number"
    return None, "none"


def numeric_equal(a: Optional[str], b: Optional[str]) -> bool:
    """Exact decimal comparison after removing commas and a currency sign."""
    if a is None or b is None:
        return False
    try:
        return Decimal(_clean_number(str(a).strip())) == Decimal(_clean_number(str(b).strip()))
    except InvalidOperation:
        return False


def answer_source(answer: Optional[str], y_image: str, y_text: str) -> str:
    """Return image, text, both or neither. 'both' occurs only if y_I equals y_T."""
    i, t = numeric_equal(answer, y_image), numeric_equal(answer, y_text)
    return "both" if i and t else "image" if i else "text" if t else "neither"


# ─── Segmenting verbalization from solving ───────────────────────────────────

_ABBREV = re.compile(r"\b(?:Mr|Mrs|Ms|Dr|St|vs|etc|e\.g|i\.e|U\.S|U\.K)\.$", re.I)
_SENT_END = re.compile(r"[.!?][\"')\]]*(?=\s|$)")
# A solving cue counts only at the start of a sentence or line. Matching anywhere cut
# "a clear problem to solve." in half, which corrupted transplant donors.
_PIVOT = re.compile(
    r"\n\s*\n"
    r"|####"
    r"|(?:^|(?<=[.!?:]\s)|(?<=[\"')]\s)|(?<=\n))"
    r"(?:to (?:solve|find|calculate|determine|figure)\b"
    r"|let'?s\b|let us\b|first,|step 1\b|solution\b|the solution\b|\d+\.\s)",
    re.I,
)
_MAX_VERBALIZATION_CHARS = 900


def _sentence_ends(text: str) -> list:
    ends = []
    for m in _SENT_END.finditer(text):
        if not _ABBREV.search(text[: m.end()][-8:]):
            ends.append(m.end())
    return ends


def split_verbalization(text: str) -> Tuple[str, str]:
    """Split an output into (verbalization, solve) at the first solving cue.

    Model outputs often run to three sentences before solving, so a fixed count of
    two cuts off the reliability statement. Falls back to two sentences when no
    cue exists early in the output. Whitespace is preserved at the boundary so that
    verbalization + solve == text.
    """
    window = text[:_MAX_VERBALIZATION_CHARS]
    ends = _sentence_ends(window)
    first_end = ends[0] if ends else 0
    for m in _PIVOT.finditer(window):
        # A cue inside the first sentence ("To solve this, ...") means no verbalization
        # happened when it opens the output; otherwise wait for a sentence to end.
        if m.start() == 0:
            return "", text
        if m.start() >= first_end:
            return text[: m.start()], text[m.start() :]
    if len(ends) >= 2:
        return text[: ends[1]], text[ends[1] :]
    return text, ""


# ─── Attempted problem ───────────────────────────────────────────────────────

_STOP = frozenset(
    """a about after all also am an and any are as at be because been before being both but by
    can could day days did do does each eight end every few find first five for four from get
    gets give given had half has have he her here hers him his hour hours how if in into is it
    its last less make many may minute minutes month months more most much must need next nine
    no not now number of on one only or other our out over per problem same second seven she
    should six so solve some step such take ten than that the their them then there these they
    third this those three through time times to total two until up us use used very want was
    we week weeks were what when where which while who why will with work would year years you
    your answer calculate cost paid sell buy runs""".split()
)


def extract_entities(question: str) -> Set[str]:
    """Lower-cased content words of a question; names count from three letters."""
    out = set()
    for w in re.findall(r"[A-Z][a-z]{2,}(?:'s)?", question):
        w = re.sub(r"'s$", "", w).lower()
        if w not in _STOP:
            out.add(w)
    for w in re.findall(r"[a-z]{4,}", question.lower()):
        if w not in _STOP:
            out.add(w)
    return out


def _count_hits(entities: Set[str], text_lower: str) -> int:
    return sum(
        1 for e in entities if re.search(r"\b" + re.escape(e) + r"(?:s|es)?\b", text_lower)
    )


@dataclass(frozen=True)
class Attempt:
    label: str  # image, text or unknown
    image_hits: int
    text_hits: int


def classify_attempt(solve_segment: str, image_q: str, text_q: str, margin: int = 2) -> Attempt:
    """Decide which problem a solve segment works on, from problem-specific words.

    Needs a real margin; otherwise 'unknown'. Run this on the solve segment, not the
    whole output, or the instructed description contaminates the label.
    """
    img, txt = extract_entities(image_q), extract_entities(text_q)
    shared = img & txt
    low = solve_segment.lower()
    hi, ht = _count_hits(img - shared, low), _count_hits(txt - shared, low)
    if hi >= ht + margin:
        return Attempt("image", hi, ht)
    if ht >= hi + margin:
        return Attempt("text", hi, ht)
    return Attempt("unknown", hi, ht)


# ─── Refusal, verdict, stated source ─────────────────────────────────────────

_REFUSAL = re.compile(
    r"cannot be (?:solved|answered|determined)|can(?:not|'t) (?:solve|answer)"
    r"|impossible to (?:solve|answer|determine)|not possible to (?:solve|answer|determine)"
    r"|not enough information|insufficient information|no (?:numerical|numeric) answer"
    r"|no need to provide|cannot provide (?:a|an|any)\b|unable to (?:solve|answer)"
    r"|cannot determine",
    re.I,
)
_SOLVE_PIVOT = re.compile(
    r"however,? (?:i|we) can (?:solve|answer)|(?:i|we) (?:can|will) (?:solve|answer)", re.I
)


def is_refusal(text: str) -> bool:
    """True if the model declines to solve: a refusal phrase and nothing computed after.

    "Cannot determine if they agree. However, I can solve..." is not a refusal, and
    neither is any output that keeps producing numbers after the phrase.
    """
    for m in _REFUSAL.finditer(text):
        after = text[m.end() :]
        if _SOLVE_PIVOT.search(after):
            continue
        if not numbers_in(after):
            return True
    return False


_V_CANNOT = re.compile(
    r"(?:cannot|can't|unable to|not possible to|impossible to)\s+(?:be\s+)?"
    r"(?:determine|determined|tell|say|assess)[^.]{0,40}(?:agree|contradict|consistent|reliab|source)",
    re.I,
)
_V_NOT_CONTRADICT = re.compile(r"\bdo(?:es)? not contradict\b|\bno contradiction\b", re.I)
_V_CONFLICT_STRONG = re.compile(
    r"\bdo(?:es)? not agree\b|\bdon't agree\b|\bdisagree\b|\bcontradict(?:s|ory)?\b"
    r"|\bcontradict each other\b|\ba contradiction\b|\binconsisten",
    re.I,
)
_V_NO_INFO = re.compile(
    r"(?:do|does) not (?:provide|contain|include|show|mention) any", re.I
)
_V_CONFLICT_WEAK = re.compile(
    r"\bdo(?:es)? not (?:match|align|relate|directly relate|correspond)\b|\bdon't match\b"
    r"|\bunrelated\b|\bnot related\b|\bnot consistent\b|\bmismatch\b"
    r"|\b(?:are|is|about|present|describe|contain)\s+(?:\w+\s+){0,2}different\b",
    re.I,
)
_V_AGREE = re.compile(r"\b(?:agree|consistent|match|align)\b", re.I)


def classify_verdict(verbalization: str) -> str:
    """Stated relation between the sources.

    Returns cannot_determine, no_relation, agree, conflict, no_info or none.

    Order matters: 'cannot determine if they agree' and 'no agreement or contradiction'
    contain the words the later patterns look for, and 'do not contradict' contains
    'contradict'.
    """
    if _V_CANNOT.search(verbalization):
        return "cannot_determine"
    if re.search(r"\bno (?:\w+ )?agreement\b", verbalization, re.I):
        return "no_relation"
    if _V_NOT_CONTRADICT.search(verbalization):
        return "agree"
    if _V_CONFLICT_STRONG.search(verbalization):
        return "conflict"
    if _V_NO_INFO.search(verbalization):
        return "no_info"
    if _V_CONFLICT_WEAK.search(verbalization):
        return "conflict"
    if _V_AGREE.search(verbalization):
        return "agree"
    return "none"


_REL_SENT = re.compile(r"[^.\n]*\breliable\b[^.\n]*", re.I)
_REL_NEG = re.compile(r"\b(?:cannot|can't|unable|not possible|impossible|neither)\b", re.I)


def stated_reliable_source(verbalization: str) -> str:
    """Which source the model calls more reliable: image, text, undetermined or absent."""
    m = _REL_SENT.search(verbalization)
    if not m:
        return "absent"
    s = m.group(0).lower()
    if _REL_NEG.search(s):
        return "undetermined"
    idx = s.find("reliable")
    before, after = s[:idx], s[idx:]
    # Prefer the subject nearest before "reliable"; else "reliable source is the X".
    i, t = before.rfind("image"), before.rfind("text")
    if i != t:
        return "image" if i > t else "text"
    i, t = after.find("image"), after.find("text")
    if i == -1 and t == -1:
        return "undetermined"
    if i == -1:
        return "text"
    if t == -1:
        return "image"
    return "image" if i < t else "text"


# ─── One-call scoring ────────────────────────────────────────────────────────


def score_output(text: str, image_q: str, text_q: str, y_image: str, y_text: str) -> dict:
    """All v4 labels for one generated output."""
    answer, method = extract_answer(text)
    verb, solve = split_verbalization(text)
    attempt = classify_attempt(solve if solve.strip() else "", image_q, text_q)
    return {
        "answer": answer,
        "answer_method": method,
        "answer_source": answer_source(answer, y_image, y_text),
        "attempt": attempt.label,
        "attempt_image_hits": attempt.image_hits,
        "attempt_text_hits": attempt.text_hits,
        "refusal": is_refusal(text),
        "verdict": classify_verdict(verb),
        "stated_reliable": stated_reliable_source(verb),
        "has_solve_segment": bool(solve.strip()),
        "verbalization_chars": len(verb),
    }
