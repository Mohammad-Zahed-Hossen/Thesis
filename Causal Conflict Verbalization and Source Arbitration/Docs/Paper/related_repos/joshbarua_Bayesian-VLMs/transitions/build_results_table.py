#!/usr/bin/env python3
"""Build a paper-ready results CSV from degraded_metrics.json.

Long-format columns: dataset, protocol, predictor, KL, R2.
Pivots cleanly to any wide layout via pandas.
"""

import argparse
import json
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from config import get_run_dir


DATASETS = [
    ("within_DocVQA", "DocVQA"),
    ("within_VQAv2", "VQAv2"),
    ("within_RealworldQA", "RealworldQA"),
]
PROTOCOLS = ["id", "ood"]
PREDICTORS = [
    "best_single_probe",
    "naive_bayes",
    "additive_log_odds",
    "unconstrained_linear",
    "bilinear_log_odds",
]


def main():
    parser = argparse.ArgumentParser(
        description="Build a paper-ready results CSV (predictor × dataset × protocol)."
    )
    parser.add_argument("--run_id", type=str, required=True)
    parser.add_argument("--out_name", type=str, default="paper_results_table.csv")
    args = parser.parse_args()

    run_dir = get_run_dir(args.run_id)
    metrics_path = run_dir / "degraded_metrics.json"
    if not metrics_path.exists():
        raise FileNotFoundError(metrics_path)
    with open(metrics_path) as f:
        m = json.load(f)

    rows = []
    for protocol in PROTOCOLS:
        for exp, dataset in DATASETS:
            test = m.get(protocol, {}).get(exp, {}).get("test", {})
            for pred in PREDICTORS:
                if pred not in test:
                    print(f"  WARN: missing {protocol}/{exp}/{pred}")
                    continue
                rows.append({
                    "dataset": dataset,
                    "protocol": protocol.upper(),
                    "predictor": pred,
                    "KL": float(test[pred]["mean_kl"]),
                    "R2": float(test[pred]["r2"]),
                })
    df = pd.DataFrame(rows)
    out_path = run_dir / args.out_name
    df.to_csv(out_path, index=False, float_format="%.4f")
    print(f"Saved {out_path}\n")

    # Console preview: wide pivot with predictors as rows.
    pivot = df.pivot_table(
        index="predictor", columns=["dataset", "protocol"],
        values=["KL", "R2"],
    )
    pivot = pivot.reorder_levels([1, 2, 0], axis=1).sort_index(axis=1)
    pivot = pivot.reindex(PREDICTORS)
    print(pivot.round(3).to_string())


if __name__ == "__main__":
    main()
