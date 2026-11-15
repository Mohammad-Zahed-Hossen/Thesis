"""VLM scorer used by every pipeline (corner / grid / steered).

Teacher-forced log-likelihood scoring for two candidate answers given a prompt
and (optionally) an image. ``score_pair`` and ``score_candidate`` accept an
optional ``hooks=`` list (subclasses of :class:`Hook`) so steering and other
forward-time interventions become a scoring mode, not a separate code path.
"""

from __future__ import annotations

import logging
import sys
from contextlib import contextmanager
from pathlib import Path
from typing import Optional

import numpy as np
import torch
from PIL import Image
from transformers import (
    AutoModelForCausalLM,
    AutoModelForImageTextToText,
    AutoProcessor,
    BitsAndBytesConfig,
)

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from config import HF_CACHE_DIR, QWEN_MODEL


# Drop the per-call noise emitted by transformers.processing_utils when
# `apply_chat_template(**kwargs)` includes a kwarg that isn't a recognised
# template variable AND isn't a processor arg (e.g. `enable_thinking=False`
# on Qwen2.5-VL, which is a Qwen3 template variable). The kwarg is silently
# ignored; the warning was logging once per forward pass and inflating
# worker logs to ~50 MB on long scoring runs.
class _DropProcessorKwargsWarning(logging.Filter):
    def filter(self, record):
        return "have to be in `processor_kwargs`" not in record.getMessage()


logging.getLogger("transformers.processing_utils").addFilter(
    _DropProcessorKwargsWarning()
)


def _maybe_promote_patch_embed_to_fp32(model) -> None:
    """If the vision tower's patch_embed is a half-precision Conv3d, promote
    its weights to fp32 and wrap forward to cast inputs/outputs at the
    boundary. No-op if the structure is missing or already fp32.
    """
    visual = getattr(model, "visual", None)
    if visual is None and hasattr(model, "model"):
        visual = getattr(model.model, "visual", None)
    if visual is None:
        return
    pe = getattr(visual, "patch_embed", None)
    proj = getattr(pe, "proj", None) if pe is not None else None
    if not isinstance(proj, torch.nn.Conv3d):
        return
    in_dtype = proj.weight.dtype
    if in_dtype == torch.float32:
        return

    proj.to(torch.float32)
    orig_forward = proj.forward

    def fp32_forward(x, _f=orig_forward, _model_dt=in_dtype):
        return _f(x.to(torch.float32)).to(_model_dt)

    proj.forward = fp32_forward
    print(f"  [patch] promoted patch_embed.proj to fp32 (was {in_dtype}) — "
          "works around slow cuDNN half-precision Conv3d")


# ============================================================================
# VLM Scorer
# ============================================================================

