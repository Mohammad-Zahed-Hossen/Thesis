"""Training loop, evaluation, loss/metric helpers, and parameter diagnostics
for the four nn.Module fusion classes."""

from __future__ import annotations

import sys
from collections import defaultdict
from pathlib import Path

import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from tqdm import tqdm

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from config import DEFAULT_EPOCHS, DEFAULT_LR, EPS, MARGIN_CLIP

from .models import (
    AdditiveLogOddsModel,
    BayesianGatedFusionModel,
    FourTermAdditiveFusionModel,
    FourTermGatedFusionModel,
)


# ============================================================================
# Loss and Metrics
# ============================================================================

def binary_cross_entropy(y: torch.Tensor, y_hat: torch.Tensor) -> torch.Tensor:
    """
    Compute binary cross-entropy: CE(y, y_hat) = -(y log y_hat + (1-y) log(1 - y_hat))
    """
    y_hat = torch.clamp(y_hat, EPS, 1 - EPS)
    ce = -(y * torch.log(y_hat) + (1 - y) * torch.log(1 - y_hat))
    return ce.mean()


def compute_kl(p: torch.Tensor, q: torch.Tensor) -> torch.Tensor:
    """Compute mean KL(P || Q) for Bernoulli distributions."""
    p = torch.clamp(p, EPS, 1 - EPS)
    q = torch.clamp(q, EPS, 1 - EPS)
    kl = p * torch.log(p / q) + (1 - p) * torch.log((1 - p) / (1 - q))
    return kl.mean()


def compute_symmetrized_kl(p: torch.Tensor, q: torch.Tensor) -> torch.Tensor:
    """Compute mean symmetrized KL for Bernoulli distributions."""
    return 0.5 * (compute_kl(p, q) + compute_kl(q, p))


def compute_argmax_match(p: torch.Tensor, q: torch.Tensor) -> float:
    """Compute argmax agreement rate between two Bernoulli parameters."""
    pred_label = (p > 0.5).float()
    obs_label = (q > 0.5).float()
    return (pred_label == obs_label).float().mean().item()


# ============================================================================
# Training
# ============================================================================

def _extract_model_inputs(
    model: nn.Module,
    df: pd.DataFrame,
    device: str = "cpu",
) -> tuple:
    """Extract the right input tensors for a model from a DataFrame."""
    if isinstance(model, (FourTermGatedFusionModel, FourTermAdditiveFusionModel)):
        return (
            torch.tensor(df["ll_text_T"].values, dtype=torch.float32, device=device),
            torch.tensor(df["ll_text_V"].values, dtype=torch.float32, device=device),
            torch.tensor(df["ll_vision_T"].values, dtype=torch.float32, device=device),
            torch.tensor(df["ll_vision_V"].values, dtype=torch.float32, device=device),
        )
    else:
        return (
            torch.tensor(df["x_T"].values, dtype=torch.float32, device=device),
            torch.tensor(df["x_V"].values, dtype=torch.float32, device=device),
        )


def train_model(
    model: nn.Module,
    train_df: pd.DataFrame,
    val_df: pd.DataFrame,
    lr: float = DEFAULT_LR,
    epochs: int = DEFAULT_EPOCHS,
    patience: int = 100,
    device: str = "cpu",
) -> tuple[dict, dict]:
    """
    Train a fusion model (AdditiveLogOddsModel, BayesianGatedFusionModel,
    FourTermAdditiveFusionModel, or FourTermGatedFusionModel).

    Returns:
        history: Training history (train_loss, val_loss per epoch)
        best_params: Best parameters by validation loss
    """
    train_inputs = _extract_model_inputs(model, train_df, device)
    val_inputs = _extract_model_inputs(model, val_df, device)
    y_train = torch.tensor(train_df["y"].values, dtype=torch.float32, device=device)
    y_val = torch.tensor(val_df["y"].values, dtype=torch.float32, device=device)

    model = model.to(device)
    optimizer = optim.LBFGS(model.parameters(), lr=lr, max_iter=20, history_size=10)

    history = defaultdict(list)
    best_val_loss = float("inf")
    best_params = None
    patience_counter = 0

    pbar = tqdm(range(epochs), desc=f"Training {model.__class__.__name__}")
    for epoch in pbar:

        def closure():
            optimizer.zero_grad()
            y_hat = model(*train_inputs)
            loss = binary_cross_entropy(y_train, y_hat)
            loss.backward()
            return loss

        optimizer.step(closure)

        model.eval()
        with torch.no_grad():
            y_hat_train = model(*train_inputs)
            train_loss = binary_cross_entropy(y_train, y_hat_train).item()

            y_hat_val = model(*val_inputs)
            val_loss = binary_cross_entropy(y_val, y_hat_val).item()
        model.train()

        history["train_loss"].append(train_loss)
        history["val_loss"].append(val_loss)

        if val_loss < best_val_loss:
            best_val_loss = val_loss
            best_params = model.get_params_dict()
            patience_counter = 0
        else:
            patience_counter += 1

        postfix = {"train": f"{train_loss:.4f}", "val": f"{val_loss:.4f}"}
        postfix.update(model.get_training_postfix())
        pbar.set_postfix(postfix)

        if patience_counter >= patience:
            print(f"\nEarly stopping at epoch {epoch}")
            break

    return dict(history), best_params


