"""Shared scoring package: VLMScorer + Hook abstractions + degradation helpers."""

from .degradation import blur_image, get_grid_config, load_text_variants
from .hooks import Hook, SteeringHook, get_decoder_layers
from .vlm_scorer import (
    VLMScorer,
    kl_divergence,
    logp_to_prob,
    normalized_entropy,
    symmetrized_kl,
)

__all__ = [
    "VLMScorer",
    "Hook",
    "SteeringHook",
    "get_decoder_layers",
    "blur_image",
    "load_text_variants",
    "get_grid_config",
    "logp_to_prob",
    "normalized_entropy",
    "kl_divergence",
    "symmetrized_kl",
]
