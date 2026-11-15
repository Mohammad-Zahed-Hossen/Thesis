#!/usr/bin/env python3
"""Fast CPU checks for the attention package's critical invariants."""

from __future__ import annotations

import sys
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import torch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from attention.attn_spans import KnockoutPlan, _knocked_row
from attention.run_knockout import _blocks
from attention.spans import Spans
from attention.summarize import bootstrap_mean


def test_span_partition() -> None:
    spans = Spans(5, image=[1], passage=[2], question=[3], other=[0, 4, 5])
    spans.check()
    bad = Spans(2, image=[0], passage=[0], question=[], other=[1, 2])
    try:
        bad.check()
    except ValueError:
        pass
    else:
        raise AssertionError("overlapping spans were accepted")


def test_knockout_mask() -> None:
    params = SimpleNamespace(index={
        "image": torch.tensor([0, 1]),
        "passage": torch.tensor([2]),
        "other": torch.tensor([3]),
    })
    logits = torch.tensor([[[0.0, 1.0, 2.0, 3.0], [1.0, -1.0, 0.0, 2.0]]])
    baseline = torch.softmax(logits, dim=-1)
    knocked = _knocked_row(params, KnockoutPlan(("image",)), logits, 4)
    assert torch.equal(knocked[..., :2], torch.zeros_like(knocked[..., :2]))
    original_ratio = baseline[..., 2] / baseline[..., 3]
    survivor_ratio = knocked[..., 2] / knocked[..., 3]
    torch.testing.assert_close(survivor_ratio, original_ratio)

    try:
        _knocked_row(
            params, KnockoutPlan(("image", "passage", "other")), logits, 4
        )
    except ValueError:
        pass
    else:
        raise AssertionError("a fully blocked attention row was accepted")


def test_layer_parsing() -> None:
    blocks = dict(_blocks(32, None))
    assert blocks["all"] == list(range(1, 33))


def test_bootstrap_is_deterministic() -> None:
    values = np.array([1.0, 2.0, 3.0, 4.0])
    first = bootstrap_mean(values, n_boot=100, seed=7)
    second = bootstrap_mean(values, n_boot=100, seed=7)
    assert first == second
    assert first[0] == 2.5


def main() -> None:
    test_span_partition()
    test_knockout_mask()
    test_layer_parsing()
    test_bootstrap_is_deterministic()
    print("attention checks passed")


if __name__ == "__main__":
    main()
