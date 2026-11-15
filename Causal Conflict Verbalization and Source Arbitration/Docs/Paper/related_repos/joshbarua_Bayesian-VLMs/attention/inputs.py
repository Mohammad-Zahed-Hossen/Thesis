"""Build aligned model inputs and extract patch-position metadata.

For an example with question ``q``, passage ``t``, image ``v``, and two
candidate answers ``a_T``/``a_V``, ``build_joint`` returns a ``ModelInput``
holding the processor outputs together with:

* ``text_positions``  -- expanded-token positions of the passage span,
* ``vision_positions`` -- expanded-token positions of the image-pad span,
* ``answer_pos = N_div - 1``, the first-divergent-token readout position,
* ``id_T_div``, ``id_V_div``, the divergent answer-token ids.

The ``inputs`` field always carries the **full a_T-augmented chat**
(``[user(...), assistant(a_T)]`` rendered with ``add_generation_prompt=False``).
We use ``a_T``'s chat -- not the prompt-only chat -- because when the two
answers share their first content token (``id_T == id_V`` at ``N_div - 1
+1`` of the prompt prefix), ``N_div`` lies past the assistant header and the
readout position falls inside the assistant content. Autoregressive locality
guarantees that the hidden state at ``N_div - 1`` depends only on the shared
prefix, so feeding the ``a_V`` chat would yield the identical readout.

``build_text_only`` and ``build_vision_only`` produce the unimodal probes
the behavioral pipeline uses (``f"{passage} {question}"`` / no image, and
``f"{question}"`` / with image).

Position-extraction algorithm:
  1. ``apply_chat_template(tokenize=False, add_generation_prompt=True)`` on
     the prompt-only msgs emits the chat string. For Qwen-style models
     this contains one ``<|image_pad|>`` per image; for Gemma-style models
     this contains no image marker (the image block is inserted only at
     tokenize=True).
  2. The tokenizer (``return_offsets_mapping=True``) gives unexpanded ids
     and char offsets for that string; the passage's char span maps to a
     contiguous unexpanded token range.
  3. ``apply_chat_template(tokenize=True, return_dict=True, ...)`` on the
     a_T-augmented msgs returns the actual model input.
  4. ``adapter.build_un_to_exp`` produces the unexp -> [exp_idx, ...] map.
     For Qwen-style: each image_pad expands to N tokens per image_grid_thw.
     For Gemma-style: the unexp form has no image markers, so the map is
     1-to-1 except across the image-block insertion point in the expanded
     form. The map is computed against the prompt-only chat; the same
     expanded indices are valid in the full a_T chat because the prompt
     is a token-prefix of it.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import torch
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from attention.adapters import ModelAdapter


@dataclass
class ModelInput:
    inputs: dict                 # ready to feed to ``model(**inputs)``
    text_positions: list[int]    # expanded indices of passage tokens (or [])
    vision_positions: list[int]  # expanded indices of image-pad tokens (or [])
    answer_pos: int              # readout position (a = N_div - 1) within ``inputs``
    id_T_div: int
    id_V_div: int
    n_total: int                 # total expanded-token length of ``inputs["input_ids"]``
    debug: dict = field(default_factory=dict)


# ----------------------------------------------------------------------------
# Pre-skip filter (raw answers).
# ----------------------------------------------------------------------------

def answers_are_skippable(tokenizer, a_T: str, a_V: str) -> bool:
    """Return True if (a_T, a_V) cannot produce a meaningful FDT contrast.

    Skip-cases:
      * empty tokenizations,
      * identical tokenizations,
      * one tokenization is a strict prefix of the other (e.g. ``a_T="blue"``,
        ``a_V="bluish"``) -- the FDT walk would land on EOS vs continuation.
    """
    ids_T = tokenizer.encode(a_T.strip(), add_special_tokens=False)
    ids_V = tokenizer.encode(a_V.strip(), add_special_tokens=False)
    if not ids_T or not ids_V:
        return True
    n = min(len(ids_T), len(ids_V))
    return ids_T[:n] == ids_V[:n]


# ----------------------------------------------------------------------------
# Chat construction helpers.
# ----------------------------------------------------------------------------

def _user_msg(image: Optional[Image.Image], text: str,
              image_first: bool = True) -> dict:
    """Build the user-turn chat dict. ``image_first`` controls the order of
    the image block relative to the text block; the default matches Qwen-VL's
    canonical layout. Reversing the order is needed when probing the causal
    information flow from text positions into vision positions (vision
    residuals only see preceding tokens, so they encode text-dependent
    information only when text precedes the image)."""
    content = []
    if image is not None and image_first:
        content.append({"type": "image", "image": image})
    content.append({"type": "text", "text": text})
    if image is not None and not image_first:
        content.append({"type": "image", "image": image})
    return {"role": "user", "content": content}


def _assistant_msg(text: str) -> dict:
    return {"role": "assistant",
            "content": [{"type": "text", "text": text.strip()}]}


def _apply_template(processor, msgs, *, tokenize: bool, add_generation_prompt: bool):
    """Tiny wrapper that pins the template kwargs we always want."""
    return processor.apply_chat_template(
        msgs,
        tokenize=tokenize,
        add_generation_prompt=add_generation_prompt,
        return_dict=tokenize,
        return_tensors="pt" if tokenize else None,
        enable_thinking=False,
    )


def _find_divergence(ids_T: torch.Tensor, ids_V: torch.Tensor) -> Optional[int]:
    n = min(ids_T.shape[1], ids_V.shape[1])
    for k in range(n):
        if ids_T[0, k].item() != ids_V[0, k].item():
            return k
    return None


# ----------------------------------------------------------------------------
# Passage location.
# ----------------------------------------------------------------------------

# ----------------------------------------------------------------------------
# Builders: joint, text-only, vision-only.
# ----------------------------------------------------------------------------

def _build_with_positions(
    adapter: ModelAdapter,
    image: Optional[Image.Image],
    user_text: str,
    a_T: str,
    a_V: str,
    *,
    locate_passage: Optional[str] = None,
    image_first: bool = True,
    assistant_prefill: Optional[str] = None,
) -> Optional[ModelInput]:
    """Shared core for joint/text-only/vision-only builders.

    The returned ``ModelInput.inputs`` is the **a_T-augmented full chat**
    (assistant turn included), so the readout position ``N_div - 1`` is
    always inside the input even when both answers share their first
    content token.

    ``assistant_prefill`` (used by the Gemma3 prior probe) prepends a
    fixed answering frame to both candidates so the FDT divergence lands
    past the prefill, with the model already committed to an answer.
    """
    processor = adapter.processor
    tokenizer = adapter.tokenizer

    if assistant_prefill is not None:
        pf = assistant_prefill.strip()
        a_T_full = f"{pf} {a_T}"
        a_V_full = f"{pf} {a_V}"
    else:
        a_T_full = a_T
        a_V_full = a_V

    user = _user_msg(image, user_text, image_first=image_first)
    msgs_prompt = [user]
    msgs_T = msgs_prompt + [_assistant_msg(a_T_full)]
    msgs_V = msgs_prompt + [_assistant_msg(a_V_full)]

    # ---- positions on the prompt-only chat string ---------------------------
    chat_text = _apply_template(processor, msgs_prompt, tokenize=False,
                                add_generation_prompt=True)
    enc_un = tokenizer(
        chat_text,
        return_offsets_mapping=True,
        add_special_tokens=False,
        return_tensors=None,
    )
    ids_un = enc_un["input_ids"]
    offs = enc_un["offset_mapping"]

    prompt_inputs = _apply_template(processor, msgs_prompt, tokenize=True,
                                    add_generation_prompt=True)
    if not isinstance(prompt_inputs, dict):
        prompt_inputs = dict(prompt_inputs)
    n_prompt_exp = int(prompt_inputs["input_ids"].shape[1])
    ids_prompt_exp = prompt_inputs["input_ids"][0].tolist()

    if locate_passage is not None:
        text_positions = adapter.find_text_positions(
            chat_text=chat_text, ids_un=ids_un, offsets=offs,
            ids_exp=ids_prompt_exp, prompt_inputs=prompt_inputs,
            passage=locate_passage, image_first=image_first,
        )
    else:
        text_positions = []

    vision_positions: list[int] = []
    if image is not None:
        vision_positions = adapter.find_vision_positions(ids_prompt_exp)

    if set(text_positions) & set(vision_positions):
        raise RuntimeError("text_positions and vision_positions overlap.")

    # ---- FDT divergence on the full a_T / a_V chats -------------------------
    full_T = _apply_template(processor, msgs_T, tokenize=True,
                             add_generation_prompt=False)
    full_V = _apply_template(processor, msgs_V, tokenize=True,
                             add_generation_prompt=False)
    if not isinstance(full_T, dict):
        full_T = dict(full_T)
    if not isinstance(full_V, dict):
        full_V = dict(full_V)
    ids_T_full = full_T["input_ids"]
    ids_V_full = full_V["input_ids"]
    N_div = _find_divergence(ids_T_full, ids_V_full)
    if N_div is None or N_div == 0:
        return None
    answer_pos = N_div - 1
    id_T_div = int(ids_T_full[0, N_div].item())
    id_V_div = int(ids_V_full[0, N_div].item())

    # ---- assert prompt-only is a prefix of full_T ---------------------------
    n_full = int(ids_T_full.shape[1])
    if n_full < n_prompt_exp:
        raise RuntimeError(
            f"full_T length {n_full} < prompt-only length {n_prompt_exp}; "
            f"can't happen if the chat template is well-formed."
        )
    if not torch.equal(ids_T_full[0, :n_prompt_exp],
                       prompt_inputs["input_ids"][0]):
        raise RuntimeError(
            "Prompt-only chat is not a token-prefix of the full a_T chat. "
            "Position metadata derived from the prompt-only chat would be "
            "invalid in the full chat."
        )
    if answer_pos >= n_full:
        raise RuntimeError(
            f"answer_pos {answer_pos} is past full_T length {n_full}."
        )
    if answer_pos in text_positions or answer_pos in vision_positions:
        raise RuntimeError(
            f"answer_pos {answer_pos} overlaps with text/vision positions."
        )

    return ModelInput(
        inputs=full_T,
        text_positions=text_positions,
        vision_positions=vision_positions,
        answer_pos=answer_pos,
        id_T_div=id_T_div,
        id_V_div=id_V_div,
        n_total=n_full,
        debug={
            "chat_text_preview": chat_text[:120],
            "n_unexp": len(ids_un),
            "n_prompt_exp": n_prompt_exp,
            "n_full": n_full,
            "n_answer_prefix_shared": n_full - answer_pos - 1,
        },
    )


def build_joint(adapter: ModelAdapter, image: Image.Image, passage: str,
                question: str, a_T: str, a_V: str,
                image_first: bool = True) -> Optional[ModelInput]:
    """Joint probe: ``[image, passage + ' ' + question]`` (image-first by
    default) or ``[passage + ' ' + question, image]`` when ``image_first=False``.
    """
    user_text = f"{passage} {question}"
    return _build_with_positions(adapter, image, user_text, a_T, a_V,
                                 locate_passage=passage,
                                 image_first=image_first)


