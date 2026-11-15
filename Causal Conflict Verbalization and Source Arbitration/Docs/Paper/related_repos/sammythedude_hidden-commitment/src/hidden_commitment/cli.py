"""Command-line entry points for environment checks and cached-feature analysis."""

from __future__ import annotations

import argparse
import json
import platform
import sys
from pathlib import Path

import numpy as np
import torch

from hidden_commitment.config import DEFAULT_QWEN
from hidden_commitment.directions import select_direction
from hidden_commitment.io import write_json
from hidden_commitment.localization import fit_sparse_localization, split_groups


def _comma_floats(value: str) -> tuple[float, ...]:
    parsed = tuple(float(part.strip()) for part in value.split(",") if part.strip())
    if not parsed:
        raise argparse.ArgumentTypeError("Expected at least one comma-separated number")
    return parsed


def command_doctor(_args: argparse.Namespace) -> None:
    report = {
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "torch": torch.__version__,
        "cuda_available": torch.cuda.is_available(),
        "cuda_version": torch.version.cuda,
        "gpu": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
        "default_model": DEFAULT_QWEN.model_id,
        "default_revision": DEFAULT_QWEN.revision,
    }
    print(json.dumps(report, indent=2))


def command_localize(args: argparse.Namespace) -> None:
    data = np.load(args.features, allow_pickle=False)
    features = data[args.feature_key]
    labels = data[args.label_key]
    groups = data[args.group_key]
    masks = split_groups(
        groups,
        train_ratio=args.train_ratio,
        validation_ratio=args.validation_ratio,
        seed=args.seed,
    )
    result = fit_sparse_localization(
        features[masks["train"]],
        labels[masks["train"]],
        features[masks["validation"]],
        labels[masks["validation"]],
        c_values=args.c_values,
        max_features=None if args.max_features <= 0 else args.max_features,
        max_iter=args.max_iter,
        seed=args.seed,
    )
    weights_path = args.output.with_suffix(".weights.npy")
    weights_path.parent.mkdir(parents=True, exist_ok=True)
    np.save(weights_path, result.weights)
    payload = {
        "feature_file": str(args.features),
        "feature_shape": list(features.shape),
        "best_c": result.best_c,
        "validation_metrics": result.validation_metrics,
        "num_nonzero": int(result.nonzero_indices.size),
        "sparsity_percent": float(100 * result.nonzero_indices.size / result.weights.size),
        "intermediate_size": args.intermediate_size,
        "neurons": result.neurons(args.intermediate_size),
        "weights_file": str(weights_path),
        "split_counts": {name: int(mask.sum()) for name, mask in masks.items()},
    }
    write_json(args.output, payload)
    print(json.dumps(payload, indent=2))


def command_fit_direction(args: argparse.Namespace) -> None:
    data = np.load(args.features, allow_pickle=False)
    features = data[args.feature_key]
    labels = data[args.label_key]
    groups = data[args.group_key]
    positions = [str(value) for value in data[args.position_key].tolist()]
    masks = split_groups(
        groups,
        train_ratio=args.train_ratio,
        validation_ratio=args.validation_ratio,
        seed=args.seed,
    )
    conditions = data[args.condition_key] if args.condition_key in data.files else None
    selected, candidates = select_direction(
        features[masks["train"]],
        labels[masks["train"]],
        features[masks["validation"]],
        labels[masks["validation"]],
        positions=positions,
        validation_conditions=conditions[masks["validation"]] if conditions is not None else None,
    )
    payload = {
        "feature_file": str(args.features),
        "selected_direction": selected.to_dict(),
        "split_counts": {name: int(mask.sum()) for name, mask in masks.items()},
        "candidates": candidates,
    }
    write_json(args.output, payload)
    print(
        json.dumps(
            {"selected_direction": {k: v for k, v in selected.to_dict().items() if k != "unit"}},
            indent=2,
        )
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="hidden-commitment")
    subparsers = parser.add_subparsers(dest="command", required=True)

    doctor = subparsers.add_parser("doctor", help="Report the local Python/PyTorch/GPU environment")
    doctor.set_defaults(handler=command_doctor)

    localize = subparsers.add_parser(
        "localize", help="Fit an L1 classifier to cached CETT features"
    )
    localize.add_argument("features", type=Path)
    localize.add_argument("--output", type=Path, default=Path("artifacts/localization.json"))
    localize.add_argument("--feature-key", default="X")
    localize.add_argument("--label-key", default="y")
    localize.add_argument("--group-key", default="qids")
    localize.add_argument("--intermediate-size", type=int, default=3584)
    localize.add_argument("--max-features", type=int, default=2000)
    localize.add_argument("--c-values", type=_comma_floats, default=(0.001, 0.01, 0.1, 1.0, 10.0))
    localize.add_argument("--max-iter", type=int, default=2000)
    localize.add_argument("--train-ratio", type=float, default=0.70)
    localize.add_argument("--validation-ratio", type=float, default=0.15)
    localize.add_argument("--seed", type=int, default=42)
    localize.set_defaults(handler=command_localize)

    direction = subparsers.add_parser(
        "fit-direction", help="Select a contrastive residual direction from cached features"
    )
    direction.add_argument("features", type=Path)
    direction.add_argument("--output", type=Path, default=Path("artifacts/direction.json"))
    direction.add_argument("--feature-key", default="X")
    direction.add_argument("--label-key", default="y")
    direction.add_argument("--group-key", default="qids")
    direction.add_argument("--position-key", default="positions")
    direction.add_argument("--condition-key", default="conditions")
    direction.add_argument("--train-ratio", type=float, default=0.70)
    direction.add_argument("--validation-ratio", type=float, default=0.15)
    direction.add_argument("--seed", type=int, default=42)
    direction.set_defaults(handler=command_fit_direction)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    args.handler(args)


if __name__ == "__main__":
    main()
