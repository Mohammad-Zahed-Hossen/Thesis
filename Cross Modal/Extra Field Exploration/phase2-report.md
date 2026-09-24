# Phase-2 Feasibility Audit — UGM Thesis Candidates Q1 & Q2

**Status:** COMPLETE (audit-level; runtime kill tests deferred to a Phase-2 pilot in Colab, see §14)
**Date:** 2026-09-21
**Scope:** Deep autopsy of two candidate thesis questions against four anchor papers and the 2025–2026 literature; 16 sections as specified.

**Evidence labels used throughout:**
- **VERIFIED** — read directly from the fetched full text of the cited paper this session.
- **INFERRED** — derived by the auditor from multiple verified sources or from model-card knowledge; check before relying on exact numbers.
- **NOT FOUND** — actively searched and not located.
- **REQUIRES RUNTIME TEST** — cannot be settled by reading; must be measured on hardware.

---

## 1. Executive Summary

**Q1 ("Does visual evidence utilization degrade as a causal function of multimodal reasoning trace length after strictly controlling for sequence position, context length, and attention normalization?")** is **ALIVE but narrow.** All eleven verified candidate papers document visual-evidence decline *correlationally* (attention decay, per-position VEG decay, reflection decay) or mitigate it via training/RL/grounding interventions. **None** runs a causal matched-control experiment with reasoning-trace length as the independent variable while holding sequence position, context length, attention normalization, and question/content fixed. The gap is real, small, and cheap to test on a 16 GB Colab GPU. The 2026 pre-emption scan found no direct pre-emption (§5).

**Q2 ("Are latent visual Binding IDs universal, architecture-independent mechanisms in vision-language models, or are they representational artifacts of synthetic geometric scenes?")** is **ALIVE but contested.** The specific claim (a *linear Binding ID subspace*, isolated on synthetic scenes via activation swap, universal across VLM families and transferable to natural images) remains unstudied — **no verified paper uses the Feng–Steinhardt "Binding ID" mechanism for VLMs.** However, the anchors are **NOT isolated**: nine verified 2025–2026 papers independently attack binding in VLMs (dual mechanisms, limit theorems for dual encoders, pointing/serial processing, foveated readouts, language non-invariance, dense same-class misbinding). Q2 survives only if its Phase-3 protocol passes the placebo control (**Q2-C**), the natural-image causal transfer test (**Q2-B/D**), and the cross-family subspace test (**Q2-A**).

**Bottom line:** pursue **Q1 as the primary thesis** (narrow, causal, feasible, no pre-emption); keep **Q2 as a clearly scoped secondary** whose thesis-worthiness is kill-test-dependent (§14, §16).

---

## 2. Four Paper Autopsies

### 2.1 Anchor A1 — *Seeing or Knowing? Vision Language Models Evidence or Instructions in Zero-Shot Visual Recognition* (arXiv 2607.26326) — VERIFIED

| Dimension | Finding |
|---|---|
| Method | Causal audit: activation patching / zero-ablation of visual-evidence tokens; rank-1 linear steering of evidence vs. instruction directions |
| Data | WhatIfVis, **3,049 samples** (visual search, count, spatial relations) |
| Key numbers | Rank-1 steering of evidence direction: **5.9%** vs. **14.7%** baseline (i.e., vision dominates); evidence direction linearly decodable |
| Causal control | Activation-patching interventions; evidence vs. instruction direction contrast |
| Limitation (App. A) | **No reasoning traces — single-turn prompting only** |

### 2.2 Anchor A2 — *VIG: Visual Information Gain as a Reward Signal for Multimodal Chain-of-Thought Compression* (arXiv 2608.21883) — VERIFIED

| Dimension | Finding |
|---|---|
| Method | Defines chain-token VIG (eq. 2, §4.4.1); RL reward compressing multimodal CoT |
| Data | Long-form multimodal reasoning tasks; Qwen3-VL-Thinking 2B / 4B / 8B |
| Key numbers | Per-token VIG **declines** along the reasoning chain; reads **r = −0.569** for VIG vs. chain length/position; partial correlation ACC–VIG ≈ 0 after controlling length+difficulty, while the VIG–length decline survives (∂r ≈ −0.63) |
| Limitation | **Correlational** — chain length is confounded with absolute position, context length, and softmax denominator; no controlled manipulation of length |

