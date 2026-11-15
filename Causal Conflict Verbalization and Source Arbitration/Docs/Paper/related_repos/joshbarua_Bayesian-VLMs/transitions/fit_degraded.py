#!/usr/bin/env python3
"""fit_degraded.py — Fit the additive log-odds model on degraded data under
two protocols and report metrics for it plus two parameter-free baselines.

  ID  (in-distribution):   train on train_ids × all cells,
                           val   on val_ids × all cells,
                           test  on test_ids × all cells.

  OOD (out-of-distribution): train on train_ids × L-shape (blur=0 OR text=0),
                             val   on val_ids × L-shape,
                             test  on test_ids × interior (blur>0 AND text>0).

Each (example, blur_level, text_level) row becomes one observation with
x_T = s_T(text_level), x_V = s_V(blur_level), y = p_J(blur, text).

Reported predictors:
  text_probe         p_T (text-only probe)
  vision_probe       p_V (vision-only probe)
  best_single_probe  whichever of p_T, p_V has larger |log-odds| per row
  naive_bayes        sigma(s_T + s_V - pi_0), the calibrated
                     unit-coefficient additive model with the
                     per-example prior subtracted
                     (pi_0 = log P(a_T|q) - log P(a_V|q))
  additive_log_odds  fitted sigma(beta_T s_T + beta_V s_V - pi_0); two-
                     parameter model that pins the prior to its
                     calibrated coefficient -1 and absorbs only the
                     evidence-weight miscalibration. Calibrated naive
                     Bayes is the nested special case beta_T = beta_V = 1.

Outputs (under run_dir):
  id_params.json                        additive coefs per experiment
  ood_params.json                       additive coefs per experiment
  degraded_metrics.json                 {"id": {...}, "ood": {...}}
  degraded_training_history.json        {"id": {...}, "ood": {...}}
"""

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import torch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from config import (
    DEFAULT_LR,
    DEFAULT_EPOCHS,
    DEFAULT_SEED,
    MARGIN_CLIP,
    get_run_dir,
    load_degradation_meta,
    use_measured_prior_in_fit,
)
from fitting import (
    AdditiveLogOddsWithPriorModel,
    BilinearLogOddsModel,
    UnconstrainedLinearModel,
)
from fitting.train import _compute_metrics

EXPERIMENTS = [
    ("within_mixture", None),
    ("within_DocVQA", "DocVQA"),
    ("within_VQAv2", "VQAv2"),
    ("within_RealworldQA", "RealworldQA"),
]


def degradation_df_to_model_df(df: pd.DataFrame) -> pd.DataFrame:
    if "pi_0" not in df.columns:
        raise KeyError(
            "degradation_scores.parquet is missing the 'pi_0' column. "
            "Re-run run_degradation_scoring.py to add per-example prior probes."
        )
    out = pd.DataFrame({
        "x_T": df["s_T"].values,
        "x_V": df["s_V"].values,
        "y": df["p_J"].values,
        "s_J": df["s_J"].values,  # for MSE-on-s_J fits (additive model only)
        "p_T": df["p_T"].values,
        "p_V": df["p_V"].values,
        "pi_0": df["pi_0"].values,
    })
    for col in ["ll_text_T", "ll_text_V", "ll_vision_T", "ll_vision_V"]:
        if col in df.columns:
            out[col] = df[col].values
    return out


