"""Architecture adapters required by the paper's two attention models."""

from .base import ModelAdapter
from .qwen2_5_vl import Qwen2_5_VLAdapter
from .qwen3_5 import Qwen3_5Adapter


_REGISTRY = [Qwen2_5_VLAdapter, Qwen3_5Adapter]


def get_adapter(processor, config) -> ModelAdapter:
    """Return the first adapter that recognizes ``config``."""
    for adapter_cls in _REGISTRY:
        if adapter_cls.matches(config):
            return adapter_cls(processor, config)
    supported = ", ".join(cls.__name__ for cls in _REGISTRY)
    raise ValueError(
        f"Unsupported model type {getattr(config, 'model_type', '?')!r}; paper attention "
        f"experiments support: {supported}"
    )


__all__ = ["ModelAdapter", "Qwen2_5_VLAdapter", "Qwen3_5Adapter", "get_adapter"]
