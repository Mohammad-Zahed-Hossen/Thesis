#!/usr/bin/env python3
"""Print main-results table rows from the merged metrics_judge_summary.json.

Usage:
    python src/scripts/generate_table3.py [outputs/judge/metrics_judge_summary.json]

Column order matches the main-results table in the paper (``tab:main_results``):
    Acc(aligned) Acc(I*) Acc(T*) Acc(both-wrong)
    MPB-img MPB-txt MFR ConfabR CDR HR DeltaAcc
"""
from __future__ import annotations

import json
import pathlib
import sys

# Stem -> display name in the paper.
MODELS: list[tuple[str, str]] = [
    ("qwen3-vl-4b",        "Qwen3-VL-4B"),
    ("lfm2_5-vl-1_6b",     "LFM2.5-VL-1.6B"),
    ("gemma-3n-e2b",       "Gemma-3n-E2B"),
    ("deepseek-vl2-small", "DeepSeek-VL2-small"),
]


def fmt(v: float) -> str:
    return f"{v:.3f}"


def row(name: str, m: dict) -> str:
    acc = m.get("accuracy", {})
    cells = [
        name,
        fmt(acc.get("aligned",        0.0)),
        fmt(acc.get("image_correct",  0.0)),
        fmt(acc.get("text_correct",   0.0)),
        fmt(acc.get("both_wrong",     0.0)),
        fmt(m.get("modality_preference_image", 0.0)),
        fmt(m.get("modality_preference_text",  0.0)),
        fmt(m.get("modality_following_rate",   0.0)),
        fmt(m.get("confabulation_rate",        0.0)),
        fmt(m.get("conflict_detection_rate",   0.0)),
        fmt(m.get("hallucination_rate",        0.0)),
        fmt(m.get("accuracy_drop",             0.0)),
    ]
    return " & ".join(cells) + r" \\"


def main() -> int:
    default = pathlib.Path("outputs/judge/metrics_judge_summary.json")
    path = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else default
    if not path.is_file():
        print(f"% MISSING summary: {path}", file=sys.stderr)
        return 1
    summary = json.loads(path.read_text())
    for stem, display in MODELS:
        m = summary.get(stem)
        if m is None:
            print(f"% MISSING model in summary: {stem}")
            continue
        print(row(display, m))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
