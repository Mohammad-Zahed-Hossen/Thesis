#!/usr/bin/env python3
"""
run_degradation_scoring.py -- Score VLM probes across a (blur, text) degradation grid.

For each example, scores text/vision/joint probes at every combination of:
  - Gaussian blur levels: selected by --grid preset
  - Text levels: selected by --grid preset and --text_degradation type

Optimizations:
  - Text probe only depends on text level (not blur) -> computed once per text level
  - Vision probe only depends on blur level (not text) -> computed once per blur level
  - Joint probe depends on both -> computed for every (blur, text) cell

Usage:
  python transitions/run_degradation_scoring.py --run_id my_run --grid 6x6
  python transitions/run_degradation_scoring.py --run_id my_run --grid 6x6 \
      --model_name Qwen/Qwen2.5-VL-3B-Instruct --splits train val test
"""

import argparse
import json
import random
import sys
from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd
import torch
from datasets import load_dataset, load_from_disk
from PIL import Image, ImageFilter
from tqdm import tqdm

# Allow imports from the conflicting_modality package root
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from config import (
    QWEN_MODEL,
    HF_CACHE_DIR,
    CONFLICTING_MODALITY_DATASET,
    TRAIN_RATIO,
    VAL_RATIO,
    DEFAULT_SEED,
    GRID_PRESETS,
    get_run_dir,
    get_token_noise_probs,
    get_token_noise_labels,
    get_prior_prefill,
)
from scoring import (
    VLMScorer,
    blur_image,
    get_grid_config,
    load_text_variants,
    logp_to_prob,
    normalized_entropy,
)
from utils.splits import (
    create_stratified_splits,
    create_within_dataset_splits,
    create_cross_dataset_splits,
)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Score VLM probes across degradation grid"
    )
    parser.add_argument(
        "--run_id", type=str, required=True,
        help="Run identifier for output directory"
    )
    parser.add_argument(
        "--grid", type=str, default="6x6",
        choices=list(GRID_PRESETS.keys()),
        help=f"Grid preset (default: 6x6). Options: {list(GRID_PRESETS.keys())}"
    )
    parser.add_argument(
        "--text_degradation", type=str, default="token_noise",
        choices=["token_noise"],
        help="Text degradation approach (token-noise only)"
    )
    parser.add_argument(
        "--sample", type=int, default=None,
        help="Only process first N examples per split (for testing)"
    )
    parser.add_argument(
        "--model_name", type=str, default=QWEN_MODEL,
        help=f"VLM model name (default: {QWEN_MODEL})"
    )
    parser.add_argument(
        "--load_in_4bit", action="store_true",
        help="Load model in 4-bit quantization"
    )
    parser.add_argument(
        "--load_in_8bit", action="store_true",
        help="Load model in 8-bit quantization"
    )
    parser.add_argument(
        "--seed", type=int, default=DEFAULT_SEED,
        help=f"Random seed (default: {DEFAULT_SEED})"
    )
    parser.add_argument(
        "--dataset_path", type=str, default=None,
        help="Path to local dataset (overrides HuggingFace dataset)"
    )
    parser.add_argument(
        "--checkpoint_every", type=int, default=10,
        help="Save checkpoint every N examples (default: 10)"
    )
    parser.add_argument(
        "--splits", type=str, nargs="+", default=["test"],
        choices=["train", "val", "test"],
        help="Which data splits to score (default: test only)"
    )
    parser.add_argument(
        "--shard_id", type=int, default=None,
        help="Shard index for multi-GPU parallel scoring (0-indexed)"
    )
    parser.add_argument(
        "--num_shards", type=int, default=None,
        help="Total number of shards for parallel scoring"
    )
    args = parser.parse_args()

    prior_prefill = get_prior_prefill(args.model_name)
    if prior_prefill is not None:
        print(f"NOTE: prior probe uses assistant prefill for "
              f"{args.model_name}: {prior_prefill!r}")

    random.seed(args.seed)
    np.random.seed(args.seed)

    run_dir = get_run_dir(args.run_id)
    run_dir.mkdir(parents=True, exist_ok=True)
    print(f"Run directory: {run_dir}")

    # Resolve grid configuration
    blur_sigmas, text_levels, text_labels = get_grid_config(args.grid, args.text_degradation)
    n_blur = len(blur_sigmas)
    n_text = len(text_levels)

    # Number of generated variants to expect from the degradation file.
    # Preset includes a leading 0 (original, not generated); drop it.
    n_generated = sum(1 for p in get_token_noise_probs(args.grid) if p > 0)

    # Load dataset
    if args.dataset_path:
        print(f"\nLoading dataset from local path: {args.dataset_path}")
        ds_dict = load_from_disk(args.dataset_path)
    else:
        print(f"\nLoading dataset: {CONFLICTING_MODALITY_DATASET}")
        ds_dict = load_dataset(CONFLICTING_MODALITY_DATASET, cache_dir=HF_CACHE_DIR)

    # Combine all splits
    splits_order = sorted(ds_dict.keys())
    all_examples = []
    for split_name in splits_order:
        ds = ds_dict[split_name]
        if args.sample:
            ds = ds.select(range(min(args.sample, len(ds))))
        for ex in ds:
            all_examples.append(ex)

    print(f"Total examples: {len(all_examples)}")

    # Load text degradations
    print(f"\nLoading text degradations (type={args.text_degradation})...")
    text_degs = {}
    offset = 0
    for split_name in splits_order:
        ds = ds_dict[split_name]
        n = min(args.sample, len(ds)) if args.sample else len(ds)
        split_degs = load_text_variants(args.text_degradation, split_name, args.grid)
        for i in range(n):
            global_idx = offset + i
            deg_variants = split_degs.get(str(i))
            if deg_variants is None:
                print(f"  WARNING: no degradation for {split_name}[{i}], using original text repeated")
                text_degs[global_idx] = None
            else:
                text_degs[global_idx] = deg_variants
        offset += n

    # Create splits (same logic as run_scoring.py)
    all_ids = list(range(len(all_examples)))
    all_datasets = [ex["dataset"] for ex in all_examples]

    within_splits = create_stratified_splits(all_ids, all_datasets, seed=args.seed)
    unique_datasets = sorted(set(all_datasets))

    cross_splits = {}
    for source_ds in unique_datasets:
        cross_splits[f"train_on_{source_ds}"] = create_cross_dataset_splits(
            all_ids, all_datasets, source_dataset=source_ds, seed=args.seed
        )

    within_dataset_splits = {}
    for ds_name in unique_datasets:
        within_dataset_splits[ds_name] = create_within_dataset_splits(
            all_ids, all_datasets, target_dataset=ds_name, seed=args.seed
        )

    splits_info = {
        "within_mixture": within_splits,
        "cross_dataset": cross_splits,
        "within_dataset": within_dataset_splits,
    }

    splits_path = run_dir / "splits.json"
    with open(splits_path, "w") as f:
        json.dump(splits_info, f, indent=2)
    print(f"Splits saved to {splits_path}")

    # Determine which examples to score based on --splits
    score_ids = set()
    for split_name in args.splits:
        score_ids |= set(within_splits[split_name])
    print(f"\nScoring splits {args.splits}: {len(score_ids)} examples "
          f"(out of {len(all_examples)} total)")

    # Shard for multi-GPU parallelism
    if args.shard_id is not None and args.num_shards is not None:
        score_ids_sorted = sorted(score_ids)
        score_ids = set(score_ids_sorted[args.shard_id::args.num_shards])
        print(f"  Shard {args.shard_id}/{args.num_shards}: {len(score_ids)} examples")

    # Load checkpoint if exists, or resume from existing parquet
    shard_suffix = f"_shard_{args.shard_id}" if args.shard_id is not None else ""
    checkpoint_path = run_dir / f"degradation_checkpoint{shard_suffix}.json"
    scores_path = run_dir / f"degradation_scores{shard_suffix}.parquet"
    completed_ids = set()
    all_rows = []
    if checkpoint_path.exists():
        print(f"\nLoading checkpoint from {checkpoint_path}")
        with open(checkpoint_path) as f:
            ckpt_data = json.load(f)
        all_rows = ckpt_data.get("rows", [])
        completed_ids = set(ckpt_data.get("completed_ids", []))
        print(f"  Resuming from checkpoint: {len(completed_ids)} examples already done")
    elif scores_path.exists():
        print(f"\nLoading existing scores from {scores_path}")
        existing_df = pd.read_parquet(scores_path)
        all_rows = existing_df.to_dict("records")
        completed_ids = set(existing_df["id"].unique())
        remaining = score_ids - completed_ids
        print(f"  Found {len(completed_ids)} scored examples, {len(remaining)} remaining")
        if len(remaining) == 0:
            print("  All requested examples already scored — nothing to do.")
            return

    # Initialize scorer
    print("\nInitializing VLM scorer...")
    scorer = VLMScorer(
        model_name=args.model_name,
        load_in_4bit=args.load_in_4bit,
        load_in_8bit=args.load_in_8bit,
    )

    print(f"\nDegradation grid: {args.grid} ({n_blur} blur x {n_text} text)")
    print(f"Text degradation: {args.text_degradation}")
    print(f"Blur sigmas: {blur_sigmas}")
    print(f"Text levels: {text_levels} -> {text_labels}")
    n_fwd = n_text + n_blur + n_blur * n_text
    print(f"Forward passes per example: {n_text} (text) + {n_blur} (vision) + {n_blur * n_text} (joint) = {n_fwd}")
    print(f"\nScoring examples...")

    remaining_ids = sorted(score_ids - completed_ids)
    desc = f"Scoring (shard {args.shard_id})" if args.shard_id is not None else "Scoring"
    for idx in tqdm(remaining_ids, desc=desc):
        example = all_examples[idx]

        dataset_name = example["dataset"]
        question = example["question"]
        original_text = example["text"]
        image = example["image"]
        a_T = example["text_answer"]
        a_V = example["vision_answer"]

        # Build text variants: index 0 = original, indices 1..n_generated = degraded
        deg_variants = text_degs.get(idx)
        text_variants = [original_text]
        if deg_variants is not None:
            vals = list(deg_variants)[:n_generated]
            if len(vals) == 0:
                vals = [original_text] * n_generated
            elif len(vals) < n_generated:
                vals.extend([vals[-1]] * (n_generated - len(vals)))
            text_variants.extend(vals)
        else:
            text_variants.extend([original_text] * n_generated)

        # --- Prior probe: question only, no text passage, no image. ---
        # Gives pi_0 = log P(a_T | q) - log P(a_V | q), the model's marginal
        # answer prior used by the calibrated naive-Bayes baseline
        # s_J = s_T + s_V - pi_0 in fit_degraded.py. For Gemma3 the assistant
        # turn is prefilled with get_prior_prefill(model_name) to push the
        # divergence past the model's "explanation-mode" opening.
        prior_scores = scorer.score_pair(question, None, a_T, a_V,
                                         prefill=prior_prefill)

        # --- Text probes: one per selected text level (blur-independent) ---
        text_scores = {}
        for m in text_levels:
            prompt_text = f"{text_variants[m]} {question}"
            scores = scorer.score_pair(prompt_text, None, a_T, a_V)
            text_scores[m] = scores

        # --- Vision probes: one per blur sigma (text-independent) ---
        vision_scores = {}
        for k, sigma in enumerate(blur_sigmas):
            blurred = blur_image(image, sigma)
            prompt_vision = f"{question}"
            scores = scorer.score_pair(prompt_vision, blurred, a_T, a_V)
            vision_scores[k] = scores

        # --- Joint probes: one per (blur, text) cell ---
        joint_scores = {}
        for k, sigma in enumerate(blur_sigmas):
            blurred = blur_image(image, sigma)
            for m in text_levels:
                prompt_joint = f"{text_variants[m]} {question}"
                scores = scorer.score_pair(prompt_joint, blurred, a_T, a_V)
                joint_scores[(k, m)] = scores

        # --- Build rows for all grid cells ---
        for k, sigma in enumerate(blur_sigmas):
            for m in text_levels:
                ts = text_scores[m]
                vs = vision_scores[k]
                js = joint_scores[(k, m)]

                row = {
                    "id": idx,
                    "dataset": dataset_name,
                    "a_T": a_T,
                    "a_V": a_V,
                    "blur_level": k,
                    "blur_sigma": sigma,
                    "text_level": m,
                    # Prior probe (constant per id; copied to every grid cell)
                    "ll_prior_T": prior_scores["ll_T"],
                    "ll_prior_V": prior_scores["ll_V"],
                    "pi_0": prior_scores["s"],
                    "p_prior_T": prior_scores["p_T"],
                    # Text probe
                    "ll_text_T": ts["ll_T"],
                    "ll_text_V": ts["ll_V"],
                    "s_T": ts["s"],
                    "p_T": ts["p_T"],
                    "c_T": ts["e"],
                    # Vision probe
                    "ll_vision_T": vs["ll_T"],
                    "ll_vision_V": vs["ll_V"],
                    "s_V": vs["s"],
                    "p_V": vs["p_T"],
                    "c_V": vs["e"],
                    # Joint probe
                    "ll_joint_T": js["ll_T"],
                    "ll_joint_V": js["ll_V"],
                    "s_J": js["s"],
                    "p_J": js["p_T"],
                }
                all_rows.append(row)

        completed_ids.add(idx)

        # Checkpoint
        if (len(completed_ids)) % args.checkpoint_every == 0:
            ckpt_data = {
                "completed_ids": sorted(completed_ids),
                "rows": all_rows,
            }
            with open(checkpoint_path, "w") as f:
                json.dump(ckpt_data, f)

    # Save final results
    df = pd.DataFrame(all_rows)
    df.to_parquet(scores_path, index=False)
    print(f"\nScores saved to {scores_path}")
    print(f"Total rows: {len(df)} ({len(completed_ids)} examples x {n_blur * n_text} grid cells)")

    # Save metadata
    meta = {
        "grid": args.grid,
        "text_degradation": args.text_degradation,
        "blur_sigmas": blur_sigmas,
        "text_levels": text_levels,
        "text_labels": text_labels,
        "model_name": args.model_name,
        "seed": args.seed,
    }
    meta_path = run_dir / "degradation_meta.json"
    with open(meta_path, "w") as f:
        json.dump(meta, f, indent=2)
    print(f"Metadata saved to {meta_path}")

    # Clean up checkpoint
    if checkpoint_path.exists():
        checkpoint_path.unlink()
        print("Checkpoint cleaned up.")

    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    print(f"Model: {args.model_name}")
    print(f"Grid: {args.grid} ({n_blur} blur x {n_text} text = {n_blur * n_text} cells/example)")
    print(f"Text degradation: {args.text_degradation}")
    print(f"Examples: {len(completed_ids)}")
    print(f"Total rows: {len(df)}")
    print(f"\nEvidence strength by blur level:")
    for k, sigma in enumerate(blur_sigmas):
        subset = df[df["blur_level"] == k]
        print(f"  sigma={sigma:2d}: mean |s_V|={subset['c_V'].mean():.4f}")
    print(f"\nEvidence strength by text level:")
    for m_idx, m in enumerate(text_levels):
        subset = df[df["text_level"] == m]
        print(f"  m={m} ({text_labels[m_idx]}): mean |s_T|={subset['c_T'].mean():.4f}")
    print(f"{'='*60}")
    print(f"\nOutput directory: {run_dir}")


if __name__ == "__main__":
    main()
