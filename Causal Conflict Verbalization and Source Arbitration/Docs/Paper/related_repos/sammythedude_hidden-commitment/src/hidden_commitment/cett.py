"""CETT feature extraction and sparse-writer alignment diagnostics."""

from __future__ import annotations

from collections.abc import Mapping, Sequence

import numpy as np
import torch

from hidden_commitment.config import DEFAULT_EPS
from hidden_commitment.hooks import ActivationCache
from hidden_commitment.modeling import get_transformer_layers


def cett_scores(
    activations: torch.Tensor,
    down_weight: torch.Tensor,
    *,
    eps: float = DEFAULT_EPS,
) -> torch.Tensor:
    """Compute all neuron/token CETT scores without materializing per-neuron writes.

    Args:
        activations: MLP intermediate activations with shape ``[..., d_mlp]``.
        down_weight: ``down_proj.weight`` with shape ``[d_model, d_mlp]``.
    """

    if activations.shape[-1] != down_weight.shape[1]:
        raise ValueError(
            f"Incompatible shapes: activations={tuple(activations.shape)}, "
            f"down_weight={tuple(down_weight.shape)}"
        )
    column_norms = torch.linalg.vector_norm(down_weight.float(), dim=0)
    output = torch.matmul(activations.float(), down_weight.float().T)
    output_norms = torch.linalg.vector_norm(output, dim=-1, keepdim=True)
    return activations.float().abs() * column_norms / (output_norms + eps)


def mean_at_positions(values: torch.Tensor, positions: Sequence[int]) -> torch.Tensor:
    positions = sorted(set(int(position) for position in positions))
    if not positions:
        raise ValueError("At least one token position is required")
    if positions[0] < 0 or positions[-1] >= values.shape[-2]:
        raise IndexError(f"Positions {positions[0]}..{positions[-1]} exceed sequence length")
    index = torch.as_tensor(positions, device=values.device)
    return values.index_select(-2, index).mean(dim=-2)


def extract_cett_vector(
    model: torch.nn.Module,
    cache: ActivationCache,
    positions: Sequence[int],
    *,
    batch_index: int = 0,
) -> np.ndarray:
    """Aggregate cached CETT at absolute sequence positions and flatten by layer."""

    features: list[np.ndarray] = []
    for layer_index, layer in enumerate(get_transformer_layers(model)):
        z = cache.require(layer_index)[batch_index]
        weight = layer.mlp.down_proj.weight.detach()
        averaged = mean_at_positions(cett_scores(z, weight), positions)
        features.append(averaged.cpu().numpy().astype(np.float32, copy=False))
    cache.clear()
    return np.concatenate(features)


def write_projection(
    mean_activations: Mapping[int, np.ndarray],
    down_weights: Mapping[int, np.ndarray],
    residual_direction: np.ndarray,
    neurons: Sequence[tuple[int, int]],
) -> float:
    """Project localized neurons' actual MLP writes onto a residual direction."""

    unit = np.asarray(residual_direction, dtype=np.float64)
    unit /= np.linalg.norm(unit)
    total = 0.0
    for layer, neuron in neurons:
        activation = float(np.asarray(mean_activations[layer])[neuron])
        column = np.asarray(down_weights[layer], dtype=np.float64)[:, neuron]
        total += activation * float(np.dot(column, unit))
    return total
