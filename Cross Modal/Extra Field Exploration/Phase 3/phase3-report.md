# Phase 3 Report — Adversarial Kill-Gate Filtering & Pre-Flight Runtime Verification

Candidates tested: **Q1** (visual-evidence utilization vs reasoning-trace length)
and **Q2** (Binding-ID universality vs synthetic-scene artifact), both evaluated
as backups to the canonical thesis **"Causal Conflict Verbalization under
Contradictory Evidence."** Pre-registration was locked before any measurement
was computed (<file path="artifacts/phase3/preregistration.md" />). All findings
follow the conservative-language output principle (§35 equivalent): nothing
below exceeds what the named evidence supports.

---

## 1. Executive Result Summary

This phase intentionally tried to kill Q1 and Q2. It did **not** fully succeed,
but it produced one major determinant and one serious complication for each.

- **Q1 must be reframed, not killed, by RH-Bench** (Liu et al. 2025,
  arXiv:2505.21523, NeurIPS 2025, `github.com/MLRM-Halu/MLRM-Halu`, HF
  `LCZZZZ/RH-Bench`): the claimed untouched niche "nobody manipulated reasoning
  length in a VLM" already has a direct prior that found *more* reasoning
  reduces visual attention and *increases* hallucination (non-monotonic). Q1
  survives only as a **mechanistic decomposition** (position vs content vs
  softmax-dilution vs causal availability) *layered on* RH-Bench's length-control
  tooling. Verdict: **SURVIVES WITH MODIFICATION — UNCERTAIN** pending pilot.
- **Q2 unprecedentedly strong prior**: C1 (arXiv:2509.24072) is a nearly
  identical mechanism study *in synthetic scenes*, which is exactly Q2's
  artifact susceptibility. The pilot's K4/K5 (placebo + natural-image transfer)
  and K7 (covariate reduction) runs are therefore the deciding gates, and all
  three will be cheap only on GPU. Verdict: **SURVIVES — UNCERTAIN, CONDITIONAL
  ON K4/K5/K7**.
- **4 of 5 required input files were missing**; the single present file
  (phase2-report.md) was fully used and is the source of the K1-K8 criteria.
- **Local environment cannot produce GPU runtime evidence** (no GPU; a 7.5 GB
  model download + full harness smoke ran on CPU). Attention extraction,
  residual-stream hooks, and stable generation are all verified working; the
  pilot must run on the user's Colab Pro 16 GB instance.
- **Phase 4 entry gate: DO NOT PROCEED — ADDITIONAL PHASE-3 PILOT REQUIRED**
  (GPU run of the pre-registered harness).

---

## 2. Required Input Files — Status

| # | File | Status | Notes |
|---|------|--------|-------|
| 1 | `Plan.md` | **MISSING (NEVER FOUND)** | Full-user-profile search; no file of this name exists anywhere |
| 2 | `Multimodal AI Thesis Feasibility Audit (Phase 2).md` | **MISSING (NEVER FOUND)** | Only `phase2-report.md` exists (deliverable from last phase, not the requested audit) |
| 3 | `Phase2 AlphaXiV Report.md` | **MISSING (NEVER FOUND)** | No such file |
| 4 | `Canonical_Thesis_Topic_Specification.md` | **MISSING (NEVER FOUND)** | No such file |
| 5 | Phase-2 report | **PRESENT** | `<file path="artifacts/phase2/phase2-report.md" />` (30,861 B) — sole usable input |

Per spec (§2) the four missing files are **reported, not reconstructed**.
All Phase-2-derived criteria below therefore come from the present
phase2-report.md, and any executable facts initially attributed to the
missing files (e.g., canonical spec, Phase-2 audit) are treated as
**not available**. This weakens only the *reporting completeness*, not the
kill-gate logic, whose criteria live in phase2-report.md.

---

## 3. Kill-Gate Overview

Test suite (K1-K8), each gate: restate hypothesis and null, list confounds,
then **audit the Phase-2 criterion's validity** and log original→corrected
(Section 7). Executability status: all gates are executable in the pilot
harness (<file path="artifacts/phase3/pilot_harness.py" />,
<file path="artifacts/phase3/pilot_run.py" />); K8 is resource-gated to GPU.

