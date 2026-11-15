"""Versioned defaults used by the paper and the public reproduction code."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ModelSpec:
    """A reproducible Hugging Face model reference."""

    model_id: str
    revision: str | None = None
    dtype: str = "float16"
    trust_remote_code: bool = False


DEFAULT_QWEN = ModelSpec(
    model_id="Qwen/Qwen3.5-0.8B",
    revision="2fc06364715b967f1860aea9cf38778875588b17",
)

GEMMA_TRANSFER = ModelSpec(
    model_id="google/gemma-3-1b-it",
    revision=None,
    dtype="bfloat16",
)

DEFAULT_SEED = 42
DEFAULT_EPS = 1e-10

DOC_CHOICE_MAX_NEW_TOKENS = 96
SURFACING_MAX_NEW_TOKENS = 224

DOC_CHOICE_LAYER = 13
SURFACING_LAYER = 17
