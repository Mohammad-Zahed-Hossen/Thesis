"""Source-span decomposition and substitution of the readout's attention write.

What this provides
------------------
For layer ``l``, head ``h``, the readout position ``r`` and a source span
``S``, the head's value aggregate restricted to that span is

    z^{l,h}_{r<-S} = sum_{j in S} A^{l,h}_{rj} V^{l,h}_j

and its contribution to the residual stream is ``W_O^{l,h} z^{l,h}_{r<-S}``.
Because the head concatenation is fed to a single linear output projection,
summing the four spans' aggregates reconstructs the head's full aggregate
exactly, so substituting one span's aggregate is exactly the intervention

    a^l_r(D)' = a^l_r(D) - c^l_{r<-S}(D) + c^l_{r<-S}(C).

This module implements that substitution *inside* the attention computation,
on the per-head aggregate ``z`` before the output projection. Doing it there
rather than on the post-projection write is what keeps it architecture-neutral:
whatever the block applies between the aggregate and the residual stream --
the output projection, an output gate, a post-sublayer norm -- still runs, on
the substituted aggregate, exactly as it would have.

Why a custom attention implementation
-------------------------------------
The fused SDPA kernel never materializes the attention matrix, so the per-span
split of the value aggregate is not recoverable from it, and hooks on
``q_proj``/``k_proj`` come too early: RoPE and the cache update happen inside
the attention forward. transformers dispatches through
``ALL_ATTENTION_FUNCTIONS`` with ``(module, query, key, value, mask, scaling)``
*after* RoPE, which is the one point where the query, keys and values are all
in final form. Registering there also means the measurement and the
intervention run through one code path, so what is substituted is exactly what
was measured.

Three things this has to get right, all of which fail quietly rather than
loudly:

* **The mask.** With SDPA the model may hand the attention function
  ``attention_mask=None`` and rely on ``is_causal``. An eager matmul that
  trusts that attends non-causally. The mask builder is selected by the same
  implementation name, so ``eager_mask`` is registered under it too.
* **The vision tower.** ``config._attn_implementation`` is read by the image
  encoder's attention as well, whose sequence is image patches and whose
  module has no ``layer_idx``. Anything that is not a registered decoder
  self-attention is delegated straight to SDPA.
* **The query position.** On a full forward the readout is at ``answer_pos``,
  which is *not* the last query position. Reading the last row measures the
  wrong token.

Precision and baselines
-----------------------
The attention logits and every derived aggregate are computed in fp32
regardless of model dtype: these are differences of small numbers, and a
single span's contribution to the readout can be a few tenths of a nat.

The eager path is numerically close to, but not bit-identical with, the fused
kernel, so every effect measured here is differenced against a baseline taken
through *this same path* with the substitution disabled. The gap to an
ordinary SDPA forward is recorded per example as ``impl_gap`` and is a
diagnostic, never a component of a reported effect.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

import torch
from transformers.integrations.sdpa_attention import sdpa_attention_forward
from transformers.masking_utils import ALL_MASK_ATTENTION_FUNCTIONS, eager_mask
from transformers.modeling_utils import AttentionInterface

IMPL_NAME = "attention_span_attn"

#: Substitution modes. ``swap`` replaces a span's whole aggregate with the
#: other run's (Experiment 3, and the ``CC`` cell of Experiment 4).
#: ``attn_other`` keeps this run's values but applies the other run's attention
#: row over the span (the ``CD`` cell: clean routing, degraded content), and
#: ``values_other`` keeps this run's routing but substitutes the other run's
#: values (the ``DC`` cell: degraded routing, clean content).
MODES = ("swap", "attn_other", "values_other", "none")

_ACTIVE: Optional["SpanAttention"] = None


def _repeat_kv(x: torch.Tensor, n_rep: int) -> torch.Tensor:
    """Expand grouped-query keys/values to one per query head."""
    if n_rep == 1:
        return x
    b, h, s, d = x.shape
    return x[:, :, None].expand(b, h, n_rep, s, d).reshape(b, h * n_rep, s, d)


@dataclass
class SubPlan:
    """One layer's substitution for the next forward.

    ``span_index`` are the source positions the substitution applies to, and
    every tensor supplied from the other run must be indexed in that same
    order. ``head_mask`` (``[n_heads]``) restricts the substitution to a subset
    of heads, which is how the head-level experiment expresses "replace only
    head h's contribution" without a separate code path.
    """
    mode: str
    span_index: torch.Tensor                      # LongTensor[|S|]
    z_other: Optional[torch.Tensor] = None        # [H, d]      for "swap"
    a_other: Optional[torch.Tensor] = None        # [H, |S|]    for "attn_other"
    v_other: Optional[torch.Tensor] = None        # [H, |S|, d] for "values_other"
    head_mask: Optional[torch.Tensor] = None      # [H]

    def __post_init__(self):
        if self.mode not in MODES:
            raise ValueError(f"mode must be one of {MODES}, got {self.mode!r}")
        need = {"swap": self.z_other, "attn_other": self.a_other,
                "values_other": self.v_other}.get(self.mode)
        if self.mode != "none" and need is None:
            raise ValueError(f"mode {self.mode!r} requires its companion tensor")


@dataclass
class QKPlan:
    """A QK cross-swap at the readout for one layer.

    Recomputes the readout row's attention from mismatched runs -- substituting
    the readout query ``q_other`` and/or a span's keys ``k_other`` and/or a
    span's values ``v_other`` from a donor run -- then re-softmaxes and replaces
    the readout's attention output. Everything omitted stays the live (target)
    run's. This splits the attention allocation into its query, key
    (per span, so competition/renormalization is visible), and value parts.

    RoPE-safe only when the donor and target share token positions (image
    degradation always; text degradation on aligned spans), since q/k are
    captured post-RoPE.
    """
    q_other: Optional[torch.Tensor] = None                          # [H, d]
    k_other: dict[str, torch.Tensor] = field(default_factory=dict)  # span -> [H, |S|, d]
    v_other: dict[str, torch.Tensor] = field(default_factory=dict)  # span -> [H, |S|, d]
    # The query is a single readout vector, so a query swap is applied by
    # *span of the logit it affects*: with ``q_span`` set, ``q_other`` is used
    # only for those spans' logits (q_other . k_j for j in the span) and the
    # live query for the rest -- the per-span parallel of a key swap. ``q_span``
    # None with ``q_other`` set applies the swapped query to every span (global).
    q_span: Optional[list] = None


@dataclass
class ClampPlan:
    """Retarget the readout's total attention mass on one or more spans.

    A single scalar ``b_S`` is added to every attention logit belonging to span
    ``S`` at the readout row::

        z'_rj = z_rj + b_S · 1[j ∈ S]

    which rescales the span's unnormalized weight by ``exp(b_S)`` and leaves the
    *relative* weights inside the span untouched. So the span's total
    allocation moves to whatever is asked for while the within-span ranking,
    the values, and every other span's internal pattern are the target run's
    own. No donor token alignment is needed -- only |clamped spans| scalars per
    head cross the boundary.

    **The offset is not ``logit(g') − logit(g)``.** That binary form is right
    only when exactly one span is clamped and everything else is residual. With
    several spans clamped at once their offsets interact through the shared
    softmax denominator, and the correct simultaneous solution is the
    multinomial one, taken against the *unclamped* residual set ``R``::

        b_S = (log g'_S − log g'_R) − (log g_S − log g_R)

    with ``g_R = 1 − Σ_S g_S`` and ``g'_R = 1 − Σ_S g'_S``. For one clamped span
    this reduces to the binary formula, since then ``g_R = 1 − g_S``. Applying
    the binary form to two spans independently overshoots both, because each
    offset is computed against a denominator the other one moves.

    ``target`` maps span name -> desired mass, either ``[H]`` (per head, the
    default and what a donor capture provides directly) or a scalar broadcast
    to every head. Spans absent from ``target`` are the residual set and take
    no offset; at least one such span must exist, since with everything clamped
    there is no free mass for the constraint to act against.

    Exact on output-gated architectures: this changes attention probabilities
    only, so the gate -- computed downstream from the target run's own hidden
    state -- still applies to the resulting aggregate untouched.
    """
    target: dict[str, torch.Tensor] = field(default_factory=dict)
    # Guard against a degenerate softmax: a target mass is floored here before
    # the log, so a span the readout genuinely ignores cannot produce -inf.
    eps: float = 1e-6


@dataclass
class KnockoutPlan:
    """Block the readout from attending to whole source spans at one layer.

    Every attention logit belonging to a blocked span is set to ``-inf`` at the
    readout row before the softmax, so the span receives exactly zero mass and
    the freed mass is redistributed over the surviving positions in proportion
    to what they already had. The values, the surviving spans' internal
    patterns, and every non-readout query position are untouched.

    This is the limiting case of :class:`ClampPlan` at ``g'_S = 0``, but it is
    not implemented through it: the offset ``b_S`` diverges as the target mass
    goes to zero, so a "clamp to epsilon" would be an unbounded logit shift
    dressed up as a small number. Masking is exact and has no free parameter.

    **What a knockout does and does not remove.** It closes the *direct* route
    from the span's tokens to the readout at that layer. It does not remove the
    span's influence: earlier layers have already written span-conditioned
    information into other positions' hidden states, and the readout can still
    attend to those. Under image degradation this package's cumulative results
    already show most of the visual signal reaching the readout through passage
    and question positions rather than from image tokens directly, so a small
    image knockout effect is evidence about the direct route specifically, not
    evidence that the image does not matter.

    At least one span must survive at every blocked layer, or the readout's
    attention row has no support and the softmax is undefined; this is checked
    rather than left to produce NaNs.
    """
    spans: tuple[str, ...] = ()


@dataclass
class LayerCapture:
    """One layer's readout-row measurements from a single forward."""
    z_span: dict[str, torch.Tensor] = field(default_factory=dict)   # [H, d]
    z_all: Optional[torch.Tensor] = None                            # [H, d]
    a_span: dict[str, torch.Tensor] = field(default_factory=dict)   # [H, |S|]
    v_span: dict[str, torch.Tensor] = field(default_factory=dict)   # [H, |S|, d]
    # ---- QK capture (want_qk): the readout query and per-span keys ----
    q_readout: Optional[torch.Tensor] = None                        # [H, d]
    k_span: dict[str, torch.Tensor] = field(default_factory=dict)   # [H, |S|, d]
    # ---- geometry (want_geometry): the factors of the attention logit ----
    # Per span, per head: everything needed to split the attention allocation
    # into query / key / normalization / value / answer-projection parts.
    logZ_span: dict[str, torch.Tensor] = field(default_factory=dict)  # [H] log Σ_{j∈S} exp(z_rj)
    q_norm: Optional[torch.Tensor] = None                             # [H] ‖q_r‖
    k_norm_span: dict[str, torch.Tensor] = field(default_factory=dict)  # [H] mean ‖k_j‖
    cos_span: dict[str, torch.Tensor] = field(default_factory=dict)     # [H] mean cosθ_rj
    v_norm_span: dict[str, torch.Tensor] = field(default_factory=dict)  # [H] mean ‖V_j‖
    ans_span: dict[str, torch.Tensor] = field(default_factory=dict)     # [H] mean |u_eff·V_j| (pre-gate)
    # ---- answer-direction contribution (want_contrib) ----
    # The signed, attention-weighted push this span makes on the readout:
    #   c_S = u_diff^T W_O (gate ⊙ Σ_{j∈S} A_rj V_j),   per head, in nats.
    # Unlike ``ans_span`` (a mean magnitude over tokens, so blind to both sign
    # and to how much attention each token actually got) this is the quantity
    # that adds up to the span's causal effect on the preference: summing
    # ``c_span`` over spans and heads reconstructs the layer's whole attention
    # write projected on u_diff. Mass can rise while this falls or flips sign,
    # which is exactly the discrepancy it exists to detect.
    c_span: dict[str, torch.Tensor] = field(default_factory=dict)       # [H] signed nats
    mass_span: dict[str, torch.Tensor] = field(default_factory=dict)    # [H] Σ_{j∈S} A_rj
    gated_contrib: bool = False   # whether c_span includes the output gate
    # The gate actually applied, kept so the capture is self-contained: the
    # hidden state it was built from is dropped at disarm, and without this a
    # caller could not reproduce c_span to check it.
    gate: Optional[torch.Tensor] = None                                 # [H, d]


def _clamped_row(p, clamp: "ClampPlan", logrow: torch.Tensor,
                 row: torch.Tensor, n_key: int) -> torch.Tensor:
    """Re-softmax the readout row with each clamped span's mass retargeted.

    ``logrow`` is the masked pre-softmax readout row ``[B, H, S]`` and ``row``
    its softmax. Returns the new row; see :class:`ClampPlan` for the offset.
    """
    eps = float(clamp.eps)
    spans = {}
    for name, tgt in clamp.target.items():
        idx = p.index[name]
        idx = idx[idx < n_key]
        if idx.numel() == 0:
            continue
        t = torch.as_tensor(tgt, dtype=row.dtype, device=row.device)
        if t.ndim == 0:
            t = t.expand(row.shape[1])
        spans[name] = (idx, t.reshape(1, -1).clamp_min(eps))   # [1, H]
    if not spans:
        return row
    if len(spans) >= len(p.index):
        raise ValueError(
            "every bound span is clamped, leaving no residual mass for the "
            "offsets to act against; leave at least one span free.")

    g = {name: row[:, :, idx].sum(-1).clamp_min(eps)           # [B, H]
         for name, (idx, _) in spans.items()}
    g_R = (1.0 - sum(g.values())).clamp_min(eps)
    g_new = {name: t for name, (_, t) in spans.items()}
    g_R_new = 1.0 - sum(g_new.values())
    if bool((g_R_new <= eps).any()):
        raise ValueError(
            f"clamp targets sum to >= 1 for some head "
            f"(max {float(sum(g_new.values()).max()):.4f}); the residual spans "
            f"would need non-positive mass.")

    z = logrow.clone()
    for name, (idx, _) in spans.items():
        b = ((g_new[name].log() - g_R_new.log())
             - (g[name].log() - g_R.log()))                    # [B, H]
        z[:, :, idx] = z[:, :, idx] + b.unsqueeze(-1)
    return torch.softmax(z, dim=-1)


def _knocked_row(p, ko: "KnockoutPlan", logrow: torch.Tensor,
                 n_key: int) -> torch.Tensor:
    """Re-softmax the readout row with the blocked spans masked out."""
    z = logrow.clone()
    blocked = torch.zeros(n_key, dtype=torch.bool, device=z.device)
    for name in ko.spans:
        if name not in p.index:
            raise KeyError(f"span {name!r} not bound (have {sorted(p.index)})")
        idx = p.index[name]
        blocked[idx[idx < n_key]] = True
    # The readout attends only at or before its own position; positions after
    # it are already -inf from the causal mask and must not be counted as
    # survivors, or a fully blocked row would look supported.
    live = torch.isfinite(logrow[0, 0]) & ~blocked
    if not bool(live.any()):
        raise ValueError(
            f"blocking {list(ko.spans)} leaves the readout with no attendable "
            f"position; at least one span must survive.")
    z[:, :, blocked] = float("-inf")
    return torch.softmax(z, dim=-1)


def _attention_forward(module, query, key, value, attention_mask, scaling,
                       dropout=0.0, **kwargs):
    p = _ACTIVE
    ell = getattr(module, "layer_idx", None)
    if (p is None or not p.armed or ell is None
            or id(module) not in p._attn_ids or (int(ell) + 1) not in p.layers):
        return sdpa_attention_forward(module, query, key, value,
                                      attention_mask, scaling=scaling,
                                      dropout=dropout, **kwargs)
    ell = int(ell) + 1  # this package indexes layers from 1

    n_rep = getattr(module, "num_key_value_groups", 1)
    k = _repeat_kv(key, n_rep).float()
    v = _repeat_kv(value, n_rep).float()

    qf = query.float()
    logits = torch.matmul(qf, k.transpose(2, 3)) * scaling
    if attention_mask is not None:
        logits = logits + attention_mask[:, :, :, : k.shape[-2]].float()
    probs = torch.softmax(logits, dim=-1)
    # Keep the readout row's pre-softmax logits for the geometry decomposition
    # and for the mass clamp; every source span sits at or before the readout
    # so its logits are unmasked and equal scaling * (q_r · k_j).
    clamp = p.clamp_plan.get(ell) if p.clamp_plan else None
    knock = p.knockout_plan.get(ell) if p.knockout_plan else None
    keep_row = p.want_geometry or clamp is not None or knock is not None
    logrow = logits[:, :, p.q_index, :].clone() if keep_row else None
    del logits

    q_idx = p.q_index
    if q_idx is None or q_idx >= probs.shape[2]:
        raise RuntimeError(
            f"readout query index {q_idx} is outside this forward's "
            f"{probs.shape[2]} query positions; the probe was armed against a "
            f"different sequence.")
    n_key = probs.shape[-1]
    row = probs[:, :, q_idx, :]                       # [B, H, S]

    # ---- span-mass clamp / knockout -------------------------------------
    # Applied before the capture, so a capture taken alongside one of these
    # reports the masses the forward actually used rather than the ones it
    # replaced.
    if clamp is not None or knock is not None:
        if p.qk_plan and ell in p.qk_plan:
            raise ValueError(
                f"layer {ell} has both a readout-row rewrite and a QKPlan; "
                f"the two rewrite the same row and would silently compose.")
        if clamp is not None and knock is not None:
            raise ValueError(
                f"layer {ell} has both a ClampPlan and a KnockoutPlan; a "
                f"clamped span that is also blocked has no well-defined mass.")
        row = (_clamped_row(p, clamp, logrow, row, n_key) if clamp is not None
               else _knocked_row(p, knock, logrow, n_key))

    # ---- measurement --------------------------------------------------
    if p.capture is not None:
        rec = LayerCapture()
        rec.z_all = torch.einsum("bhs,bhsd->bhd", row, v)[0].cpu()
        # The output gate multiplies the head aggregate elementwise before the
        # output projection, so a contribution that omits it is wrong by a
        # per-head-dim factor on gated stacks. Recomputed here from the layer's
        # own stashed hidden state rather than approximated.
        gate = p.gate_row(module, ell) if p.want_contrib else None
        rec.gated_contrib = gate is not None
        rec.gate = gate.cpu() if gate is not None else None
        u_eff = p.u_eff.get(ell) if p.u_eff else None
        for name, idx in p.index.items():
            ii = idx[idx < n_key]
            if ii.numel() == 0:
                rec.z_span[name] = torch.zeros(v.shape[1], v.shape[-1])
                if p.want_contrib:
                    rec.c_span[name] = torch.zeros(v.shape[1])
                    rec.mass_span[name] = torch.zeros(v.shape[1])
                continue
            if p.want_contrib:
                rec.mass_span[name] = row[:, :, ii].sum(-1)[0].cpu()
                if u_eff is not None:
                    z_S = torch.einsum("bhs,bhsd->bhd", row[:, :, ii],
                                       v[:, :, ii, :])          # [B, H, d]
                    if gate is not None:
                        z_S = z_S * gate.unsqueeze(0)
                    rec.c_span[name] = torch.einsum(
                        "bhd,hd->bh", z_S, u_eff)[0].cpu()       # [H] nats
            rec.z_span[name] = torch.einsum(
                "bhs,bhsd->bhd", row[:, :, ii], v[:, :, ii, :])[0].cpu()
            if p.want_rows:
                rec.a_span[name] = row[:, :, ii][0].cpu()
            if p.want_values:
                rec.v_span[name] = v[:, :, ii, :][0].cpu()
            if p.want_geometry:
                lr = logrow[:, :, ii]                     # [B, H, |S|] scaled dots
                kn = k[:, :, ii, :].norm(dim=-1)          # [B, H, |S|]
                vn = v[:, :, ii, :].norm(dim=-1)          # [B, H, |S|]
                qn = qf[:, :, q_idx, :].norm(dim=-1)      # [B, H]
                rec.logZ_span[name] = torch.logsumexp(lr, dim=-1)[0].cpu()  # [H]
                rec.k_norm_span[name] = kn.mean(dim=-1)[0].cpu()
                rec.v_norm_span[name] = vn.mean(dim=-1)[0].cpu()
                # cosθ_rj = (q_r·k_j) / (‖q_r‖‖k_j‖); the raw dot is lr/scaling.
                cos = (lr / scaling) / (qn.unsqueeze(-1) * kn).clamp_min(1e-12)
                rec.cos_span[name] = cos.mean(dim=-1)[0].cpu()
                ue = p.u_eff.get(ell) if p.u_eff else None
                if ue is not None:
                    proj = torch.einsum("bhsd,hd->bhs", v[:, :, ii, :], ue)
                    rec.ans_span[name] = proj.abs().mean(dim=-1)[0].cpu()
            if p.want_qk:
                rec.k_span[name] = k[:, :, ii, :][0].cpu()
        if p.want_geometry:
            rec.q_norm = qf[:, :, q_idx, :].norm(dim=-1)[0].cpu()
        if p.want_qk:
            rec.q_readout = qf[:, :, q_idx, :][0].cpu()
        p.capture[ell] = rec

    out = torch.matmul(probs, v)                       # [B, H, q, d]

    # The clamp rewrote the readout row only; every other query position keeps
    # the model's own attention, so only that row's aggregate is replaced.
    if clamp is not None or knock is not None:
        out = out.clone()
        out[:, :, q_idx, :] = torch.einsum(
            "bhs,bhsd->bhd", row, v).to(out.dtype)

    # ---- QK cross-swap: recompute the readout row from mismatched q/k/V ---
    qk = p.qk_plan.get(ell) if p.qk_plan else None
    if qk is not None:
        k_used = k
        if qk.k_other:
            k_used = k.clone()
            for name, ko in qk.k_other.items():
                idx = p.index[name]; idx = idx[idx < n_key]
                k_used[:, :, idx, :] = ko.unsqueeze(0).to(k_used.device, k_used.dtype)
        q_tgt = qf[:, :, q_idx, :]                                  # [B, H, d]
        z_row = torch.einsum("bhd,bhsd->bhs", q_tgt.float(), k_used.float()) * scaling
        if qk.q_other is not None:
            q_o = qk.q_other.unsqueeze(0).to(qf.device, qf.dtype)
            z_o = torch.einsum("bhd,bhsd->bhs", q_o.float(), k_used.float()) * scaling
            if qk.q_span is None:
                z_row = z_o                                         # global query swap
            else:
                for name in qk.q_span:                             # per-span query swap
                    idx = p.index[name]; idx = idx[idx < n_key]
                    z_row[:, :, idx] = z_o[:, :, idx]
        if attention_mask is not None:
            z_row = z_row + attention_mask[:, :, q_idx, :n_key].float()
        probs_row = torch.softmax(z_row, dim=-1)                    # [B, H, S]
        v_used = v
        if qk.v_other:
            v_used = v.clone()
            for name, vo in qk.v_other.items():
                idx = p.index[name]; idx = idx[idx < n_key]
                v_used[:, :, idx, :] = vo.unsqueeze(0).to(v_used.device, v_used.dtype)
        new_row = torch.einsum("bhs,bhsd->bhd", probs_row, v_used)  # [B, H, d]
        out = out.clone()
        out[:, :, q_idx, :] = new_row.to(out.dtype)
        # record the post-swap attention mass per span (renormalization effect)
        if p._qk_A is not None:
            p._qk_A[ell] = {name: float(
                probs_row[:, :, p.index[name][p.index[name] < n_key]].sum(-1).mean())
                for name in p.index}
        return out.to(value.dtype).transpose(1, 2).contiguous(), None

    # ---- substitution -------------------------------------------------
    plan = p.plan.get(ell) if p.plan else None
    if plan is not None and plan.mode != "none":
        idx = plan.span_index.to(out.device)
        idx = idx[idx < n_key]
        cur = torch.einsum("bhs,bhsd->bhd", row[:, :, idx], v[:, :, idx, :])
        if plan.mode == "swap":
            new = plan.z_other.to(out.device, out.dtype).unsqueeze(0)
        elif plan.mode == "attn_other":
            a = plan.a_other.to(out.device, out.dtype).unsqueeze(0)
            new = torch.einsum("bhs,bhsd->bhd", a, v[:, :, idx, :])
        else:  # values_other
            vo = plan.v_other.to(out.device, out.dtype).unsqueeze(0)
            new = torch.einsum("bhs,bhsd->bhd", row[:, :, idx], vo)
        delta = new - cur
        if plan.head_mask is not None:
            delta = delta * plan.head_mask.to(delta.device, delta.dtype).view(1, -1, 1)
        out = out.clone()
        out[:, :, q_idx, :] = out[:, :, q_idx, :] + delta

    return out.to(value.dtype).transpose(1, 2).contiguous(), None


AttentionInterface.register(IMPL_NAME, _attention_forward)
# The mask builder is selected by the SAME name. Without this the model hands
# back SDPA's mask -- None whenever it can rely on is_causal -- and the eager
# matmul above would attend non-causally.
ALL_MASK_ATTENTION_FUNCTIONS.register(IMPL_NAME, eager_mask)


class SpanAttention:
    """Captures and substitutes per-source-span attention aggregates.

    Lifecycle::

        sa = SpanAttention(model, adapter, layers=[8, 12, 16]).attach()
        sa.bind(spans.as_dict(), q_index=r)
        sa.arm(capture=True)                 # measure
        ...forward...
        cap = sa.take_capture()
        sa.arm(plan={12: SubPlan(...)})      # intervene
        ...forward...
        sa.disarm()
        sa.remove()
    """

    def __init__(self, model, adapter, layers):
        self.model = model
        self.adapter = adapter
        requested = sorted({int(e) for e in layers})
        if requested and requested[0] < 1:
            raise ValueError("layers are 1-based")

        from attention.patch_hooks import get_layers
        stack = get_layers(model, adapter)
        self.n_layers = len(stack)
        for ell in requested:
            if ell > self.n_layers:
                raise ValueError(f"layer {ell} > {self.n_layers} decoder layers")
        # Only modules that are decoder self-attentions with a layer_idx are
        # eligible; everything else (notably the image encoder, and the
        # linear-attention layers of a hybrid stack) never calls the attention
        # interface and cannot be decomposed by source span.
        self._attn_ids = set()
        self.attn_layers: list[int] = []
        self.layer_types: dict[int, str] = {}
        self.sliding_windows: dict[int, Optional[int]] = {}
        self.contrib_exact_layers: list[int] = []
        for i, layer in enumerate(stack):
            sa = getattr(layer, "self_attn", None)
            if sa is not None and getattr(sa, "layer_idx", None) is not None:
                self._attn_ids.add(id(sa))
                ell = i + 1
                self.attn_layers.append(ell)
                self.layer_types[ell] = str(
                    getattr(sa, "layer_type", None) or "full_attention"
                )
                self.sliding_windows[ell] = getattr(sa, "sliding_window", None)
                # Per-span contributions are additive in the residual stream
                # only when the projected attention aggregate is added
                # directly. Gemma3 and GLM-4.xV apply an output-side RMSNorm
                # first, so their attention masses and knockout effects are
                # exact but an additive per-span residual attribution is not
                # mathematically defined.
                has_output_norm = (
                    hasattr(layer, "post_self_attn_layernorm")
                    or (
                        hasattr(layer, "pre_feedforward_layernorm")
                        and hasattr(layer, "post_attention_layernorm")
                    )
                )
                if not has_output_norm:
                    self.contrib_exact_layers.append(ell)
        # Restrict to the softmax-attention layers rather than raising: on a
        # hybrid stack (e.g. Qwen3.5, where only every 4th layer is full
        # attention) the caller legitimately passes a window that mixes both
        # kinds, and only the softmax layers can be probed. self.layers is the
        # set actually decomposed; dropped layers are reported so a hybrid run
        # never silently probes fewer layers than intended.
        self.layers = [e for e in requested if e in self.attn_layers]
        dropped = [e for e in requested if e not in self.attn_layers]
        if dropped:
            print(f"SpanAttention: {len(dropped)} of {len(requested)} requested "
                  f"layers have no softmax attention and are skipped for span "
                  f"decomposition: {dropped}. Probing {self.layers}.")
        if not self.layers:
            raise RuntimeError(
                f"none of the requested layers {requested} are softmax-attention "
                f"layers; this architecture's attention layers are "
                f"{self.attn_layers}. Source-span decomposition is undefined here.")

        cfg = getattr(model.config, "text_config", model.config)
        self.n_heads = int(getattr(cfg, "num_attention_heads"))
        self.gated = self._detect_output_gate(stack)

        # Per-softmax-layer output projection reshaped to [d_model, H, head_dim]
        # (the concatenation is head-major, so head h owns a column block). Used
        # only by the geometry capture, to fold W_O^T u_diff into the answer-
        # projection ‖u_diff·W_O·V_j‖.
        self._Wo: dict[int, torch.Tensor] = {}
        for ell in self.layers:
            op = self._find_o_proj(stack[ell - 1])
            if op is not None:
                hd = op.in_features // self.n_heads
                self._Wo[ell] = op.weight.detach().float().view(-1, self.n_heads, hd)

        self._prev_impl: Optional[str] = None
        self.armed = False
        self.q_index: Optional[int] = None
        self.index: dict[str, torch.Tensor] = {}
        self.capture: Optional[dict[int, LayerCapture]] = None
        self.plan: dict[int, SubPlan] = {}
        self.want_rows = False
        self.want_values = False
        self.want_geometry = False
        self.want_qk = False
        self.want_contrib = False
        self.u_eff: dict[int, torch.Tensor] = {}
        self.qk_plan: dict[int, QKPlan] = {}
        self.clamp_plan: dict[int, ClampPlan] = {}
        self.knockout_plan: dict[int, KnockoutPlan] = {}
        self._qk_A: Optional[dict[int, dict[str, float]]] = None
        # Readout-position hidden state per softmax layer, stashed by a
        # pre-hook so the output gate can be recomputed exactly. Only installed
        # on gated stacks, and only used by the contribution capture.
        self._h_readout: dict[int, torch.Tensor] = {}
        self._gate_handles: list = []
        if self.gated:
            self._install_gate_hooks(stack)

    def _install_gate_hooks(self, stack) -> None:
        """Stash each softmax layer's readout hidden state for the gate.

        The gate is a function of the block's input hidden state, which the
        attention interface never sees -- it is handed queries, keys and values
        only. A forward pre-hook on the attention module captures the one row
        that matters, so ``gate_row`` can reproduce the model's own gate exactly
        instead of dividing it out of the output.
        """
        for ell in self.layers:
            sa = getattr(stack[ell - 1], "self_attn", None)
            if sa is None:
                continue

            def hook(mod, args, kwargs, _ell=ell):
                if not (self.armed and self.want_contrib):
                    return
                h = kwargs.get("hidden_states")
                if h is None and args:
                    h = args[0]
                if h is not None and self.q_index is not None:
                    self._h_readout[_ell] = h[:, self.q_index, :].detach()

            self._gate_handles.append(
                sa.register_forward_pre_hook(hook, with_kwargs=True))

    def gate_row(self, module, ell: int) -> Optional[torch.Tensor]:
        """``sigmoid(gate)`` at the readout for layer ``ell``, or None.

        Mirrors the gated architecture's own construction: ``q_proj`` emits
        query and gate interleaved per head as ``2 * head_dim``, the model
        chunks them apart, and the gate multiplies the flattened head aggregate
        elementwise. Returns ``[H, head_dim]``, aligned with the per-head
        aggregate the capture holds.
        """
        if not self.gated:
            return None
        h = self._h_readout.get(ell)
        qp = getattr(module, "q_proj", None)
        head_dim = getattr(module, "head_dim", None)
        if h is None or qp is None or not head_dim:
            return None
        head_dim = int(head_dim)
        proj = qp(h).view(h.shape[0], -1, head_dim * 2)     # [B, H, 2*hd]
        _, gate = torch.chunk(proj, 2, dim=-1)              # [B, H, hd]
        return torch.sigmoid(gate.float())[0]               # [H, hd]

    @staticmethod
    def _find_o_proj(layer):
        sa = getattr(layer, "self_attn", None)
        if sa is None:
            return None
        for name in ("o_proj", "dense", "out_proj"):
            m = getattr(sa, name, None)
            if isinstance(m, torch.nn.Linear):
                return m
        return None

    # ------------------------------------------------------------------

    def _detect_output_gate(self, stack) -> bool:
        """True if the block gates the head aggregate before the projection.

        Detected structurally -- the query projection is twice as wide as the
        queries need -- rather than by model name. Substitution still lands in
        the right place when a gate is present (it happens upstream of the
        gate), but the gate is computed from the *current* run's hidden state,
        so a full-aggregate substitution reproduces the other run's attention
        write only up to that gate. Callers record this so the caveat travels
        with the run.
        """
        for ell in self.attn_layers:
            sa = getattr(stack[ell - 1], "self_attn", None)
            qp = getattr(sa, "q_proj", None) if sa is not None else None
            kp = getattr(sa, "k_proj", None) if sa is not None else None
            if qp is None or kp is None:
                continue
            head_dim = getattr(sa, "head_dim", None)
            if head_dim and qp.out_features == 2 * self.n_heads * int(head_dim):
                return True
        return False

    def attach(self) -> "SpanAttention":
        global _ACTIVE
        if _ACTIVE is not None and _ACTIVE is not self:
            raise RuntimeError("another SpanAttention is already attached")
        cfg = getattr(self.model.config, "text_config", self.model.config)
        self._prev_impl = cfg._attn_implementation
        cfg._attn_implementation = IMPL_NAME
        self.model.config._attn_implementation = IMPL_NAME
        _ACTIVE = self
        return self

    def remove(self) -> None:
        global _ACTIVE
        if self._prev_impl is not None:
            cfg = getattr(self.model.config, "text_config", self.model.config)
            cfg._attn_implementation = self._prev_impl
            self.model.config._attn_implementation = self._prev_impl
            self._prev_impl = None
        for h in self._gate_handles:
            h.remove()
        self._gate_handles.clear()
        self._h_readout.clear()
        self.armed = False
        if _ACTIVE is self:
            _ACTIVE = None

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.remove()

    # ------------------------------------------------------------------

    def bind(self, spans: dict[str, list[int]], q_index: int,
             u_diff: Optional[torch.Tensor] = None) -> "SpanAttention":
        """Install this example's source spans and readout query position.

        ``u_diff`` (the readout unembedding difference ``W_lm[id_T] -
        W_lm[id_V]``) enables the answer-projection geometry term: it is folded
        through each layer's output projection into ``u_eff[ell] = W_O^T u_diff``,
        so the capture can report ‖u_diff·W_O·V_j‖ per span. On an output-gated
        architecture this omits the gate (applied to the value aggregate), so
        the answer-projection is approximate there; the logit-side geometry
        (drives, key/query norms, cosθ) is gate-independent and exact.
        """
        dev = self.model.device
        self.index = {name: torch.as_tensor(sorted(int(i) for i in pos),
                                            device=dev, dtype=torch.long)
                      for name, pos in spans.items()}
        self.q_index = int(q_index)
        if u_diff is not None and self._Wo:
            ud = u_diff.detach().float().to(dev)
            self.u_eff = {ell: torch.einsum("dhe,d->he", Wo.to(dev), ud)
                          for ell, Wo in self._Wo.items()}
        else:
            self.u_eff = {}
        return self

    def span_index(self, name: str) -> torch.Tensor:
        if name == "all":
            return torch.cat([v for v in self.index.values()]).sort().values
        if name not in self.index:
            raise KeyError(f"span {name!r} not bound (have {sorted(self.index)})")
        return self.index[name]

    def arm(self, *, capture: bool = False, plan: Optional[dict] = None,
            want_rows: bool = False, want_values: bool = False,
            want_geometry: bool = False, want_qk: bool = False,
            want_contrib: bool = False, qk_plan: Optional[dict] = None,
            clamp_plan: Optional[dict] = None,
            knockout_plan: Optional[dict] = None) -> None:
        if want_contrib and not self.u_eff:
            raise ValueError(
                "want_contrib needs the answer direction: pass u_diff to "
                "bind() so W_O^T u_diff can be folded per layer.")
        self.capture = {} if capture else None
        self.plan = dict(plan) if plan else {}
        self.qk_plan = dict(qk_plan) if qk_plan else {}
        self.clamp_plan = dict(clamp_plan) if clamp_plan else {}
        self.knockout_plan = dict(knockout_plan) if knockout_plan else {}
        self._qk_A = {} if qk_plan else None
        self.want_rows = want_rows
        self.want_values = want_values
        self.want_geometry = want_geometry
        self.want_qk = want_qk
        self.want_contrib = want_contrib
        self._h_readout.clear()
        self.armed = True

    def take_qk_A(self) -> dict[int, dict[str, float]]:
        """Post-swap attention mass per span, per layer, from the last QK swap."""
        a, self._qk_A = self._qk_A, None
        return a or {}

    def disarm(self) -> None:
        """Stop intercepting. The capture is left in place for the caller to
        collect, since ``disarm`` is normally the ``finally`` clause of the
        very forward that produced it."""
        self.armed = False
        self.plan = {}
        self.qk_plan = {}
        self.clamp_plan = {}
        self.knockout_plan = {}
        self._h_readout.clear()

    def take_capture(self) -> dict[int, LayerCapture]:
        cap, self.capture = self.capture, None
        if cap is None:
            raise RuntimeError("SpanAttention was not armed with capture=True")
        return cap

    # ------------------------------------------------------------------

    @staticmethod
    def reconstruction_error(cap: LayerCapture) -> float:
        """Max deviation of ``sum_S z_{r<-S}`` from the full aggregate.

        The four spans partition every position the readout can attend to, so
        this is zero up to floating-point summation order. It is the
        implementation sanity check of design section 14: a non-trivial value
        means the spans do not actually cover the attended positions.
        """
        if cap.z_all is None or not cap.z_span:
            return float("nan")
        total = None
        for z in cap.z_span.values():
            total = z.clone() if total is None else total + z
        return float((total - cap.z_all).abs().max())