| Gate | Candidate | Question |
|------|-----------|----------|
| K1 | Q1 | Trace-length effect separable from answer-position effect? |
| K2 | Q1 | Is the decline mere softmax/dilution? |
| K3 | Q1 | Is evidence still *available* (decodable, steerable) when unused? |
| K4 | Q2 | Does a matched placebo reproduce the swap effect? |
| K5 | Q2 | Does the effect transfer to natural images with real object boxes? |
| K6 | Q2-A | Does the mechanism generalize across architectures? |
| K7 | Q2 | Is the effect reducible to naming/color/nearest-patch/framing? |
| K8 | Both | Do all pilot steps fit 16 GB Colab VRAM within budget? |

---

## 4. Q1 — Reconstructed Statement (Post-RH-Bench Pre-emption)

Hundreds of papers manipulate reasoning length in LLMs; RH-Bench did it in a
VLM and found *more reasoning reduces visual attention and increases
hallucination, non-monotonically* (moderate length best; RH-AUC metric; latent
steering + budget forcing on 1,000 video/image samples; transforms). What
RH-Bench does **not** establish, and what Q1 must therefore claim:

1. **Positional mechanism** — whether the decline is due to the reasoning
   *content* or just the *distance/position* of the answer relative to the
   image block (fixed-answer-layout control).
2. **Softmax/dilution logic** — whether the decline tracks the uniform-null
   `M/N` attention share exactly (dilution) or deviates (reallocation).
3. **Causal availability** — whether the evidence can still be steered/decoded
   at generation time even when unattended.

Reframed Q1 contribution: **a mechanistic decomposition of RH-Bench's
controlled length effect**, reusing its steering/budget tooling. This
narrowing preserves a de-novo claim (none of A1, RH-Bench, or any located
prior controls all three) while conceding the headline result is taken.

---

## 5. Q2 — Reconstructed Statement

