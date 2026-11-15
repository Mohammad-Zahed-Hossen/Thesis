"""Forward-hook abstractions used by VLMScorer.

A `Hook` is both a torch forward-hook callable (via ``__call__(module, inputs,
output)``) and a self-attach helper (``attach(model) -> list[handles]``). This
lets steering, attribution, ablation, etc. all plug into ``VLMScorer.score_pair``
through the same ``hooks=[...]`` arg.
"""

from __future__ import annotations

import torch


def get_decoder_layers(model):
    """Locate the transformer decoder layer stack on a HF VLM/LLM.

    Handles both nested-language-model wrappings (Qwen2.5-VL:
    ``model.model.language_model.layers``) and direct (``model.language_model.layers``).
    """
    inner = model.model
    if hasattr(inner, "language_model"):
        return inner.language_model.layers
    if hasattr(model, "language_model"):
        return model.language_model.layers
    raise AttributeError("Could not locate decoder layers on model.")


class Hook:
    """Abstract forward hook. Subclasses define `__call__` and `attach`."""

    def __call__(self, module, inputs, output):  # pragma: no cover - abstract
        raise NotImplementedError

    def attach(self, model) -> list:
        """Register this hook on `model`; return a list of removable handles."""
        raise NotImplementedError

    @staticmethod
    def remove_all(handles) -> None:
        for h in handles:
            h.remove()


class SteeringHook(Hook):
    """Adds ``vec`` to the output of a single decoder layer.

    Args:
        layer: 1-indexed layer number. ``layer=1`` hooks ``layers[0]`` (whose
            output corresponds to ``hidden_states[1]`` in HF parlance).
        vec: shape ``[hidden_size]``. Detached on construction; cast to the
            module's device/dtype at hook time.
    """

    def __init__(self, layer: int, vec: torch.Tensor):
        if layer < 1:
            raise ValueError(f"layer must be 1-indexed (>= 1), got {layer}")
        self.layer = int(layer)
        self.vec = vec.detach()

    def __call__(self, module, inputs, output):
        if isinstance(output, tuple):
            h = output[0]
            v = self.vec.to(h.device, h.dtype)
            return (h + v,) + output[1:]
        v = self.vec.to(output.device, output.dtype)
        return output + v

    def attach(self, model) -> list:
        layers = get_decoder_layers(model)
        if self.layer - 1 >= len(layers):
            raise ValueError(
                f"layer={self.layer} exceeds number of layers ({len(layers)})"
            )
        return [layers[self.layer - 1].register_forward_hook(self)]
