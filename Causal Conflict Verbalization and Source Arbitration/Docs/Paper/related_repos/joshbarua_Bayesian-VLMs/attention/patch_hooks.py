"""Qwen decoder-layer lookup and readout-write scaling hooks."""

from __future__ import annotations

from typing import Iterable

import torch


ATTENTION_MODULES = ("self_attn", "linear_attn", "attention", "attn")


def get_layers(model, adapter=None):
    """Return the model's decoder layer stack."""
    if adapter is not None:
        return adapter.get_decoder_layers(model)
    for path in (
        ("model", "language_model", "layers"),
        ("language_model", "model", "layers"),
        ("language_model", "layers"),
        ("model", "layers"),
    ):
        value = model
        for attribute in path:
            value = getattr(value, attribute, None)
            if value is None:
                break
        if value is not None and hasattr(value, "__len__"):
            return value
    raise AttributeError("could not locate the decoder layer stack")


def _tensor(output):
    return output[0] if isinstance(output, tuple) else output


def _rewrap(output, tensor):
    return (tensor,) + tuple(output[1:]) if isinstance(output, tuple) else tensor


class BlockPorts:
    """Resolve the token-mixing module whose output enters the residual stream."""

    def __init__(self, layer):
        for name in ATTENTION_MODULES:
            module = getattr(layer, name, None)
            if module is not None:
                self.attn_module_name = name
                self.attn_module = module
                self.attn_write = module
                return
        raise AttributeError(
            f"{type(layer).__name__} exposes none of {ATTENTION_MODULES}"
        )


class ScaleAttentionWrites:
    """Scale selected token-mixer writes at selected positions and layers.

    Qwen3.5 linear-attention layers expose no tokenwise attention row. Setting
    ``scale=0`` removes their direct residual write at the answer readout while
    leaving recurrent-state updates and every other position untouched.
    ``scale=1`` is the exactness control for the same hook path.
    """

    def __init__(self, layers: Iterable[int], positions: list[int], *,
                 scale: float, adapter=None):
        self.layers = sorted({int(layer) for layer in layers})
        if self.layers and self.layers[0] < 1:
            raise ValueError("layers must be 1-based")
        self.positions = [int(position) for position in positions]
        self.scale = float(scale)
        self.rms: dict[int, float] = {}
        self.handles: list = []
        self.adapter = adapter

    def _hook(self, layer: int):
        def apply(module, inputs, output):
            if not self.positions:
                return output
            tensor = _tensor(output)
            index = torch.as_tensor(
                self.positions, device=tensor.device, dtype=torch.long
            )
            selected = tensor[:, index, :]
            self.rms[layer] = float(
                selected.detach().float().square().mean().sqrt().cpu()
            )
            changed = tensor.clone()
            if self.scale == 0.0:
                changed[:, index, :] = 0
            elif self.scale == 1.0:
                changed[:, index, :] = selected
            else:
                changed[:, index, :] = selected * self.scale
            return _rewrap(output, changed)

        return apply

    def attach(self, model):
        stack = get_layers(model, self.adapter)
        for layer in self.layers:
            if layer > len(stack):
                raise ValueError(f"layer {layer} > {len(stack)} decoder layers")
            port = BlockPorts(stack[layer - 1])
            self.handles.append(
                port.attn_write.register_forward_hook(self._hook(layer))
            )
        return self

    def remove(self) -> None:
        for handle in self.handles:
            handle.remove()
        self.handles.clear()
