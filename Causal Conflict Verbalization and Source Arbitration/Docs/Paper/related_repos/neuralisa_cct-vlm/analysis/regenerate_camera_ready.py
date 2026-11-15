#!/usr/bin/env python3
"""Validate compact artifacts and regenerate decision tables."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
from statistics import mean


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def fmt(value: float) -> str:
    return f"{value:.3f}"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifacts", type=Path, default=Path("artifacts"))
    parser.add_argument("--output-dir", type=Path, default=Path("reproduced"))
    args = parser.parse_args()

    groups = read_csv(args.artifacts / "main" / "normalized_group_metrics.csv")
    paired = read_csv(args.artifacts / "main" / "normalized_paired_inference.csv")
    audit = read_csv(args.artifacts / "audit" / "item_consensus.csv")
    snli_color = read_csv(args.artifacts / "color" / "snlive_122.csv")
    aok_color = read_csv(args.artifacts / "color" / "aokvqa_122.csv")

    expected = {"group rows": (len(groups), 48), "paired rows": (len(paired), 16),
                "audit items": (len(audit), 60), "SNLI color rows": (len(snli_color), 8),
                "A-OKVQA color rows": (len(aok_color), 8)}
    for label, (actual, target) in expected.items():
        if actual != target:
            raise ValueError(f"{label}: expected {target}, found {actual}")

    main_rows = []
    for dataset in ("A-OKVQA", "SNLI-VE"):
        for model in sorted({r["model"] for r in groups if r["dataset"] == dataset}):
            modes = {r["mode"]: r for r in groups if r["dataset"] == dataset and r["model"] == model}
            pe, cot = modes["PE"], modes["CoT"]
            main_rows.append({
                "dataset": dataset,
                "model": model,
                "pe_vCCT": fmt(float(pe["normalized_vcct"])),
                "cot_vCCT": fmt(float(cot["normalized_vcct"])),
                "gap": fmt(float(pe["normalized_vcct"]) - float(cot["normalized_vcct"])),
                "pe_vCT": fmt(float(pe["vct"])),
                "cot_vCT": fmt(float(cot["vct"])),
                "pe_flips": pe["flip_count"],
                "cot_flips": cot["flip_count"],
            })
    fields = list(main_rows[0])
    write_csv(args.output_dir / "main_results.csv", main_rows, fields)

    color_rows = []
    for dataset, rows in (("SNLI-VE", snli_color), ("A-OKVQA", aok_color)):
        for row in rows:
            color_rows.append({"dataset": dataset, **row})
    write_csv(args.output_dir / "color_results.csv", color_rows, list(color_rows[0]))

    gaps = [float(r["gap"]) for r in paired]
    target_valid = sum(r["target_valid_consensus"] == "yes" for r in audit) / len(audit)
    task_preserved = sum(r["task_preserved_consensus"] == "yes" for r in audit) / len(audit)
    report = [
        "# Regenerated compact checks",
        "",
        f"- Primary paired PE–CoT comparisons: {sum(g > 0 for g in gaps)}/{len(gaps)} positive.",
        f"- Mean candidate-normalized PE–CoT vCCT gap: {mean(gaps):.4f}.",
        f"- Blinded-audit target-valid consensus: {target_valid:.1%}.",
        f"- Blinded-audit task-preserved consensus: {task_preserved:.1%}.",
        "- Color tables regenerated for 8 models × 2 datasets.",
    ]
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "SUMMARY.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    print("\n".join(report[2:]))


if __name__ == "__main__":
    main()
