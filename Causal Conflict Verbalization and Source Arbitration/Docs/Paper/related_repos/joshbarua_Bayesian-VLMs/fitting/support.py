"""Cell-support modes for fitting and evaluation on the (blur, text-noise) grid.

Three canonical fit-time supports, each of which selects which (blur_level,
text_level) cells are included for training. **L_shape includes the (0,0)
corner** — this is the standardised definition.

    corner    {(0, 0)}                                       single cell
    L_shape   {(blur, text) : blur == 0 OR text == 0}        single-modality axes + corner
    grid      all rows                                       full 2D grid

Use `select_train_mask` to pick training cells and `select_test_mask` to pick
held-out cells (the natural complement / split for each support).
"""

from __future__ import annotations

import numpy as np
import pandas as pd


SUPPORT_MODES = ("corner", "L_shape", "grid")


def _validate(support: str) -> None:
    if support not in SUPPORT_MODES:
        raise ValueError(f"Unknown support {support!r}; expected one of {SUPPORT_MODES}")


def _blur_text_cols(df: pd.DataFrame) -> tuple[np.ndarray, np.ndarray]:
    """Return (blur_level, text_level) arrays. If the columns are absent
    (e.g. an undegraded scores.parquet), treat all rows as the (0,0) corner."""
    n = len(df)
    blur = df["blur_level"].to_numpy() if "blur_level" in df.columns else np.zeros(n, dtype=int)
    text = df["text_level"].to_numpy() if "text_level" in df.columns else np.zeros(n, dtype=int)
    return blur, text


def select_train_mask(df: pd.DataFrame, support: str) -> np.ndarray:
    """Boolean mask selecting the rows used for training under `support`."""
    _validate(support)
    blur, text = _blur_text_cols(df)
    if support == "corner":
        return (blur == 0) & (text == 0)
    if support == "L_shape":
        return (blur == 0) | (text == 0)
    return np.ones(len(df), dtype=bool)


def select_test_mask(df: pd.DataFrame, support: str) -> np.ndarray:
    """Boolean mask selecting the held-out rows for evaluation under `support`.

    By convention:
      corner   -> all non-corner cells
      L_shape  -> the interior {(blur, text) : blur > 0 AND text > 0}
      grid     -> all rows (caller usually composes with an external split)
    """
    _validate(support)
    blur, text = _blur_text_cols(df)
    if support == "corner":
        return ~((blur == 0) & (text == 0))
    if support == "L_shape":
        return (blur != 0) & (text != 0)
    return np.ones(len(df), dtype=bool)
