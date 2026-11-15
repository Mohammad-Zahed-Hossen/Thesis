"""First-divergent-token answer-preference readout.

The readout
-----------
At the first-divergent-token prefix position ``r = N_div - 1`` the answer
preference is

    s(x) = logit_x(a_T) - logit_x(a_V)
         = log p(a_T | prefix) - log p(a_V | prefix)

(the softmax denominators cancel). This is the same quantity the behavioral
pipeline fits its cue-combination model on, so the causal effects measured
here are in the units of that model.

Why not read ``out.logits``
---------------------------
In bf16 a logit near 20 has an ulp of ~0.125, so the *difference* of two
logits is quantised at roughly the size of the effects this package needs to
resolve -- a single source span's contribution to the readout can be a few
tenths of a nat. We therefore contract the final hidden state against the
unembedding difference in fp32,

    s = h_final(fp32) . (W_lm[id_T] - W_lm[id_V])(fp32),

which is the same number computed without the output rounding. The model's
own bf16 logit difference is recorded alongside it so rows remain joinable
with ``fdt_scores.parquet``.

:class:`Readout` checks the two agree on the first example it sees. A gross
disagreement means the head applies something other than a plain linear
unembedding (logit softcapping, a scaled or biased head), in which case the
fp32 shortcut is not the readout and the class falls back to the logits.

"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import torch


@dataclass
class ReadoutValues:
    """One forward's readout, in both precisions."""
    s: float          # fp32, from the final hidden state
    s_bf16: float     # the model's own logit difference, as-computed
    norm_scale: float = float("nan")  # RMS of the pre-final-norm residual at r


class Readout:
    """fp32 first-divergent-token readout, bound to one model.

    ``bind`` installs the unembedding difference for one example; ``score``
    consumes a model output (run with ``output_hidden_states=True``) and
    returns the readout at ``r``.
    """

    #: Absolute tolerance for the fp32-vs-logits agreement check. Loose enough
    #: to absorb bf16 rounding of two logits, tight enough that a softcapped or
    #: otherwise non-linear head cannot slip through.
    AGREEMENT_TOL = 0.5

    def __init__(self, model):
        self.model = model
        self._w_diff: Optional[torch.Tensor] = None
        self._ids: tuple[int, int] = (-1, -1)
        self.use_fp32 = True
        self.calibrated = False
        self.calibration_gap = float("nan")

    # ------------------------------------------------------------------

    def bind(self, model_input) -> "Readout":
        """Install ``W_lm[id_T] - W_lm[id_V]`` for this example."""
        W = self.model.lm_head.weight
        id_T, id_V = int(model_input.id_T_div), int(model_input.id_V_div)
        self._w_diff = (W[id_T].detach().float() - W[id_V].detach().float())
        self._ids = (id_T, id_V)
        return self

    def score(self, out, answer_pos: int) -> ReadoutValues:
        """Read out at ``answer_pos`` from a model output."""
        if self._w_diff is None:
            raise RuntimeError("Readout.bind() must be called before score().")
        a = int(answer_pos)
        id_T, id_V = self._ids

        lg = out.logits[0, a]
        s_bf16 = float((lg[id_T] - lg[id_V]).detach().float().cpu())

        s_fp32 = float("nan")
        norm_scale = float("nan")
        hs = getattr(out, "hidden_states", None)
        if hs is not None:
            h = hs[-1][0, a].detach().float()
            s_fp32 = float(h @ self._w_diff)
            # hidden_states[-1] is post-final-norm; [-2] is the last decoder
            # block's output, i.e. the residual the norm consumes.
            pre = hs[-2][0, a].detach().float()
            norm_scale = float(pre.pow(2).mean().sqrt())

        if not self.calibrated and hs is not None:
            self.calibration_gap = abs(s_fp32 - s_bf16)
            self.use_fp32 = self.calibration_gap <= self.AGREEMENT_TOL
            self.calibrated = True

        s = s_fp32 if (self.use_fp32 and hs is not None) else s_bf16
        return ReadoutValues(s=s, s_bf16=s_bf16, norm_scale=norm_scale)

    def calibration_report(self) -> str:
        if not self.calibrated:
            return "readout: not calibrated"
        mode = "fp32 hidden-state" if self.use_fp32 else "bf16 logits (fallback)"
        return (f"readout: {mode}; |s_fp32 - s_logits| = "
                f"{self.calibration_gap:.3e} on the calibration example")


@torch.no_grad()
def forward(model, inputs) -> object:
    """One no-grad forward with the hidden states the fp32 readout needs."""
    return model(**inputs, use_cache=False, return_dict=True,
                 output_hidden_states=True)