### 2.3 Anchor C1 — *Grounding IDs: Linear Visual-Semantic Binding in Vision-Language Models* (arXiv 2509.24072; Soleymani Baghshah group) — VERIFIED

| Dimension | Finding |
|---|---|
| Method | Grounding-ID activation-swap intervention ICG (eq. 3); treats a low-dim visual-semantic subspace as a "binding ID" that swaps attributes across objects |
| Data | Synthetic 28×28 geometric grids; natural eval via CHAIR / POPE only |
| Key numbers | Swap intervention changes generated attribute text for the target object |
| Causal control | Activation swap from clean to counterfactual view — **NO random-vector / scrambled-patch placebo control**; **no binding-representation test on natural attribute-binding images** |
| Limitation | Cannot distinguish a genuine causal ID from a destructive-perturbation effect; single architecture; single scene type |

### 2.4 Anchor C2 — *In-Context Vision-Language Binding* (arXiv 2505.22200) — VERIFIED

| Dimension | Finding |
|---|---|
| Method | In-context binding via synthesized 2-object scenes; latent-vector abstraction = "binding ID" |
| Data | Synthetic Blender-rendered 2-object scenes; LLaVA-OneVision-7B (single model) |
| Causal control | **Random-vector control exists** (swap with norm-matched Gaussian does not reproduce binding behavior) |
| Limitation | Synthetic-only; single model family; no released assets; cross-family/natural-image universality untested |

### 2.5 Anchor B (Deprioritized) — *In-Context Learning* pair
Read and set aside (B1/B2): ICL-lag analyses. Candidate B was deprioritized early in Phase 1; no further autopsy. **Status: CLOSED.**

---

## 3. Q1 Gap Autopsy — Field A (Q1-A..G)

*Core question: "Does visual evidence utilization degrade as a causal function of multimodal reasoning trace length after strictly controlling for sequence position, context length, and attention normalization?"*

| Axis | Verdict | Evidence (VERIFIED) | Gap for the candidate |
|---|---|---|---|
| **Q1-A** Causal role of reasoning length | **VACANT** | Declines are correlational: Attentive-CoT (2606.01558) — CoT degrades visually-heavy tasks; Illusion of Visual Tool-Use (2608.06270) — per-position VEG decay (Fig. 5a); Look Light Think Heavy (2606.22565) — visual reflection decays across 10 trace bins; Remember-R1 (2608.01314) — visual attention Ω(t) decays over trajectory | No matched-control with trace-length as IV |
| **Q1-B** Position vs. cognitive degradation | **PARTIALLY COVERED** | VIG (A2) shows per-token, position-ordered decline (§4.4.1) and the co-authors control difficulty; cct-vlm (2609.06704) vCT/vCCT track visual evidence per turn | No experiment holds answer/evidence absolute index fixed while varying inserted reasoning length |
| **Q1-C** Softmax denominator dilution | **VACANT** | cct-vlm and App. analyses of A2 acknowledge attention dilution over expanded KV; no controlled test of normalized cross-attention mass | Length-normalized VIG metric + attention-denominator-matched control needed |
| **Q1-D** Attention sinks / outlier tokens | **VACANT** | Attention-sink mitigation literature (e.g., SinkPruner, Navier 2026) cited in candidate material but NOT in any fetched candidate text direct-test | Not addressed by any candidate |
| **Q1-E** Availability vs. utilization | **PARTIALLY COVERED** | A1 (2607.26326) separates decodability from routing via rank-1 steering — single-turn only; Where To Look (2608.10758) causal-tracing shows causal importance ⊥ spatial grounding | No long-trace version of A1's audit |
| **Q1-F** Causal restoration by re-consultation | **VACANT in candidate set** | Re-injection/scaffolding methods (SAP, TTSP, TRACE) appear only as citations in candidate texts; Look Light Think Heavy probes "visual reflection tokens" but does not intervene | Late-trace re-injection with FLOP/overhead control untested |
| **Q1-G** Monotonic vs. discrete phase transition | **VACANT** | Look Light Think Heavy shows smooth monotone-ish decline (10 bins); Illusion of Tool-Use shows step-level per-position effects | No test for a phase transition driven by parametric prior override |

