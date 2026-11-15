"""Contrastive residual directions, validation sweeps, and controls."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np

from hidden_commitment.metrics import safe_auroc


@dataclass(frozen=True, slots=True)
class ContrastiveDirection:
    layer: int
    position: str
    unit: np.ndarray
    positive_label: str = "doc2"
    negative_label: str = "doc1"

    def __post_init__(self) -> None:
        vector = np.asarray(self.unit, dtype=np.float32).reshape(-1)
        norm = float(np.linalg.norm(vector))
        if not np.isfinite(norm) or norm <= 1e-12:
            raise ValueError("Direction must have a finite non-zero norm")
        object.__setattr__(self, "unit", vector / norm)

    def project(self, vectors: np.ndarray) -> np.ndarray:
        return np.asarray(vectors) @ self.unit

    def to_dict(self) -> dict[str, Any]:
        return {
            "layer": self.layer,
            "position": self.position,
            "unit": self.unit.tolist(),
            "positive_label": self.positive_label,
            "negative_label": self.negative_label,
        }

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> ContrastiveDirection:
        return cls(
            layer=int(value["layer"]),
            position=str(value["position"]),
            unit=np.asarray(value["unit"], dtype=np.float32),
            positive_label=str(value.get("positive_label", "doc2")),
            negative_label=str(value.get("negative_label", "doc1")),
        )


def fit_contrastive_direction(positive: np.ndarray, negative: np.ndarray) -> np.ndarray:
    """Fit a normalized difference-of-means direction."""

    positive = np.asarray(positive, dtype=np.float64)
    negative = np.asarray(negative, dtype=np.float64)
    if positive.ndim != 2 or negative.ndim != 2 or positive.shape[1] != negative.shape[1]:
        raise ValueError("positive and negative must be 2-D arrays with the same width")
    if not len(positive) or not len(negative):
        raise ValueError("Both classes require at least one example")
    direction = positive.mean(axis=0) - negative.mean(axis=0)
    norm = np.linalg.norm(direction)
    if not np.isfinite(norm) or norm <= 1e-12:
        raise ValueError("Class means do not define a finite non-zero direction")
    return (direction / norm).astype(np.float32)


def orthogonal_random_unit(reference: np.ndarray, seed: int = 42) -> np.ndarray:
    reference = np.asarray(reference, dtype=np.float64).reshape(-1)
    reference /= np.linalg.norm(reference)
    random = np.random.default_rng(seed).standard_normal(reference.size)
    random -= np.dot(random, reference) * reference
    norm = np.linalg.norm(random)
    if norm <= 1e-12:
        raise RuntimeError("Failed to sample an orthogonal random direction")
    return (random / norm).astype(np.float32)


def select_direction(
    train: np.ndarray,
    train_labels: np.ndarray,
    validation: np.ndarray,
    validation_labels: np.ndarray,
    *,
    positions: list[str],
    validation_conditions: np.ndarray | None = None,
) -> tuple[ContrastiveDirection, list[dict[str, Any]]]:
    """Select a layer/position using validation AUROC only.

    Arrays must have shape ``[samples, positions, layers, hidden]``. If
    conditions are supplied, the ranking follows the paper: mean condition
    AUROC, minimum condition AUROC, then pooled AUROC.
    """

    train = np.asarray(train)
    validation = np.asarray(validation)
    train_labels = np.asarray(train_labels, dtype=np.int32)
    validation_labels = np.asarray(validation_labels, dtype=np.int32)
    if train.ndim != 4 or validation.ndim != 4:
        raise ValueError("Feature arrays must have shape [samples, positions, layers, hidden]")
    if train.shape[1:] != validation.shape[1:] or train.shape[1] != len(positions):
        raise ValueError("Train/validation feature layouts do not match positions")
    condition_values = (
        np.unique(validation_conditions) if validation_conditions is not None else np.array([])
    )
    candidates: list[dict[str, Any]] = []
    best_rank: tuple[float, ...] | None = None
    best: ContrastiveDirection | None = None

    for position_index, position in enumerate(positions):
        for layer in range(train.shape[2]):
            try:
                unit = fit_contrastive_direction(
                    train[train_labels == 1, position_index, layer],
                    train[train_labels == 0, position_index, layer],
                )
            except ValueError:
                continue
            scores = validation[:, position_index, layer] @ unit
            pooled = safe_auroc(validation_labels, scores)
            if pooled is None:
                continue
            condition_aurocs: dict[str, float] = {}
            for condition in condition_values:
                mask = validation_conditions == condition
                value = safe_auroc(validation_labels[mask], scores[mask])
                if value is not None:
                    condition_aurocs[str(condition)] = value
            usable = list(condition_aurocs.values())
            mean_condition = float(np.mean(usable)) if usable else pooled
            min_condition = float(np.min(usable)) if usable else pooled
            positive_mean = scores[validation_labels == 1].mean()
            negative_mean = scores[validation_labels == 0].mean()
            gap = float(positive_mean - negative_mean)
            candidate = {
                "position": position,
                "layer": layer,
                "validation_auroc": pooled,
                "condition_aurocs": condition_aurocs,
                "mean_condition_auroc": mean_condition,
                "min_condition_auroc": min_condition,
                "class_mean_gap": gap,
            }
            candidates.append(candidate)
            rank = (mean_condition, min_condition, pooled, gap)
            if best_rank is None or rank > best_rank:
                best_rank = rank
                best = ContrastiveDirection(layer=layer, position=position, unit=unit)
    if best is None:
        raise RuntimeError("No valid direction candidate could be selected")
    return best, candidates
