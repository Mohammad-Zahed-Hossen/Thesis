"""Evaluation metrics used across readout and intervention experiments."""

from __future__ import annotations

import math

import numpy as np
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, roc_auc_score


def binary_metrics(
    labels: np.ndarray,
    scores: np.ndarray,
    threshold: float = 0.5,
) -> dict[str, float]:
    labels = np.asarray(labels, dtype=np.int32)
    scores = np.asarray(scores, dtype=np.float64)
    predictions = (scores >= threshold).astype(np.int32)
    result = {
        "accuracy": float(accuracy_score(labels, predictions)),
        "precision": float(precision_score(labels, predictions, zero_division=0)),
        "recall": float(recall_score(labels, predictions, zero_division=0)),
        "f1": float(f1_score(labels, predictions, zero_division=0)),
    }
    result["auroc"] = (
        float(roc_auc_score(labels, scores)) if np.unique(labels).size == 2 else float("nan")
    )
    return result


def safe_auroc(labels: np.ndarray, scores: np.ndarray) -> float | None:
    labels = np.asarray(labels)
    return float(roc_auc_score(labels, scores)) if np.unique(labels).size == 2 else None


def wilson_interval(successes: int, total: int, z: float = 1.96) -> tuple[float, float]:
    if total <= 0:
        return float("nan"), float("nan")
    proportion = successes / total
    denominator = 1.0 + z**2 / total
    center = (proportion + z**2 / (2 * total)) / denominator
    margin = z * math.sqrt((proportion * (1 - proportion) + z**2 / (4 * total)) / total)
    margin /= denominator
    return max(0.0, center - margin), min(1.0, center + margin)
