"""Group-disjoint L1 localization for CETT feature matrices."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.linear_model import LogisticRegression

from hidden_commitment.metrics import binary_metrics


@dataclass(frozen=True, slots=True)
class SparseLocalization:
    weights: np.ndarray
    intercept: float
    best_c: float
    validation_metrics: dict[str, float]
    selected_feature_indices: np.ndarray

    @property
    def nonzero_indices(self) -> np.ndarray:
        return np.flatnonzero(self.weights)

    def neurons(self, intermediate_size: int) -> list[dict[str, Any]]:
        result = []
        for index in self.nonzero_indices:
            result.append(
                {
                    "layer": int(index // intermediate_size),
                    "neuron": int(index % intermediate_size),
                    "weight": float(self.weights[index]),
                    "sign": 1 if self.weights[index] > 0 else -1,
                }
            )
        return sorted(result, key=lambda item: abs(item["weight"]), reverse=True)


def split_groups(
    groups: np.ndarray,
    *,
    train_ratio: float = 0.7,
    validation_ratio: float = 0.15,
    seed: int = 42,
) -> dict[str, np.ndarray]:
    """Split whole question IDs so paired/order variants cannot leak across splits."""

    groups = np.asarray(groups)
    unique = np.unique(groups)
    if unique.size < 3:
        raise ValueError("At least three unique groups are required")
    shuffled = np.random.default_rng(seed).permutation(unique)
    train_end = max(1, min(int(len(shuffled) * train_ratio), len(shuffled) - 2))
    validation_size = max(1, int(len(shuffled) * validation_ratio))
    validation_end = min(train_end + validation_size, len(shuffled) - 1)
    selected = {
        "train": shuffled[:train_end],
        "validation": shuffled[train_end:validation_end],
        "test": shuffled[validation_end:],
    }
    return {name: np.isin(groups, values) for name, values in selected.items()}


def fit_sparse_localization(
    train_features: np.ndarray,
    train_labels: np.ndarray,
    validation_features: np.ndarray,
    validation_labels: np.ndarray,
    *,
    c_values: tuple[float, ...] = (0.001, 0.01, 0.1, 1.0, 10.0),
    max_features: int | None = 2_000,
    max_iter: int = 2_000,
    seed: int = 42,
) -> SparseLocalization:
    """Select ``C`` by validation AUROC, accuracy, then sparsity."""

    train_features = np.asarray(train_features, dtype=np.float32)
    validation_features = np.asarray(validation_features, dtype=np.float32)
    train_labels = np.asarray(train_labels, dtype=np.int32)
    validation_labels = np.asarray(validation_labels, dtype=np.int32)
    if np.unique(train_labels).size != 2 or np.unique(validation_labels).size != 2:
        raise ValueError("Train and validation splits must both contain two classes")

    selector: SelectKBest | None = None
    if max_features is not None and max_features < train_features.shape[1]:
        selector = SelectKBest(f_classif, k=max_features)
        train_selected = selector.fit_transform(train_features, train_labels)
        validation_selected = selector.transform(validation_features)
        selected_indices = selector.get_support(indices=True)
    else:
        train_selected = train_features
        validation_selected = validation_features
        selected_indices = np.arange(train_features.shape[1])

    best: tuple[tuple[float, float, int], float, LogisticRegression, dict[str, float]] | None = None
    for c_value in c_values:
        classifier = LogisticRegression(
            l1_ratio=1.0,
            solver="liblinear",
            C=c_value,
            max_iter=max_iter,
            class_weight="balanced",
            random_state=seed,
        )
        classifier.fit(train_selected, train_labels)
        probabilities = classifier.predict_proba(validation_selected)[:, 1]
        metrics = binary_metrics(validation_labels, probabilities)
        nonzero = int(np.count_nonzero(classifier.coef_))
        rank = (metrics["auroc"], metrics["accuracy"], -nonzero)
        if best is None or rank > best[0]:
            best = rank, c_value, classifier, metrics
    if best is None:
        raise RuntimeError("No classifier was trained")
    _, best_c, _selected_classifier, metrics = best
    final_classifier = LogisticRegression(
        l1_ratio=1.0,
        solver="liblinear",
        C=best_c,
        max_iter=max_iter,
        class_weight="balanced",
        random_state=seed,
    )
    final_classifier.fit(
        np.concatenate([train_selected, validation_selected]),
        np.concatenate([train_labels, validation_labels]),
    )
    weights = np.zeros(train_features.shape[1], dtype=np.float32)
    weights[selected_indices] = final_classifier.coef_[0].astype(np.float32)
    return SparseLocalization(
        weights=weights,
        intercept=float(final_classifier.intercept_[0]),
        best_c=float(best_c),
        validation_metrics=metrics,
        selected_feature_indices=np.asarray(selected_indices),
    )


def stable_neurons(
    localizations: list[SparseLocalization],
    *,
    minimum_runs: int | None = None,
) -> list[dict[str, float | int]]:
    """Find features recurring with the same non-zero sign across localization runs."""

    if not localizations:
        return []
    width = localizations[0].weights.size
    if any(item.weights.size != width for item in localizations):
        raise ValueError("All localization runs must use the same feature layout")
    required = minimum_runs if minimum_runs is not None else len(localizations)
    if not 1 <= required <= len(localizations):
        raise ValueError("minimum_runs must be between one and the number of runs")
    weights = np.stack([item.weights for item in localizations])
    result: list[dict[str, float | int]] = []
    for feature in range(width):
        nonzero = weights[:, feature][weights[:, feature] != 0]
        if nonzero.size < required:
            continue
        signs = np.sign(nonzero)
        for sign in (-1, 1):
            signed = nonzero[signs == sign]
            if signed.size >= required:
                result.append(
                    {
                        "feature": feature,
                        "sign": sign,
                        "runs": int(signed.size),
                        "mean_weight": float(signed.mean()),
                    }
                )
    return sorted(result, key=lambda item: (-int(item["runs"]), -abs(item["mean_weight"])))