Claim: C1's binding-ID phenomenon (row-partition activation swap transfers
symbol bindings in 2x4 synthetic grids) is a **general mechanism**, not a
synthetic-scene artifact — it should (a) survive matched placebo at equal
norm/location/layer ([K4], (b) transfer to natural images with box-segmented
instances ([K5]), (c) survive covariate reduction to naming/color-histogram/
nearest-patch/[spatial proximity ([K7]), and (d) behave cross-architecturally
as a *mechanism* (residual-stream lookup + swap), not as token identity ([K6]).

Contribution: A1-style what-if benchmarks + C1's synthetic grids are what-if
benchmarks; nobody has demonstrated the swap mechanism on natural boxed
objects. If K5 transfers, a natural-image binding intervention library is a
novel instrument.

---

## 6. Q1 & Q2 — Relations and Fit vs Canonical Thesis

- **Q1 bears on the canonical claim directly**: the canonical thesis centers
  on *how a model verbalizes under contradictory visual evidence*. If evidence
  utilization irreversibly collapses with deliberation length, conflict
  verbalization may be *length-dependent by mechanism*, which RH-Bench's
  hallucination result already suggests. Q1 therefore strengthens or
  constrains the canonical thesis's causal-utilization account.
- **Q2 does not directly compete with the canonical thesis**; it is a
  methodology-dependency: the canonical thesis and A1 both rely on the model
  correctly using visual bindings. If bindings are synthetic-scene artifacts,
  the canonical thesis's mechanism assumptions weaken. Q2 thus secures a
  shared assumption rather than offering a rival.
- **No mutual-kill relation**: results consistent for one candidate do not
  hand the thesis to the other; they are independent axes.

---

## 7. Validity Audit of the Kill-Gate Criteria (K1-K8) — original → corrected

Per spec (§7): every gate's Phase-2 criterion was audited *before* execution.
Changes are explicit; no criterion was silently "repaired" without a logged
replacement.

### K1 — length vs position
- Hypothesis: reasoning-trace length drives utilization decline independent of
  answer position. Null: the effect is fully attributable to position.
- Phase-2 criterion: "effect vanishes with answer position fixed -> Q1
  collapses to position." **VALID directionally; UNSUITABLE as written**:
  it only detects collapse, not the reasoning-vs-any-content confound.
- **Corrected**: 4-condition factorial, pre-registered (short / long-reasoning
  / long-neutral-no-reasoning / position-matched-short; `<file path="artifacts/phase3/pilot_run.py" />`).
  Kill requires TOST-equivalence (margin 0.05 normalized-VIG units) of
  *both* long-vs-neutral (content-nonspecific) and long-vs-position-matched.
  Logged: original 1-gate rule → 2-equivalence rule + a positive
  reasoning-specific contrast requirement.

### K2 — softmax dilution
- Hypothesis: decline = uniform-attention dilution as `N` grows; null: no
  deviation from the `M/N` slope.
- Phase-2 criterion: "normalized VIG" — **INVALID as written**: no explicit
  null model, no normalization definition, and the `1/N` or `xN` convention
  was ambiguous.
- **Corrected**: metric = `VIG_mass − M/N` with a *derived* uniform-attention
  null (attention = chance over all keys, vision block size M, key count N),
  and a slope test `Δ(mass)/Δ(N) = Δ(M/N)/Δ(N)` within the equivalence margin.
  This makes the dilution claim falsifiable rather than a "duh" consequence of
  normalization.

### K3 — availability
- Phase-2 criterion: "steering/decodability survives at long trace; if
  evidence no longer decodable, Q1 reframes as decay." **Criterion mixes two
  constructs (representational decodability and causal steering)** and ties a
  gate to an unjustified absolute threshold (~70%).
- **Corrected**: split into K3a (logistic probe AUC over the answer-token
  residual, minus chance, permutation p, class-balanced) and K3b (steering/
  ablation at the generation token). No absolute accuracy gates; decisions on
  AUC-e CI vs chance.

### K4 — placebo (Q2)
- Phase-2 criterion: "if placebo reproduces the effect, Q2 dies." **VALID in
  direction; controls underspecified.**
- **Corrected**: placebo must match source in norm, location (same token
  rows), and layer; three placebos are pre-specified: random vector,
  mean-orthogonalized perturbation, and a same-layer same-row random swap;
  plus the real source-swap. Decision metric: `net_flip = flip_target −
  flip_nontarget` with CI; kill if placebo `net_flip` CI contains 0 in the
  swap direction *or* fully overlaps the swap CI.

### K5 — natural transfer
- Phase-2 criterion: "swap effect ≤ placebo on natural data -> dies." **Valid.
  Instrument choice repaired**: What'sUp is open-ended (weak ground truth);
  replaced by InstaBind-Lite/DSCAM (public; 9,580 deterministic questions,
  boxed source instances; deterministic gold). Corrected metric as for K4,
  plus a preservation gate (`acc_non` must not collapse).

### K6 — cross-model
- Phase-2 criterion: "CCA overlap ~ 0 -> architecture-specific." **Threshold
  unjustified and dims differ across families.**
- **Corrected**: `CC1` from (randomly projected) residual streams on matched
  semantic inputs, permutation significance, plus vector correlation vs
  shuffled baseline; comparison is *descriptive* at pilot power and the
  verdict for the universality claim is behavioral (same intervention spec
  reproduces the flip in the second family) rather than CCA-alone.

### K7 — reduction (recovered from phase2-report.md, not missing)
- Recovery: phase2-report.md's K7 row explicitly specifies
  "Alternative-explanation survival (Q2-E/H) + framing (Q2-G); naming /
  color-histogram / nearest-patch explains the effect -> Q2 dies by
  reduction." **It IS specified in the present file; recovered verbatim.**
- Audit: bundles several rival explanations into one gate. **Corrected** to a
  covariate matrix: each rival (co-occurrence prior for symbols, color
  histogram delta, nearest-patch overlap, spatial-attention proximity, and
  grid/bbox framing) is entered as an alternative model of `flip_target`;
  Q2 dies by reduction if any single rival reproduces the swap CI without the
  activation patch.

### K8 — resources
- Phase-2 criterion: "Colab 16 GB activation cache ≤ 2GB/500 items; overflow
  -> rescope." **Valid; implementation entangled** (cache vs VRAM vs stateless
  recompute). Corrected to measured `torch.cuda.max_memory_allocated` per
  pilot step with a 16 GB budget and a pre-specified rescale ladder (batch 1,
  head sampling, ≤24 probed layers, stateless recompute instead of cache).
  Pre-flight CPU evidence (7.51 GB weights bf16, 1.4-2.8 GB RSS) gives a
  lower bound; T4-class VRAM figures are **REQUIRES RUNTIME TEST**.

---

## 8. Statistical Design

Pre-registered in `<file path="artifacts/phase3/preregistration.md" />`.
Design choices:

- **Q1**: 50 items × 4 conditions (within-item), teacher-forced attention pass
  + greedy correctness pass; bootstrap 95% CIs on per-condition mean of
  `VIG_mass − M/N`; primary contrasts: `long−neutral` (reasoning-specific,
  net of dilution) and `posmatch_short−short` (position).
- **Q2**: 25 synthetic + 25 natural, swap vs 3 placebos; direction is
  predicted by the source image's true binding; `net_flip` with CIs.
- **Equivalence**: TOST with pre-set bound `θ = 0.05` for dilution (K2) and
  `θ(flip) = 0` planes; **no `p > 0.05`-implies-equivalence** anywhere.
- **Honest power note**: the Phase-2 gate (p < 0.001, Δ ≥ 0.05) was set for
  n ≈ 2,000-3,000 from the 2025 pilot; at n = 50 it is underpowered
  (~0.07-0.15 for that effect). The pilot therefore reports CIs +
  standardized differences and treats gate *passes* as confirmatory signals,
  not proof of equivalence, and any "absence of effect" claim is explicitly
  labeled underpowered until the full-sample run.

---

## 9. Runtime QR / Architecture / API Compatibility (public info only)

Verified against public artifacts (config.json read; model card; no physics
inference):

- **Qwen2.5-VL-3B-Instruct**: decoder-only UNIFIED self-attention (no
  cross-attention modules); 36 layers, hidden 2048, 16 heads, 2 KV heads;
  32-layer vision tower (hidden 1280, patch 14, spatial merge 2, temporal
  patch 2); mrope with text/img sections; vocab 151,936 (bf16 weights,
  7.51 GB).
- **API compatibility (transformers 5.17.0, verified in-running on CPU)**:
  `output_attentions` requires `attn_implementation="eager"` (Flash/SDPA
  normally suppress `attentions`); residual capture via
  `model.model.language_model.layers[L].register_forward_pre_hook` verified;
  prompt placeholder is **`<|image_pad|>`**, and vision_start/end tokens are
  NOT added to `input_ids` (1:1 token replacement; attention qlen ==
  input_ids length — an assert in the harness).
- **Gemma-3-4B-it (Q2-A secondary)**: raw `config.json` returns **401
  (GATED)** without auth — a license + token requirement is confirmed. Model
  card (public) confirms multimodal (SigLIP 400M; 896x896 -> 256 soft image
  tokens; 62 layers; mixed local/global). Gating and the 16 GB envelope make
  Gemma a **possible but constrained** Q2-A target; fallbacks are registered
  in the preregistration.

## 10. Pre-Flight Runtime Test (local CPU)

Performed before the pilot, with a downloaded copy of Qwen2.5-VL-3B-Instruct
(7.5 GB; cache verified, config.json read). No GPU available on this machine;
numbers below are CPU-only engineering evidence, labeled as such.

| Check | Result (CPU) |
|-------|--------------|
| Model load | 3.755 B params / 7.51 GB bf16; ~44-66 s; RSS 1.4-2.8 GB (mmap) |
| Prompt prep | `<\|image_pad\|>` placeholder -> 64 image tokens; qlen == input_ids len |
| Attention exposure | `output_attentions` under eager: 36 layers × (1,16,q,k); verified |
| Hidden states | 37 × (1,70,2048) captured |
| Residual hook | `layers[18]` pre-forward hook captures (70,2048); verified |
| Generation | greedy, 32 tokens, **7.4 s/token CPU**; coherent output; stable |
| Forward | 70-token prompt: ~60 s on CPU (dominated by vision/conv path) |

Exploratory (CPU, single short prompt, **not** a result, added for plausibility
only): attention mass on the image block at the final position ≈ 0.29 vs a
uniform-chance share ≈ 0.91 — directionally consistent with A1's "raw
attention underweights vision," but with the corrected K2 metric the pilot
(not this number) decides.

**Smoke pilot (CPU, `--tiny`, n=1, THESIS_TINY truncation)**: the full Q1
pipeline ran end-to-end for all four conditions on one balance-scale item and
wrote checkpoints; `long − neutral` and `posmatch` conditions all completed.
Q2 smoke exposed an answer-space fragility: greedy top-k over the *vocabulary*
rarely lands on a bare symbol token; harness now scores the **8-symbol answer
space directly** and uses a larger glyph font. These changes are mechanical
(F3-class, per the failure taxonomy) and were made *before* any statistical
claim; the smoke rows were deleted so the real GPU run computes all 50 samples
fresh. The smoke numbers themselves are not reportable (n=1, CPU, truncated
traces).

**Runtime verdict**: engineering feasibility **VERIFIED**; the 7.4 s/token CPU
rate alone rules out the 50-sample pilot locally (~many GPU-hours), so all K1-K8
measurements are **REQUIRES RUNTIME TEST** on the user's Colab Pro 16 GB (the
pre-registered harness + instructions are in the artifacts).

