"""ModelAdapter ABC + shared defaults.

Each adapter declares the *string names* of the special tokens it cares
about; the base class resolves them to integer ids via the tokenizer at
construction time. This avoids brittle hardcoded ids that drift across
tokenizer-versions or model variants with the same architecture but
different vocabularies (e.g. Qwen2.5 vs Qwen3.5).

Subclasses can override:
  * `matches(config)`       -- registry dispatch on model_type
  * `_init_extra(config)`   -- per-arch config reads (e.g. spatial_merge)
  * `expanded_image_token_count(prompt_inputs)` -- per-image expansion list
  * `optimize_vision_tower(model)` -- arch-specific vision-tower fixups
  * `get_decoder_layers(model)`    -- override only if the multi-path
                                       fallback below misses

Position-finding (vision_positions in the expanded ids and the
unexp -> exp position map) is implemented in the base class with two
algorithms covering both Qwen-style ("one image_pad placeholder per
image in the unexpanded form") and Gemma-style ("no image marker in
the unexpanded form; image block inserted at tokenization time").
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

import torch


def _passage_unexp_token_indices(adapter, chat_text: str, ids_un: list[int],
                                 offsets: list[tuple[int, int]],
                                 passage: str,
                                 image_first: bool = True) -> list[int]:
    """Char-offset based locator for the passage span in the prompt-only
    chat text. Used by the default Qwen-style find_text_positions.

    When ``image_first=False`` the passage precedes the image block, so we
    search the entire chat_text rather than the post-vision_end suffix."""
    search_start = (adapter.passage_search_start(chat_text, ids_un, offsets)
                    if image_first else 0)
    p_start = chat_text.find(passage, search_start)
    if p_start < 0:
        raise RuntimeError(
            f"Passage substring not found in chat_text suffix "
            f"(search_start={search_start}). Passage[:60]={passage[:60]!r}"
        )
    if chat_text.find(passage, p_start + 1) >= 0:
        raise RuntimeError(
            f"Passage occurs more than once after search_start; cannot "
            f"disambiguate. Passage[:60]={passage[:60]!r}"
        )
    p_end = p_start + len(passage)
    return [k for k, (a, b) in enumerate(offsets)
            if (a, b) != (0, 0) and a >= p_start and b <= p_end]


class ModelAdapter(ABC):
    """Per-architecture configuration for the patching pipeline."""

    name: str = "<base>"

    # Special-token names. Subclasses must set image_pad_token; vision
    # bracket tokens are optional (used by find_vision_positions when
    # available, otherwise we fall back to scanning for image_pad runs).
    image_pad_token: str = ""
    vision_start_token: Optional[str] = None
    vision_end_token: Optional[str] = None
    im_start_token: Optional[str] = None
    im_end_token: Optional[str] = None

    # ------------------------------------------------------------------
    # Construction.
    # ------------------------------------------------------------------

    @classmethod
    @abstractmethod
    def matches(cls, config) -> bool:
        """Return True iff this adapter handles models with `config`."""

    def __init__(self, processor, config):
        self.processor = processor
        self.tokenizer = processor.tokenizer
        self.config = config

        self.image_pad_id = self._resolve(self.image_pad_token, required=True)
        self.vision_start_id = self._resolve(self.vision_start_token, required=False)
        self.vision_end_id = self._resolve(self.vision_end_token, required=False)
        self.im_start_id = self._resolve(self.im_start_token, required=False)
        self.im_end_id = self._resolve(self.im_end_token, required=False)

        if (self.vision_start_id is None) != (self.vision_end_id is None):
            raise RuntimeError(
                f"{self.name}: vision_start and vision_end must both be "
                f"defined or both be None."
            )

        self._init_extra(config)

    def _resolve(self, name: Optional[str], *, required: bool) -> Optional[int]:
        if not name:
            return None
        tid = self.tokenizer.convert_tokens_to_ids(name)
        unk = getattr(self.tokenizer, "unk_token_id", None)
        if tid is None or (unk is not None and tid == unk):
            if required:
                raise RuntimeError(
                    f"{self.name} adapter could not resolve required special "
                    f"token {name!r} via tokenizer.convert_tokens_to_ids."
                )
            return None
        return int(tid)

    def _init_extra(self, config) -> None:
        """Hook for per-arch config reads. Default no-op."""
        pass

    # ------------------------------------------------------------------
    # Image-token expansion.
    # ------------------------------------------------------------------

    @abstractmethod
    def expanded_image_token_counts(self, prompt_inputs: dict) -> list[int]:
        """Return [n_exp_for_image_0, ...] for the images in prompt_inputs.

        Used to translate one unexpanded image-marker token into N
        expanded image-pad tokens. Empty list if there are no images.
        For Qwen-style: read image_grid_thw and apply (T*H*W)/merge².
        For Gemma-style: the prompt_inputs may not carry image_grid_thw;
        infer from the expanded ids (count of image_pad tokens / image)."""

    # ------------------------------------------------------------------
    # Position finding in the expanded ids.
    # ------------------------------------------------------------------

    def find_vision_positions(self, ids_exp: list[int]) -> list[int]:
        """Return expanded-token positions of the image (image_pad) tokens.

        Default: bracket via vision_start/vision_end. Falls back to a
        direct scan for image_pad if no brackets are defined.
        """
        if self.vision_start_id is None or self.vision_end_id is None:
            return [i for i, t in enumerate(ids_exp) if t == self.image_pad_id]
        starts = [i for i, t in enumerate(ids_exp) if t == self.vision_start_id]
        ends = [i for i, t in enumerate(ids_exp) if t == self.vision_end_id]
        if len(starts) != len(ends):
            raise RuntimeError(
                f"{self.name}: vision_start ({len(starts)}) and vision_end "
                f"({len(ends)}) counts disagree."
            )
        out: list[int] = []
        for s, e in zip(starts, ends):
            out.extend(range(s + 1, e))
        return out

    def passage_search_start(self, chat_text: str, ids_un: list[int],
                             offsets: list[tuple[int, int]]) -> int:
        """Char offset in chat_text from which to search for the passage
        substring. Default: end of the last vision_end token if any,
        else 0."""
        if self.vision_end_id is None:
            return 0
        search_start = 0
        for i, tok in enumerate(ids_un):
            if tok == self.vision_end_id:
                search_start = offsets[i][1]
        return search_start

    def find_text_positions(self, *, chat_text: str, ids_un: list[int],
                            offsets: list[tuple[int, int]],
                            ids_exp: list[int], prompt_inputs: dict,
                            passage: str,
                            image_first: bool = True) -> list[int]:
        """Return expanded-token positions of the passage span.

        Default implementation: char-offset based. Find passage substring
        in chat_text (the apply_chat_template(tokenize=False) output);
        translate the char span to unexpanded token indices via offsets;
        translate unexp -> exp via build_un_to_exp.

        Works cleanly when `apply_chat_template(tokenize=False)` produces
        a token sequence that is a strict prefix of (or aligns with) the
        tokenized output up to image-block expansion. Holds for Qwen-VL
        models. Subclasses override for architectures where the two
        tokenizations diverge in non-image ways (Gemma-3 inserts extra
        whitespace + omits the image expansion + omits vision_end in the
        unexp form, so we use direct subsequence matching there).
        """
        unexp_text = _passage_unexp_token_indices(
            self, chat_text, ids_un, offsets, passage, image_first=image_first
        )
        un_to_exp = self._build_un_to_exp_qwen_style(ids_un, ids_exp, prompt_inputs)
        return sorted({e for k in unexp_text for e in un_to_exp[k]})

    def _build_un_to_exp_qwen_style(self, ids_un, ids_exp, prompt_inputs) -> list[list[int]]:
        """Each `image_pad_id` token in ids_un maps to a run of
        `expanded_image_token_counts(prompt_inputs)[img_idx]` tokens in
        ids_exp; non-image tokens map 1-to-1 in order. Used by the default
        Qwen-style path of `find_text_positions`."""
        n_per_img = self.expanded_image_token_counts(prompt_inputs)
        n_total_exp = len(ids_exp)
        un_to_exp: list[list[int]] = []
        exp_idx = 0
        img_idx = 0
        for tok in ids_un:
            if tok == self.image_pad_id:
                if img_idx >= len(n_per_img):
                    raise RuntimeError(
                        f"{self.name}: image_pad #{img_idx + 1} in ids_un but "
                        f"only {len(n_per_img)} expansion counts available."
                    )
                run = n_per_img[img_idx]
                un_to_exp.append(list(range(exp_idx, exp_idx + run)))
                exp_idx += run
                img_idx += 1
            else:
                un_to_exp.append([exp_idx])
                exp_idx += 1
        if exp_idx != n_total_exp:
            raise RuntimeError(
                f"{self.name}: unexp->exp walk reached {exp_idx} but expanded "
                f"length is {n_total_exp}; position map is wrong."
            )
        return un_to_exp

    def find_passage_by_subsequence(self, ids_exp: list[int], passage: str,
                                    *, restrict_after: int = 0) -> list[int]:
        """Locate `passage` in `ids_exp[restrict_after:]` by matching
        candidate standalone tokenizations as a contiguous subsequence.

        Useful for adapters whose unexp/exp tokenizations diverge in
        non-image ways (Gemma-3). Tries plain and leading-space
        tokenizations to handle BPE/SentencePiece boundary effects.
        Raises if zero or >1 matches.
        """
        candidates = []
        for prefix in ("", " "):
            ids = self.tokenizer.encode(prefix + passage, add_special_tokens=False)
            if ids and ids not in candidates:
                candidates.append(ids)
        last_err = None
        for cand in candidates:
            n = len(cand)
            matches = [i for i in range(restrict_after, len(ids_exp) - n + 1)
                       if ids_exp[i:i + n] == cand]
            if len(matches) == 1:
                return list(range(matches[0], matches[0] + n))
            if len(matches) > 1:
                last_err = (f"passage matches {len(matches)} positions in "
                            f"expanded ids ({matches[:3]}...) with candidate "
                            f"len={n}; cannot disambiguate.")
                continue
            last_err = (f"passage tokens (len={n}) not found in expanded ids "
                        f"after pos {restrict_after}.")
        raise RuntimeError(
            f"{self.name}: find_passage_by_subsequence failed. {last_err}"
        )

    # ------------------------------------------------------------------
    # Vision-tower / decoder-layer access.
    # ------------------------------------------------------------------

    def optimize_vision_tower(self, model) -> None:
        """No-op default. Subclasses override (e.g. Qwen2.5-VL Conv3d)."""
        pass

    def get_decoder_layers(self, model):
        """Locate the transformer decoder layer stack on a HF VLM model.

        Tries several common nesting patterns. Subclasses can override
        if their architecture sits at a non-standard path.
        """
        candidates = [
            ("model", "language_model", "layers"),
            ("language_model", "model", "layers"),
            ("language_model", "layers"),
            ("model", "layers"),
            ("model", "decoder", "layers"),
        ]
        for path in candidates:
            obj = model
            ok = True
            for attr in path:
                if not hasattr(obj, attr):
                    ok = False
                    break
                obj = getattr(obj, attr)
            if ok and hasattr(obj, "__len__") and hasattr(obj, "__iter__"):
                return obj
        raise AttributeError(
            f"{self.name}: could not locate decoder layers on model "
            f"(tried {candidates})."
        )
