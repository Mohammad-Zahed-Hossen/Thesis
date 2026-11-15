#!/usr/bin/env python3
"""
generate_text_degradations.py -- Generate token-noise text degradations.

Algorithmic word-level noise: for each passage, a single random permutation of
word positions is sampled, and level *i* substitutes the first
``round(n_words * probs[i])`` positions with random in-domain vocabulary words.
Levels are therefore nested (each a strict superset of the previous), preserving
the reliability ordering along the text axis.

Output:
  text_degradations/token_noise_{grid}_{split}.json
  Format: {str(idx): [variant_1, ..., variant_N]} (one variant per non-zero
  token-noise probability in the grid preset). Level 0 (original text) is NOT
  stored -- it is loaded from the dataset at eval time.

Usage:
  python transitions/generate_text_degradations.py --grid 6x6
  python transitions/generate_text_degradations.py --grid 6x6 --dataset_path /path/to/dataset_pixnorm
"""

import argparse
import json
import random
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from datasets import load_dataset, load_from_disk
from tqdm import tqdm

from config import (
    CONFLICTING_MODALITY_DATASET,
    GRID_PRESETS,
    get_token_noise_probs,
)

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
SPLITS = ["DocVQA", "VQAv2", "RealworldQA"]
_PARENT_DIR = Path(__file__).resolve().parent.parent  # repo root
CHECKPOINT_DIR = _PARENT_DIR / "checkpoints"
OUTPUT_DIR = _PARENT_DIR / "text_degradations"


# ---------------------------------------------------------------------------
# Token noise helpers
# ---------------------------------------------------------------------------

_STOP_WORDS = {
    "the", "a", "an", "and", "or", "but", "in", "on", "at", "to",
    "for", "of", "is", "are", "was", "were", "it", "that", "this",
    "with", "as", "by", "from", "be", "been", "has", "have", "had",
    "not", "no", "so", "if", "its", "their", "they", "he", "she",
    "we", "you", "i", "my", "our", "his", "her", "do", "did", "does",
    "will", "would", "can", "could", "may", "might", "shall", "should",
}


def build_vocab(examples: list[dict], min_freq: int = 3) -> list[str]:
    """Build in-domain word vocabulary from all text evidence fields."""
    counter: Counter = Counter()
    for ex in examples:
        tokens = re.findall(r"[a-zA-Z]+", ex.get("text", "").lower())
        counter.update(tokens)

    vocab = [
        w for w, c in counter.items()
        if c >= min_freq and w not in _STOP_WORDS and len(w) > 2
    ]
    print(f"  [vocab] {len(vocab)} in-domain content words (min_freq={min_freq})")
    return vocab


def noise_text_iterative(
    text: str,
    probs: list[float],
    vocab: list[str],
    rng: random.Random,
) -> list[str]:
    """Apply cumulative word-level noise across increasing probability levels.

    All word positions are shuffled once.  For level *i* with target
    fraction ``probs[i]``, the first ``round(n_words * probs[i])``
    positions in that shuffled order are perturbed, so each level is a
    strict superset of all previous levels.

    Each perturbed word is substituted with a random in-domain vocabulary
    word (capitalization preserved).
    """
    if not vocab:
        return [text] * len(probs)

    words = text.split()
    eligible = list(range(len(words)))
    n_eligible = len(eligible)

    if n_eligible == 0:
        return [text] * len(probs)

    # Shuffle once — order determines which positions are noised first
    rng.shuffle(eligible)

    # Pre-determine the replacement for every eligible position
    perturbations: dict[int, str] = {}
    for idx in eligible:
        word = words[idx]
        replacement = rng.choice(vocab)
        if word and word[0].isupper():
            replacement = replacement.capitalize()
        perturbations[idx] = replacement

    # Build one variant per probability level (cumulative)
    variants: list[str] = []
    for p in probs:
        n_to_noise = int(round(n_eligible * p))
        noised_positions = set(eligible[:n_to_noise])

        result = [
            perturbations[idx] if idx in noised_positions else word
            for idx, word in enumerate(words)
        ]
        variants.append(" ".join(result))

    return variants