class VLMScorer:
    """
    Scores candidate answers using teacher-forced log-likelihood from a VLM.
    """

    def __init__(
        self,
        model_name: str = QWEN_MODEL,
        load_in_4bit: bool = False,
        load_in_8bit: bool = False,
        device: Optional[str] = None,
        debug: bool = False,
    ):
        self.debug = debug
        print(f"Loading model: {model_name}")

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

        self.processor = AutoProcessor.from_pretrained(
            model_name, trust_remote_code=True, cache_dir=HF_CACHE_DIR
        )

        model_kwargs = {
            "trust_remote_code": True,
            "torch_dtype": torch.bfloat16,
            "device_map": "auto" if device is None else device,
            "cache_dir": HF_CACHE_DIR,
        }
        if quantization_config:
            model_kwargs["quantization_config"] = quantization_config

        try:
            self.model = AutoModelForImageTextToText.from_pretrained(
                model_name, **model_kwargs
            )
        except (ValueError, KeyError):
            self.model = AutoModelForCausalLM.from_pretrained(
                model_name, **model_kwargs
            )
        self.model.eval()
        self.model_name = model_name
        # cuDNN has no fast bf16/fp16 algorithm for the (k=stride=(2,16,16),
        # in=3) Conv3d used as patch_embed by Qwen3.5-VL et al; the fallback
        # kernel runs ~6000x slower than fp32 (4500ms vs 0.7ms per call).
        # Promote that one Conv to fp32 with dtype shims at the boundary.
        _maybe_promote_patch_embed_to_fp32(self.model)
        print("Model loaded successfully")

    @contextmanager
    def _hooks_active(self, hooks):
        """Attach the supplied hooks for the duration of the with-block."""
        handles = []
        if hooks:
            for h in hooks:
                handles.extend(h.attach(self.model))
        try:
            yield
        finally:
            for handle in handles:
                handle.remove()

    def score_candidate(
        self,
        prompt: str,
        candidate: str,
        image: Optional[Image.Image] = None,
        few_shot: Optional[list] = None,
        hooks: Optional[list] = None,
        prefill: Optional[str] = None,
    ) -> float:
        """
        Compute mean log-prob per answer token given prompt and optional image.

        Uses apply_chat_template(tokenize=True, return_dict=True) so that all
        model-specific fields (rope_deltas, position_ids, pixel_values,
        image_grid_thw, …) are produced by the processor and passed through
        to the model unchanged.  Labels masking ensures only answer tokens
        contribute to the NLL.

        Returns the *mean* log-prob per answer token (not the sum) so that
        the LLR s = score(a_T) - score(a_V) is not inflated by length
        differences between the two candidates.

        When ``few_shot`` is a non-empty list of {"prompt", "candidate",
        "image"?} dicts, those pairs are prepended as (user, assistant) chat
        turns before the final test turn. All few-shot tokens are masked from
        the loss — only the final candidate tokens contribute.

        Args:
            prompt: The text prompt (final user turn)
            candidate: The candidate answer string (final assistant turn)
            image: Optional PIL Image for the final user turn
            few_shot: Optional list of in-context examples. Each element is a
                dict with keys ``prompt`` (str), ``candidate`` (str), and
                optionally ``image`` (PIL.Image). Provided in order.
            hooks: Optional list of :class:`scoring.hooks.Hook` instances.
                Each is attached before the forward pass and removed after.

        Returns:
            Mean log-prob per answer token (teacher-forced).
        """
        msgs = []
        for shot in few_shot or []:
            sc = []
            if shot.get("image") is not None:
                sc.append({"type": "image", "image": shot["image"]})
            sc.append({"type": "text", "text": shot["prompt"]})
            msgs.append({"role": "user", "content": sc})
            msgs.append({
                "role": "assistant",
                "content": [{"type": "text", "text": str(shot["candidate"]).strip()}],
            })

        user_content = []
        if image is not None:
            user_content.append({"type": "image", "image": image})
        user_content.append({"type": "text", "text": prompt})
        msgs.append({"role": "user", "content": user_content})

        candidate_text = candidate.strip()
        if prefill is not None:
            assistant_text = f"{prefill.strip()} {candidate_text}"
        else:
            assistant_text = candidate_text

        try:
            full_msgs = msgs + [
                {"role": "assistant", "content": [{"type": "text", "text": assistant_text}]}
            ]
            full_inputs = self.processor.apply_chat_template(
                full_msgs,
                tokenize=True,
                add_generation_prompt=False,
                return_dict=True,
                return_tensors="pt",
                enable_thinking=False,
            )

            # Prompt-only inputs (ends at the assistant generation prompt).
            prompt_inputs = self.processor.apply_chat_template(
                msgs,
                tokenize=True,
                add_generation_prompt=True,
                return_dict=True,
                return_tensors="pt",
                enable_thinking=False,
            )

            if prefill is not None:
                # Find the candidate boundary by diffing the prefill-only
                # chat against the full chat: the candidate starts at the
                # first token where they disagree. This is robust to chat
                # templates that append trailing tokens (e.g. Gemma3 emits
                # <end_of_turn>\n after the assistant content, and the
                # candidate tokens REPLACE those when appended within the
                # same assistant turn).
                prefill_msgs = msgs + [
                    {"role": "assistant",
                     "content": [{"type": "text", "text": prefill.strip()}]}
                ]
                prefill_full = self.processor.apply_chat_template(
                    prefill_msgs,
                    tokenize=True,
                    add_generation_prompt=False,
                    return_dict=True,
                    return_tensors="pt",
                    enable_thinking=False,
                )
                pf_ids = prefill_full["input_ids"][0].tolist()
                full_ids = full_inputs["input_ids"][0].tolist()
                n_cmp = min(len(pf_ids), len(full_ids))
                prefill_end = n_cmp
                for k in range(n_cmp):
                    if pf_ids[k] != full_ids[k]:
                        prefill_end = k
                        break
            else:
                prefill_end = None
        except (ValueError, AttributeError, TypeError) as e:
            raise RuntimeError(
                f"apply_chat_template(tokenize=True, return_dict=True) failed: {e}. "
                "Ensure the processor supports this API (transformers >= 4.49)."
            ) from e

        full_inputs = {k: v.to(self.model.device) for k, v in full_inputs.items()}
        prompt_inputs = {k_: v.to(self.model.device) for k_, v in prompt_inputs.items()}
        prefix_end = prompt_inputs["input_ids"].shape[1]
        if prefill_end is not None:
            # Mask through the end of the prefill so only the candidate
            # tokens contribute to the mean log-prob.
            prefix_end = max(prefix_end, prefill_end)
        if self.debug:
            assert torch.equal(
                full_inputs["input_ids"][:, :prefix_end],
                prompt_inputs["input_ids"],
            ), (
                f"Prompt is not a prefix of full input_ids; masking is wrong.\n"
                f"  prompt tokens: {prompt_inputs['input_ids'].tolist()}\n"
                f"  full[:prefix_end]: {full_inputs['input_ids'][:, :prefix_end].tolist()}"
            )

        # Mask everything up to the candidate tokens.
        labels = full_inputs["input_ids"].clone()
        labels[:, :prefix_end] = -100

        # Mask the chat-template suffix (turn terminator and anything after).
        # Prefer generation_config.eos_token_id (often a list including the
        # template's end-of-turn id, e.g. Gemma-3 sets [<eos>=1, <end_of_turn>=106])
        # and fall back to tokenizer.eos_token_id (Qwen instruct sets this to
        # <|im_end|>).
        gen_eos = getattr(self.model.generation_config, "eos_token_id", None)
        if isinstance(gen_eos, int):
            eos_ids = [gen_eos]
        elif isinstance(gen_eos, (list, tuple)) and gen_eos:
            eos_ids = list(gen_eos)
        else:
            eos_ids = [self.processor.tokenizer.eos_token_id]
        ans_ids = full_inputs["input_ids"][0, prefix_end:]
        eos_mask = torch.zeros_like(ans_ids, dtype=torch.bool)
        for eid in eos_ids:
            if eid is not None:
                eos_mask |= ans_ids == eid
        eos_positions = eos_mask.nonzero(as_tuple=True)[0]
        if len(eos_positions) > 0:
            labels[:, prefix_end + eos_positions[0].item():] = -100

        n_ans = (labels != -100).sum().item()
        if n_ans == 0:
            # No answer tokens scored (shouldn't happen, but guard against it)
            return float("-inf")

        with self._hooks_active(hooks), torch.no_grad():
            out = self.model(**full_inputs, labels=labels)
            # out.loss is already mean NLL per unmasked token → negate for mean log-prob
            mean_logprob = -out.loss.item()

        return float(mean_logprob)

    def get_token_counts(
        self,
        passage: str,
        image: Optional[Image.Image],
    ) -> tuple[int, int]:
        """
        Return (n_T, n_V): passage token count and visual token count.

        n_T: number of tokens in the passage text only (no question / scaffolding),
             using the VLM's own tokenizer.
        n_V: number of visual tokens produced by the vision encoder for this image.
             For Qwen2.5-VL: read directly from image_grid_thw (T*H*W).
             Falls back to input_ids length difference if image_grid_thw is absent.
             Returns 0 if image is None.
        """
        n_T = len(self.processor.tokenizer.encode(passage))

        if image is None:
            return n_T, 0

        try:
            msgs = [{"role": "user", "content": [
                {"type": "image", "image": image},
                {"type": "text", "text": "x"},
            ]}]
            inputs = self.processor.apply_chat_template(
                msgs,
                tokenize=True,
                add_generation_prompt=True,
                return_dict=True,
                return_tensors="pt",
                enable_thinking=False,
            )
            if "image_grid_thw" in inputs:
                # shape [num_images, 3]: each row is [temporal, height, width]
                n_V = int(inputs["image_grid_thw"].prod(dim=-1).sum().item())
            else:
                # Fallback: compare against text-only version of same prompt
                text_msgs = [{"role": "user", "content": [{"type": "text", "text": "x"}]}]
                text_inputs = self.processor.apply_chat_template(
                    text_msgs,
                    tokenize=True,
                    add_generation_prompt=True,
                    return_dict=True,
                    return_tensors="pt",
                    enable_thinking=False,
                )
                n_V = max(0, inputs["input_ids"].shape[1] - text_inputs["input_ids"].shape[1])
        except Exception:
            n_V = 0

        return n_T, n_V

    def score_pair(
        self,
        prompt: str,
        image: Optional[Image.Image],
        a_T: str,
        a_V: str,
        few_shot: Optional[list] = None,
        hooks: Optional[list] = None,
        prefill: Optional[str] = None,
    ) -> dict:
        """
        Score two candidates and return log-likelihoods + LLR-based features.

        Args:
            prompt: The text prompt
            image: Optional PIL Image
            a_T: Text-supported answer
            a_V: Vision-supported answer
            few_shot: Optional list of in-context examples. Applied identically
                to both candidates so LLR semantics are preserved.
            hooks: Optional list of :class:`scoring.hooks.Hook` instances. Each
                is attached once for the lifetime of this call (covering both
                the a_T and a_V forward passes), then removed.

        Returns:
            Dictionary with:
                ll_T: log P(a_T | prompt)
                ll_V: log P(a_V | prompt)
                p_T:  sigma(s) = 2-way probability for a_T
                s:    LLR = ll_T - ll_V (log-likelihood ratio)
                e:    |s| = evidence strength (LLR magnitude)
                U:    normalized binary entropy of p_T
        """
        with self._hooks_active(hooks):
            ll_T = self.score_candidate(prompt, a_T, image, few_shot=few_shot,
                                        prefill=prefill)
            ll_V = self.score_candidate(prompt, a_V, image, few_shot=few_shot,
                                        prefill=prefill)

        s = ll_T - ll_V                # LLR (log-likelihood ratio)
        p_T = logp_to_prob(ll_T, ll_V)  # 2-way probability
        e = abs(s)                       # evidence strength
        U = normalized_entropy(p_T)

        return {
            "ll_T": ll_T,
            "ll_V": ll_V,
            "p_T": p_T,
            "s": s,
            "e": e,
            "U": U,
        }


