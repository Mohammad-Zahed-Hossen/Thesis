from __future__ import annotations

import numpy as np

from hidden_commitment.directions import (
    fit_contrastive_direction,
    orthogonal_random_unit,
    select_direction,
)


def test_difference_of_means_points_to_positive_class() -> None:
    positive = np.array([[2.0, 0.0], [4.0, 0.0]])
    negative = np.array([[0.0, 0.0], [1.0, 0.0]])
    np.testing.assert_allclose(fit_contrastive_direction(positive, negative), [1.0, 0.0])


def test_random_control_is_unit_and_orthogonal() -> None:
    reference = np.array([1.0, 2.0, 3.0])
    control = orthogonal_random_unit(reference, seed=7)
    assert np.isclose(np.linalg.norm(control), 1.0)
    assert np.isclose(np.dot(control, reference / np.linalg.norm(reference)), 0.0, atol=1e-6)


def test_select_direction_finds_informative_layer() -> None:
    rng = np.random.default_rng(3)
    train_labels = np.repeat([0, 1], 20)
    validation_labels = np.repeat([0, 1], 10)
    train = rng.normal(size=(40, 2, 3, 4))
    validation = rng.normal(size=(20, 2, 3, 4))
    train[train_labels == 1, 1, 2, 0] += 5
    validation[validation_labels == 1, 1, 2, 0] += 5
    selected, _ = select_direction(
        train,
        train_labels,
        validation,
        validation_labels,
        positions=["early", "decision"],
    )
    assert selected.position == "decision"
    assert selected.layer == 2