# ============================================================================
# Evaluation
# ============================================================================

def _compute_metrics(y: torch.Tensor, y_hat: torch.Tensor) -> dict:
    """Compute standard match metrics for a single predictor vs target."""
    return {
        "mean_kl": compute_kl(y, y_hat).item(),
        "mean_skl": compute_symmetrized_kl(y, y_hat).item(),
        "argmax_pct": compute_argmax_match(y, y_hat),
        "mean_ce": binary_cross_entropy(y, y_hat).item(),
    }


def evaluate_split(
    logodds_model: AdditiveLogOddsModel,
    gated_model: BayesianGatedFusionModel,
    four_term_model: FourTermGatedFusionModel,
    df: pd.DataFrame,
    device: str = "cpu",
    four_term_additive_model: FourTermAdditiveFusionModel | None = None,
) -> dict:
    """
    Evaluate all models against the joint probe and unimodal baselines.

    Returns metrics for: additive_log_odds, gated_fusion, four_term_gated_fusion,
    four_term_additive_fusion (if provided), text_probe, vision_probe.
    """
    s_T = torch.tensor(df["x_T"].values, dtype=torch.float32, device=device)
    s_V = torch.tensor(df["x_V"].values, dtype=torch.float32, device=device)
    y = torch.tensor(df["y"].values, dtype=torch.float32, device=device)
    p_T = torch.tensor(df["p_T"].values, dtype=torch.float32, device=device)
    p_V = torch.tensor(df["p_V"].values, dtype=torch.float32, device=device)

    ll_TT = torch.tensor(df["ll_text_T"].values, dtype=torch.float32, device=device)
    ll_TV = torch.tensor(df["ll_text_V"].values, dtype=torch.float32, device=device)
    ll_VT = torch.tensor(df["ll_vision_T"].values, dtype=torch.float32, device=device)
    ll_VV = torch.tensor(df["ll_vision_V"].values, dtype=torch.float32, device=device)

    logodds_model.eval()
    gated_model.eval()
    four_term_model.eval()
    with torch.no_grad():
        y_hat_lo = logodds_model(s_T, s_V)
        y_hat_gate = gated_model(s_T, s_V)
        y_hat_4t = four_term_model(ll_TT, ll_TV, ll_VT, ll_VV)

    results = {
        "additive_log_odds": _compute_metrics(y, y_hat_lo),
        "gated_fusion": _compute_metrics(y, y_hat_gate),
        "four_term_gated_fusion": _compute_metrics(y, y_hat_4t),
        "text_probe": _compute_metrics(y, p_T),
        "vision_probe": _compute_metrics(y, p_V),
    }

    if four_term_additive_model is not None:
        four_term_additive_model.eval()
        with torch.no_grad():
            y_hat_4ta = four_term_additive_model(ll_TT, ll_TV, ll_VT, ll_VV)
        results["four_term_additive_fusion"] = _compute_metrics(y, y_hat_4ta)

    return results


# ============================================================================
# Diagnostics
# ============================================================================

def print_gate_diagnostics(
    model: BayesianGatedFusionModel,
    df: pd.DataFrame,
    split_name: str = "train",
    device: str = "cpu",
):
    """
    Print Bayesian strategy-selection diagnostics for the gate.

    Catches "not actually switching" immediately:
      - w histogram + % near 0 and % near 1
      - Corr(evidence_diff, w) should be positive if beta >= 0
    """
    s_T = torch.tensor(df["x_T"].values, dtype=torch.float32, device=device)
    s_V = torch.tensor(df["x_V"].values, dtype=torch.float32, device=device)

    model.eval()
    with torch.no_grad():
        _, w, evidence_diff = model.forward_with_gate(s_T, s_V)
        w_np = w.cpu().numpy()
        ev_diff_np = evidence_diff.cpu().numpy()

    print(f"\n  GATE DIAGNOSTICS ({split_name}, n={len(df)}):")
    print(f"    w = P(S=text | evidence)")
    print(f"    w stats:       mean={w_np.mean():.4f}, std={w_np.std():.4f}, "
          f"min={w_np.min():.4f}, max={w_np.max():.4f}")
    print(f"    w < 0.1:       {(w_np < 0.1).mean():.1%}  (vision-dominant)")
    print(f"    w > 0.9:       {(w_np > 0.9).mean():.1%}  (text-dominant)")
    print(f"    0.3<=w<=0.7:   {((w_np >= 0.3) & (w_np <= 0.7)).mean():.1%}  (mixed)")
    print(f"    |s_T|-|s_V|:   mean={ev_diff_np.mean():.4f}, std={ev_diff_np.std():.4f}")
    corr = np.corrcoef(ev_diff_np, w_np)[0, 1]
    print(f"    Corr(|s_T|-|s_V|, w): {corr:.4f}  {'(OK)' if corr > 0 else '(WARN: negative)'}")