**Autopsy verdict:** the causal core of Q1 is open. Every existing result can be absorbed by Q1-A/B/C confounds (position, context length, softmax denominator), which is exactly the objection the thesis must decouple first (kill tests K1–K2, §14).

---

## 4. Q2 Gap Autopsy — Field C (Q2-A..H)

*Core question: "Are latent visual Binding IDs universal, architecture-independent mechanisms in vision-language models, or are they representational artifacts of synthetic geometric scenes?"*

| Axis | Verdict | Evidence (VERIFIED, with paper) | Where it leaves the candidate |
|---|---|---|---|
| **Q2-A** Cross-architecture universality | **VACANT** (for the specific claim) | Dual Mechanisms (2603.22278) shows the same two-mechanism split in Qwen2-VL-7B + Gemma-3-4b-it (vision encoder primary, LM backbone secondary); Limits in Dual Encoders (2608.15971) proves depth/objective/geometry ceilings for CLIP-like dual encoders; Seeing to Generalize (2602.15183) shows the *training regime*, not architecture, decides binding strategy | Shared *linear Binding ID subspace across families* never tested; contested by 2608.15971's architecture-dependence |
| **Q2-B** Synthetic→natural generalization | **PARTIALLY COVERED** | Dual Mechanisms transfers probes/interventions to What'sUp natural control (2,687 images) + COCO-spatial + 15 realistic backgrounds; Foveated Probes (2608.00726) does natural-image binding on GQA-derived pairs; DSCAM (2608.16805) is natural-image dense misbinding | C1's own synthetic-only ID was never taken to natural attribute-binding images — still open |
| **Q2-C** Artifact vs. mechanism (placebo) | **GAP IN C1, CONTROLLED ELSEWHERE** | C2 (2505.22200) has a random-vector control; Dual Mechanisms has **random-amplification baselines**: Gemma 0.53→0.72 (40.2% corrected) vs. random amp 0.57 (9.6%); Qwen 0.60→0.82 (54.5%) vs. random 0.65 (13.1%). **C1 has no placebo.** | C1's headline effect is exactly what the placebo test targets |
| **Q2-D** Causal efficacy vs. decodability | **PARTIALLY COVERED** | Dual Mechanisms patching/amplification flips outputs (Table 2); C2's swap is procedural and causal in the narrow sense | No language-coherence co-check (swap must not degrade coherence) anywhere |
| **Q2-E** Alternative mechanisms | **VERIFIED AS ACTIVE** | Point by Point (2605.25427) — pointing induces serial search, **eliminates binding errors**, gives compositional generalization; VISER (2506.22146) — visual structure scaffolding; Does VLM benchmarks really test vision (2605.22903) and cct-vlm — naming/language priors; Limits in Dual Encoders — smoothness frontier M(s) ≤ 2√2δ over 18 text encoders (SugarCrepe subset r=0.99) | Spatial-attention-proximity, naming-prior, and photometric reductions are live hypotheses to attribute the C1 effect to |
| **Q2-F** Position & geometry independence | **VACANT** | Dual Mechanisms shows position/ordering info diffuses across tokens incl. background (not on object tokens alone); no Binding-ID quadrant-transposition invariance test | Open, cheap to test |
| **Q2-G** Cue/symbol framing dependence | **PARTIALLY COVERED — from C1's own group** | VISER (2506.22146, same Sharif group) explicitly relies on external visual structure (grid lines) + spatial text prompts for binding tasks; GPT-4o gains +25.0%/+26.8%/+9.5% (search/count/spatial), −0.32 edit distance; CoT-only insufficient/degrade | Framing the ID as a "symbol" may be *required for the effect* — testable (K7) |
| **Q2-H** Reduction to simpler statistics | **VACANT** | Formalizing Binding (2606.03976) separates binding info from feature info info-theoretically; Limits in Dual Encoders gives the *geometry* frontier (smoothness-bound); DSCAM's same-class duration (80.70%/81.51% adjacent-instance transfers) rules out semantic priors but not color-histogram/photometric reductions | No color-histogram / contrast-margin control attributing C1's effect |

