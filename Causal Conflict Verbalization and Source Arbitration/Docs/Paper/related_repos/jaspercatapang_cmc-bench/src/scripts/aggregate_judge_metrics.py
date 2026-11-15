#!/usr/bin/env python3
"""
Build metrics_judge_summary.json from existing behavioral_*.jsonl (no remote judge / no VLM re-run).

Uses the same metrics and label breakdowns as run_llm_judge_metrics.py.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_SRC = Path(__file__).resolve().parents[1]
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from evaluation.judge_report import aggregate_summary_from_judge_dir


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Aggregate metrics_judge_summary.json from behavioral_*.jsonl on disk",
    )
    ap.add_argument(
        "--instances",
        type=Path,
        default=Path("outputs/cmc_bench_instances.jsonl"),
        help="Benchmark instances JSONL (full split, same as judge run)",
    )
    ap.add_argument(
        "--judge-dir",
        type=Path,
        default=Path("outputs/judge"),
        help="Directory containing behavioral_*.jsonl",
    )
    ap.add_argument(
        "--models",
        nargs="+",
        metavar="NAME",
        help="Only refresh these model stems (e.g. gemma-3n-e2b). Default: all behavioral_*.jsonl",
    )
    ap.add_argument(
        "--out",
        type=Path,
        default=None,
        help="Output JSON path (default: <judge-dir>/metrics_judge_summary.json)",
    )
    ap.add_argument(
        "--no-merge",
        action="store_true",
        help="Do not merge with existing metrics_judge_summary.json; output only models found on disk",
    )
    args = ap.parse_args()

    if not args.instances.is_file():
        ap.error(f"instances not found: {args.instances}")
    if not args.judge_dir.is_dir():
        ap.error(f"judge dir not found: {args.judge_dir}")

    merged = aggregate_summary_from_judge_dir(
        instances_path=args.instances,
        judge_dir=args.judge_dir,
        models=args.models,
        merge_existing=not args.no_merge,
    )
    out_path = args.out or (args.judge_dir / "metrics_judge_summary.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(merged, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {out_path} ({len(merged)} model(s))")


if __name__ == "__main__":
    main()
