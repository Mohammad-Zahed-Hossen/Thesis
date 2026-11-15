"""Fusion model classes shared across the corner / L-shape / grid fitting pipelines.

Central model — Additive Log-Odds (3 params, nonneg evidence weights):

    Joint log-odds is an affine function of the two unimodal LLRs:
        log P_J(a_T | t,v,q) / P_J(a_V | t,v,q)
            = b + beta_T * s_T + beta_V * s_V
        p_hat = sigma(b + beta_T * s_T + beta_V * s_V)

Baseline — Bayesian Gated Fusion, no calibration (2 params):

    Interpolates between unimodal probes based on evidence strength:
        p_T = sigma(s_T),  p_V = sigma(s_V)
        e_T = |s_T|,       e_V = |s_V|
        w   = P(S=text | evidence) = sigma(b0 + beta * (e_T - e_V))
        p_hat = w * p_T + (1 - w) * p_V

Ablation — Four-Term Additive Fusion (5 params, nonneg weights):

    Uses four raw log-likelihoods instead of collapsed LLRs:
        s_hat_J = c + α_TT*ℓ_TT - α_TV*ℓ_TV + α_VT*ℓ_VT - α_VV*ℓ_VV
        p_hat   = sigma(s_hat_J)

Ablation — Full 4-term Gated Fusion (5 params):

    Same experts and mixture as the gated baseline, but the gate uses all four
    raw log-likelihoods with independent nonneg coefficients.

Common preprocessing: LLR clipping to [-MARGIN_CLIP, MARGIN_CLIP].
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from config import EPS, MARGIN_CLIP


# ============================================================================
# Central model: Additive Log-Odds
# ============================================================================

class AdditiveLogOddsModel(nn.Module):
    """
    3-parameter additive log-odds model for joint conflict resolution.

    log P_J(a_T | t,v,q) / P_J(a_V | t,v,q) = b + beta_T * s_T + beta_V * s_V
    p_hat = sigma(b + beta_T * s_T + beta_V * s_V)

    Inputs (sign convention: LLR in favor of a_T over a_V):
        s_T = log P(a_T | t,q) - log P(a_V | t,q)
        s_V = log P(a_T | v,q) - log P(a_V | v,q)

    Params:
        beta_T = softplus(beta_T_raw) >= 0  (text evidence calibration)
        beta_V = softplus(beta_V_raw) >= 0  (vision evidence calibration)
        b:     unconstrained                 (prior text-vs-vision preference)

    Reliability: as vision blur grows, s_V -> 0 and the joint log-odds shift
    toward b + beta_T * s_T (text-dominated); as text noise grows, s_T -> 0
    and the joint shifts toward b + beta_V * s_V (vision-dominated).
    """

    def __init__(self):
        super().__init__()
        self.beta_T_raw = nn.Parameter(torch.tensor(0.0))
        self.beta_V_raw = nn.Parameter(torch.tensor(0.0))
        self.b = nn.Parameter(torch.tensor(0.0))

    @property
    def beta_T(self) -> torch.Tensor:
        return F.softplus(self.beta_T_raw)

    @property
    def beta_V(self) -> torch.Tensor:
        return F.softplus(self.beta_V_raw)

    def forward_logodds(
        self,
        s_T: torch.Tensor,
        s_V: torch.Tensor,
    ) -> torch.Tensor:
        s_T = s_T.clamp(-MARGIN_CLIP, MARGIN_CLIP)
        s_V = s_V.clamp(-MARGIN_CLIP, MARGIN_CLIP)
        return self.b + self.beta_T * s_T + self.beta_V * s_V

    def forward(
        self,
        s_T: torch.Tensor,
        s_V: torch.Tensor,
    ) -> torch.Tensor:
        return torch.sigmoid(self.forward_logodds(s_T, s_V))

    def get_params_dict(self) -> dict:
        return {
            "b": self.b.item(),
            "beta_T": self.beta_T.item(),
            "beta_V": self.beta_V.item(),
            "beta_T_raw": self.beta_T_raw.item(),
            "beta_V_raw": self.beta_V_raw.item(),
        }

    def load_params_dict(self, params: dict):
        # New names first; fall back to legacy (c, gamma_T, gamma_V) so old
        # params.json files still load.
        if "beta_T_raw" in params:
            self.beta_T_raw.data = torch.tensor(float(params["beta_T_raw"]))
            self.beta_V_raw.data = torch.tensor(float(params["beta_V_raw"]))
        elif "gamma_T_raw" in params:
            self.beta_T_raw.data = torch.tensor(float(params["gamma_T_raw"]))
            self.beta_V_raw.data = torch.tensor(float(params["gamma_V_raw"]))
        else:
            bT = max(float(params.get("beta_T", params.get("gamma_T"))), 1e-4)
            bV = max(float(params.get("beta_V", params.get("gamma_V"))), 1e-4)
            self.beta_T_raw.data = torch.tensor(float(np.log(np.expm1(bT))))
            self.beta_V_raw.data = torch.tensor(float(np.log(np.expm1(bV))))
        self.b.data = torch.tensor(float(params.get("b", params.get("c"))))

    def get_training_postfix(self) -> dict:
        return {
            "b": f"{self.b.item():.3f}",
            "bT": f"{self.beta_T.item():.3f}",
            "bV": f"{self.beta_V.item():.3f}",
        }


# Backward-compat alias: external modules still import the old name.
AdditiveEvidenceFusionModel = AdditiveLogOddsModel


# ============================================================================
# Extension: additive + per-example prior log-odds regressor
# ============================================================================

class AdditiveLogOddsWithPriorModel(nn.Module):
    """
    Two-parameter linear cue combination over Bayes factors:

        s_hat_J = beta_T * (s_T - pi_0) + beta_V * (s_V - pi_0) + pi_0
                = beta_T * s_T + beta_V * s_V + (1 - beta_T - beta_V) * pi_0
        p_hat   = sigma(s_hat_J)

    Motivation: each unimodal probe contains the prior (s_T = log B_T + pi_0,
    s_V = log B_V + pi_0, where B_T, B_V are the per-modality Bayes
    factors). Reweighting the Bayes factors and adding the prior back is
    the algebraically clean cue-combination form. Calibrated naive Bayes
    (s_J = s_T + s_V - pi_0) is nested as the special case
    beta_T = beta_V = 1.

    Inputs:
        s_T  = log P(a_T | t, q) - log P(a_V | t, q)
        s_V  = log P(a_T | v, q) - log P(a_V | v, q)
        pi_0 = log P(a_T | q)    - log P(a_V | q)     (question-only prior)

    Params:
        beta_T = softplus(beta_T_raw) >= 0  (text Bayes-factor weight)
        beta_V = softplus(beta_V_raw) >= 0  (vision Bayes-factor weight)
    """

    def __init__(self):
        super().__init__()
        self.beta_T_raw = nn.Parameter(torch.tensor(0.0))
        self.beta_V_raw = nn.Parameter(torch.tensor(0.0))

    @property
    def beta_T(self) -> torch.Tensor:
        return F.softplus(self.beta_T_raw)

    @property
    def beta_V(self) -> torch.Tensor:
        return F.softplus(self.beta_V_raw)

    def forward_logodds(
        self,
        s_T: torch.Tensor,
        s_V: torch.Tensor,
        pi_0: torch.Tensor,
    ) -> torch.Tensor:
        s_T = s_T.clamp(-MARGIN_CLIP, MARGIN_CLIP)
        s_V = s_V.clamp(-MARGIN_CLIP, MARGIN_CLIP)
        pi_0 = pi_0.clamp(-MARGIN_CLIP, MARGIN_CLIP)
        return self.beta_T * (s_T - pi_0) + self.beta_V * (s_V - pi_0) + pi_0

    def forward(
        self,
        s_T: torch.Tensor,
        s_V: torch.Tensor,
        pi_0: torch.Tensor,
    ) -> torch.Tensor:
        return torch.sigmoid(self.forward_logodds(s_T, s_V, pi_0))

    def get_params_dict(self) -> dict:
        return {
            "beta_T": self.beta_T.item(),
            "beta_V": self.beta_V.item(),
            "beta_T_raw": self.beta_T_raw.item(),
            "beta_V_raw": self.beta_V_raw.item(),
        }

    def load_params_dict(self, params: dict):
        if "beta_T_raw" in params:
            self.beta_T_raw.data = torch.tensor(float(params["beta_T_raw"]))
            self.beta_V_raw.data = torch.tensor(float(params["beta_V_raw"]))
        else:
            bT = max(float(params["beta_T"]), 1e-4)
            bV = max(float(params["beta_V"]), 1e-4)
            self.beta_T_raw.data = torch.tensor(float(np.log(np.expm1(bT))))
            self.beta_V_raw.data = torch.tensor(float(np.log(np.expm1(bV))))

    def get_training_postfix(self) -> dict:
        return {
            "bT": f"{self.beta_T.item():.3f}",
            "bV": f"{self.beta_V.item():.3f}",
        }


# ============================================================================
# Bilinear extension: additive + s_T*s_V interaction term
# ============================================================================

class BilinearLogOddsModel(nn.Module):
    """
    Bilinear extension of the linear cue combination over Bayes factors:

        s_hat_J = beta_T * (s_T - pi_0) + beta_V * (s_V - pi_0)
                  + beta_I * (s_T - pi_0) * (s_V - pi_0) + pi_0
        p_hat   = sigma(s_hat_J)

    The interaction term beta_I * (s_T - pi_0) * (s_V - pi_0) is the
    simplest local relaxation of the conditional-independence assumption,
    on the Bayes factors rather than the raw probes. Sign:
        beta_I < 0:  modalities share information (don't double-count when
                     both Bayes factors agree).
        beta_I > 0:  modalities reinforce when they agree.
        beta_I = 0:  recovers AdditiveLogOddsWithPriorModel.

    Calibrated naive Bayes (s_J = s_T + s_V - pi_0) is the nested case
    beta_T = beta_V = 1, beta_I = 0.

    Constraints:
        beta_T = softplus(beta_T_raw) >= 0
        beta_V = softplus(beta_V_raw) >= 0
        beta_I unconstrained (sign is empirical).
    """

    def __init__(self):
        super().__init__()
        self.beta_T_raw = nn.Parameter(torch.tensor(0.0))
        self.beta_V_raw = nn.Parameter(torch.tensor(0.0))
        self.beta_I = nn.Parameter(torch.tensor(0.0))

    @property
    def beta_T(self) -> torch.Tensor:
        return F.softplus(self.beta_T_raw)

    @property
    def beta_V(self) -> torch.Tensor:
        return F.softplus(self.beta_V_raw)

    def forward_logodds(
        self,
        s_T: torch.Tensor,
        s_V: torch.Tensor,
        pi_0: torch.Tensor,
    ) -> torch.Tensor:
        s_T = s_T.clamp(-MARGIN_CLIP, MARGIN_CLIP)
        s_V = s_V.clamp(-MARGIN_CLIP, MARGIN_CLIP)
        pi_0 = pi_0.clamp(-MARGIN_CLIP, MARGIN_CLIP)
        bt = s_T - pi_0
        bv = s_V - pi_0
        return (
            self.beta_T * bt
            + self.beta_V * bv
            + self.beta_I * bt * bv
            + pi_0
        )

    def forward(
        self,
        s_T: torch.Tensor,
        s_V: torch.Tensor,
        pi_0: torch.Tensor,
    ) -> torch.Tensor:
        return torch.sigmoid(self.forward_logodds(s_T, s_V, pi_0))

    def get_params_dict(self) -> dict:
        return {
            "beta_T": self.beta_T.item(),
            "beta_V": self.beta_V.item(),
            "beta_I": self.beta_I.item(),
            "beta_T_raw": self.beta_T_raw.item(),
            "beta_V_raw": self.beta_V_raw.item(),
        }

    def load_params_dict(self, params: dict):
        if "beta_T_raw" in params:
            self.beta_T_raw.data = torch.tensor(float(params["beta_T_raw"]))
            self.beta_V_raw.data = torch.tensor(float(params["beta_V_raw"]))
        else:
            bT = max(float(params["beta_T"]), 1e-4)
            bV = max(float(params["beta_V"]), 1e-4)
            self.beta_T_raw.data = torch.tensor(float(np.log(np.expm1(bT))))
            self.beta_V_raw.data = torch.tensor(float(np.log(np.expm1(bV))))
        self.beta_I.data = torch.tensor(float(params["beta_I"]))

    def get_training_postfix(self) -> dict:
        return {
            "bT": f"{self.beta_T.item():.3f}",
            "bI": f"{self.beta_I.item():+.3f}",
            "bV": f"{self.beta_V.item():.3f}",
        }


class UnconstrainedLinearModel(nn.Module):
    """
    Unconstrained linear predictor in log-odds space:

        s_hat_J = w_T * s_T + w_V * s_V + w_pi * pi_0 + w_0

    Four free parameters with no sign or coupling constraints. This is the
    skyline that relaxes the Bayesian structure of the linear cue combination
    (AdditiveLogOddsWithPriorModel), whose form

        s_hat_J = beta_T * s_T + beta_V * s_V + (1 - beta_T - beta_V) * pi_0

    is the special case w_T = beta_T, w_V = beta_V,
    w_pi = 1 - beta_T - beta_V, w_0 = 0. Comparing the two isolates the
    predictive cost of the derivation's constraint on the prior coefficient
    (and the absence of an intercept), as opposed to merely having more free
    parameters. When pi_0 is zeroed (e.g. Gemma), w_pi is inactive and the
    model reduces to w_T * s_T + w_V * s_V + w_0.
    """

    def __init__(self):
        super().__init__()
        self.w_T = nn.Parameter(torch.tensor(0.0))
        self.w_V = nn.Parameter(torch.tensor(0.0))
        self.w_pi = nn.Parameter(torch.tensor(0.0))
        self.w_0 = nn.Parameter(torch.tensor(0.0))

    def forward_logodds(
        self,
        s_T: torch.Tensor,
        s_V: torch.Tensor,
        pi_0: torch.Tensor,
    ) -> torch.Tensor:
        s_T = s_T.clamp(-MARGIN_CLIP, MARGIN_CLIP)
        s_V = s_V.clamp(-MARGIN_CLIP, MARGIN_CLIP)
        pi_0 = pi_0.clamp(-MARGIN_CLIP, MARGIN_CLIP)
        return self.w_T * s_T + self.w_V * s_V + self.w_pi * pi_0 + self.w_0

    def forward(
        self,
        s_T: torch.Tensor,
        s_V: torch.Tensor,
        pi_0: torch.Tensor,
    ) -> torch.Tensor:
        return torch.sigmoid(self.forward_logodds(s_T, s_V, pi_0))

    def get_params_dict(self) -> dict:
        return {
            "w_T": self.w_T.item(),
            "w_V": self.w_V.item(),
            "w_pi": self.w_pi.item(),
            "w_0": self.w_0.item(),
        }

    def load_params_dict(self, params: dict):
        self.w_T.data = torch.tensor(float(params["w_T"]))
        self.w_V.data = torch.tensor(float(params["w_V"]))
        self.w_pi.data = torch.tensor(float(params["w_pi"]))
        self.w_0.data = torch.tensor(float(params["w_0"]))

    def get_training_postfix(self) -> dict:
        return {
            "wT": f"{self.w_T.item():.3f}",
            "wV": f"{self.w_V.item():.3f}",
            "wpi": f"{self.w_pi.item():+.3f}",
            "w0": f"{self.w_0.item():+.3f}",
        }


# ============================================================================
# Ablation: Four-Term Additive Fusion (raw-score additive)
# ============================================================================

class FourTermAdditiveFusionModel(nn.Module):
    """
    5-parameter additive fusion using all four raw log-likelihoods.

    Joint log-odds:
        s_hat_J = c + α_TT*ℓ_TT - α_TV*ℓ_TV + α_VT*ℓ_VT - α_VV*ℓ_VV
        p_hat   = sigma(s_hat_J)

    All α >= 0 via softplus reparameterization. Signs are fixed:
        +ℓ_TT: text supports text answer → increases s_hat_J
        -ℓ_TV: text supports vision answer → decreases s_hat_J
        +ℓ_VT: vision supports text answer → increases s_hat_J
        -ℓ_VV: vision supports vision answer → decreases s_hat_J
    """

    def __init__(self):
        super().__init__()
        self.c = nn.Parameter(torch.tensor(0.0))
        self.alpha_TT_raw = nn.Parameter(torch.tensor(0.0))
        self.alpha_TV_raw = nn.Parameter(torch.tensor(0.0))
        self.alpha_VT_raw = nn.Parameter(torch.tensor(0.0))
        self.alpha_VV_raw = nn.Parameter(torch.tensor(0.0))

    @property
    def alpha_TT(self) -> torch.Tensor:
        return F.softplus(self.alpha_TT_raw)

    @property
    def alpha_TV(self) -> torch.Tensor:
        return F.softplus(self.alpha_TV_raw)

    @property
    def alpha_VT(self) -> torch.Tensor:
        return F.softplus(self.alpha_VT_raw)

    @property
    def alpha_VV(self) -> torch.Tensor:
        return F.softplus(self.alpha_VV_raw)

    def forward(
        self,
        ll_TT: torch.Tensor,
        ll_TV: torch.Tensor,
        ll_VT: torch.Tensor,
        ll_VV: torch.Tensor,
    ) -> torch.Tensor:
        s_hat_J = (
            self.c
            + self.alpha_TT * ll_TT
            - self.alpha_TV * ll_TV
            + self.alpha_VT * ll_VT
            - self.alpha_VV * ll_VV
        )
        return torch.sigmoid(s_hat_J)

    def get_params_dict(self) -> dict:
        return {
            "c": self.c.item(),
            "alpha_TT": self.alpha_TT.item(),
            "alpha_TV": self.alpha_TV.item(),
            "alpha_VT": self.alpha_VT.item(),
            "alpha_VV": self.alpha_VV.item(),
            "alpha_TT_raw": self.alpha_TT_raw.item(),
            "alpha_TV_raw": self.alpha_TV_raw.item(),
            "alpha_VT_raw": self.alpha_VT_raw.item(),
            "alpha_VV_raw": self.alpha_VV_raw.item(),
        }

    def load_params_dict(self, params: dict):
        self.c.data = torch.tensor(float(params["c"]))
        for name in ["alpha_TT", "alpha_TV", "alpha_VT", "alpha_VV"]:
            raw_key = f"{name}_raw"
            if raw_key in params:
                getattr(self, raw_key).data = torch.tensor(float(params[raw_key]))
            else:
                val = max(float(params[name]), 1e-4)
                getattr(self, raw_key).data = torch.tensor(float(np.log(np.expm1(val))))

    def get_training_postfix(self) -> dict:
        return {
            "c": f"{self.c.item():.3f}",
            "aTT": f"{self.alpha_TT.item():.3f}",
            "aTV": f"{self.alpha_TV.item():.3f}",
            "aVT": f"{self.alpha_VT.item():.3f}",
            "aVV": f"{self.alpha_VV.item():.3f}",
        }


# ============================================================================
# Baseline: Bayesian Gated Fusion (no calibration)
# ============================================================================

class BayesianGatedFusionModel(nn.Module):
    """
    2-parameter Bayesian strategy-selection model (no calibration).

    Arbitrates between text and vision strategies based on evidence strength:
        p_T = sigma(s_T),  p_V = sigma(s_V)
        e_T = |s_T|,       e_V = |s_V|
        w   = P(S=text | evidence) = sigma(b0 + beta * (e_T - e_V))
        p_hat = w * p_T + (1 - w) * p_V

    p_hat is a convex combination of p_T and p_V:
        p_hat in [min(p_T, p_V), max(p_T, p_V)]
    This model arbitrates between strategies; it does not amplify confidence.

    Params:
        beta = softplus(b_raw) >= 0   (evidence sensitivity)
        b0   unconstrained             (log-prior: P(S=text) = sigma(b0))

    Switch point w=0.5 at e_T - e_V = -b0 / beta.
    """

    def __init__(self):
        super().__init__()
        self.b_raw = nn.Parameter(torch.tensor(0.0))   # beta = softplus(b_raw)
        self.b0 = nn.Parameter(torch.tensor(0.0))      # log-prior P(S=text)

    @property
    def beta(self) -> torch.Tensor:
        return F.softplus(self.b_raw)

    def forward(
        self,
        s_T: torch.Tensor,
        s_V: torch.Tensor,
    ) -> torch.Tensor:
        y_hat, _, _ = self._forward_impl(s_T, s_V)
        return y_hat

    def forward_with_gate(
        self,
        s_T: torch.Tensor,
        s_V: torch.Tensor,
    ) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        """Forward pass returning (y_hat, w, evidence_diff) for diagnostics."""
        return self._forward_impl(s_T, s_V)

    def _forward_impl(
        self,
        s_T: torch.Tensor,
        s_V: torch.Tensor,
    ) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        s_T = s_T.clamp(-MARGIN_CLIP, MARGIN_CLIP)
        s_V = s_V.clamp(-MARGIN_CLIP, MARGIN_CLIP)

        p_T = torch.sigmoid(s_T)
        p_V = torch.sigmoid(s_V)

        e_T = s_T.abs()
        e_V = s_V.abs()

        evidence_diff = e_T - e_V
        gate_logit = self.b0 + self.beta * evidence_diff
        w = torch.sigmoid(gate_logit)

        p_mix = w * p_T + (1 - w) * p_V
        p_mix = torch.clamp(p_mix, EPS, 1 - EPS)

        return p_mix, w, evidence_diff

    def get_params_dict(self) -> dict:
        return {
            "beta": self.beta.item(),
            "b0": self.b0.item(),
            "b_raw": self.b_raw.item(),
        }

    def load_params_dict(self, params: dict):
        if "b_raw" in params:
            self.b_raw.data = torch.tensor(float(params["b_raw"]))
        else:
            beta_val = max(float(params["beta"]), 1e-4)
            self.b_raw.data = torch.tensor(float(np.log(np.expm1(beta_val))))
        self.b0.data = torch.tensor(float(params["b0"]))

    def get_training_postfix(self) -> dict:
        return {
            "beta": f"{self.beta.item():.3f}",
            "b0": f"{self.b0.item():.3f}",
        }


# ============================================================================
# Ablation: Full 4-term Gated Fusion
# ============================================================================

class FourTermGatedFusionModel(nn.Module):
    """
    5-parameter gated fusion with independent coefficients on all four raw
    log-likelihoods.

    Gate log-odds:
        η = b0 + β_T_sup*ℓ_TT - β_T_anti*ℓ_TV + β_V_anti*ℓ_VT - β_V_sup*ℓ_VV

    Experts (unchanged):
        s_T = ℓ_TT - ℓ_TV,  p_T = sigma(s_T)
        s_V = ℓ_VT - ℓ_VV,  p_V = sigma(s_V)

    Mixture:
        w = sigma(η),  p_hat = w * p_T + (1 - w) * p_V

    All β >= 0 via softplus reparameterization.
    """

    def __init__(self):
        super().__init__()
        self.b0 = nn.Parameter(torch.tensor(0.0))
        self.beta_T_sup_raw = nn.Parameter(torch.tensor(0.0))
        self.beta_T_anti_raw = nn.Parameter(torch.tensor(0.0))
        self.beta_V_anti_raw = nn.Parameter(torch.tensor(0.0))
        self.beta_V_sup_raw = nn.Parameter(torch.tensor(0.0))

    @property
    def beta_T_sup(self) -> torch.Tensor:
        return F.softplus(self.beta_T_sup_raw)

    @property
    def beta_T_anti(self) -> torch.Tensor:
        return F.softplus(self.beta_T_anti_raw)

    @property
    def beta_V_anti(self) -> torch.Tensor:
        return F.softplus(self.beta_V_anti_raw)

    @property
    def beta_V_sup(self) -> torch.Tensor:
        return F.softplus(self.beta_V_sup_raw)

    def forward(
        self,
        ll_TT: torch.Tensor,
        ll_TV: torch.Tensor,
        ll_VT: torch.Tensor,
        ll_VV: torch.Tensor,
    ) -> torch.Tensor:
        y_hat, _, _ = self._forward_impl(ll_TT, ll_TV, ll_VT, ll_VV)
        return y_hat

    def forward_with_gate(
        self,
        ll_TT: torch.Tensor,
        ll_TV: torch.Tensor,
        ll_VT: torch.Tensor,
        ll_VV: torch.Tensor,
    ) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        """Forward pass returning (y_hat, w, gate_logit) for diagnostics."""
        return self._forward_impl(ll_TT, ll_TV, ll_VT, ll_VV)

    def _forward_impl(
        self,
        ll_TT: torch.Tensor,
        ll_TV: torch.Tensor,
        ll_VT: torch.Tensor,
        ll_VV: torch.Tensor,
    ) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        # Experts: same as the 2-param gated baseline
        s_T = (ll_TT - ll_TV).clamp(-MARGIN_CLIP, MARGIN_CLIP)
        s_V = (ll_VT - ll_VV).clamp(-MARGIN_CLIP, MARGIN_CLIP)
        p_T = torch.sigmoid(s_T)
        p_V = torch.sigmoid(s_V)

        # Gate: 4-term linear in raw LLs
        gate_logit = (
            self.b0
            + self.beta_T_sup * ll_TT
            - self.beta_T_anti * ll_TV
            + self.beta_V_anti * ll_VT
            - self.beta_V_sup * ll_VV
        )
        w = torch.sigmoid(gate_logit)

        p_mix = w * p_T + (1 - w) * p_V
        p_mix = torch.clamp(p_mix, EPS, 1 - EPS)

        return p_mix, w, gate_logit

    def get_params_dict(self) -> dict:
        return {
            "b0": self.b0.item(),
            "beta_T_sup": self.beta_T_sup.item(),
            "beta_T_anti": self.beta_T_anti.item(),
            "beta_V_anti": self.beta_V_anti.item(),
            "beta_V_sup": self.beta_V_sup.item(),
            "beta_T_sup_raw": self.beta_T_sup_raw.item(),
            "beta_T_anti_raw": self.beta_T_anti_raw.item(),
            "beta_V_anti_raw": self.beta_V_anti_raw.item(),
            "beta_V_sup_raw": self.beta_V_sup_raw.item(),
        }

    def load_params_dict(self, params: dict):
        self.b0.data = torch.tensor(float(params["b0"]))
        for name in ["beta_T_sup", "beta_T_anti", "beta_V_anti", "beta_V_sup"]:
            raw_key = f"{name}_raw"
            if raw_key in params:
                getattr(self, raw_key).data = torch.tensor(float(params[raw_key]))
            else:
                val = max(float(params[name]), 1e-4)
                getattr(self, raw_key).data = torch.tensor(float(np.log(np.expm1(val))))

    def get_training_postfix(self) -> dict:
        return {
            "b0": f"{self.b0.item():.3f}",
            "bTs": f"{self.beta_T_sup.item():.3f}",
            "bTa": f"{self.beta_T_anti.item():.3f}",
            "bVa": f"{self.beta_V_anti.item():.3f}",
            "bVs": f"{self.beta_V_sup.item():.3f}",
        }