# ============================================================================
# Probability and Uncertainty Utilities
# ============================================================================

def logp_to_prob(logp_a: float, logp_b: float) -> float:
    """Convert two log-likelihoods to 2-way probability for a."""
    max_logp = max(logp_a, logp_b)
    exp_a = np.exp(logp_a - max_logp)
    exp_b = np.exp(logp_b - max_logp)
    return exp_a / (exp_a + exp_b)


def normalized_entropy(p: float, eps: float = 1e-12) -> float:
    """
    Compute normalized binary entropy in [0, 1].

    U(p) = H(p) / log(2) where H(p) = -p*log(p) - (1-p)*log(1-p)
    """
    p = np.clip(p, eps, 1 - eps)
    H = -(p * np.log(p) + (1 - p) * np.log(1 - p))
    return H / np.log(2)


def kl_divergence(p: float, q: float, eps: float = 1e-8) -> float:
    """Compute KL(P || Q) for Bernoulli distributions."""
    p = np.clip(p, eps, 1 - eps)
    q = np.clip(q, eps, 1 - eps)
    return p * np.log(p / q) + (1 - p) * np.log((1 - p) / (1 - q))


def symmetrized_kl(p: float, q: float, eps: float = 1e-8) -> float:
    """Compute symmetrized KL: SKL(p, q) = 0.5*(KL(p||q) + KL(q||p))."""
    return 0.5 * (kl_divergence(p, q, eps) + kl_divergence(q, p, eps))
