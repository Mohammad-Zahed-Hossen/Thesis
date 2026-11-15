"""Shared fitting package: fusion model classes, training/eval helpers, OLS
path, and support-mode utilities for corner / L-shape / grid fitting."""

from .models import (
    AdditiveEvidenceFusionModel,
    AdditiveLogOddsModel,
    AdditiveLogOddsWithPriorModel,
    BayesianGatedFusionModel,
    BilinearLogOddsModel,
    FourTermAdditiveFusionModel,
    FourTermGatedFusionModel,
    UnconstrainedLinearModel,
)
from .train import (
    binary_cross_entropy,
    compute_argmax_match,
    compute_kl,
    compute_symmetrized_kl,
    evaluate_split,
    print_additive_diagnostics,
    print_four_term_additive_diagnostics,
    print_four_term_gate_diagnostics,
    print_gate_diagnostics,
    print_logodds_diagnostics,
    train_model,
)
from .fit import fit_models
from .support import SUPPORT_MODES, select_test_mask, select_train_mask

__all__ = [
    # models
    "AdditiveLogOddsModel",
    "AdditiveEvidenceFusionModel",
    "AdditiveLogOddsWithPriorModel",
    "BilinearLogOddsModel",
    "BayesianGatedFusionModel",
    "FourTermAdditiveFusionModel",
    "FourTermGatedFusionModel",
    "UnconstrainedLinearModel",
    # train / eval
    "train_model",
    "evaluate_split",
    "binary_cross_entropy",
    "compute_kl",
    "compute_symmetrized_kl",
    "compute_argmax_match",
    # diagnostics
    "print_logodds_diagnostics",
    "print_additive_diagnostics",
    "print_gate_diagnostics",
    "print_four_term_gate_diagnostics",
    "print_four_term_additive_diagnostics",
    # unified entry
    "fit_models",
    # support helpers
    "SUPPORT_MODES",
    "select_train_mask",
    "select_test_mask",
]