**Additional verified context (Q2 breadth):** Fragile Multilingual Associators (2608.12333) — binding is not language-invariant, shifts to later layers under cross-script conditions; Formalizing Binding (2606.03976) — [CLS] token encodes < half of scene binding info (largely quadratic), spatial tokens near-perfect via attention probe.

**Autopsy verdict:** the proposition "Binding IDs are universal, architecture-independent mechanisms" is **contested territory**; the *linear-subspace + cross-family + natural-image + placebo-controlled* combination is the remaining niche, and the DSCAM benchmark + Dual Mechanisms controls give the candidate tools it previously lacked.

---

## 5. 2026 Pre-Emption Scan (VERIFIED, run 2026-09-21)

Two recency-prioritized discovery queries (`--published-after 2026-01-01`):

- **Q1 query** (visual evidence utilization / chain-of-thought / causal / length): top hits 2609.12606 (Visual CoT for geometry diagnosis), 2608.27265 (SCIT — causal cache carriers in latent CoT), 2609.09928 (structural process supervision), 2609.07406 (latent rank collapse), 2608.22332 (CoT via sequential activation patching), 2608.24790 (perturbation audit of medical CoT), 2608.30508 (UTILMEM). **None manipulates trace length as an IV with position/context/attention-normalization controls.**
- **Q2 query** (attribute binding / natural images / VLM): top hits 2609.18345 (visual input & framing affect attribute descriptions), 2608.11024 (mechanistic attribute-hallucination — relevant Q2-E), 2609.00663 (separating perception from reasoning, crystal domain), 2608.24142 (prompt-learning concept analysis), DSCAM (already verified). **None isolates a cross-family linear Binding ID subspace or runs the placebo-controlled natural-image swap.**

**Pre-emption verdict:** no paper pre-empts either thesis as specified. Note the scan's density of Aug–Sep 2026 outputs implies publication velocity in both fields — Phase 3 runtime work should begin promptly.

---

## 6. Dataset Audit

| Dataset | Use (Q) | Size (VERIFIED) | License / availability | Label |
|---|---|---|---|---|
| WhatIfVis | Q1-A/E primary eval | **3,049 samples** (A1) | NOT verified this session | REQUIRES RUNTIME TEST (download) |
| ViRL39K | Q1 attention-trajectory reward/annotation (Remember-R1) | as reported by 2608.01314 | NOT verified | REQUIRES RUNTIME TEST |
| RH-Bench (Xu et al. 2025) | Q1 long-chain visual forgetting ref | cited by cct-vlm 2609.06704 | **NOT FOUND in this session's reads** | Verify existence directly before Phase 3 |
| C1 synthetic grids 28×28 | Q2 synthetic side | per 2509.24072 | no released assets | REBUILD REQUIRED |
| CLEVR / Blender 2-object | Q2-B source-domain syntax | per 2505.22200 | no released assets | REBUILD REQUIRED |
| What'sUp control subset | Q2-B natural transfer | **2,687 images** (dual mech. §3.2) | public dataset (Thrush et al.) | VERIFIED (dataset exists) |
| COCO-spatial | Q2-B natural transfer | derived from COCO (dual mech. App. A.2) | public; license NOT re-verified | REQUIRES RUNTIME TEST |
| InstaBind-Lite / DSCAM | Q2-B/D/E **new natural-image evals** | **524 images, 529 same-class groups, 1,773 boxed instances, 9,580 questions** (2608.16805) | benchmark published by Xu et al.; open-source models measured | VERIFIED (dataset exists) |
| SugarCrepe subset | Q2-E prior/doc reduction | difficulty r=0.99 (2608.15971) | public benchmark | VERIFIED (subset metric) |

