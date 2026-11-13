#!/usr/bin/env python3
"""Scoring for the v5 verdict-transplant study. Standard library only.

This module adds to score_v4; it changes nothing there, so v4 results still
reproduce. New pieces:

  stated_reliable_source()  Recognises chart/report as well as image/text and uses
                            word boundaries ("context" no longer counts as "text").
  extract_answer_strict()   The strict parser for ChartQA, after Which Source Wins? §3.3.
                            It never searches reasoning for numbers.
  answers_match()           Numeric comparison where both sides are numbers; otherwise
                            normalised string comparison ("14.8%" matches "14.8").
  margin()                  The log-likelihood margin, image minus text.

Labels other than numeric or string answer match are heuristics until human
coding validates them (see sample_for_coding.py).
"""
from __future__ import annotations

import math
import re
from decimal import Decimal, InvalidOperation
from typing import Optional, Sequence, Tuple

import score_v4 as v4

# Re-exported so v5 code needs only this module.
split_verbalization = v4.split_verbalization
extract_answer = v4.extract_answer
numeric_equal = v4.numeric_equal

# ─── Stated reliable source ──────────────────────────────────────────────────

# Longest alternatives first so "typed text" wins over "text".
_SOURCE_NOUN = re.compile(
    r"\b(typed text|textual information|visual information|image|picture|visual|chart|report|text|written)\b",
    re.I,
)
_NOUN_LABEL = {
    "typed text": "text",
    "textual information": "text",
    "text": "text",
    "written": "text",
    "visual information": "image",
    "image": "image",
    "picture": "image",
    "visual": "image",
    "chart": "chart",
    "report": "report",
}
_REL_SENT = re.compile(r"[^.\n]*\b(?:un)?reliable\b[^.\n]*", re.I)
_REL_NEG = re.compile(
    r"\b(?:cannot|can't|unable|not possible|impossible|neither|equally|less reliable|not (?:as )?reliable|unreliable|no more reliable)\b",
    re.I,
)

SOURCES = {"math": ("image", "text"), "chartqa": ("chart", "report")}


def stated_reliable_source(verbalization: str, regime: Optional[str] = None) -> str:
    """Return image, text, chart, report, undetermined or absent.

    Uses the first sentence that contains "reliable" (or "unreliable"). Inside it,
    the source noun nearest before "reliable" wins ("the typed text is more reliable").
    With none before, the first one after it wins ("the more reliable source is the chart").
    When regime is provided, only nouns belonging to SOURCES[regime] are considered.
    """
    m = _REL_SENT.search(verbalization)
    if not m:
        return "absent"
    s = m.group(0)
    if _REL_NEG.search(s):
        return "undetermined"
    allowed = set(SOURCES[regime]) if regime is not None else None
    idx = s.lower().find("reliable")
    before = [
        _NOUN_LABEL[x.group(1).lower()]
        for x in _SOURCE_NOUN.finditer(s[:idx])
        if allowed is None or _NOUN_LABEL[x.group(1).lower()] in allowed
    ]
    if before:
        return before[-1]
    after = [
        _NOUN_LABEL[x.group(1).lower()]
        for x in _SOURCE_NOUN.finditer(s[idx:])
        if allowed is None or _NOUN_LABEL[x.group(1).lower()] in allowed
    ]
    return after[0] if after else "undetermined"


def opposite_source(label: str, regime: str) -> Optional[str]:
    a, b = SOURCES[regime]
    return b if label == a else a if label == b else None


# ─── Answers ─────────────────────────────────────────────────────────────────

_MARKUP = re.compile(r"</?answer>|\*\*|\\boxed|[{}`]|\\\(|\\\)|\\\[|\\\]", re.I)
_EDGE = re.compile(r"^[\s\"'.,:;!?()\[\]]+|[\s\"'.,:;!?()\[\]]+$")
_ARTICLE = re.compile(r"^(?:the|a|an)\s+", re.I)
_MAX_ANSWER_WORDS = 4


def normalize_answer(raw: Optional[str]) -> Optional[str]:
    """Lower-case, strip markup, edge punctuation, a leading article, '%', '$' and commas."""
    if raw is None:
        return None
    s = _MARKUP.sub(" ", str(raw)).strip()
    s = _EDGE.sub("", s)
    s = _ARTICLE.sub("", s)
    s = s.replace("%", "").replace("$", "").strip()
    s = re.sub(r"(?<=\d),(?=\d{3}\b)", "", s)
    s = re.sub(r"\s+", " ", s).lower()
    return s or None


def _as_decimal(s: Optional[str]) -> Optional[Decimal]:
    if s is None or not re.fullmatch(r"[+-]?\d+(?:\.\d+)?", s):
        return None
    try:
        return Decimal(s)
    except InvalidOperation:
        return None


