# Hidden Commitment

Research code for **Hidden Commitment: When Language Models Silently Pick a Side and How Steering Can Surface It**, accepted at the [ICML 2026 AI4GOOD Workshop](https://openreview.net/forum?id=ldaR8qyupo).

Samuel Dawit Assefa and Jae Won Cho

Language models can process contradictory documents, select one source, and still present a one-sided answer without disclosing the conflict. This repository packages the paper's reusable mechanistic tools: answer-span attribution, CETT neuron localization, residual source-choice directions, sparse-writer alignment, and RMS-scaled residual steering.

## What is included

```text
.
├── configs/paper.toml             # Reported model, generation, split, and steering settings
├── docs/
│   ├── data-contracts.md          # JSONL/NPZ schemas
│   └── method.md                  # Paper-method-to-code map and required controls
├── src/hidden_commitment/
│   ├── text.py                    # Source labels and decision-span alignment
│   ├── modeling.py                # Text-only model loading and generation
│   ├── hooks.py                   # Scoped activation capture and interventions
│   ├── cett.py                    # Vectorized CETT and write projections
│   ├── residuals.py               # Named token-position features
│   ├── directions.py              # Contrastive readouts and random controls
│   ├── localization.py            # Group-disjoint sparse classifiers
│   ├── judging.py                 # Structured conflict-surfacing audits
│   └── cli.py                     # Small analysis CLI
└── tests/                         # CPU-only tests of the mathematical core
```

Historical exploratory scripts and manuscript sources are intentionally excluded from this public helper release. New work should import the package in `src/`; it has no hard-coded local paths and keeps model/dataset revisions explicit.

## Install with uv

Python 3.11+ is required. From the repository root:

```bash
uv sync --extra cu126 --extra dev   # NVIDIA GPU (paper workstation)
# uv sync --extra cpu --extra dev   # CPU-only development
uv run hidden-commitment doctor
uv run pytest
```

Optional dependencies are isolated:

```bash
uv sync --extra cu126 --extra plots  # publication figures on NVIDIA
uv sync --extra cu126 --extra judge  # Gemini-based response audits on NVIDIA
```

The `cpu` and `cu126` extras are mutually exclusive, so the lockfile records both environments without silently installing a CPU-only PyTorch build on Windows. CUDA 12.6 is the conservative binary target for the RTX 3060 workstation; change the explicit PyTorch index in `pyproject.toml` if your deployment requires another backend.

## Core API

### Attribute an answer and locate its tokens

```python
from hidden_commitment.text import label_response, locate_alias_span

label = label_response(response, doc1_aliases, doc2_aliases)
aliases = doc1_aliases if label == "doc1" else doc2_aliases
span = locate_alias_span(response, aliases, tokenizer)
```

Only responses matching exactly one answer family should enter a source-choice analysis. `span.token_indices` is relative to the generated response.

### Compute CETT

```python
import torch

from hidden_commitment.cett import extract_cett_vector
from hidden_commitment.hooks import capture_mlp_inputs

cache, hooks = capture_mlp_inputs(model)
try:
    with torch.inference_mode():
        model(**teacher_forced_inputs)
    feature = extract_cett_vector(model, cache, absolute_decision_positions)
finally:
    hooks.close()
```

For activation `z[t,j]` and down projection `W[:,j]`, CETT is computed as:

```text
abs(z[t,j]) * norm(W[:,j]) / (norm(W @ z[t]) + 1e-10)
```

The implementation evaluates every neuron at once and never materializes a `[tokens, neurons, hidden]` tensor.

### Fit a source-choice direction

```python
from hidden_commitment.directions import fit_contrastive_direction

unit = fit_contrastive_direction(doc2_train_vectors, doc1_train_vectors)
validation_scores = validation_vectors @ unit
```

For the complete layer/position sweep, save residual features using the contract in `docs/data-contracts.md`, then run:

```bash
uv run hidden-commitment fit-direction artifacts/residual_features.npz \
  --output artifacts/source_direction.json
```

### Fit a sparse CETT classifier

```bash
uv run hidden-commitment localize artifacts/cett_features.npz \
  --output artifacts/localization.json \
  --intermediate-size 3584
```

Both CLI analyses split by question ID, preventing original/swapped or repeated-generation variants from leaking across train, validation, and test partitions.

### Steer a residual direction

```python
from hidden_commitment.hooks import SteeringWindow, residual_steering_hook

with residual_steering_hook(
    model,
    layer=13,
    direction=unit,
    delta=2.0,
    window=SteeringWindow(prompt_tail=32, response_start=0, response_end=12),
):
    response = model.generate(**inputs)
```

Always verify that a zero-strength hook exactly reproduces the unhooked generation before interpreting steering results.

## Reproducing the paper responsibly

The [method map](docs/method.md) explains the analysis sequence and controls. The [data contracts](docs/data-contracts.md) define portable input/output artifacts. Reported defaults are centralized in [configs/paper.toml](configs/paper.toml).

The main evidence chain is:

1. Generate and attribute one-sided answers under contradictory documents.
2. Keep all variants of a question in one data split.
3. Localize sparse MLP neurons with decision-span CETT.
4. Fit the residual source-choice direction on training rows and select layer/position on validation rows.
5. Evaluate once on held-out original and swapped document order.
6. Project localized neurons' actual MLP writes onto the independently learned residual direction.
7. Compare with layer-matched neuron controls and an orthogonal random residual control.
8. Run bidirectional steering and report decided, ambiguous, weak, and truncated denominators.

Raw generations, judge outputs, large feature matrices, checkpoints, and API keys are intentionally excluded from version control.

## Paper and citation

Read the accepted paper on [OpenReview](https://openreview.net/forum?id=ldaR8qyupo). Citation metadata is available in `CITATION.cff`.

This repository is a curated research release, not a deployment-ready model monitor. The paper's steering interventions are diagnostic, partial, and model/format-specific.