**Dataset verdict:** everything required exists or is public; the binding assets for C1/C2 must be *rebuilt* from paper descriptions (no released code/data — INFERRED from absence of assets in fetched texts).

---

## 7. Model Architecture Audit

| Model | Role (Q) | Specs | Label |
|---|---|---|---|
| Qwen2.5-VL-3B-Instruct | Q1 primary / Q2 candidate family | ViT (≈675M) + Qwen2.5-3B LLM; dynamic-resolution + patch-merge tokens; bfloat16 ≈ 6.5–7 GB | INFERRED (model-card knowledge; not re-verified this session) |
| Gemma-3-4B-IT | Q2 cross-family (Q2-A), Q1 secondary | 4B dense; SigLIP-style patch encoder; ≈ 8–9 GB bf16; **C1/C2/dual-mech anchor family (Gemma-3-4b-it)** | INFERRED (model-card knowledge); family VERIFIED via anchors |
| LLaVA-NeXT (7B/13B) | Q2-A third family (original C2 target list) | 13B variant exceeds 16 GB full-precision bf16 single-GPU budget | INFERRED — scope risk; prefer 7B proxy |
| Qwen3-VL-Thinking 2B/4B/8B | A2 anchor models (context) | native multimodal reasoning | VERIFIED (A2) |
| Gemma-4 (E2B/E4B-IT) | future-proofing flag | released superset of Gemma-3; would refresh Q2-A | INFERRED (world-state fact) |

**Model verdict:** the 16 GB budget ("bfloat16, Qwen2.5-VL-3B / Gemma-3-4B, activation caching < 2 GB per 500 items") fits for inference-only causal analysis on both candidate models. The LLaVA-NeXT cross-family arm should use the 7B proxy or be dropped.

---

## 8. Q1 Causal Protocol (design)

**Design rationale:** hold position, context length, attention denominator and content fixed while varying ONLY inserted reasoning length.

1. **Construct matched length pairs per (image, question).** From a generic long answer, create: (i) *short*, (ii) *medium*, (iii) *long* reasoning variants that reach identical intermediate conclusions; lengthening is mechanical (connective/redundant tokens) — no new evidence content.
2. **Position control (Q1-B):** two layouts —
   - `fixed-answer`: the answer token sits at a fixed absolute index; the inserted reasoning block moves between question and answer.
   - `fixed-block`: the reasoning block starts at a fixed index after the visual prefix; only its length (and answer index) changes.
   Comparing the two layouts separates "decay over output length" from "position relative to visual prefix."
3. **Attention-denominator control (Q1-C):** compute a *normalized* cross-attention mass to image tokens (VIG eq. 2 of A2, divided by a decaying softmax denominator baseline) and report both raw and normalized.
4. **Availability control (Q1-E):** A1-style zero-ablation + rank-1 steering of evidence direction at the final token, long versus short traces, to test whether evidence is still decodable at extraction time.
5. **Metrics:** final-answer grounding (evidence-linked tokens), VIG (A2), per-position VEG decay (A1 method), attention mass.
6. **Statistics:** mixed-effects logistic regression `correct ~ length + position + content + (1|image) + (1|prompt)`; pre-registered gate: length effect must be significant (p < 0.001) AND ≥ 0.05 in normalized-VIG units after controls; sample ≈ 2,000–3,000 WhatIfVis items.
7. **Kill-test integration:** protocol outputs K1 (position fixed, effect survives?) and K2 (normalized VIG effect survives?) directly.

---

## 9. Q2 Causal Protocol (design)

