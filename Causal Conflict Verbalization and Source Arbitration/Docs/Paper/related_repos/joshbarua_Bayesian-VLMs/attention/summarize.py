#!/usr/bin/env python3
"""Bootstrap the attention-knockout effects reported in the paper."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from config import get_run_dir


def load_parquet(run_dir: Path, stem: str) -> pd.DataFrame | None:
    """Load one combined parquet or all of its sharded equivalents."""
    combined = run_dir / f"{stem}.parquet"
    paths = [combined] if combined.exists() else sorted(
        run_dir.glob(f"{stem}_shard_*.parquet")
    )
    if not paths:
        return None
    return pd.concat([pd.read_parquet(path) for path in paths], ignore_index=True)


def bootstrap_mean(values, *, n_boot: int = 5000, seed: int = 0):
    values = np.asarray(values, dtype=float)
    values = values[np.isfinite(values)]
    if not values.size:
        return float("nan"), float("nan"), float("nan")
    rng = np.random.default_rng(seed)
    indices = rng.integers(0, values.size, size=(n_boot, values.size))
    draws = values[indices].mean(axis=1)
    return (
        float(values.mean()),
        float(np.percentile(draws, 2.5)),
        float(np.percentile(draws, 97.5)),
    )


def summarize_span_knockout(frame: pd.DataFrame, *, seed: int = 0) -> pd.DataFrame:
    control = frame[frame["span"] == "none"]
    if not control.empty and float(control["delta"].abs().max()) >= 1e-6:
        raise RuntimeError("empty-knockout control changed the readout")

    rows = []
    for (cell, block, span), group in frame[frame["span"] != "none"].groupby(
        ["cell", "block", "span"], sort=True
    ):
        per_id = group.groupby("id")[["delta", "mass_removed", "s_base"]].mean()
        mean, lo, hi = bootstrap_mean(per_id["delta"], seed=seed)
        abs_mean, abs_lo, abs_hi = bootstrap_mean(per_id["delta"].abs(), seed=seed)
        rows.append({
            "cell": cell,
            "block": block,
            "span": span,
            "layer_lo": int(group["layer_lo"].iloc[0]),
            "layer_hi": int(group["layer_hi"].iloc[0]),
            "n": len(per_id),
            "delta_mean": mean,
            "delta_lo": lo,
            "delta_hi": hi,
            "delta_excludes_zero": bool(lo > 0 or hi < 0),
            "abs_delta_mean": abs_mean,
            "abs_delta_lo": abs_lo,
            "abs_delta_hi": abs_hi,
            "mass_removed_mean": float(per_id["mass_removed"].mean()),
            "s_base_mean": float(per_id["s_base"].mean()),
        })
    return pd.DataFrame(rows)


def summarize_linear_knockout(frame: pd.DataFrame, *, seed: int = 0) -> pd.DataFrame:
    if float(frame["identity_delta"].abs().max()) >= 1e-6:
        raise RuntimeError("scale-one linear-attention control changed the readout")

    rows = []
    for (cell, block), group in frame.groupby(["cell", "block"], sort=True):
        per_id = group.groupby("id")[[
            "delta", "write_rms_mean", "s_base", "identity_delta"
        ]].mean()
        mean, lo, hi = bootstrap_mean(per_id["delta"], seed=seed)
        abs_mean, abs_lo, abs_hi = bootstrap_mean(per_id["delta"].abs(), seed=seed)
        rows.append({
            "cell": cell,
            "block": block,
            "layer_lo": int(group["layer_lo"].iloc[0]),
            "layer_hi": int(group["layer_hi"].iloc[0]),
            "n_layers_blocked": int(group["n_layers_blocked"].iloc[0]),
            "linear_layers": str(group["linear_layers"].iloc[0]),
            "n": len(per_id),
            "delta_mean": mean,
            "delta_lo": lo,
            "delta_hi": hi,
            "delta_excludes_zero": bool(lo > 0 or hi < 0),
            "abs_delta_mean": abs_mean,
            "abs_delta_lo": abs_lo,
            "abs_delta_hi": abs_hi,
            "write_rms_mean": float(per_id["write_rms_mean"].mean()),
            "s_base_mean": float(per_id["s_base"].mean()),
            "identity_max_abs": float(per_id["identity_delta"].abs().max()),
        })
    return pd.DataFrame(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run_id", required=True)
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args()

    run_dir = get_run_dir(args.run_id)
    knockout = load_parquet(run_dir, "knockout")
    if knockout is None:
        raise SystemExit(f"no knockout parquet in {run_dir}")
    summary = summarize_span_knockout(knockout, seed=args.seed)
    path = run_dir / "summary_knockout.csv"
    summary.to_csv(path, index=False)
    print(path)

    linear = load_parquet(run_dir, "linear_output_knockout")
    if linear is not None:
        summary = summarize_linear_knockout(linear, seed=args.seed)
        path = run_dir / "summary_linear_output_knockout.csv"
        summary.to_csv(path, index=False)
        print(path)


if __name__ == "__main__":
    main()
