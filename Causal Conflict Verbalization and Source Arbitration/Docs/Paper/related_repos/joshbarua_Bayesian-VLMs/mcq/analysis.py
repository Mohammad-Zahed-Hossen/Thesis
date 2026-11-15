#!/usr/bin/env python3
"""Position-debiased, pooled MCQ-vs-s_J agreement across models.

Each run dir holds ``mcq_generations_shard_*.parquet`` (one per worker)
and a ``meta.json`` describing the grid. We:

1. Merge shards into a single dataframe per model.
2. Pair the two-position trials by (id, blur_idx, text_idx).
3. Join s_J from the model's ``degradation_scores.parquet`` on the same
   (id, blur_sigma, text_level) key.
4. Compute, per model, pooled across the whole grid:
     - consistency rate: per-pair, model gave the same content choice
       at both positions
     - debiased agreement (on consistent pairs only):
       P(consistent picks_text == sign(s_J))
     - per-position-A vs position-B agreement (positional bias)
     - AUROC of sigma(s_J) -> picks_text (trial level)
5. Write a LaTeX-ready rows fragment and a JSON summary.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd


def wilson_ci(k: int, n: int, z: float = 1.96):
    if n == 0:
        return (float("nan"), float("nan"))
    p = k / n
    denom = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / denom
    half = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return (centre - half, centre + half)


def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-np.asarray(x)))


def merge_shards(run_dir: Path) -> pd.DataFrame:
    shards = sorted(run_dir.glob("mcq_generations_shard_*.parquet"))
    if not shards:
        raise FileNotFoundError(f"No shard parquets in {run_dir}")
    dfs = [pd.read_parquet(s) for s in shards]
    for s, d in zip(shards, dfs):
        print(f"  {s.name}: {len(d)} rows ({d['id'].nunique()} ids)")
    return pd.concat(dfs, ignore_index=True)


def join_s_J(trials: pd.DataFrame, scores_parquet: Path) -> pd.DataFrame:
    df = pd.read_parquet(scores_parquet)
    keep = df[["id", "blur_sigma", "text_level", "s_J"]].drop_duplicates(
        subset=["id", "blur_sigma", "text_level"]
    )
    merged = trials.merge(keep, on=["id", "blur_sigma", "text_level"], how="left")
    missing = merged["s_J"].isna().sum()
    if missing:
        print(f"  WARNING: {missing} trials had no matching s_J in scores parquet")
    return merged


def pair_positions(trials: pd.DataFrame) -> pd.DataFrame:
    """Pivot to one row per (id, blur_idx, text_idx) with both positions."""
    key = ["id", "dataset", "blur_idx", "text_idx", "blur_sigma",
           "text_level", "s_J"]
    A = trials[trials["position"] == "text_at_A"].set_index(key)
    B = trials[trials["position"] == "text_at_B"].set_index(key)
    A = A[["gen_prefers_text"]].rename(columns={"gen_prefers_text": "picks_text_A"})
    B = B[["gen_prefers_text"]].rename(columns={"gen_prefers_text": "picks_text_B"})
    paired = A.join(B, how="inner").reset_index()
    paired = paired.dropna(subset=["picks_text_A", "picks_text_B"])
    paired["picks_text_A"] = paired["picks_text_A"].astype(bool)
    paired["picks_text_B"] = paired["picks_text_B"].astype(bool)
    paired["consistent"] = paired["picks_text_A"] == paired["picks_text_B"]
    paired["debiased_picks_text"] = paired["picks_text_A"].where(
        paired["consistent"], other=np.nan,
    )
    return paired


def summarize(trials: pd.DataFrame, paired: pd.DataFrame) -> dict:
    s_pos = trials["s_J"] > 0
    parsed_mask = trials["parsed_letter"].notna()
    trial_n = int(parsed_mask.sum())
    trial_agree = float(
        (trials.loc[parsed_mask, "gen_prefers_text"].astype(bool)
         == s_pos[parsed_mask]).mean()
    )

    # Position-stratified per-trial agreement
    agree_A = float(
        (trials[(trials["position"] == "text_at_A") & parsed_mask]
         ["gen_prefers_text"].astype(bool)
         == (trials[(trials["position"] == "text_at_A") & parsed_mask]["s_J"] > 0)).mean()
    )
    agree_B = float(
        (trials[(trials["position"] == "text_at_B") & parsed_mask]
         ["gen_prefers_text"].astype(bool)
         == (trials[(trials["position"] == "text_at_B") & parsed_mask]["s_J"] > 0)).mean()
    )

    n_pairs = len(paired)
    consistency = float(paired["consistent"].mean()) if n_pairs else float("nan")
    cons = paired[paired["consistent"]]
    cons_agree = (cons["debiased_picks_text"].astype(bool) == (cons["s_J"] > 0))
    k_cons = int(cons_agree.sum())
    rate_cons = k_cons / len(cons) if len(cons) else float("nan")
    ci_cons = wilson_ci(k_cons, len(cons))

    # |s_J| tercile on the paired (consistent) subset
    tercile_stats = {}
    if len(cons):
        abs_sJ = cons["s_J"].abs()
        qs = abs_sJ.quantile([1 / 3, 2 / 3]).values
        tercile = pd.cut(abs_sJ, [-np.inf, qs[0], qs[1], np.inf],
                         labels=["low", "mid", "high"])
        for t in ["low", "mid", "high"]:
            m = tercile == t
            sub = cons[m]
            k_t = int((sub["debiased_picks_text"].astype(bool)
                       == (sub["s_J"] > 0)).sum())
            n_t = int(m.sum())
            tercile_stats[t] = {
                "n": n_t,
                "rate": k_t / n_t if n_t else float("nan"),
                "ci": wilson_ci(k_t, n_t),
            }

    # AUROC at trial level
    try:
        from sklearn.metrics import roc_auc_score
        valid = trials[parsed_mask & trials["s_J"].notna()]
        p_J = sigmoid(valid["s_J"].values)
        y = valid["gen_prefers_text"].astype(int).values
        auroc = float(roc_auc_score(y, p_J))
    except Exception:
        auroc = None

    # Letter-A selection rate (position bias diagnostic)
    letter_A_rate = float(
        (trials.loc[parsed_mask, "parsed_letter"] == "A").mean()
    )

    return {
        "n_trials": trial_n,
        "n_pairs": n_pairs,
        "agree_per_trial": trial_agree,
        "agree_position_A": agree_A,
        "agree_position_B": agree_B,
        "consistency": consistency,
        "n_consistent": int(paired["consistent"].sum()),
        "agree_debiased": rate_cons,
        "agree_debiased_ci": ci_cons,
        "tercile": tercile_stats,
        "auroc_trial": auroc,
        "letter_A_rate": letter_A_rate,
    }


def fmt(rate, ci=None):
    if rate is None or (isinstance(rate, float) and np.isnan(rate)):
        return "—"
    if ci is None or any(np.isnan(c) for c in ci):
        return f"{rate:.3f}"
    return f"{rate:.3f} [{ci[0]:.3f}, {ci[1]:.3f}]"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--runs", nargs="+", required=True,
        help="label=mcq_run_dir=scores_parquet triples, e.g. "
             "'Qwen2.5-VL-3B=runs/mcq_qwen3b=runs/deg_Qwen.../degradation_scores.parquet'",
    )
    parser.add_argument("--out_dir", type=Path, required=True)
    args = parser.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)

    summaries = {}
    rows_tex = []
    for spec in args.runs:
        parts = spec.split("=")
        if len(parts) != 3:
            raise SystemExit(f"Bad --runs spec: {spec!r}")
        label, run_dir, scores_path = parts
        print(f"\n=== {label} ===")
        run_dir = Path(run_dir)
        trials = merge_shards(run_dir)
        trials = join_s_J(trials, Path(scores_path))
        print(f"Total trials: {len(trials)} "
              f"({trials['parsed_letter'].notna().sum()} parseable)")
        paired = pair_positions(trials)
        print(f"Paired (both positions): {len(paired)} pairs "
              f"({paired['consistent'].sum()} consistent)")
        s = summarize(trials, paired)
        summaries[label] = s

        print(f"  Letter A rate:        {s['letter_A_rate']:.3f}")
        print(f"  Per-trial agree:      {s['agree_per_trial']:.3f}")
        print(f"  At position A:        {s['agree_position_A']:.3f}")
        print(f"  At position B:        {s['agree_position_B']:.3f}")
        print(f"  Consistency:          {s['consistency']:.3f}")
        print(f"  Debiased agree (consistent only): "
              f"{fmt(s['agree_debiased'], s['agree_debiased_ci'])}")
        if s["auroc_trial"] is not None:
            print(f"  AUROC (trial):        {s['auroc_trial']:.3f}")
        if s["tercile"]:
            print("  By |s_J| tercile (consistent only):")
            for t in ["low", "mid", "high"]:
                ts = s["tercile"][t]
                print(f"    {t}: n={ts['n']}  {fmt(ts['rate'], ts['ci'])}")

        if s["tercile"]:
            low = fmt(s["tercile"]["low"]["rate"], s["tercile"]["low"]["ci"])
            mid = fmt(s["tercile"]["mid"]["rate"], s["tercile"]["mid"]["ci"])
            high = fmt(s["tercile"]["high"]["rate"], s["tercile"]["high"]["ci"])
        else:
            low = mid = high = "—"
        rows_tex.append(
            f"    {label} & {s['n_pairs']} "
            f"& {s['consistency']:.3f} "
            f"& {fmt(s['agree_debiased'], s['agree_debiased_ci'])} "
            f"& {low} & {mid} & {high} \\\\"
        )

    def to_json(o):
        if isinstance(o, dict):
            return {k: to_json(v) for k, v in o.items()}
        if isinstance(o, (list, tuple)):
            return [to_json(x) for x in o]
        if isinstance(o, (np.integer, np.floating)):
            return float(o)
        return o

    with open(args.out_dir / "debiased_summary.json", "w") as f:
        json.dump(to_json(summaries), f, indent=2)
    with open(args.out_dir / "table_rows.tex", "w") as f:
        f.write("\n".join(rows_tex) + "\n")
    print("\n--- LaTeX rows ---")
    print("\n".join(rows_tex))
    print(f"\nWrote {args.out_dir}/debiased_summary.json + table_rows.tex")


if __name__ == "__main__":
    main()
