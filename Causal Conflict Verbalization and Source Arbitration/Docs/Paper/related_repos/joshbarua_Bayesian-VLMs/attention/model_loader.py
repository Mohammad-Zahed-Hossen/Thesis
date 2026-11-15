"""Local model + processor loader for the attention experiments.

Loads the processor and model with bf16 + device_map=auto (and optional
4-/8-bit quantization), selects the per-architecture adapter from the
loaded config, and lets the adapter apply any vision-tower fixups it needs
(e.g. Qwen2.5-VL Conv3d patch_embed fp32 promotion).
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path
from typing import Optional

import torch
from transformers import (
    AutoConfig,
    AutoModelForCausalLM,
    AutoModelForImageTextToText,
    AutoProcessor,
    BitsAndBytesConfig,
)

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from config import HF_CACHE_DIR, QWEN_MODEL
from attention.adapters import ModelAdapter, get_adapter


# Drop the per-call processor warning that would otherwise inflate worker
# logs to tens of MB on long sweeps.
class _DropProcessorKwargsWarning(logging.Filter):
    def filter(self, record):  # pragma: no cover - log filter
        return "have to be in `processor_kwargs`" not in record.getMessage()


logging.getLogger("transformers.processing_utils").addFilter(_DropProcessorKwargsWarning())


def load_model_and_processor(
    model_name: str = QWEN_MODEL,
    *,
    load_in_4bit: bool = False,
    load_in_8bit: bool = False,
    device: Optional[str] = None,
    dtype: torch.dtype = torch.bfloat16,
) -> tuple[object, object, ModelAdapter]:
    """Return ``(model, processor, adapter)``. ``device`` defaults to ``"auto"``.

    ``dtype`` selects compute precision. The paper attention results use fp32
    because small differences of large logits are sensitive to bf16 rounding.
    """
    print(f"Loading model: {model_name} (dtype={dtype})")

    quantization_config = None
    if load_in_4bit:
        quantization_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_compute_dtype=torch.bfloat16,
            bnb_4bit_use_double_quant=True,
            bnb_4bit_quant_type="nf4",
        )
    elif load_in_8bit:
        quantization_config = BitsAndBytesConfig(load_in_8bit=True)

    processor = AutoProcessor.from_pretrained(
        model_name, trust_remote_code=True, cache_dir=HF_CACHE_DIR
    )
    config = AutoConfig.from_pretrained(
        model_name, trust_remote_code=True, cache_dir=HF_CACHE_DIR
    )

    model_kwargs = {
        "trust_remote_code": True,
        "torch_dtype": dtype,
        "device_map": "auto" if device is None else device,
        "cache_dir": HF_CACHE_DIR,
    }
    if quantization_config:
        model_kwargs["quantization_config"] = quantization_config

    try:
        model = AutoModelForImageTextToText.from_pretrained(model_name, **model_kwargs)
    except (ValueError, KeyError):
        model = AutoModelForCausalLM.from_pretrained(model_name, **model_kwargs)

    model.eval()

    adapter = get_adapter(processor, config)
    print(f"Selected adapter: {adapter.name} "
          f"(vocab_size={processor.tokenizer.vocab_size}, "
          f"image_pad_id={adapter.image_pad_id})")
    adapter.optimize_vision_tower(model)

    print("Model loaded.")
    return model, processor, adapter


def move_to_device(inputs: dict, device) -> dict:
    """Move every tensor in ``inputs`` to ``device``. Skips non-tensors."""
    out = {}
    for k, v in inputs.items():
        if isinstance(v, torch.Tensor):
            out[k] = v.to(device)
        else:
            out[k] = v
    return out
