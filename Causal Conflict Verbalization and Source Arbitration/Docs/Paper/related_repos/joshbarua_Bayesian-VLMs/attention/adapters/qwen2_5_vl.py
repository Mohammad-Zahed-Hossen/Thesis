"""Adapter for Qwen2.5-VL (model_type=qwen2_5_vl)."""

from __future__ import annotations

import torch

from .base import ModelAdapter


class Qwen2_5_VLAdapter(ModelAdapter):
    name = "qwen2_5_vl"
    image_pad_token = "<|image_pad|>"
    vision_start_token = "<|vision_start|>"
    vision_end_token = "<|vision_end|>"
    im_start_token = "<|im_start|>"
    im_end_token = "<|im_end|>"
    unexp_has_image_marker = True  # one <|image_pad|> per image in unexp form

    @classmethod
    def matches(cls, config) -> bool:
        return getattr(config, "model_type", None) == "qwen2_5_vl"

    def _init_extra(self, config) -> None:
        # vision_config.spatial_merge_size is the per-axis merge factor
        # (=2 for Qwen2.5-VL); the expansion divisor is its square.
        vc = getattr(config, "vision_config", None)
        merge = getattr(vc, "spatial_merge_size", None) if vc is not None else None
        if merge is None:
            merge = 2  # Qwen2.5-VL default
        self.spatial_merge = int(merge)
        self._expansion_divisor = self.spatial_merge ** 2

    def expanded_image_token_counts(self, prompt_inputs: dict) -> list[int]:
        thw = prompt_inputs.get("image_grid_thw", None)
        if thw is None:
            return []
        out: list[int] = []
        for g in thw:
            out.append(int(g.prod().item()) // self._expansion_divisor)
        return out

    def optimize_vision_tower(self, model) -> None:
        """Cast Qwen2.5-VL's vision-tower Conv3d patch_embed to fp32 with
        input/output dtype shims; works around a ~6000x slowdown in cuDNN's
        half-precision Conv3d fallback for the (k=stride=(2,16,16), in=3)
        shape."""
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
        print(f"  [adapter:{self.name}] promoted patch_embed.proj to fp32 "
              f"(was {in_dtype})")
