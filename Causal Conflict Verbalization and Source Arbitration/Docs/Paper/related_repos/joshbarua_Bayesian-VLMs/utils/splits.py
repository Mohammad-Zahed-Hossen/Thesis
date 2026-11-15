"""Stratified / within-dataset / cross-dataset split helpers shared across pipelines."""

from __future__ import annotations

import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from config import TRAIN_RATIO, VAL_RATIO, DEFAULT_SEED


def create_stratified_splits(
    ids: list[int],
    datasets: list[str],
    train_ratio: float = TRAIN_RATIO,
    val_ratio: float = VAL_RATIO,
    seed: int = DEFAULT_SEED,
) -> dict:
    """
    Create stratified train/val/test splits preserving dataset proportions.

    Args:
        ids: Example indices
        datasets: Dataset label per example (e.g. "DocVQA" or "VQAv2")
        train_ratio: Fraction for training
        val_ratio: Fraction for validation
        seed: Random seed

    Returns:
        Dictionary with 'train', 'val', 'test' lists of IDs, plus metadata.
    """
    rng = random.Random(seed)

    groups: dict[str, list[int]] = {}
    for idx, ds_name in zip(ids, datasets):
        groups.setdefault(ds_name, []).append(idx)

    train_ids, val_ids, test_ids = [], [], []

    for ds_name, ds_ids in groups.items():
        ds_ids = sorted(ds_ids)
        rng.shuffle(ds_ids)
        n = len(ds_ids)
        n_train = int(n * train_ratio)
        n_val = int(n * val_ratio)

        train_ids.extend(ds_ids[:n_train])
        val_ids.extend(ds_ids[n_train:n_train + n_val])
        test_ids.extend(ds_ids[n_train + n_val:])

    return {
        "train": sorted(train_ids),
        "val": sorted(val_ids),
        "test": sorted(test_ids),
        "seed": seed,
        "train_ratio": train_ratio,
        "val_ratio": val_ratio,
    }


def create_within_dataset_splits(
    ids: list[int],
    datasets: list[str],
    target_dataset: str,
    train_ratio: float = TRAIN_RATIO,
    val_ratio: float = VAL_RATIO,
    seed: int = DEFAULT_SEED,
) -> dict:
    """
    Create train/val/test splits using only examples from a single dataset.

    Args:
        ids: Example indices
        datasets: Dataset label per example
        target_dataset: Name of the dataset to use (e.g. "DocVQA" or "VQAv2")
        train_ratio: Fraction for training
        val_ratio: Fraction for validation
        seed: Random seed

    Returns:
        Dictionary with 'train', 'val', 'test' lists of IDs.
    """
    rng = random.Random(seed)

    ds_ids = [i for i, d in zip(ids, datasets) if d == target_dataset]
    rng.shuffle(ds_ids)

    n = len(ds_ids)
    n_train = int(n * train_ratio)
    n_val = int(n * val_ratio)

    return {
        "train": sorted(ds_ids[:n_train]),
        "val": sorted(ds_ids[n_train:n_train + n_val]),
        "test": sorted(ds_ids[n_train + n_val:]),
        "seed": seed,
        "target_dataset": target_dataset,
        "train_ratio": train_ratio,
        "val_ratio": val_ratio,
    }


def create_cross_dataset_splits(
    ids: list[int],
    datasets: list[str],
    source_dataset: str,
    train_ratio: float = 0.85,
    seed: int = DEFAULT_SEED,
) -> dict:
    """
    Create cross-dataset splits: train/val on source, test on target.

    Args:
        ids: Example indices
        datasets: Dataset label per example
        source_dataset: Name of the source dataset (train/val come from here)
        train_ratio: Fraction of source for training (rest is val)
        seed: Random seed

    Returns:
        Dictionary with 'train', 'val', 'test' lists of IDs.
    """
    rng = random.Random(seed)

    source_ids = [i for i, d in zip(ids, datasets) if d == source_dataset]
    target_ids = [i for i, d in zip(ids, datasets) if d != source_dataset]

    rng.shuffle(source_ids)
    n_train = int(len(source_ids) * train_ratio)

    return {
        "train": sorted(source_ids[:n_train]),
        "val": sorted(source_ids[n_train:]),
        "test": sorted(target_ids),
        "seed": seed,
        "source_dataset": source_dataset,
        "train_ratio": train_ratio,
    }