def print_four_term_gate_diagnostics(
    model: FourTermGatedFusionModel,
    df: pd.DataFrame,
    split_name: str = "train",
    device: str = "cpu",
):
    """Print 4-term gate diagnostics."""
    ll_TT = torch.tensor(df["ll_text_T"].values, dtype=torch.float32, device=device)
    ll_TV = torch.tensor(df["ll_text_V"].values, dtype=torch.float32, device=device)
    ll_VT = torch.tensor(df["ll_vision_T"].values, dtype=torch.float32, device=device)
    ll_VV = torch.tensor(df["ll_vision_V"].values, dtype=torch.float32, device=device)

    model.eval()
    with torch.no_grad():
        _, w, gate_logit = model.forward_with_gate(ll_TT, ll_TV, ll_VT, ll_VV)
        w_np = w.cpu().numpy()
        gl_np = gate_logit.cpu().numpy()

    print(f"\n  4-TERM GATE DIAGNOSTICS ({split_name}, n={len(df)}):")
    print(f"    w = P(S=text | 4 LLs)")
    print(f"    w stats:       mean={w_np.mean():.4f}, std={w_np.std():.4f}, "
          f"min={w_np.min():.4f}, max={w_np.max():.4f}")
    print(f"    w < 0.1:       {(w_np < 0.1).mean():.1%}  (vision-dominant)")
    print(f"    w > 0.9:       {(w_np > 0.9).mean():.1%}  (text-dominant)")
    print(f"    0.3<=w<=0.7:   {((w_np >= 0.3) & (w_np <= 0.7)).mean():.1%}  (mixed)")
    print(f"    gate logit η:  mean={gl_np.mean():.4f}, std={gl_np.std():.4f}")


def print_logodds_diagnostics(
    model: AdditiveLogOddsModel,
    df: pd.DataFrame,
    split_name: str = "train",
    device: str = "cpu",
):
    """Print additive log-odds model diagnostics."""
    s_T = torch.tensor(df["x_T"].values, dtype=torch.float32, device=device)
    s_V = torch.tensor(df["x_V"].values, dtype=torch.float32, device=device)

    model.eval()
    with torch.no_grad():
        s_T_clip = s_T.clamp(-MARGIN_CLIP, MARGIN_CLIP)
        s_V_clip = s_V.clamp(-MARGIN_CLIP, MARGIN_CLIP)
        s_hat = model.b + model.beta_T * s_T_clip + model.beta_V * s_V_clip
        p_hat = torch.sigmoid(s_hat)
        p_hat_np = p_hat.cpu().numpy()
        s_hat_np = s_hat.cpu().numpy()

    print(f"\n  ADDITIVE LOG-ODDS DIAGNOSTICS ({split_name}, n={len(df)}):")
    print(f"    s_hat_J = b + beta_T*s_T + beta_V*s_V")
    print(f"    s_hat_J: mean={s_hat_np.mean():.4f}, std={s_hat_np.std():.4f}")
    print(f"    p_hat:   mean={p_hat_np.mean():.4f}, std={p_hat_np.std():.4f}")
    print(f"    p_hat<0.1: {(p_hat_np < 0.1).mean():.1%},  p_hat>0.9: {(p_hat_np > 0.9).mean():.1%}")


# Backward-compat alias for the diagnostic function's old name.
print_additive_diagnostics = print_logodds_diagnostics


def print_four_term_additive_diagnostics(
    model: FourTermAdditiveFusionModel,
    df: pd.DataFrame,
    split_name: str = "train",
    device: str = "cpu",
):
    """Print 4-term additive fusion diagnostics."""
    ll_TT = torch.tensor(df["ll_text_T"].values, dtype=torch.float32, device=device)
    ll_TV = torch.tensor(df["ll_text_V"].values, dtype=torch.float32, device=device)
    ll_VT = torch.tensor(df["ll_vision_T"].values, dtype=torch.float32, device=device)
    ll_VV = torch.tensor(df["ll_vision_V"].values, dtype=torch.float32, device=device)

    model.eval()
    with torch.no_grad():
        s_hat = (model.c + model.alpha_TT * ll_TT - model.alpha_TV * ll_TV
                 + model.alpha_VT * ll_VT - model.alpha_VV * ll_VV)
        p_hat = torch.sigmoid(s_hat)
        p_hat_np = p_hat.cpu().numpy()
        s_hat_np = s_hat.cpu().numpy()

    print(f"\n  4-TERM ADDITIVE DIAGNOSTICS ({split_name}, n={len(df)}):")
    print(f"    s_hat_J = c + α_TT*ℓ_TT - α_TV*ℓ_TV + α_VT*ℓ_VT - α_VV*ℓ_VV")
    print(f"    s_hat_J: mean={s_hat_np.mean():.4f}, std={s_hat_np.std():.4f}")
    print(f"    p_hat:   mean={p_hat_np.mean():.4f}, std={p_hat_np.std():.4f}")
    print(f"    p_hat<0.1: {(p_hat_np < 0.1).mean():.1%},  p_hat>0.9: {(p_hat_np > 0.9).mean():.1%}")