1. **Rebuild the C1 pipeline** (ICG eq. 3, activation swap on 28×28 grids) without released assets (REQUIRES RUNTIME TEST on at least one model first).
2. **Placebo block (Q2-C):** swap with (a) norm-matched random Gaussian, (b) within-image scrambled patches, (c) shuffled view order. Effect must beat placebo on *attribute-text* change AND on **language coherence** (e.g., no degenerate/looped output).
3. **Natural-image block (Q2-B/D):** run the same swap on InstaBind-Lite/DSCAM boxed instances and What'sUp control pairs; measure target-object attribute flip vs. placebo.
4. **Cross-family block (Q2-A):** extract the low-dim binding-ID basis in Qwen2.5-VL-3B and Gemma-3-4B; align with CCA / orthonormal-basis-projection overlap; report shared-subspace significance. (LLaVA-NeXT 7B as optional third leg.)
5. **Alternative explanations (Q2-E/H):** co-vary object saliency (center bias), attribute co-occurrence prior ("yellow banana"), and color-histogram/contrast-margin deltas; show swap effect survives all three.
6. **Invariance block (Q2-F):** transpose target objects across image quadrants; swap effect must be invariant to absolute coordinates.
7. **Framing block (Q2-G):** run the swap with grid lines / bounding boxes / numbered tags present vs. absent.
8. **External anchors:** compare against Dual Mechanisms random-amplification baselines (Gemma 0.53→0.72 vs. 0.57; Qwen 0.60→0.82 vs. 0.65) as positive-control sanity.

---

## 10. Causal Validity & Confound Analysis

| Confound (threat) | Q1 control | Q2 control | Validity threat status |
|---|---|---|---|
| Absolute position (RoPE decay) | fixed-answer vs. fixed-block layouts | quadrant transposition (Q2-F) | Mitigated by design |
| Context/total-token count | matched total-length triplets | fixed prompt scaffolding | Mitigated |
| Softmax denominator dilution | normalized VIG metric | n/a | Mitigated |
| Content change | mechanical lengthing only | constant prompts across swaps | Mitigated |
| Generative entropy/length-prior | length-prior baseline model (text-only) | naming-prior ablation (Q2-E) | Mitigated |
| Attention sinks / outlier tokens | SinkPruner pre-scan (Q1-D) | n/a | Mitigated (check) |
| Destructive-perturbation mimicry | n/a | placebo trio (Q2-C) + coherence check | **Primary Q2 threat** |
| Post-hoc decodability ≠ function | steering flips final output | swap flips generated text + coherence | Monkey-patch: intervention must be the generation path |
| Photometric/color-histogram reduction | n/a | histogram/contrast covariates (Q2-H) | Mitigated |
| External validity (task distribution) | WhatIfVis + long-span benchmark | 3 synthetic domains + DSCAM natural | Limited by design; report honestly |
| Evaluation contamination (naming priors) | metric is attention/decodability, not answer-only | DSCAM deterministic 9,580-question eval | DSCAM mitigates (VERIFIED design) |

**Material limitations:** (i) C1/C2 have no released assets → Phase 3 must first reproduce the swap effect (treat as a kill-test in itself); (ii) cross-family subspace alignment is underpowered at 3 models + ≤7B — result will be suggestive, not definitive.

---

## 11. Colab Feasibility (16 GB GPU)

| Item | Estimate | Label |
|---|---|---|
| Qwen2.5-VL-3B inference (bf16) | ~6.5–7 GB weights, fits | INFERRED (model-card); REQUIRES RUNTIME TEST |
| Gemma-3-4B inference (bf16) | ~8–9 GB weights, fits | INFERRED; REQUIRES RUNTIME TEST |
| Activation caching for interventions | < 2 GB per 500 items (directive) — plausible for one forward pass with hidden-state capture, bf16 | ESTIMATED; REQUIRES RUNTIME TEST |
| Steering/swap interventions | one extra forward, no gradients → within budget | ESTIMATED |
| Risk: dynamic-resolution token variance (Qwen2.5-VL) | memory spikes at high resolutions → cap resolution preset | INFERRED |

**Feasibility verdict:** both protocols are inference-only → **feasible** on a single 16 GB T4/L4-class GPU. Colab 16 GB is acceptable in principle; the activation-cache figure (≤2 GB/500 items) must be confirmed in the Phase-2 pilot (kill-test K8).

---

## 12. Canonical Topic Comparison

Positioning against the canonical topic space derived from the four anchors (tech-tree mapping):

