"""Model loading and deterministic text-only generation."""

from __future__ import annotations

import os
import random
from collections.abc import Sequence
from typing import Any

import numpy as np
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from hidden_commitment.config import DEFAULT_QWEN, ModelSpec

os.environ.setdefault("PYTORCH_CUDA_ALLOC_CONF", "expandable_segments:True")
os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")


def seed_everything(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


def resolve_device(device: str | torch.device | None = None) -> torch.device:
    if device is not None:
        return torch.device(device)
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")


def _torch_dtype(name: str) -> torch.dtype:
    try:
        value = getattr(torch, name)
    except AttributeError as error:
        raise ValueError(f"Unsupported torch dtype: {name}") from error
    if not isinstance(value, torch.dtype):
        raise ValueError(f"Unsupported torch dtype: {name}")
    return value


def load_model_and_tokenizer(
    spec: ModelSpec = DEFAULT_QWEN,
    *,
    device: str | torch.device | None = None,
    local_files_only: bool = False,
) -> tuple[torch.nn.Module, Any]:
    """Load on CPU first, then move to one device to avoid Windows mmap/offload failures."""

    common = {
        "revision": spec.revision,
        "trust_remote_code": spec.trust_remote_code,
        "local_files_only": local_files_only,
    }
    tokenizer = AutoTokenizer.from_pretrained(spec.model_id, **common)
    model = AutoModelForCausalLM.from_pretrained(
        spec.model_id,
        dtype=_torch_dtype(spec.dtype),
        low_cpu_mem_usage=True,
        **common,
    )
    target = resolve_device(device)
    if target.type == "cuda":
        torch.cuda.empty_cache()
    model = model.to(target)
    model.eval()
    return model, tokenizer


def get_language_model(model: torch.nn.Module) -> torch.nn.Module:
    """Resolve a text backbone from plain, multimodal, or adapter-wrapped models."""

    visited: set[int] = set()
    current = model
    for _ in range(6):
        if id(current) in visited:
            break
        visited.add(id(current))
        language_model = getattr(current, "language_model", None)
        if language_model is not None:
            current = language_model
            continue
        inner = getattr(current, "model", None)
        if inner is not None and hasattr(inner, "language_model"):
            current = inner.language_model
            continue
        break
    return current


def get_transformer_layers(model: torch.nn.Module) -> Sequence[torch.nn.Module]:
    backbone = get_language_model(model)
    candidates = [backbone, getattr(backbone, "model", None)]
    candidates.append(getattr(candidates[-1], "model", None))
    for candidate in candidates:
        if candidate is not None and hasattr(candidate, "layers"):
            return candidate.layers
    raise TypeError(f"Could not resolve transformer layers from {type(model)!r}")


def format_chat_prompt(tokenizer: Any, user_prompt: str) -> str:
    messages = [{"role": "user", "content": user_prompt}]
    try:
        return tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
            enable_thinking=False,
        )
    except TypeError:
        return tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
        )


def generate_text(
    model: torch.nn.Module,
    tokenizer: Any,
    user_prompt: str,
    *,
    seed: int = 42,
    max_new_tokens: int = 96,
    temperature: float = 0.0,
    top_p: float = 0.9,
    top_k: int = 50,
) -> str:
    seed_everything(seed)
    prompt = format_chat_prompt(tokenizer, user_prompt)
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    sample = temperature > 0
    generation = {
        "max_new_tokens": max_new_tokens,
        "do_sample": sample,
        "pad_token_id": tokenizer.eos_token_id,
    }
    if sample:
        generation.update(temperature=temperature, top_p=top_p, top_k=top_k)
    with torch.inference_mode():
        output = model.generate(**inputs, **generation)
    return tokenizer.decode(
        output[0, inputs.input_ids.shape[1] :],
        skip_special_tokens=True,
    ).strip()