def train_mse_s_j(
    model,
    train_df: pd.DataFrame,
    val_df: pd.DataFrame,
    lr: float,
    epochs: int,
    device: str = "cpu",
    patience: int = 100,
) -> tuple[dict, dict]:
    """Train any fusion model exposing
    `forward_logodds(s_T, s_V, pi_0) -> s_hat_J` with MSE on s_J. The
    additivity claim is that s_J ≈ <linear in s> is linear in log-odds;
    matching that with MSE-on-s_J avoids BCE's sigmoid-saturation bias
    that systematically shrinks coefficients.

    Returns (history, best_params) with the same schema as
    fitting.train_model.
    """
    def _tensors(df):
        return (
            torch.tensor(df["x_T"].values, dtype=torch.float32, device=device),
            torch.tensor(df["x_V"].values, dtype=torch.float32, device=device),
            torch.tensor(df["pi_0"].values, dtype=torch.float32, device=device),
            torch.tensor(df["s_J"].values, dtype=torch.float32, device=device),
        )

    sT_tr, sV_tr, pi_tr, sJ_tr = _tensors(train_df)
    sT_va, sV_va, pi_va, sJ_va = _tensors(val_df)
    model = model.to(device)
    optimizer = torch.optim.LBFGS(model.parameters(), lr=lr,
                                  max_iter=20, history_size=10)

    history: dict = {"train_loss": [], "val_loss": []}
    best_val = float("inf")
    best_params: dict | None = None
    bad = 0

    for epoch in range(epochs):
        def closure():
            optimizer.zero_grad()
            loss = ((model.forward_logodds(sT_tr, sV_tr, pi_tr) - sJ_tr) ** 2).mean()
            loss.backward()
            return loss
        optimizer.step(closure)

        model.eval()
        with torch.no_grad():
            tr_loss = ((model.forward_logodds(sT_tr, sV_tr, pi_tr) - sJ_tr) ** 2).mean().item()
            va_loss = ((model.forward_logodds(sT_va, sV_va, pi_va) - sJ_va) ** 2).mean().item()
        model.train()

        history["train_loss"].append(tr_loss)
        history["val_loss"].append(va_loss)

        if va_loss < best_val - 1e-9:
            best_val = va_loss
            best_params = model.get_params_dict()
            bad = 0
        else:
            bad += 1
        if bad >= patience:
            print(f"    early stop at epoch {epoch}, best val MSE_s = {best_val:.4f}")
            break

    return history, best_params


def slice_protocol(df: pd.DataFrame, protocol: str, role: str) -> pd.DataFrame:
    """Restrict rows to the cell support for (protocol, role).

    protocol="id":   all roles use all cells.
    protocol="ood":  train/val use L-shape (blur==0 OR text==0);
                     test uses interior (blur>0 AND text>0).
    """
    if protocol == "id":
        return df
    if protocol == "ood":
        if role in ("train", "val"):
            mask = (df["blur_level"] == 0) | (df["text_level"] == 0)
        elif role == "test":
            mask = (df["blur_level"] != 0) & (df["text_level"] != 0)
        else:
            raise ValueError(f"Unknown role {role!r}")
        return df.loc[mask].reset_index(drop=True)
    raise ValueError(f"Unknown protocol {protocol!r}")


def select_split_dfs(exp_df, train_ids, val_ids, test_ids):
    return (
        exp_df[exp_df["id"].isin(train_ids)].reset_index(drop=True),
        exp_df[exp_df["id"].isin(val_ids)].reset_index(drop=True),
        exp_df[exp_df["id"].isin(test_ids)].reset_index(drop=True),
    )


def _r2(y: np.ndarray, yhat: np.ndarray) -> float:
    finite = np.isfinite(y) & np.isfinite(yhat)
    y, yhat = y[finite], yhat[finite]
    if y.size < 2:
        return float("nan")
    ss_res = float(np.sum((y - yhat) ** 2))
    ss_tot = float(np.sum((y - y.mean()) ** 2))
    return 1.0 - ss_res / ss_tot if ss_tot > 0 else float("nan")