# ---------------------------------------------------------------------------
# Checkpointing
# ---------------------------------------------------------------------------

def _file_stem(grid: str) -> str:
    return f"token_noise_{grid}"


def checkpoint_path(split: str, grid: str) -> Path:
    return CHECKPOINT_DIR / f"text_degradations_{_file_stem(grid)}_{split}.json"


def load_checkpoint(split: str, grid: str) -> dict:
    p = checkpoint_path(split, grid)
    if p.exists():
        with open(p) as f:
            return json.load(f)
    return {}


def save_checkpoint(split: str, grid: str, data: dict):
    CHECKPOINT_DIR.mkdir(parents=True, exist_ok=True)
    with open(checkpoint_path(split, grid), "w") as f:
        json.dump(data, f)


def output_file_path(split: str, grid: str) -> Path:
    return OUTPUT_DIR / f"{_file_stem(grid)}_{split}.json"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(
        description="Generate token-noise text degradations"
    )
    ap.add_argument(
        "--grid", type=str, default="6x6",
        choices=list(GRID_PRESETS.keys()),
        help=f"Grid preset (selects token-noise probs). Options: {list(GRID_PRESETS.keys())}"
    )
    ap.add_argument(
        "--sample", type=int, default=None,
        help="Only process first N examples per split (for testing)"
    )
    ap.add_argument(
        "--dataset_path", type=str, default=None,
        help="Path to local dataset (overrides HuggingFace dataset)"
    )
    ap.add_argument(
        "--seed", type=int, default=42,
        help="Random seed for token noise (default: 42)"
    )
    args = ap.parse_args()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    CHECKPOINT_DIR.mkdir(parents=True, exist_ok=True)

    # Load dataset
    if args.dataset_path:
        print(f"Loading dataset from local path: {args.dataset_path}")
        ds_dict = load_from_disk(args.dataset_path)
    else:
        print(f"Loading dataset: {CONFLICTING_MODALITY_DATASET}")
        ds_dict = load_dataset(CONFLICTING_MODALITY_DATASET)

    # Preset includes leading 0 (original, not generated) — drop it here.
    token_noise_probs = [p for p in get_token_noise_probs(args.grid) if p > 0]
    print(f"\nGrid preset: {args.grid}")
    print(f"Noise probabilities (generated): {token_noise_probs}")

    for split in SPLITS:
        print(f"\n{'='*60}")
        print(f"Processing split: {split}")
        print(f"{'='*60}")

        if split not in ds_dict:
            print(f"  Split {split} not found, skipping")
            continue

        ds = ds_dict[split]
        n = min(args.sample, len(ds)) if args.sample else len(ds)
        # We only need text fields; skip image columns to avoid OOM.
        text_cols = [c for c in ("text", "text_answer") if c in ds.column_names]
        ds_text = ds.select_columns(text_cols)
        examples = [ds_text[i] for i in range(n)]
        print(f"  Processing {n} examples")

        ckpt = load_checkpoint(split, args.grid)
        print(f"  Checkpoint: {len(ckpt)} entries")

        vocab = build_vocab(examples)

        for i in tqdm(range(n), desc=f"  {split}"):
            if str(i) in ckpt:
                continue
            text = examples[i]["text"]
            rng = random.Random(args.seed + i)
            variants = noise_text_iterative(text, token_noise_probs, vocab, rng)
            ckpt[str(i)] = variants

            if (i + 1) % 200 == 0:
                save_checkpoint(split, args.grid, ckpt)

        save_checkpoint(split, args.grid, ckpt)

        final = {k: v for k, v in ckpt.items() if v is not None}
        out_path = output_file_path(split, args.grid)
        with open(out_path, "w") as f:
            json.dump(final, f, indent=2)
        print(f"  Saved to {out_path} ({len(final)} entries)")

    print("\nDone!")
    print(f"\nAll outputs -> {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()
