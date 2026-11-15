"""Scoped activation capture and residual-stream interventions."""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from typing import Any

import numpy as np
import torch

from hidden_commitment.modeling import get_language_model, get_transformer_layers


class HookGroup:
    """Own hook handles and remove them reliably on context exit."""

    def __init__(self, handles: Iterable[Any] = ()) -> None:
        self.handles = list(handles)

    def append(self, handle: Any) -> None:
        self.handles.append(handle)

    def close(self) -> None:
        while self.handles:
            self.handles.pop().remove()

    def __enter__(self) -> HookGroup:
        return self

    def __exit__(self, *_: object) -> None:
        self.close()


class ActivationCache:
    """A mutable layer-indexed cache cleared between examples."""

    def __init__(self, layer_count: int) -> None:
        self.values: dict[int, torch.Tensor | None] = dict.fromkeys(range(layer_count))

    def clear(self) -> None:
        self.values.update(dict.fromkeys(self.values))

    def require(self, layer: int) -> torch.Tensor:
        value = self.values[layer]
        if value is None:
            raise RuntimeError(f"No activation captured for layer {layer}")
        return value


def capture_mlp_inputs(model: torch.nn.Module) -> tuple[ActivationCache, HookGroup]:
    """Capture ``z`` at every MLP ``down_proj`` input."""

    backbone = get_language_model(model)
    layers = get_transformer_layers(model)
    cache = ActivationCache(len(layers))
    hooks = HookGroup()

    for layer_index, layer in enumerate(layers):
        mlp = getattr(layer, "mlp", None)
        down_proj = getattr(mlp, "down_proj", None)
        if down_proj is None:
            hooks.close()
            raise TypeError(f"Layer {layer_index} has no mlp.down_proj in {type(backbone)!r}")

        def capture(
            _module: torch.nn.Module,
            inputs: tuple[torch.Tensor, ...],
            _output: Any,
            *,
            index: int = layer_index,
        ) -> None:
            cache.values[index] = inputs[0].detach()

        hooks.append(down_proj.register_forward_hook(capture))
    return cache, hooks


def capture_residual_inputs(model: torch.nn.Module) -> tuple[ActivationCache, HookGroup]:
    """Capture the residual stream entering every transformer block."""

    layers = get_transformer_layers(model)
    cache = ActivationCache(len(layers))
    hooks = HookGroup()
    for layer_index, layer in enumerate(layers):

        def capture(
            _module: torch.nn.Module, inputs: tuple[torch.Tensor, ...], *, index: int = layer_index
        ) -> None:
            cache.values[index] = inputs[0].detach()

        hooks.append(layer.register_forward_pre_hook(capture))
    return cache, hooks


@dataclass(frozen=True, slots=True)
class SteeringWindow:
    """Tokens to edit during prompt prefill and autoregressive decoding."""

    prompt_tail: int = 0
    response_start: int = 0
    response_end: int = 0

    def __post_init__(self) -> None:
        if min(self.prompt_tail, self.response_start, self.response_end) < 0:
            raise ValueError("Steering-window bounds must be non-negative")
        if self.response_end < self.response_start:
            raise ValueError("response_end must be >= response_start")


def residual_steering_hook(
    model: torch.nn.Module,
    *,
    layer: int,
    direction: np.ndarray | torch.Tensor,
    delta: float,
    window: SteeringWindow,
) -> HookGroup:
    """Add ``delta * RMS(x) * direction`` to the input of ``layer``.

    The hook edits the previous block's output because the paper's readout is fit
    on the input to the selected layer. Layer zero is consequently unsupported.
    """

    layers: Sequence[torch.nn.Module] = get_transformer_layers(model)
    if not 0 < layer < len(layers):
        raise ValueError(f"layer must be in [1, {len(layers) - 1}], got {layer}")
    vector = torch.as_tensor(direction, dtype=torch.float32, device=model.device).flatten()
    norm = torch.linalg.vector_norm(vector)
    if not torch.isfinite(norm) or float(norm) <= 1e-12:
        raise ValueError("Steering direction must have a finite non-zero norm")
    vector = vector / norm
    generated = 0

    def add_(hidden: torch.Tensor) -> None:
        rms = torch.sqrt(torch.mean(hidden.float().square(), dim=-1, keepdim=True) + 1e-8)
        update = float(delta) * rms * vector.view(1, 1, -1)
        hidden.add_(update.to(hidden.dtype))

    def steer(_module: torch.nn.Module, _inputs: tuple[torch.Tensor, ...], output: Any) -> None:
        nonlocal generated
        if abs(delta) <= 1e-12:
            return
        hidden = output[0] if isinstance(output, tuple) else output
        if not torch.is_tensor(hidden):
            raise TypeError(f"Unsupported transformer output type: {type(hidden)!r}")
        if hidden.shape[1] > 1:
            generated = 0
            tail = min(window.prompt_tail, hidden.shape[1])
            if tail:
                add_(hidden[:, -tail:, :])
            return
        if window.response_start <= generated < window.response_end:
            add_(hidden)
        generated += 1

    return HookGroup([layers[layer - 1].register_forward_hook(steer)])