def answers_match(a: Optional[str], b: Optional[str]) -> bool:
    """Numbers compare exactly as decimals; anything else as a normalised string."""
    na, nb = normalize_answer(a), normalize_answer(b)
    if na is None or nb is None:
        return False
    da, db = _as_decimal(na), _as_decimal(nb)
    if da is not None and db is not None:
        return da == db
    return na == nb


def extract_answer_strict(text: str) -> Tuple[Optional[str], str]:
    """Strict answer-only parser. Returns (answer, method).

    method: hash         the line after the last '####'
            first_line   no '####'; the first non-empty line is itself a short answer
            none         nothing usable; reasoning is never searched
    """
    if "####" in text:
        tail = text[text.rfind("####") + 4 :]
        line = tail.strip().splitlines()[0] if tail.strip() else ""
        ans = normalize_answer(line)
        return (ans, "hash") if ans else (None, "none")
    for line in text.splitlines():
        if line.strip():
            ans = normalize_answer(line)
            if ans and len(ans.split()) <= _MAX_ANSWER_WORDS and not re.search(r"[.!?]\s", line.strip()):
                return ans, "first_line"
            return None, "none"
    return None, "none"


def answer_source_v5(answer: Optional[str], y_image: str, y_text: str) -> str:
    i, t = answers_match(answer, y_image), answers_match(answer, y_text)
    return "both" if i and t else "image" if i else "text" if t else "neither"


_MATH_FINAL_ANSWER = re.compile(
    r"(?:the\s+(?:final\s+)?(?:answer|number|result|total)\s+(?:is|=|:)|\\boxed\s*\{)\s*\$?\s*([+-]?\d[\d,]*(?:\.\d+)?)",
    re.I,
)


def extract_math_final_answer(text: str) -> Optional[str]:
    """Extract an explicit final-answer declaration when #### is omitted."""
    matches = _MATH_FINAL_ANSWER.findall(text)
    return v4._clean_number(matches[-1]) if matches else None


def behavioural_source(
    text: str,
    regime: str,
    y_image: str,
    y_text: str,
    allow_math_fallback: bool = False,
) -> Tuple[str, Optional[str], str]:
    """Secondary outcome. Returns (source, answer, method).

    math     score_v4.extract_answer; rejects fallback_last_number when allow_math_fallback is False,
             and rescues structured final-answer declarations or fallback_last_number when True.
    chartqa  extract_answer_strict
    """
    if regime == "chartqa":
        ans, method = extract_answer_strict(text)
    else:
        ans, method = v4.extract_answer(text)
        if method in ("fallback_last_number", "hash_no_number", "none"):
            if allow_math_fallback:
                structured = extract_math_final_answer(text)
                if structured is not None:
                    ans, method = structured, "structured_final_answer"
                elif method != "fallback_last_number":
                    ans = None
            else:
                ans = None
    return answer_source_v5(ans, y_image, y_text), ans, method


# ─── Log-likelihood margin ───────────────────────────────────────────────────


def log_softmax(row: Sequence[float]) -> list:
    """Numerically stable log-softmax of one logit row (pure Python, for tests)."""
    m = max(row)
    z = math.log(sum(math.exp(x - m) for x in row)) + m
    return [x - z for x in row]


def continuation_positions(prefix_len: int, full_len: int) -> list:
    """(logit_row, token_index) pairs that score the continuation tokens.

    The logits at position t predict token t + 1, so token j is scored by row j - 1.
    """
    if not 0 < prefix_len < full_len:
        raise ValueError(f"need 0 < prefix_len < full_len, got {prefix_len}, {full_len}")
    return [(j - 1, j) for j in range(prefix_len, full_len)]


def leading_ws_skip(pieces: Sequence[str]) -> int:
    """How many leading continuation tokens to leave unscored: 1 if the first is only whitespace.

    The candidate is written as " " + y. Qwen tokenizers emit that space as its own
    token, which both candidates share. Counting it in |y| would change the length
    normalisation, so it is skipped (prereg §6.1). The last token is always scored.
    """
    return 1 if len(pieces) > 1 and pieces[0].strip() == "" else 0


def continuation_logprob(
    logits: Sequence[Sequence[float]], ids: Sequence[int], prefix_len: int, skip: int = 0
) -> Tuple[float, int]:
    """Summed log-probability of ids[prefix_len + skip:] and the token count. Pure Python."""
    total = 0.0
    pos = continuation_positions(prefix_len + skip, len(ids))
    for row, tok in pos:
        total += log_softmax(logits[row])[ids[tok]]
    return total, len(pos)


def margin(lp_image: float, n_image: int, lp_text: float, n_text: int) -> float:
    """Δℓ = lp_I/|y_I| − lp_T/|y_T|. Positive favours the image (or chart) answer."""
    if n_image <= 0 or n_text <= 0:
        raise ValueError("candidate with no tokens")
    return lp_image / n_image - lp_text / n_text
