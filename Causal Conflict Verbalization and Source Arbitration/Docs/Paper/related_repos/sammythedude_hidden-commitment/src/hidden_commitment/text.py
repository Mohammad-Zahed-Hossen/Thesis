"""Prompt construction, source attribution, and answer-span alignment."""

from __future__ import annotations

import re
from collections.abc import Sequence
from dataclasses import dataclass
from enum import StrEnum
from typing import Any, Protocol


class OffsetTokenizer(Protocol):
    def __call__(self, text: str, **kwargs: Any) -> dict[str, Any]: ...


class DecisionLabel(StrEnum):
    DOC1 = "doc1"
    DOC2 = "doc2"
    BOTH = "both"
    NEITHER = "neither"


@dataclass(frozen=True, slots=True)
class LocatedSpan:
    text: str
    char_start: int
    char_end: int
    token_indices: tuple[int, ...]
    matched_alias: str


DEFAULT_TASK_INSTRUCTION = (
    "Answer the question using the provided context. If the documents disagree, "
    "explicitly describe the conflict before answering."
)


def normalize_text(text: str) -> str:
    """Normalize text for conservative, whole-phrase alias matching."""

    return " ".join(re.sub(r"[^\w\s]", " ", str(text).casefold()).split())


def alias_hits(text: str, aliases: Sequence[str]) -> list[str]:
    normalized = f" {normalize_text(text)} "
    return [
        alias
        for alias in aliases
        if (candidate := normalize_text(alias)) and f" {candidate} " in normalized
    ]


def label_response(
    response: str,
    doc1_aliases: Sequence[str],
    doc2_aliases: Sequence[str],
) -> DecisionLabel:
    """Attribute a response only when exactly one document's aliases occur."""

    doc1 = bool(alias_hits(response, doc1_aliases))
    doc2 = bool(alias_hits(response, doc2_aliases))
    if doc1 and doc2:
        return DecisionLabel.BOTH
    if doc1:
        return DecisionLabel.DOC1
    if doc2:
        return DecisionLabel.DOC2
    return DecisionLabel.NEITHER


def locate_alias_span(
    response: str,
    aliases: Sequence[str],
    tokenizer: OffsetTokenizer,
) -> LocatedSpan | None:
    """Return the shortest token-aligned substring equal to an alias after normalization."""

    if not response:
        return None
    encoded = tokenizer(response, add_special_tokens=False, return_offsets_mapping=True)
    offsets = [(int(start), int(end)) for start, end in encoded["offset_mapping"]]
    candidates: list[LocatedSpan] = []
    for alias in aliases:
        target = normalize_text(alias)
        if not target:
            continue
        for first, (start, _) in enumerate(offsets):
            for last in range(first, len(offsets)):
                end = offsets[last][1]
                if end <= start or normalize_text(response[start:end]) != target:
                    continue
                candidates.append(
                    LocatedSpan(
                        text=response[start:end],
                        char_start=start,
                        char_end=end,
                        token_indices=tuple(range(first, last + 1)),
                        matched_alias=str(alias),
                    )
                )
                break
    if not candidates:
        return None
    return min(candidates, key=lambda item: (item.char_end - item.char_start, item.char_start))


def split_documents(context: str) -> list[str]:
    """Split the FaithEval ``Document:`` serialization without changing document text."""

    text = str(context).strip()
    if not text:
        return []
    parts = [part.strip() for part in re.split(r"(?=Document:)", text) if part.strip()]
    return [part if part.startswith("Document:") else f"Document: {part}" for part in parts]


def swap_documents(context: str) -> str:
    documents = split_documents(context)
    if len(documents) != 2:
        raise ValueError(f"Expected exactly two documents, found {len(documents)}")
    return "\n\n".join(reversed(documents))


def build_conflict_prompt(
    question: str,
    context: str,
    instruction: str = DEFAULT_TASK_INSTRUCTION,
) -> str:
    return (
        f"{instruction.strip()}\n\n"
        f"Context:\n{context.strip()}\n\n"
        f"Question: {question.strip()}\n\n"
        "Answer:"
    )
