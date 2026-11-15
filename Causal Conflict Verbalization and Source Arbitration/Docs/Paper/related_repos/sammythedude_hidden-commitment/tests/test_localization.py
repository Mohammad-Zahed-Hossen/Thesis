from __future__ import annotations

import numpy as np

from hidden_commitment.localization import (
    SparseLocalization,
    fit_sparse_localization,
    split_groups,
    stable_neurons,
)


def test_group_split_is_disjoint() -> None:
    groups = np.repeat(np.arange(20), 2)
    masks = split_groups(groups, seed=5)
    group_sets = [set(groups[mask]) for mask in masks.values()]
    assert group_sets[0].isdisjoint(group_sets[1])
    assert group_sets[0].isdisjoint(group_sets[2])
    assert group_sets[1].isdisjoint(group_sets[2])
    assert sum(mask.sum() for mask in masks.values()) == len(groups)


def test_sparse_localization_recovers_signal() -> None:
    rng = np.random.default_rng(11)
    train_labels = np.repeat([0, 1], 60)
    validation_labels = np.repeat([0, 1], 30)
    train = rng.normal(size=(120, 20)).astype(np.float32)
    validation = rng.normal(size=(60, 20)).astype(np.float32)
    train[:, 7] += train_labels * 4
    validation[:, 7] += validation_labels * 4
    result = fit_sparse_localization(
        train,
        train_labels,
        validation,
        validation_labels,
        c_values=(0.1, 1.0),
        max_features=None,
    )
    assert result.validation_metrics["auroc"] > 0.95
    assert result.weights[7] > 0


def test_stable_neurons_requires_recurring_sign() -> None:
    def artifact(weights: list[float]) -> SparseLocalization:
        return SparseLocalization(
            weights=np.asarray(weights, dtype=np.float32),
            intercept=0.0,
            best_c=1.0,
            validation_metrics={},
            selected_feature_indices=np.arange(len(weights)),
        )

    stable = stable_neurons(
        [artifact([1, -1, 0]), artifact([2, 1, 0]), artifact([3, -2, 4])],
        minimum_runs=2,
    )
    assert [item["feature"] for item in stable] == [0, 1]
    assert stable[0]["sign"] == 1
