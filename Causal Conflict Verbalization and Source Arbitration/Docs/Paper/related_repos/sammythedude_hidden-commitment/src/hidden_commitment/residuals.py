"""Turn captured residual streams into named position features."""

from __future__ import annotations

from collections.abc import Sequence
from enum import StrEnum

import numpy as np

from hidden_commitment.hooks import ActivationCache


class Position(StrEnum):
    PRE_DECISION_LAST = "pre_decision_last"
    FIRST_DECISION = "first_decision"
    LAST_DECISION = "last_decision"
    MEAN_DECISION = "mean_decision"
    PRE_RESPONSE_LAST = "pre_response_last"
    RESPONSE_FIRST = "response_first"
    RESPONSE_FIRST4_MEAN = "response_first4_mean"


def position_indices(
    position: Position,
    *,
    prompt_length: int,
    response_length: int,
    decision_token_indices: Sequence[int],
) -> tuple[int, ...]:
    decision = sorted(set(int(index) for index in decision_token_indices))
    if response_length <= 0:
        raise ValueError("Response must contain at least one token")
    if any(index < 0 or index >= response_length for index in decision):
        raise IndexError("A decision token lies outside the response")
    absolute = [prompt_length + index for index in decision]
    if position == Position.PRE_RESPONSE_LAST:
        return (prompt_length - 1,)
    if position == Position.RESPONSE_FIRST:
        return (prompt_length,)
    if position == Position.RESPONSE_FIRST4_MEAN:
        return tuple(range(prompt_length, prompt_length + min(4, response_length)))
    if not absolute:
        raise ValueError(f"{position} requires decision-token indices")
    if position == Position.PRE_DECISION_LAST:
        if absolute[0] == 0:
            raise ValueError("No token precedes the decision span")
        return (absolute[0] - 1,)
    if position == Position.FIRST_DECISION:
        return (absolute[0],)
    if position == Position.LAST_DECISION:
        return (absolute[-1],)
    if position == Position.MEAN_DECISION:
        return tuple(absolute)
    raise ValueError(f"Unsupported position: {position}")


def vectors_at_positions(
    cache: ActivationCache,
    positions: Sequence[int],
    *,
    batch_index: int = 0,
) -> np.ndarray:
    """Return ``[layers, hidden]`` residual vectors averaged over positions."""

    indices = sorted(set(int(position) for position in positions))
    if not indices:
        raise ValueError("At least one position is required")
    result: list[np.ndarray] = []
    for layer in range(len(cache.values)):
        tensor = cache.require(layer)[batch_index]
        if indices[0] < 0 or indices[-1] >= tensor.shape[0]:
            raise IndexError("Residual position lies outside the captured sequence")
        vector = tensor[indices].mean(dim=0).float().cpu().numpy()
        result.append(vector.astype(np.float32, copy=False))
    return np.stack(result)
