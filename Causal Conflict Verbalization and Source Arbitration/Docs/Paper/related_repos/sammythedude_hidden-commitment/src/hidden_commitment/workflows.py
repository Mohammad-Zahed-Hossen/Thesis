"""Thin orchestration functions built from the reusable primitives."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

import numpy as np
import torch

from hidden_commitment.cett import extract_cett_vector
from hidden_commitment.hooks import ActivationCache
from hidden_commitment.modeling import format_chat_prompt
from hidden_commitment.residuals import Position, position_indices, vectors_at_positions


def teacher_forced_inputs(
    tokenizer: Any,
    user_prompt: str,
    response: str,
    *,
    device: torch.device,
) -> tuple[Mapping[str, torch.Tensor], int, int]:
    """Construct prompt+response IDs while preserving an exact response-token boundary."""

    chat_prompt = format_chat_prompt(tokenizer, user_prompt)
    prompt_ids = tokenizer(chat_prompt, add_special_tokens=False).input_ids
    response_ids = tokenizer(response, add_special_tokens=False).input_ids
    if not prompt_ids or not response_ids:
        raise ValueError("Prompt and response must each contain at least one token")
    input_ids = torch.tensor([prompt_ids + response_ids], dtype=torch.long, device=device)
    attention_mask = torch.ones_like(input_ids)
    return (
        {"input_ids": input_ids, "attention_mask": attention_mask},
        len(prompt_ids),
        len(response_ids),
    )


def extract_cett_example(
    model: torch.nn.Module,
    tokenizer: Any,
    mlp_cache: ActivationCache,
    *,
    user_prompt: str,
    response: str,
    decision_token_indices: Sequence[int],
) -> np.ndarray:
    inputs, prompt_length, response_length = teacher_forced_inputs(
        tokenizer, user_prompt, response, device=model.device
    )
    response_positions = sorted(set(int(index) for index in decision_token_indices))
    if not response_positions or response_positions[-1] >= response_length:
        raise ValueError("Decision-token indices are empty or outside the response")
    with torch.inference_mode():
        model(**inputs)
    absolute_positions = [prompt_length + index for index in response_positions]
    return extract_cett_vector(model, mlp_cache, absolute_positions)


def extract_residual_example(
    model: torch.nn.Module,
    tokenizer: Any,
    residual_cache: ActivationCache,
    *,
    user_prompt: str,
    response: str,
    decision_token_indices: Sequence[int],
    positions: Sequence[Position] = tuple(Position),
) -> dict[str, np.ndarray]:
    inputs, prompt_length, response_length = teacher_forced_inputs(
        tokenizer, user_prompt, response, device=model.device
    )
    with torch.inference_mode():
        model(**inputs)
    result: dict[str, np.ndarray] = {}
    for position in positions:
        indices = position_indices(
            position,
            prompt_length=prompt_length,
            response_length=response_length,
            decision_token_indices=decision_token_indices,
        )
        result[position.value] = vectors_at_positions(residual_cache, indices)
    residual_cache.clear()
    return result
