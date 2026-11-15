"""
Configuration for conflicting-modality Bayesian probing + fusion experiments.
"""

import os
from pathlib import Path

# Model configuration
QWEN_MODEL = "Qwen/Qwen2.5-VL-3B-Instruct"
HF_CACHE_DIR = os.getenv("HF_CACHE_DIR", None)

# Dataset
CONFLICTING_MODALITY_DATASET = "joshbarua/conflicting_modality"

# Data splits
TRAIN_RATIO = 0.7
VAL_RATIO = 0.15
# test = 1 - TRAIN_RATIO - VAL_RATIO = 0.15

# Training parameters
DEFAULT_LR = 0.1
DEFAULT_EPOCHS = 1000
DEFAULT_SEED = 42
EPS = 1e-6

# Smoothing epsilon for token-ratio log computation: r = log((n_T + eps) / (n_V + eps))
TOKEN_RATIO_EPS = 1.0

# Margin clipping (prevents outlier log-odds from dominating gating)
MARGIN_CLIP = 30.0

# Diagnostic plot parameters
N_UNCERTAINTY_BUCKETS = 10

# Degradation experiment parameters

# Grid preset for degradation scoring.
# Each degradation list includes 0 at index 0 to denote "no degradation"
# (blur σ=0 / token-noise p=0 = original text). Generators skip the leading 0
# (originals come from the dataset at score-time).
GRID_PRESETS = {
    "6x6": {
        "blur_sigmas": [0, 2, 4, 8, 16, 32],
        "token_noise_probs": [0, 0.2, 0.4, 0.6, 0.8, 1.0],
    },
}


def get_token_noise_probs(grid: str) -> list[float]:
    """Return the token-noise probabilities for a grid (index 0 = original, p=0)."""
    return list(GRID_PRESETS[grid]["token_noise_probs"])


def get_token_noise_labels(grid: str) -> list[str]:
    """Return text-level labels for a token-noise grid: 'original' at p=0, else f'p={p:.2f}'."""
    return ["original" if p == 0 else f"p={p:.2f}" for p in get_token_noise_probs(grid)]

# Paths
DEFAULT_RUNS_DIR = Path(__file__).parent / "runs"


def get_run_dir(run_id: str) -> Path:
    """Get the run directory for a given run ID."""
    return DEFAULT_RUNS_DIR / run_id


def load_degradation_meta(run_dir: Path) -> dict:
    """Load degradation metadata from a run directory.

    Returns a dict with keys: grid, text_degradation, blur_sigmas, text_levels,
    text_labels, model_name, seed.
    """
    import json
    meta_path = run_dir / "degradation_meta.json"
    if not meta_path.exists():
        raise FileNotFoundError(
            f"Missing: {meta_path}\n"
            "Run run_degradation_scoring.py first (it saves this metadata)."
        )
    with open(meta_path) as f:
        return json.load(f)


def model_name_to_folder(model_name: str) -> str:
    """Convert model name to filesystem-safe folder name."""
    return model_name.replace("/", "--")


def use_measured_prior_in_fit(model_name: str) -> bool:
    """Whether the measured pi_0 should enter downstream fits (calibrated
    naive Bayes / linear cue combination / bilinear log-odds).

    Returns False for Gemma3 even though `get_prior_prefill` produces a
    finite measurement: the prefill probe conditions on a different chat
    prefix ("Based on my prior knowledge, the answer to the question is")
    than the bare-question chat used for s_T, s_V, s_J. The calibrated NB
    chain rule

        s_J = log P(a_T|q,t,v) - log P(a_V|q,t,v)
            = s_T + s_V - pi_0

    requires pi_0 to be log P(a_T|q) - log P(a_V|q) under the SAME chat
    template as the evidence probes. Plugging in a prefill-conditioned
    pi_0 breaks the cancellation and adds residual variance to predicted
    s_J -- empirically the R^2 on Gemma3-4B DocVQA drops from ~0.71 to
    ~-0.04 once the prefill-pi_0 is included. The prefill measurement is
    kept in the parquet for diagnostic use; it is zeroed at the fit step
    via this gate.

    Returns True for Qwen (where pi_0 and the evidence probes share the
    same chat conditioning and the chain rule holds).
    """
    return "gemma" not in model_name.lower()


def get_prior_prefill(model_name: str) -> str | None:
    """Assistant-side prefill to prepend to both candidate answers when
    computing pi_0 (the question-only prior probe).

    Bare-question prompts on Gemma3 trigger long-form descriptive responses,
    pushing single-word answer tokens deep into the response-distribution
    tail; the resulting relative log-odds between two tail tokens is
    noise-dominated (we measured |pi_0|>10 on ~28% of Gemma3-4B and ~19%
    of Gemma3-12B examples, vs <1% for Qwen). Prepending a fixed
    answering frame as an assistant prefill before each candidate forces
    the model out of "explanation mode" before the candidate diverges,
    cutting the |pi_0|>10 outlier rate to ~6% on both Gemma3 sizes
    (n=100 ablation in runs/prior_probe_ablation/).

    The prefill tokens are masked from the mean-log-prob loss (so they
    don't dilute the readout) and naturally land before the FDT
    divergence position (so the FDT readout sees the post-prefill
    candidate token).
    """
    if "gemma" in model_name.lower():
        return "Based on my prior knowledge, the answer to the question is"
    return None
