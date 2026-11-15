"""Adapter for Qwen3.5-4B (model_type=qwen3_5).

Empirically (probe of Qwen/Qwen3.5-4B at HEAD):
  * Same special-token *strings* as Qwen2.5-VL (<|vision_start|>,
    <|vision_end|>, <|image_pad|>, <|im_start|>, <|im_end|>) but
    different *integer ids* (vocab_size 248044 vs 151643).
  * Same image expansion model: image_grid_thw is present in processor
    output; expansion divisor = vision_config.spatial_merge_size**2 (=4).
  * Same vision-tower Conv3d patch_embed shape; needs the same fp32
    promotion (subclass inherits it).

So the adapter is a thin subclass of Qwen2.5-VL; only `matches` differs.
"""

from __future__ import annotations

from .qwen2_5_vl import Qwen2_5_VLAdapter


class Qwen3_5Adapter(Qwen2_5_VLAdapter):
    name = "qwen3_5"

    @classmethod
    def matches(cls, config) -> bool:
        return getattr(config, "model_type", None) == "qwen3_5"