## 11. Dataset Verification

| Dataset | Status | Use | Source / license |
|---------|--------|-----|------------------|
| RH-Bench | **VERIFIED public** (HF `LCZZZZ/RH-Bench`, repo `github.com/MLRM-Halu/MLRM-Halu`) | Q1 length-control tooling + reframe evidence | arXiv 2505.21523 (NeurIPS 2025); dataset metadata verified by two sources |
| WhatIfVis (A1, 3,049 items) | **NOT DIRECTLY DOWNLOADABLE** (released as A1-derived; no confirmed public index) | Q1 item pool | Must be **reconstructed** from documented public sources: VLind-Bench + Pixels-versus-Priors + A1's 67 generated balance-scale items; licenses per-source |
| InstaBind-Lite / DSCAM | **VERIFIED public** (`github.com/InstaBind-Lite/InstaBind-Lite`; 524 images / 529 groups / 1,773 source-instance boxes / 9,580 deterministic questions) | Q2 natural transfer (K5) | Public repo; deterministic QA; boxes = clean swap targets |
| SugarCrepe / What'sUp | public (standard benchmarks); SugarCrepe subset (r=0.99) already validated in Phase 2 | Q2 fallback / adjunct | Standard open licenses; re-verification pending fetch |

## 12. Intervention Feasibility Verification