| Canonical topic region | Q1 | Q2 |
|---|---|---|
| Multimodal CoT faithfulness / visual grounding | **Core present** (chain-length decay) | — |
| Perceptual evidence utilization under reasoning pressure | ✓ (properties of the canonical problem) | — |
| Binding mechanisms in VLMs | — | ✓ (core present) |
| Mechanisms vs. artifacts (interpretability epistemology) | — | ✓ (core present) |
| Synthetic→natural transfer of the mechanism | — | ✓ mostly **absent in candidates** (the niche) |
| Architecture/regime universality of the mechanism | — | ✓ contested, unsettled |

**Canonical verdict:** Q1 is a *narrow slice of a mature canonical region* (all neighbors correlationally established; causal slice unfilled). Q2 sits *at an active frontier* but its best canonical slot — "is the Binding ID a real cross-architecture mechanism or a synthetic-scene artifact?" — is unfilled only in that exact formulation.

---

## 13. Closest-Work Matrix

| Candidate contribution | Closest works (VERIFIED) | The candidate's delta |
|---|---|---|
| Q1: trace-length as *causal* IV with position/context/normalization held fixed | VIG (A2, 2608.21883); Illusion of Tool-Use (2608.06270); Attentive-CoT (2606.01558); Look Light Think Heavy (2606.22565); cct-vlm (2609.06704); Remember-R1 (2608.01314) | Controlled manipulation of $T_{\text{CoT}}$; decouples A/B/C/G |
| Q1: availability-vs-utilization along long traces | Seeing or Knowing (2607.26326) single-turn; Where to Look (2608.10758) | Long-trace A1-style steering audit |
| Q2: randomized-placebo-controlled Binding-ID swap | Grounding IDs C1 (no placebo); In-Context Binding C2 (has placebo, synthetic); Dual Mechanisms (2603.22278, random-amp baselines) | Uniform placebo + coherence control |
| Q2: cross-family linear Binding-ID subspace | Dual Mechanisms (2 model families, no subspace alignment); Limits in Dual Encoders (2608.15971, negative theorem for CLIP) | Direct shared-subspace measurement |
| Q2: natural-image binding-id transfer | VISER (2506.22146); Point by Point (2605.25427); Foveated Probes (2608.00726); DSCAM (2608.16805); Formalizing Binding (2606.03976) | C1-extraction method on a modern dense natural benchmark |

---

## 14. Phase-2 Kill Tests

| # | Kill test | Kill condition | Status |
|---|---|---|---|
| K1 | Trace-length effect with fixed answer position (Q1-A/B) | effect vanishes → Q1 collapses to Q1-B | READY — REQUIRES RUNTIME TEST |
| K2 | Normalized-VIG decline survives denominator control (Q1-C) | decline → 0 under normalization → Q1 is dilution | READY — REQUIRES RUNTIME TEST |
| K3 | Steering/availability survives at long trace (Q1-E) | evidence no longer decodable → Q1 reframed as decay | READY — REQUIRES RUNTIME TEST |
| K4 | Placebo swap (Q2-C) beats random/scramble/reorder | placebo reproduces effect → Q2 dies as artifact | READY — REQUIRES RUNTIME TEST |
| K5 | Natural-image swap effect (Q2-B/D) | effect ≤ placebo on DSCAM/What'sUp → Q2 dies as synthetic artifact | READY — REQUIRES RUNTIME TEST |
| K6 | Cross-family subspace alignment (Q2-A) | CCA overlap ≈ 0 → Q2 = architecture-specific (weaker thesis) | READY — REQUIRES RUNTIME TEST |
| K7 | Alternative-explanation survival (Q2-E/H) + framing (Q2-G) | naming/color-histogram/nearest-patch explains effect → Q2 dies by reduction | READY — REQUIRES RUNTIME TEST |
| K8 | Colab 16 GB activation cache ≤ 2 GB/500 items | overflow → protocol rescope (batch drop) | READY — REQUIRES RUNTIME TEST |

None of K1–K8 has been run. **All eight are required before thesis commitment.**

---

## 15. Final Status