def evaluate_predictors(
    additive_model: AdditiveLogOddsWithPriorModel,
    bilinear_model: BilinearLogOddsModel,
    unconstrained_model: UnconstrainedLinearModel,
    df: pd.DataFrame,
    device: str = "cpu",
) -> dict:
    """Evaluate the additive log-odds model, its bilinear extension, and
    parameter-free baselines:

      text_probe         — p_T directly  (log-odds: s_T)
      vision_probe       — p_V directly  (log-odds: s_V)
      best_single_probe  — per row, the more confident probe
                           (log-odds: s_T or s_V, whichever has larger |.|)
      naive_bayes        — calibrated, sigmoid(s_T + s_V - pi_0)
                           / log-odds: s_T + s_V - pi_0, where
                           pi_0 = log P(a_T | q) - log P(a_V | q) is the
                           per-example prior from the question-only probe
      additive_log_odds  — fitted sigmoid(beta_T s_T + beta_V s_V - pi_0);
                           two-parameter affine reweighting of the
                           calibrated naive-Bayes form. Calibrated naive
                           Bayes is the nested case beta_T = beta_V = 1.
      bilinear_log_odds  — fitted sigmoid(beta_T s_T + beta_V s_V
                                            + beta_I s_T s_V - pi_0)
                           — minimal interaction extension of additive
                           that tests the conditional-independence
                           assumption. Calibrated naive Bayes is the
                           nested case beta_T = beta_V = 1, beta_I = 0.

    For each predictor we report KL, sKL, argmax, CE plus per-row R^2 in
    log-odds space (s_J space). Log-odds matches the MSE-on-s_J fit objective.
    """
    s_T = torch.tensor(df["x_T"].values, dtype=torch.float32, device=device)
    s_V = torch.tensor(df["x_V"].values, dtype=torch.float32, device=device)
    p_T = torch.tensor(df["p_T"].values, dtype=torch.float32, device=device)
    p_V = torch.tensor(df["p_V"].values, dtype=torch.float32, device=device)
    pi0 = torch.tensor(df["pi_0"].values, dtype=torch.float32, device=device)
    y = torch.tensor(df["y"].values, dtype=torch.float32, device=device)

    additive_model.eval()
    bilinear_model.eval()
    unconstrained_model.eval()
    with torch.no_grad():
        y_hat_lo = additive_model(s_T, s_V, pi0)
        y_hat_bi = bilinear_model(s_T, s_V, pi0)
        y_hat_un = unconstrained_model(s_T, s_V, pi0)

    sT_clip = s_T.clamp(-MARGIN_CLIP, MARGIN_CLIP)
    sV_clip = s_V.clamp(-MARGIN_CLIP, MARGIN_CLIP)
    pi0_clip = pi0.clamp(-MARGIN_CLIP, MARGIN_CLIP)
    y_hat_nb = torch.sigmoid(
        (sT_clip + sV_clip - pi0_clip).clamp(-MARGIN_CLIP, MARGIN_CLIP)
    )
    pick_text = (s_T.abs() >= s_V.abs())
    y_hat_best = torch.where(pick_text, p_T, p_V)

    # Log-odds predictions corresponding to each probability predictor above.
    bT_a = float(additive_model.beta_T.item())
    bV_a = float(additive_model.beta_V.item())
    bT_b = float(bilinear_model.beta_T.item())
    bV_b = float(bilinear_model.beta_V.item())
    bI_b = float(bilinear_model.beta_I.item())
    wT_u = float(unconstrained_model.w_T.item())
    wV_u = float(unconstrained_model.w_V.item())
    wpi_u = float(unconstrained_model.w_pi.item())
    w0_u = float(unconstrained_model.w_0.item())

    sT_np = sT_clip.detach().cpu().numpy().astype(np.float64)
    sV_np = sV_clip.detach().cpu().numpy().astype(np.float64)
    pi0_np = pi0_clip.detach().cpu().numpy().astype(np.float64)
    s_hat_text = sT_np
    s_hat_vision = sV_np
    s_hat_best = np.where(np.abs(sT_np) >= np.abs(sV_np), sT_np, sV_np)
    s_hat_nb = np.clip(sT_np + sV_np - pi0_np, -MARGIN_CLIP, MARGIN_CLIP)
    bf_T = sT_np - pi0_np
    bf_V = sV_np - pi0_np
    s_hat_additive = np.clip(bT_a * bf_T + bV_a * bf_V + pi0_np,
                             -MARGIN_CLIP, MARGIN_CLIP)
    s_hat_bilinear = np.clip(bT_b * bf_T + bV_b * bf_V
                             + bI_b * bf_T * bf_V + pi0_np,
                             -MARGIN_CLIP, MARGIN_CLIP)
    s_hat_unconstrained = np.clip(wT_u * sT_np + wV_u * sV_np
                                  + wpi_u * pi0_np + w0_u,
                                  -MARGIN_CLIP, MARGIN_CLIP)

    s_J = np.clip(df["s_J"].to_numpy(dtype=np.float64), -MARGIN_CLIP, MARGIN_CLIP)

    out: dict = {}
    for name, y_hat, s_hat in [
        ("text_probe", p_T, s_hat_text),
        ("vision_probe", p_V, s_hat_vision),
        ("best_single_probe", y_hat_best, s_hat_best),
        ("naive_bayes", y_hat_nb, s_hat_nb),
        ("additive_log_odds", y_hat_lo, s_hat_additive),
        ("unconstrained_linear", y_hat_un, s_hat_unconstrained),
        ("bilinear_log_odds", y_hat_bi, s_hat_bilinear),
    ]:
        m = _compute_metrics(y, y_hat)
        m["r2"] = _r2(s_J, s_hat)
        out[name] = m
    return out


