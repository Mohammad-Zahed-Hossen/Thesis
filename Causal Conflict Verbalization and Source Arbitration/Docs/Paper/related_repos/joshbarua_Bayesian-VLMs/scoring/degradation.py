"""Image / text degradation helpers shared by the scoring callers.

`blur_image` and the text-variant loader live here because they describe the
input axes that VLMScorer operates over (the (blur_level, text_level) grid).
`get_grid_config` resolves a named preset + degradation type into the actual
sigma/level lists.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from PIL import Image, ImageFilter

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from config import (
    GRID_PRESETS,
    get_token_noise_labels,
)


def blur_image(image: Image.Image, sigma: int) -> Image.Image:
    """Apply Gaussian blur to an image. sigma=0 returns the original."""
    if sigma == 0:
        return image
    return image.filter(ImageFilter.GaussianBlur(radius=sigma))


def load_text_variants(text_degradation: str, split: str, grid: str) -> dict:
    """Load pre-generated token-noise text degradation variants for a split.

    Files are stored as ``text_degradations/token_noise_{grid}_{split}.json``
    (grid-suffixed); an unsuffixed ``token_noise_{split}.json`` is accepted as
    a fallback if the grid-suffixed file is absent.
    """
    deg_dir = Path(__file__).resolve().parent.parent / "text_degradations"
    candidates = [
        deg_dir / f"token_noise_{grid}_{split}.json",
        deg_dir / f"{text_degradation}_{split}.json",
    ]
    deg_path = next((p for p in candidates if p.exists()), None)
    if deg_path is None:
        raise FileNotFoundError(
            f"Text degradations not found. Tried:\n"
            + "\n".join(f"  {p}" for p in candidates)
            + f"\nRun generate_text_degradations.py --grid {grid} first."
        )
    print(f"  Loaded text degradations from: {deg_path}")
    with open(deg_path) as f:
        return json.load(f)


def get_grid_config(grid_name: str, text_degradation: str = "token_noise"):
    """Return (blur_sigmas, text_levels, text_labels) for the given grid.

    Only token-noise text degradation is supported: text levels are
    0 (original) plus one per non-zero token-noise probability in the preset.
    """
    preset = GRID_PRESETS[grid_name]
    blur_sigmas = preset["blur_sigmas"]

    text_labels = get_token_noise_labels(grid_name)
    text_levels = list(range(len(text_labels)))
    return blur_sigmas, text_levels, text_labels
