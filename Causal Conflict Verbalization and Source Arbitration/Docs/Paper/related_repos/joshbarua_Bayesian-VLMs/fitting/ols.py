"""Closed-form OLS path for fitting linear-in-(m, s_T, s_V) models on
arbitrary cell supports (corner / L-shape / grid).

Used by the steering pipeline (intrinsic/) to fit
    s_J = a*m + b + beta_T*s_T + beta_V*s_V
on the L-shape and predict the interior; can also serve any other linear
model in the fusion family that does not need a softplus reparameterization.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def design(df: pd.DataFrame, terms: list[str]) -> np.ndarray:
    """Build design matrix with a leading intercept column + requested terms."""
    cols = [np.ones(len(df))]
    for t in terms:
        if t == "m":
            cols.append(df["m"].to_numpy(dtype=np.float64))
        elif t == "s_T":
            cols.append(df["s_T"].to_numpy(dtype=np.float64))
        elif t == "s_V":
            cols.append(df["s_V"].to_numpy(dtype=np.float64))
        elif t == "m*s_T":
            cols.append((df["m"].to_numpy(dtype=np.float64)
                         * df["s_T"].to_numpy(dtype=np.float64)))
        elif t == "m*s_V":
            cols.append((df["m"].to_numpy(dtype=np.float64)
                         * df["s_V"].to_numpy(dtype=np.float64)))
        else:
            raise ValueError(f"Unknown term: {t}")
    return np.column_stack(cols)


def ols(X: np.ndarray, y: np.ndarray) -> np.ndarray:
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    return beta


def _r2_rmse(y_true: np.ndarray, y_pred: np.ndarray) -> dict:
    ss_res = float(np.sum((y_true - y_pred) ** 2))
    ss_tot = float(np.sum((y_true - y_true.mean()) ** 2))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else float("nan")
    rmse = float(np.sqrt(ss_res / len(y_true)))
    return {"r2": r2, "rmse": rmse, "n": int(len(y_true))}


def cell_masks(df: pd.DataFrame) -> tuple[np.ndarray, np.ndarray]:
    """Return (l_shape_mask, interior_mask) for train/test on the (blur, text) grid.

    L-shape  = {(sigma, 0)} U {(0, p)}  -- the single-modality axes (includes (0,0))
    Interior = {(sigma > 0) and (p > 0)} -- the jointly-degraded cells
    """
    blur = df["blur_level"].to_numpy()
    text = df["text_level"].to_numpy()
    l_shape = (blur == 0) | (text == 0)
    interior = (blur != 0) & (text != 0)
    return l_shape, interior


def cell_split_eval(df: pd.DataFrame, terms: list[str]) -> dict:
    """Fit OLS on the L-shape, evaluate on the interior.

    Returns in-sample (L-shape) and held-out (interior) per-row R^2 / RMSE
    plus the fitted coefficients.
    """
    l_mask, i_mask = cell_masks(df)
    if l_mask.sum() == 0:
        raise RuntimeError("No L-shape cells in dataframe; cannot fit.")
    if i_mask.sum() == 0:
        raise RuntimeError("No interior cells in dataframe; nothing to evaluate on.")

    y = df["s_J"].to_numpy(dtype=np.float64)
    X = design(df, terms)
    beta = ols(X[l_mask], y[l_mask])
    yhat = X @ beta

    names = ["intercept"] + list(terms)
    coefs = dict(zip(names, [float(b) for b in beta]))
    return {
        "coefs": coefs,
        "train_cells": "L-shape {(sigma,0)} U {(0,p)}",
        "test_cells": "interior {sigma>0 and p>0}",
        "in_sample": _r2_rmse(y[l_mask], yhat[l_mask]),
        "held_out": _r2_rmse(y[i_mask], yhat[i_mask]),
    }