def fit_one_protocol(
    protocol: str, exp_df: pd.DataFrame,
    train_ids, val_ids, test_ids,
    args: argparse.Namespace,
) -> tuple[dict, dict, dict] | None:
    """Run one protocol pass for one experiment. Returns (params, metrics, histories)
    or None if data is insufficient."""
    train_df, val_df, test_df = select_split_dfs(exp_df, train_ids, val_ids, test_ids)
    train_df = slice_protocol(train_df, protocol, "train")
    val_df = slice_protocol(val_df, protocol, "val")
    test_df = slice_protocol(test_df, protocol, "test")

    print(f"  [{protocol.upper()}] Train: {len(train_df)} rows  "
          f"Val: {len(val_df)} rows  Test: {len(test_df)} rows")
    if len(train_df) == 0 or len(val_df) == 0:
        print(f"  [{protocol.upper()}] SKIPPING: insufficient data")
        return None

    train_model_df = degradation_df_to_model_df(train_df)
    val_model_df = degradation_df_to_model_df(val_df)
    test_model_df = degradation_df_to_model_df(test_df)
    if args.hard_labels:
        for mdf in [train_model_df, val_model_df, test_model_df]:
            mdf["y"] = (mdf["y"] > 0.5).astype(float)

    # Both transitions fusion models pin pi_0 at coefficient -1 (no free
    # intercept). Calibrated naive Bayes is the nested case beta_T = beta_V = 1
    # (with beta_I = 0 for the bilinear).
    print(f"\n  [{protocol.upper()}] Training Additive Log-Odds "
          f"(MSE on s_J; pi_0 pinned at -1)...")
    additive_model = AdditiveLogOddsWithPriorModel()
    add_history, add_best = train_mse_s_j(
        additive_model, train_model_df, val_model_df,
        lr=args.lr, epochs=args.epochs, device=args.device,
    )
    if add_best is None:
        print(f"  [{protocol.upper()}] additive failed"); return None
    additive_model.load_params_dict(add_best)
    print(f"    beta_T={add_best['beta_T']:.4f}  beta_V={add_best['beta_V']:.4f}   "
          f"(calibrated naive Bayes: beta_T = beta_V = 1)")

    print(f"\n  [{protocol.upper()}] Training Bilinear Log-Odds "
          f"(MSE on s_J; pi_0 pinned at -1)...")
    bilinear_model = BilinearLogOddsModel()
    bi_history, bi_best = train_mse_s_j(
        bilinear_model, train_model_df, val_model_df,
        lr=args.lr, epochs=args.epochs, device=args.device,
    )
    if bi_best is None:
        print(f"  [{protocol.upper()}] bilinear failed"); return None
    bilinear_model.load_params_dict(bi_best)
    print(f"    beta_T={bi_best['beta_T']:.4f}  beta_I={bi_best['beta_I']:+.4f}  "
          f"beta_V={bi_best['beta_V']:.4f}")

    print(f"\n  [{protocol.upper()}] Training Unconstrained Linear "
          f"(MSE on s_J; 4 free weights w_T, w_V, w_pi, w_0)...")
    unconstrained_model = UnconstrainedLinearModel()
    un_history, un_best = train_mse_s_j(
        unconstrained_model, train_model_df, val_model_df,
        lr=args.lr, epochs=args.epochs, device=args.device,
    )
    if un_best is None:
        print(f"  [{protocol.upper()}] unconstrained failed"); return None
    unconstrained_model.load_params_dict(un_best)
    print(f"    w_T={un_best['w_T']:.4f}  w_V={un_best['w_V']:.4f}  "
          f"w_pi={un_best['w_pi']:+.4f}  w_0={un_best['w_0']:+.4f}")

    metrics = {}
    for split_name, split_df in [("train", train_model_df),
                                  ("val", val_model_df),
                                  ("test", test_model_df)]:
        if len(split_df) == 0:
            continue
        metrics[split_name] = evaluate_predictors(
            additive_model, bilinear_model, unconstrained_model, split_df,
            device=args.device,
        )

    print(f"\n  [{protocol.upper()}] METRICS:")
    for split_name, sm in metrics.items():
        for predictor, pm in sm.items():
            print(f"    {split_name} / {predictor:>20s}: "
                  f"KL={pm['mean_kl']:.4f}  "
                  f"R2={pm['r2']:.4f}  argmax={pm['argmax_pct']:.4f}")

    params = {
        "additive_fusion": add_best.copy(),
        "bilinear_fusion": bi_best.copy(),
        "unconstrained_linear": un_best.copy(),
    }
    histories = {
        "additive_fusion": add_history,
        "bilinear_fusion": bi_history,
        "unconstrained_linear": un_history,
    }
    return params, metrics, histories


