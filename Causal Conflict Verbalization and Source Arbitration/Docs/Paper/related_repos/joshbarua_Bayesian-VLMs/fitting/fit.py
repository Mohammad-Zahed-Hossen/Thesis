"""Unified entry point for fitting one or more fusion models.

`fit_models` accepts already-partitioned (train_df, val_df, test_df) and a list
of model names, and returns `{name: {"params", "history", "metrics"}}`. The
existing callers in model/fit_and_eval.py and transitions/fit_degraded.py keep
their own orchestration and call `train_model` / `evaluate_split` directly;
this wrapper is for new callers that just want fitted params.

Model registry (nn.Module fusion classes):
    "additive_logodds"      -> AdditiveLogOddsModel
    "four_term_additive"    -> FourTermAdditiveFusionModel
    "bayesian_gated"        -> BayesianGatedFusionModel
    "four_term_gated"       -> FourTermGatedFusionModel
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import torch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from config import DEFAULT_EPOCHS, DEFAULT_LR

from .models import (
    AdditiveLogOddsModel,
    BayesianGatedFusionModel,
    FourTermAdditiveFusionModel,
    FourTermGatedFusionModel,
)
from .train import (
    _compute_metrics,
    _extract_model_inputs,
    evaluate_split,
    train_model,
)


_MODEL_REGISTRY: dict[str, type] = {
    "additive_logodds": AdditiveLogOddsModel,
    "four_term_additive": FourTermAdditiveFusionModel,
    "bayesian_gated": BayesianGatedFusionModel,
    "four_term_gated": FourTermGatedFusionModel,
}


def fit_models(
    train_df: pd.DataFrame,
    val_df: pd.DataFrame,
    test_df: pd.DataFrame | None = None,
    models: tuple[str, ...] = (
        "additive_logodds",
        "four_term_additive",
        "bayesian_gated",
        "four_term_gated",
    ),
    lr: float = DEFAULT_LR,
    epochs: int = DEFAULT_EPOCHS,
    device: str = "cpu",
) -> dict[str, dict]:
    """Fit each requested fusion model on (train_df, val_df) and (optionally)
    score it on test_df.

    Returns:
        {
          "additive_logodds":   {"params": {...}, "history": {...},
                                 "metrics_test": {...} | None,
                                 "model": <fitted nn.Module>},
          ...
        }
    """
    results: dict[str, dict] = {}
    for name in models:
        if name not in _MODEL_REGISTRY:
            raise ValueError(
                f"Unknown model {name!r}; expected one of {tuple(_MODEL_REGISTRY)}"
            )
        cls = _MODEL_REGISTRY[name]
        model = cls()
        history, best_params = train_model(
            model, train_df, val_df, lr=lr, epochs=epochs, device=device,
        )
        if best_params is None:
            results[name] = {"params": None, "history": history, "metrics_test": None,
                             "model": None}
            continue
        model.load_params_dict(best_params)

        metrics_test = None
        if test_df is not None and len(test_df) > 0:
            inputs = _extract_model_inputs(model, test_df, device)
            y = torch.tensor(test_df["y"].values, dtype=torch.float32, device=device)
            model.eval()
            with torch.no_grad():
                y_hat = model(*inputs)
            metrics_test = _compute_metrics(y, y_hat)

        results[name] = {
            "params": best_params,
            "history": history,
            "metrics_test": metrics_test,
            "model": model,
        }
    return results