- **C1-style activation swap** (Q2): the paper's mechanism (row-partition
  tokens; 2 rows × 4 columns; non-ordinal glyph sets {&,$,#,@}; predictions
  follow swapped bindings) is reconstructed from paper text. Feasible in the
  harness: residual-input patch at `layers[L]` with token-row indices derived
  from `grid_thw` (16x16 patches -> 8x8 merged tokens; row index settled from
  merged geometry). Patch + capture verified mechanically on CPU. Per-row
  spatial mapping is **RECONSTRUCTION**, marked as such.
- **Natural-object partition (K5)**: InstaBind boxes are converted to vision-token
  subsets from the box→grid mapping; implementation present in the harness
  spec, actual box run REQUIRES RUNTIME.
- **K3 decodability probe**: logistic probe on teacher-forced answer-token
  residual; hidden states verified exposed; probe training is offline.
- **Q2-A (K6)**: Gemma gated (Section 9); behavioral second-family comparison
  implemented as intervention-spec parity; requires a HF token + license on
  the user's Colab and a second 16 GB model swap.

## 13. Statistical Verification (estimation)

- Equivalence machinery (TOST) and CIs implemented in analysis plan; bounds
  pre-set (§8); no equivalence-from-ns anywhere.
- Estimator sanity: `VIG_mass − M/N` need not be in [-1,1] (it is a deviation
  measured in attention-probability units); CI bootstrap is used rather than
  normal-approx due to optional strong per-item skew.
- Power table (Section 8) shows the n=50 pilot can only gate *clear* effects;
  full-sample pass/fail is the Phase-4 scale. Any pilot-level "survive" is a
  *provisional* survive pending the full run.

## 14. Final Kill-Gate Decision Matrix

