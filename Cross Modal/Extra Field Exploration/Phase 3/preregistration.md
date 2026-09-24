# Pre-Registration Lock — Phase 3 Pilot (Q1 & Q2)

Locked **before** any pilot results were inspected or generated. Pre-flight
engineering evidence (model loads, hook capture, eager-attention extraction,
generation smoke test on CPU) was gathered before this file and is reported
separately under the Phase-3 report's engineering sections. No Q1/Q2 kill-gate
*measurement* is reported from the local CPU environment; all statistical
estimates below are pre-specified.

## 1. Models (primary)

- `Qwen/Qwen2.5-VL-3B-Instruct` — open weights; verified in-context: 36
  decoder layers, hidden 2048, 16 heads, 2 KV heads, unified self-attention
  (no cross-attention modules), 32-layer vision tower (hidden 1280, patch 14,
  spatial merge 2, temporal patch 2), `attn_implementation="eager"` required
  to expose `output_attentions`. Weights 7.51 GB bf16.
- Secondary for Q2-A (cross-family): `google/gemma-3-4b-it` — gated (HF token
  + license acceptance verified required: raw `config.json` returns 401 without
  auth). Multimodal per model card (SigLIP 400M encoder, 896x896, 256 image
  soft-tokens, 62 layers, mixed local/global attention, Qwen-style pooled
  bidirectional image attention). Fallback if gating cannot be satisfied:
  `MindSpec/InternVL2-2B` or `openbmb/MiniCPM-V-2_6` (open, ungated).
  Q2-A comparisons are **mechanism** (residual-stream lookup + swap) not token
  identity, because vision tokenization differs across families.

## 2. Datasets (all verified publicly accessible unless noted)

- **Q1 image+question pool**: reconstructed WhatIfVis-style cases. WhatIfVis
  itself (A1, 3,049 samples) is **not directly downloadable**; cases are
  rebuilt from documented public sources: VLind-Bench (COCO Lite + synthetic),
  Pixels-versus-Priors, plus our own generated balance-scale items (VIG-style
  visual-arithmetic). All 5 conflict dimensions (spatial-temporal, color,
  count, size, weight) targeted. License notes recorded per source.
- **Q1 length-manipulation probes**: RH-Bench (`LCZZZZ/RH-Bench`, public HF
  dataset + `github.com/MLRM-Halu/MLRM-Halu`) recommended for *length-control
  tooling only* (latent steering + budget forcing). RH-Bench's own finding
  (longer chains -> more hallucination, non-monotonic) does **not** answer
  Q1's mechanistic questions (position vs content vs softmax-dilution vs
  causal availability). Not used as labels; used as length-manipulation
  reference.
- **Q2 synthetic grid**: 2 rows x 4 columns, non-ordinal symbol sets
  (`{&,$,#,@}` per row), C1-style lookup questions; 25 synthetic images.
- **Q2 natural transfer**: InstaBind-Lite / DSCAM (`github.com/InstaBind-Lite/InstaBind-Lite`;
  524 images, 529 groups, 1,773 source-instance object boxes, 9,580
  deterministic questions, source-instance annotations; boxes give clean
  swap targets). Subset only (25 natural images) for the pilot. SugarCrepe
  and What'sUp as fallback/adjunct if InstaBind fetch fails.

## 3. Hypotheses

### Q1 — Visual-evidence utilization under reasoning length

- **H1 (causal length effect, mechanistic):** manipulating the *reasoning
  trace* between the image block and the final answer reduces the model's
  utilization of visual evidence at the answer token, *holding answer
  position and answer content fixed and net of softmax dilution*.
- **H1a (position-not-content control):** control condition adds length by
  placing a *fixed block* of text tokens between image and answer (so answer
  position is fixed); reasoning trace is varied separately.
- **H1b (dilution null):** under no positional bias, if attention were
  uniform over `N` key positions and the vision block uses `M` of them, the
  null vision mass is `M/N`. Softmax dilution predicts
  `Δ(mass_v_vision)/Δ(N) = Δ(M/N)/Δ(N)`. Kill condition: no deviation from
  this dilution slope is detected (equivalence test below).
- **H1c (availability check):** the evidence's binding information is still
  linearly decodable from the residual stream / answer-token activation even
  when utilization (attention) drops. If decodability drops to chance while
  utilization drops, the effect is better described as *evidence decay*
  (reframe Q1 toward decay, not only attention reallocation).

### Q2 — Binding-ID universality vs synthetic-scene artifact

- **H2 (mechanism existence in a natural-image scene):** swapping
  row-partition / source-instance activations between two images transfers
  the *binding relation* (which symbol associates with which reference) in
  natural images, producing the predicted target-flip, and does so
  significantly more than matched placebo interventions.
- **H2a (placebo):** matched-norm, matched-location, matched-layer random
  vectors and orthogonal perturbations do not reproduce the flip.
- **H2b (natural transfer):** the effect transfers to InstaBind-Lite natural
  images with box-segmented instances.
- **H2c (universality, cross-family):** the mechanism generalizes across
  architectures (Qwen2.5-VL vs Gemma-3-4B-it as *mechanism*, not token
  identity) — descriptive/suggestive at pilot power.

## 4. Primary variables and metrics

Q1 (per condition, per sample, per layer block 0-11 / 12-23 / 24-35, and
averaged): vision-attention mass at the final answer token (`VIG_mass`),
deviation from uniform null `VIG_mass - M/N`, final-token vs prior-token
difference, linear-probe (logistic) AUC for evidence binding from answer-token
residual with random-label baseline, greedy answer correctness (deterministic
single-word parsing + gold label).

