from __future__ import annotations

import numpy as np
import torch

from hidden_commitment.cett import cett_scores, write_projection


def test_cett_matches_explicit_neuron_norms() -> None:
    z = torch.tensor([[2.0, -1.0], [0.5, 3.0]])
    weight = torch.tensor([[1.0, 2.0], [2.0, 0.0], [0.0, -1.0]])
    observed = cett_scores(z, weight)
    expected = torch.empty_like(observed)
    full = z @ weight.T
    for token in range(z.shape[0]):
        for neuron in range(z.shape[1]):
            contribution = z[token, neuron] * weight[:, neuron]
            numerator = torch.linalg.vector_norm(contribution)
            denominator = torch.linalg.vector_norm(full[token])
            expected[token, neuron] = numerator / denominator
    torch.testing.assert_close(observed, expected)


def test_write_projection_sums_signed_writes() -> None:
    score = write_projection(
        mean_activations={0: np.array([2.0, -1.0])},
        down_weights={0: np.array([[1.0, 0.0], [0.0, 1.0]])},
        residual_direction=np.array([1.0, 0.0]),
        neurons=[(0, 0), (0, 1)],
    )
    assert score == 2.0
