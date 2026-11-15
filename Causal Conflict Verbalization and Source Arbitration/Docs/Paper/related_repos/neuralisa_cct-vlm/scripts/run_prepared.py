#!/usr/bin/env python3
"""Run PE or CoT on an existing counterfactual generator.csv."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

JUDGE_REVISION = "768f209d9ea81521153ed38c47d515654e938aea"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--generator-csv", type=Path, required=True)
    parser.add_argument("--model", required=True, help="Alias from metadata/models.json")
    parser.add_argument("--mode", choices=("pe", "cot", "ep"), required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--judge-model", default="Qwen/Qwen3-4B-Thinking-2507")
    parser.add_argument("--device", default="cuda")
    parser.add_argument("--override", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    models = json.loads((ROOT / "metadata" / "models.json").read_text())
    if args.model not in models:
        parser.error(f"unknown model '{args.model}'; choose from {', '.join(models)}")
    model = models[args.model]
    prompt_modes = {
        "pe": "predict-then-explain",
        "cot": "chain-of-thought",
        "ep": "explain-then-predict",
    }
    prompt_mode = prompt_modes[args.mode]
    config = {
        "output_dir": str(args.output_dir),
        "override": args.override,
        "run_generator": False,
        "generator": "QwenImageEdit",
        "model": "ChatVLM",
        "evaluator": "LLM-based",
        "model_kwargs": {
            "model_name": model["model_name"],
            "revision": model["revision"],
            "prompt_mode": prompt_mode,
            "device": args.device,
        },
        "evaluator_kwargs": {
            "llm_model_name": args.judge_model,
            "llm_revision": JUDGE_REVISION if args.judge_model == "Qwen/Qwen3-4B-Thinking-2507" else None,
            "device": args.device,
        },
        "visualizer_kwargs": {"skip": True},
    }
    print(json.dumps({"required_transformers": model["transformers"], **config}, indent=2))
    if args.dry_run:
        return

    if not args.generator_csv.is_file():
        raise FileNotFoundError(args.generator_csv)
    data_dir = args.output_dir / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    destination = data_dir / "generator.csv"
    if args.generator_csv.resolve() != destination.resolve():
        shutil.copy2(args.generator_csv, destination)
    (args.output_dir / "config_used.json").write_text(json.dumps(config, indent=2) + "\n")

    from main import CCT
    CCT(**config)()


if __name__ == "__main__":
    main()