Q2 (per sample): target-flip rate `flip_target`, non-target preservation
`acc_target`/`acc_non` (lookup accuracy before and after swap),
target-column flip rate, net directed flip
`net_flip = flip_target - flip_nontarget`, coherence (degeneration/repetition
detector on generated prefix, bounded max generation length).

## 5. Conditions (Q1, within-item factorial)

- `short`: short trace (no added reasoning).
- `long`: long reasoning trace (filled with explicit intermediate
  reasoning; content controlled to same answer).
- `neutral`: same length as `long` with neutral non-reasoning filler
  (length control for softmax-dilution; checks content-nonspecific length).
- `posmatch_short`: same *final answer position* as `long` by moving the
  whole prefix block (position control); short trace.

Design: matched pairs on position and answer; 4 conditions per item; 50
items.

## 6. Statistical plan

- Q1: paired analysis over conditions; primary estimator: mean deviation of
  `VIG_mass - M/N` per condition, 95% bootstrap CI; the **reasoning-specific
  contrast** is `long` vs `neutral` (dilution-net). Position effect is
  `posmatch_short` vs `short`.
- Equivalence: two one-sided tests (TOST) with equivalence bound
  `theta = 0.05` on normalized VIG units for the null (dilution) contrast,
  and on `flip_target - flip_placebo` (Q2). **No `p > 0.05` claim of
  equivalence is accepted**; only a TOST/CI decision rule is used.
- Effect-size reporting: standardized difference (Cohen's `d_av`) with CI for
  all primary contrasts, not p-values alone.
- Decodability: 5-fold cross-validated logistic regression AUC minus chance,
  with permutation-based p (1,000 shuffles), random-label baseline; class
  balanced. Report AUC-e: net over chance.
- Q2: net flip rate with 95% CI over 25+25 samples; placebo-difference
  two-sided equivalence bound on `flip_target - flip_placebo`; coherence
  gate: mean length/normalized repetition below a pre-set degeneration
  threshold (see hard stops).

## 7. Kill-gate decision rules (pilot, pre-registered)

K1 (reasoning-vs-position): kill Q1 if TOST-accept equivalence of
`long` vs `neutral` and of `long` vs `posmatch_short` on the primary metric
(no reasoning-specific or position effect beyond dilution).

K2 (softmax dilution): accept dilution if the `long`/`short` slope equals the
`M/N` slope within `theta` (TOST); kills the non-dilution Q1 story.

K3 (availability): evidence reframed to decay if probe AUC-e reaches ~0 at
`long` while utilization also drops.

K4 (Q2 placebo): kill Q2 if the placebo net-flip 95% CI fully includes the
real-swap net-flip CI, or if placebo `net_flip > 0` with CI excluding 0 in
the *same* direction as the real swap at matched location/norm/layer.

K5 (natural transfer): kill Q2 if natural-image `net_flip` fails to beat
matched placebo CI at InstaBind images, or if `acc_non` collapses (coarse
new-binding failure).

K6 (cross-family): keep descriptive only; kill the *universality claim* if
the mechanism-specific flip is not behaviorally present in the second family
(see Section 7 note on pilot power).

K7 (alternative explanations): kill Q2 by reduction if, after controlling for
co-occurrence/prior naming, color-histogram delta, nearest-patch overlap and
spatial proximity (covariate model selection vs swap), a covariate alone
reproduces the net flip with 95% CI overlapping the swap.

K8 (resources): rescope if GPU VRAM budget exceeds 16 GB at any step
(measured `torch.cuda.max_memory_allocated`); batching/threshold-reduction
prescribed before aborting the run.

## 8. Failure taxonomy (per Phase-3 spec)

- F1 configuration/environment (missing dependency, wrong device): fix and
  rerun.
- F2 harness/machinery (processor token mismatch, hook misplacement, VRAM):
  fix, keep pre-registered analysis identical, document the fix.
- F3 dataset (fetch failure, answer-parse failure > threshold): replace with
  verified fallback (recorded) while keeping metrics.
- F4 model-architecture mismatch (e.g., `output_attentions` unavailable under
  a chosen backend): switch backend/`attn_implementation`, document.
- F5 compute-infrastructure (wall-clock, OOM, gating): rescope or move, not
  a failure of the science.
- F6 scientifically fatal (answer set unreachable, degenerate generation
  above threshold blocking the measurement): stop and report.
Only F4-F6 can bear against the science; F1-F3/F5 get repaired and rerun with
the same locked analysis.

## 9. Budget and order

- Q1: 50 items x 4 conditions, greedy, max_length 180, bf16 eager. Q2: 25
  synthetic + 25 natural, swap vs 3 placebos. Total estimated <
  ~6 GPU-hours on a 16 GB T4/L4-class GPU.
- Execution order: harness smoke (5 items) -> F-checks -> Q1 staging ->
  Q1 K1/K2 -> K3 -> Q2 synthetic staging -> Q2 swap/placebo -> natural ->
  Q2-A descriptive (optional) -> K7 covariate matrix (budget gate) -> K8
  report.
- Deviations require this file to be edited with a dated DEVIATION note
  before the affected analysis is run.

## 10. Hard stops

- Stop and report if any of: (1) generation degenerate (mean generated length
  below 4 tokens or repetition > 0.6 across a condition); (2) answer parse
  success < 70% on gold labels; (3) VRAM overflow at any step after the
  prescribed fix; (4) any unanticipated script-level crash that cannot be
  attributed to F1-F3; (5) elapsed pilot wall-clock > 12 GPU-hours.

Signed/locked: Phase-3 report date. No pilot results existed at lock time.