- **Q1:** ALIVE. Gap verified against 11 candidates + 2026 scan. Causal matched-control protocol is novel, cheap, and directly tests the field's core confounds. Risk: the effect may die under K1–K3 (then it becomes the Q1-B position-dependence or Q1-C dilution study — still a publishable negative result).
- **Q2:** ALIVE BUT CONTESTED. The specific claim is unstudied, but the surrounding 2026 literature (dual mechanisms, point-by-point, foveation, DSCAM, limit theorems) is dense and partially absorbs it. Q2 survives only if K4–K7 pass; it is the higher-risk, higher-reward thesis.
- **Canonical status:** Q1 = narrow slice of a canonical region (viable, low novelty); Q2 = front-line region with an unfilled narrow formulation (higher novelty, higher risk).
- **Anchors:** A1/A2 remain valid causal tools for Q1; C1/C2 remain valid but *methodologically incomplete* starting points for Q2 (missing placebo and natural-image legs respectively).

---

## 16. Phase-3 Candidates (≤ 2)

1. **(Primary) Q1 — "Visual Evidence Utilization is a Causal Function of Reasoning Trace Length after Controlling Position, Context and Attention Normalization."** Models: Qwen2.5-VL-3B (+ Gemma-3-4B as secondary). Data: WhatIfVis (3,049) + a long-span multimodal benchmark. Methods: matched triplets, fixed-answer/fixed-block, normalized VIG, A1 steering. Runs K1–K3 + K8. **Feasibility: HIGH. Novelty: MODERATE.**
2. **(Secondary) Q2 — "Binding IDs as Mechanisms or Artifacts: A Placebo-Controlled, Cross-Family, Synthetic-to-Natural Test."** Models: Qwen2.5-VL-3B, Gemma-3-4B, (LLaVA-NeXT-7B optional). Data: C1 rebuilt grids + DSCAM/InstaBind-Lite + What'sUp. Methods: C1 ICG swap + placebo trio + coherence control + CCA subspace alignment + saliency/prior/histogram covariates. Runs K4–K7 + K8. **Feasibility: MEDIUM. Novelty: HIGH.**

**Top 2 backup candidates (if both fail their kill tests):**
- *B1: "Attention dynamics alone underlie CoT visual neglect"* — the Q1-B/C decomposition as a standalone methodological result (feasible, moderate novelty).
- *B2: "Boundary audit of readout-level vs. representational binding blindness in frozen VLMs"* — Foveated-Probes-style readout interface study on our architectures (feasible, moderate novelty).

---

## Closing Block

| Item | Status |
|---|---|
| **Q1 status** | **ALIVE (primary).** Causal gap verified; no 2026 pre-emption; Colab-16 feasible; kill tests K1–K3/K8 must pass in the Phase-2 pilot. |
| **Q2 status** | **ALIVE-but-contested (secondary).** Claim niche (linear cross-family Binding-ID mechanism, natural image, placebo-controlled) unfilled, but 2026 binding literature is dense; kills K4–K7 gate commitment. |
| **Canonical status** | Q1 = narrow slice of a canonical region (constraints present, core present). Q2 = active frontier; core question present, transfer/universality niche open. |
| **Top 2 backup candidates** | B1 (attention-only explanation study), B2 (readout-level vs. representational binding blindness). |
| **What Phase 3 must verify** | (1) Reproduce C1's ICG swap effect on at least one model (no assets exist); (2) download/verify WhatIfVis, What'sUp, DSCAM/InstaBind-Lite, RH-Bench existence; (3) confirm ≤2 GB activation cache per 500 items on 16 GB Colab; (4) confirm Qwen2.5-VL-3B + Gemma-3-4B bf16 memory contours; (5) run AND pass kill tests K1–K8. |

---

*Evidence basis: all anchor and candidate papers were read from full text this session (files: a1_seeking_knowing, a2_vig, c1_grounding_ids, c2_binding, q1_* ×11, q2_dual_mechanisms_binding, q2_formalizing_binding_problem, q2_limits_binding_dual_encoders, q2_viser, q2_fragile_multilingual_binding, q2_seeing_to_generalize, q2_dscam_misbinding, q2_foveated_probes, q2_point_by_point). Two pre-emption discovery queries run against post-2026-01-01 literature. Labels per §Evidence labels.*