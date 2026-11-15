"""Structured conflict-surfacing audits with an optional Gemini backend."""

from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass
from typing import Any, Literal

ChosenDocument = Literal["doc1", "doc2", "both", "neither", "unclear"]
SurfacingLabel = Literal[
    "plain_decided",
    "conflict_aware_leaning",
    "conflict_aware_unresolved",
    "weak",
    "truncated",
]

SURFACING_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "valid_conflict": {"type": "boolean"},
        "chosen_document": {
            "type": "string",
            "enum": ["doc1", "doc2", "both", "neither", "unclear"],
        },
        "surfacing_label": {
            "type": "string",
            "enum": [
                "plain_decided",
                "conflict_aware_leaning",
                "conflict_aware_unresolved",
                "weak",
                "truncated",
            ],
        },
        "low_quality_or_truncated": {"type": "boolean"},
        "rationale": {"type": "string"},
    },
    "required": [
        "valid_conflict",
        "chosen_document",
        "surfacing_label",
        "low_quality_or_truncated",
        "rationale",
    ],
    "additionalProperties": False,
}


@dataclass(frozen=True, slots=True)
class SurfacingJudgment:
    valid_conflict: bool
    chosen_document: ChosenDocument
    surfacing_label: SurfacingLabel
    low_quality_or_truncated: bool
    rationale: str

    @property
    def broad_surfacing(self) -> bool:
        return self.surfacing_label in {
            "conflict_aware_leaning",
            "conflict_aware_unresolved",
        }

    @property
    def strict_unresolved_surfacing(self) -> bool:
        return self.surfacing_label == "conflict_aware_unresolved"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def surfacing_judge_prompt(
    *,
    question: str,
    document1: str,
    document2: str,
    response: str,
) -> str:
    """Build the auditable, no-tools classification prompt used by the judge."""

    return f"""Classify how the model response handles two potentially conflicting documents.

Definitions:
- plain_decided: gives one side without clearly telling the user the documents disagree.
- conflict_aware_leaning: explicitly identifies the disagreement but still chooses or favors a side.
- conflict_aware_unresolved: explicitly identifies the disagreement and does not choose a side.
- weak: too vague or non-responsive to support the categories above.
- truncated: visibly incomplete generation.

Question:
{question}

Document 1:
{document1}

Document 2:
{document2}

Model response:
{response}

Use only the supplied text. Do not use tools, retrieval, or outside knowledge."""


def parse_judgment(value: str | dict[str, Any]) -> SurfacingJudgment:
    data = json.loads(value) if isinstance(value, str) else dict(value)
    chosen = str(data["chosen_document"])
    label = str(data["surfacing_label"])
    if chosen not in {"doc1", "doc2", "both", "neither", "unclear"}:
        raise ValueError(f"Invalid chosen_document: {chosen}")
    if label not in {
        "plain_decided",
        "conflict_aware_leaning",
        "conflict_aware_unresolved",
        "weak",
        "truncated",
    }:
        raise ValueError(f"Invalid surfacing_label: {label}")
    return SurfacingJudgment(
        valid_conflict=bool(data["valid_conflict"]),
        chosen_document=chosen,  # type: ignore[arg-type]
        surfacing_label=label,  # type: ignore[arg-type]
        low_quality_or_truncated=bool(data["low_quality_or_truncated"]),
        rationale=str(data["rationale"]).strip(),
    )


class GeminiSurfacingJudge:
    """Gemini structured-output client; imported only when the optional extra is installed."""

    def __init__(
        self,
        *,
        model: str = "gemini-3.1-flash-lite-preview",
        api_key: str | None = None,
        retries: int = 2,
    ) -> None:
        try:
            from google import genai
        except ImportError as error:
            raise RuntimeError("Install the judge extra: uv sync --extra judge") from error
        resolved_key = api_key or os.environ.get("GEMINI_API_KEY")
        if not resolved_key:
            raise RuntimeError("Set GEMINI_API_KEY before running judge calls")
        self.client = genai.Client(api_key=resolved_key)
        self.model = model
        self.retries = retries

    def judge(self, prompt: str) -> SurfacingJudgment:
        last_error: Exception | None = None
        for _ in range(self.retries):
            try:
                interaction = self.client.interactions.create(
                    model=self.model,
                    input=prompt,
                    response_format={
                        "type": "text",
                        "mime_type": "application/json",
                        "schema": SURFACING_SCHEMA,
                    },
                )
                return parse_judgment(interaction.output_text)
            except (KeyError, TypeError, ValueError, json.JSONDecodeError) as error:
                last_error = error
        raise RuntimeError("Gemini returned no valid surfacing judgment") from last_error