def main():
    parser = argparse.ArgumentParser(
        description="Fit fusion models on degraded data under ID and OOD protocols."
    )
    parser.add_argument("--run_id", type=str, required=True)
    parser.add_argument("--experiment", type=str, default=None,
                        help="Single experiment to run (default: all)")
    parser.add_argument("--lr", type=float, default=DEFAULT_LR)
    parser.add_argument("--epochs", type=int, default=DEFAULT_EPOCHS)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--device", type=str, default="cpu")
    parser.add_argument("--hard_labels", action="store_true",
                        help="Convert targets to y* = 1[p_J > 0.5]")
    args = parser.parse_args()

    torch.manual_seed(args.seed)
    np.random.seed(args.seed)

    run_dir = get_run_dir(args.run_id)
    df = pd.read_parquet(run_dir / "degradation_scores.parquet")
    print(f"Loaded {len(df)} rows; unique IDs: {df['id'].nunique()}")

    meta = load_degradation_meta(run_dir)
    model_name = meta.get("model_name", "")
    if not use_measured_prior_in_fit(model_name):
        print(f"NOTE: zeroing pi_0 for {model_name} fits "
              "(prefill-pi_0 is chat-template inconsistent with s_T/s_V/s_J; "
              "see config.use_measured_prior_in_fit). Measured pi_0 is "
              "preserved in the parquet for diagnostics.")
        df["pi_0"] = 0.0

    with open(run_dir / "splits.json") as f:
        splits_info = json.load(f)
    within_splits = splits_info["within_mixture"]

    if args.experiment:
        experiments = [(args.experiment,
                        args.experiment.split("_", 1)[1] if "_" in args.experiment else None)]
        if experiments[0][1] == "mixture":
            experiments = [("within_mixture", None)]
    else:
        experiments = EXPERIMENTS

    id_params: dict = {}
    ood_params: dict = {}
    metrics_out = {"id": {}, "ood": {}}
    histories_out = {"id": {}, "ood": {}}

    for exp_name, dataset_filter in experiments:
        print(f"\n{'='*70}\nEXPERIMENT: {exp_name}\n{'='*70}")
        exp_df = df.copy()
        if dataset_filter and "dataset" in exp_df.columns:
            exp_df = exp_df[exp_df["dataset"] == dataset_filter].reset_index(drop=True)
            print(f"Filtered to dataset={dataset_filter}: {len(exp_df)} rows")

        # Use within-dataset splits when available, else fall back to within_mixture.
        if dataset_filter and "within_dataset" in splits_info:
            ds_splits = splits_info["within_dataset"].get(dataset_filter, {})
            if ds_splits:
                train_ids = set(ds_splits["train"])
                val_ids = set(ds_splits["val"])
                test_ids = set(ds_splits["test"])
            else:
                train_ids = set(within_splits["train"])
                val_ids = set(within_splits["val"])
                test_ids = set(within_splits["test"])
        else:
            train_ids = set(within_splits["train"])
            val_ids = set(within_splits["val"])
            test_ids = set(within_splits["test"])

        print(f"Splits: train={len(train_ids)}  val={len(val_ids)}  test={len(test_ids)} ids")

        for protocol, store_p, store_m, store_h in [
            ("id", id_params, metrics_out["id"], histories_out["id"]),
            ("ood", ood_params, metrics_out["ood"], histories_out["ood"]),
        ]:
            result = fit_one_protocol(
                protocol, exp_df, train_ids, val_ids, test_ids, args,
            )
            if result is None:
                continue
            params, metrics, histories = result
            store_p[exp_name] = params
            store_m[exp_name] = metrics
            store_h[exp_name] = histories

    for filename, data in [
        ("id_params.json", id_params),
        ("ood_params.json", ood_params),
        ("degraded_metrics.json", metrics_out),
        ("degraded_training_history.json", histories_out),
    ]:
        out_path = run_dir / filename
        with open(out_path, "w") as f:
            json.dump(data, f, indent=2)
        print(f"Saved: {out_path}")


if __name__ == "__main__":
    main()
