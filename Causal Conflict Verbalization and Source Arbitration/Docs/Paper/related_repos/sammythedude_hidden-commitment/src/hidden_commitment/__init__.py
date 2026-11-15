"""Mechanistic helpers for the Hidden Commitment experiments."""

from hidden_commitment.config import DEFAULT_QWEN, ModelSpec
from hidden_commitment.directions import ContrastiveDirection, fit_contrastive_direction
from hidden_commitment.text import DecisionLabel, label_response, locate_alias_span

__all__ = [
    "ContrastiveDirection",
    "DEFAULT_QWEN",
    "DecisionLabel",
    "ModelSpec",
    "fit_contrastive_direction",
    "label_response",
    "locate_alias_span",
]

__version__ = "0.1.0"