| Gate | Pilot-state | Status | Basis |
|------|-------------|--------|-------|
| K1 | not run (GPU) | **REQUIRES RUNTIME** | mechanism valid; no measurement |
| K2 | not run (GPU) | **REQUIRES RUNTIME** | criterion corrected; metric operational |
| K3 | not run (GPU) | **REQUIRES RUNTIME** | split to K3a/K3b; harness ready |
| K4 | not run (GPU) | **REQUIRES RUNTIME** | 3 placebos pre-specified |
| K5 | not run (GPU) | **REQUIRES RUNTIME** | InstaBind verified; natural box path present |
| K6 | blocked | **REQUIRES AUTHORIZATION + RUNTIME** | Gemma gated (401); fallbacks registered |
| K7 | not run (GPU) | **REQUIRES RUNTIME** | recovered verbatim + corrected to covariate matrix |
| K8 | partially verified (CPU) | **REQUIRES RUNTIME (GPU figures)** | CPU floor measured; T4-class numbers absent |

No gate measured a pass or fail in this phase; all seven unmeasured gates are
pre-registered and executable on GPU. This is exactly what "ADDITIONAL PHASE 3
TEST REQUIRED" means.

## 15. Final Verdicts (status categories)

- **Q1 — "SURVIVES WITH MODIFICATION" (UNCERTAIN, pending RH-Bench reframe)**
  Basis for not killing: RH-Bench removes the naive novelty claim but Q1's
  three mechanistic sub-claims are unclaimed by any located prior; the K1/K2/K3
  corrected criteria can test them. Basis for not proclaiming: zero GPU
  measurements exist.
- **Q2 — "SURVIVES" (UNCERTAIN, conditional on K4/K5/K7)**: the artifact risk
  is real (C1 partially pre-empts the mechanism in synthetic scenes), so Q2
  lives or dies on natural-image transfer and covariates; nothing measured yet.
- **Canonical thesis — unaffected**: no evidence raised against the canonical
  claim; Q1 (if it survives) would *strengthen* its utilization account.

## 16. Post-Hoc Analyses

None registered. All post-pilot deviations, if any, will be recorded with a
POST-HOC tag in a dated addendum to this file and to the preregistration.

## 17. Next Round of Tests (Phase 4 pilot — list)

1. Colab Pro 16 GB; run `python pilot_harness.py --smoke` (5-item) then full
   `--stage q1` (50×4) and `--stage q2` (25+25), per README in artifacts.
2. First reduce envelopes if `torch.cuda.max_memory_allocated` exceeds budget;
   then RERUN, not reinterpret.
3. Compute the table in Section 14; replay each kill decision on the
   pre-registered rules.
4. If K5 transfers, expand natural set (529 groups) for the intervention
   library claim; if K6 blocked by gating, reroute to fallback model.
5. Re-examine canonical thesis only if K1/K2 show a reasoning-specific effect;
   otherwise confirm Q2 at K4/K5/K7 and report both as dead ends.

## 18. Phase 4 Entry Gate

**DO NOT PROCEED — ADDITIONAL PHASE 3 TEST REQUIRED** (the pre-registered GPU
pilot). Rationale: (i) no knockout measured — every gate is still open; (ii)
four input documents never existed, reducing reporting completeness; (iii) the
only runtime block is GPU availability, which the user can supply; (iv) every
remaining question is small, cheap, and pre-specified. The moment the pilot CSV
lands, the Section 14 table becomes decisive.

---

## Answering the specification's final asks (§32-§33)

- **§32 comparison vs canonical thesis**: with the four missing documents,
  only phase2-report.md anchors the canonical thesis; Q2 is a dependency of it
  (methodology), Q1 is a potential modifier of its utilization mechanism. No
  result yet modifies either.
- **§33 most important question**: "Does making the model reason longer make it
  *visually blinder* by a mechanism RH-Bench and every what-if-utilization
  prior must assume away?" — currently **unanswered**; answerable only by the
  K1/K2 pilot contrasts. This single answer would disambiguate whether the
  canonical thesis's utilization claim needs a length- or dilution correction.
  Every other deliverable this phase (dataset, harness, preregistration,
  corrected gates) exists to enable exactly this answer.