#!/usr/bin/env python3
"""Run one real Qwen-Image-Edit example followed by mock inference/judging."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from main import CCT


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", required=True)
    parser.add_argument("--sam-checkpoint", required=True)
    parser.add_argument("--editor", default="Qwen/Qwen-Image-Edit")
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--n-examples", type=int, default=3)
    args = parser.parse_args()

    CCT(
        output_dir=args.output_dir,
        override=True,
        run_generator=True,
        generator="QwenImageEdit",
        model="Perfect Mock",
        evaluator="Mock",
        generator_kwargs={
            "dataset_name": "AOKVQA",
            "data_dir": args.data_dir,
            "split": "train",
            "n_examples": args.n_examples,
            "image_size": [1024, 1024],
            "sam_checkpoint": args.sam_checkpoint,
            "model_path": args.editor,
            "model_revision": "ac7f9318f633fc4b5778c59367c8128225f1e3de",
            "dino_revision": "a2bb814dd30d776dcf7e30523b00659f4f141c71",
        },
        visualizer_kwargs={"skip": True},
    )()

    expected = Path(args.output_dir) / "data" / "evaluator.csv"
    if not expected.is_file():
        raise RuntimeError(f"Integration test did not create {expected}")
    with expected.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    accepted = sum(row["error"].strip().lower() == "false" for row in rows)
    if accepted == 0:
        raise RuntimeError(
            "All integration examples were filtered. Increase --n-examples "
            "to exercise a successful edit."
        )
    print(f"Integration smoke test completed: {accepted}/{len(rows)} accepted; {expected}")


if __name__ == "__main__":
    main()
