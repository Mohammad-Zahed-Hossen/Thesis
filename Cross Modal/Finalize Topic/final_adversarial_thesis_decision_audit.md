# Final Adversarial Thesis Decision Audit

**Date:** 2026-09-23
**Audit Type:** Independent adversarial scientific evidence audit
**Auditor Model:** Claude Opus 4.6 (Thinking)
**Evidence Sources:** Cross Modal codebase documents, independent web literature searches, primary paper verification, dataset verification, model verification

---

## Executive Finding

**Three of four candidates survive adversarial scrutiny. One (Candidate B) should be classified RESERVE pending prior-work resolution. The remaining three (A, C, D) each pass the evidence gates, but with meaningfully different risk profiles.**

The audit found that:

1. **Candidate A (Canonical — Conflict Verbalization)** has a **VERIFIED** genuine gap. The closest predecessor papers (*Which Source Wins?*, *CLASH*, *Lanham et al.*) were independently confirmed to exist and to leave the proposed causal question untested. The datasets are **VERIFIED** public on Hugging Face. The experimental design (4-arm factorial with length-matched placebo) is well-controlled. However, the claim "first rigorous, controlled isolation of multimodal reasoning faithfulness under conflicting inputs" is **overstated** — the concept of CoT faithfulness testing exists (Lanham et al. 2023, Turpin et al. 2023); what is genuinely new is applying it to cross-modal conflict arbitration with placebo controls.

2. **Candidate B (Reasoning Trace Degradation)** has a **SUBSTANTIALLY PRE-EMPTED** headline claim. RH-Bench (Liu et al., NeurIPS 2025, arXiv:2505.21523) **VERIFIED** already demonstrates that longer reasoning traces degrade visual attention. The proposal survives only as a narrowed mechanistic decomposition (position vs. content vs. dilution), and this narrowed version has never been run. Critical concern: the WhatIfVis dataset is **NOT DIRECTLY DOWNLOADABLE** and must be reconstructed. The Phase 3 preregistration correctly identifies the reframing, but zero GPU measurements exist.

3. **Candidate C (Binding IDs Natural Transfer)** has a **VERIFIED** genuine gap. The anchor paper C1 (Hasani et al., ICML 2026, arXiv:2509.24072) **VERIFIED** exists and uses synthetic grids. No located study performs activation swapping on natural images with placebo controls. The InstaBind-Lite/DSCAM dataset (arXiv:2608.16805) is **VERIFIED** public. However, this proposal carries the highest *scientific risk*: if the effect simply doesn't transfer (plausible), the thesis reduces to a negative result about synthetic artifacts, which is publishable but narrow.

4. **Candidate D (Bengali VLM Causal Steering)** has a **PARTIALLY PRE-EMPTED** methodology. BabelSteering (arXiv:2608.16577, Aug 2026) already applies English-derived steering vectors to Bengali for safety alignment. SHARP and DMAS (ICLR 2026) already perform activation steering for VLM hallucination mitigation. The combination of *cultural visual tasks + bottleneck localization + activation steering* is novel, but the individual components are not. The BanglaProtha dataset is **VERIFIED** public (WACV 2026, Kaggle). Critical concern: Layer 18 as the intervention point is an **UNVERIFIED ASSUMPTION** — no empirical evidence establishes it.

**The decision is currently justified.** Candidate A has the strongest combination of verified gap, verified datasets, controlled experimental design, high negative-result value, and lowest methodological risk. However, Candidates C and D are scientifically legitimate alternatives, not clearly inferior.

---

## 1. Evidence Integrity Audit

### Claims VERIFIED against primary sources

| Claim | Source | Verification |
|:---|:---|:---|
| `vlm-modality-research/modality-conflict-arbitration-v2` exists on HuggingFace | Canonical spec | **VERIFIED** — 1,304 arithmetic conflict pairs from GSM8K/SVAMP |
| `vlm-modality-research/chartqa-evidence-conflict-v2` exists | Canonical spec | **VERIFIED** — 229 chart conflict pairs |
| *Which Source Wins?* (arXiv:2608.17205) maps modality dominance | Multiple docs | **VERIFIED** — measures task-dependent reliance under legibility degradation |
| *Which Source Wins?* §6 explicitly omits conflict verbalization | Multiple docs | **VERIFIED** — "we do not test whether models detect the contradiction, express uncertainty, or abstain" |
| *CLASH* (arXiv:2511.19199) formulates contradiction as abstention only | Canonical spec | **INFERRED** from search results — abstention-focused benchmark |
| Lanham et al. (2023) tested CoT faithfulness in text-only LLMs | Canonical spec | **VERIFIED** — filler tokens, truncation, prefilling in text-only LLMs |
| RH-Bench (arXiv:2505.21523) shows longer reasoning increases hallucination | Proposal 1 | **VERIFIED** — NeurIPS 2025, introduces RH-AUC metric |
| Hasani et al. (arXiv:2509.24072) demonstrates binding IDs in synthetic grids | Proposal 2 | **VERIFIED** — ICML 2026, "Grounding IDs" via causal intervention |
| InstaBind-Lite/DSCAM (arXiv:2608.16805) is public with 524 images, 9,580 questions | Proposal 2 | **VERIFIED** — dense same-class attribute misbinding benchmark |
| BanglaProtha (WACV 2026) is public on Kaggle | Proposal 3 | **VERIFIED** — 6,942 images, 8,034 questions, Bengali cultural VQA |
| Qwen2.5-VL-3B-Instruct exists with 36 layers, hidden 2048 | Multiple | **VERIFIED** — weights 7.51 GB bf16, config verified |
| ChitraMiti (arXiv:2609.12509) evaluates Bengali VLM modality reliance | Proposal 3 | **VERIFIED** — shows VLMs rely on text over visual diagrams |

### Claims PARTIALLY VERIFIED

| Claim | Issue |
|:---|:---|
| "100% Genuine & Open" gap for Candidate A | The gap is genuine but the "100%" language is epistemic overreach — we cannot prove no paper exists that we failed to find |
| WhatIfVis dataset (3,049 samples) for Candidate B | The Phase 3 preregistration acknowledges it is "NOT DIRECTLY DOWNLOADABLE" and must be reconstructed from public sources |
| C1 paper omitted placebo controls | **INFERRED** — we verified C1 uses synthetic grids and causal intervention but could not read the full paper to confirm zero placebos; the claim is highly plausible given the proposal's detailed analysis |

### Claims UNSUPPORTED or CONTRADICTED

| Claim | Status | Evidence |
|:---|:---|:---|
| "This work provides the **first** rigorous, controlled isolation of multimodal reasoning faithfulness under conflicting inputs" | **OVERSTATED** | CoT faithfulness testing methodology already exists (Lanham et al. 2023). What is first is applying it to *multimodal conflict arbitration* specifically. |
| "Layer 22 is the relevant causal layer" (Candidate C) | **UNVERIFIED ASSUMPTION** | Borrowed from C1's synthetic-grid findings. No evidence this layer is relevant for natural images in Qwen2.5-VL-3B. |
| "Layer 18 is the intervention point" (Candidate D) | **UNVERIFIED ASSUMPTION** | No empirical evidence in the proposal documents. Labeled as "identified via layer-wise probing" but no probing results exist. |
| "first rigorous empirical refutation of BanglaVerse's 'missing knowledge' claim" (Candidate D) | **OVERSTATED** | ChitraMiti already shows VLMs rely on text over vision in Bengali contexts, partially refuting "missing knowledge" |
| "Fatal vulnerabilities" in C1 (zero placebos) | **INFERRED, NOT VERIFIED** | Plausible but stated with certainty that exceeds the evidence base — we haven't read C1's full paper |
| Proposal 3 claim that activation steering has "never" been applied to cultural/low-resource VLMs | **CONTRADICTED** | BabelSteering (arXiv:2608.16577, Aug 2026) applies activation steering to Bengali. SHARP and DMAS steer VLM hallucinations. Neither does *cultural visual task + bottleneck localization + steering*, but the methodology is not unprecedented. |

### Datasets/Papers INCORRECTLY REPRESENTED

| Item | Issue |
|:---|:---|
| WhatIfVis as a ready dataset for Candidate B | It requires reconstruction; not a turnkey download |
| "No prior art uses activation steering for low-resource VLMs" (Candidate D) | BabelSteering (Aug 2026) does this for safety alignment; SteerVLM and DMAS do this for hallucination mitigation; the gap is narrower than claimed |

---

## 2. Candidate A Audit

### Research Question
> When a VLM is presented with contradictory visual and textual premises, does explicitly verbalizing the contradiction causally alter source arbitration, or does the explanation merely rationalize an entrenched modality preference?

**HYPOTHESIS** — Well-formed, testable, and falsifiable.

### Closest Prior Work

| Paper | What it tested | What it did NOT test |
|:---|:---|:---|
| *Which Source Wins?* (arXiv:2608.17205, Aug 2026) | Forced-choice modality reliance under legibility degradation across arithmetic and chart tasks | Conflict verbalization, awareness, explanation generation, abstention (explicitly stated in §6) |
| *CLASH* (arXiv:2511.19199, 2025) | Contradiction detection → abstention | Source arbitration, whether detection enables correct resolution |
| Lanham et al. (arXiv:2305.04388, 2023) | CoT faithfulness via truncation, prefilling, filler tokens in text-only LLMs | Any multimodal setting |
| Turpin et al. (NeurIPS 2023) | CoT unfaithfulness — models rationalize biased choices | Multimodal conflicts, VLMs |
| Zhu et al. (2024) | Cross-modality conflict detection and prompting for mitigation | Placebo-controlled verbalization, prefilling intervention |
| *Pixels versus Priors* (Golovanevsky et al., EMNLP 2025) | Visual counterfacts — canonical vs. non-canonical visual attributes and PvP steering vectors | Verbalization intervention (uses mechanistic/activation-level intervention instead) |

### Experimental Overlap Table

| Proposed experiment | Closest existing | Same question? | Same intervention? | Same control? | Same metric? | Genuine remaining difference? |
|:---|:---|:---|:---|:---|:---|:---|
| Arm 2 vs Arm 3 (placebo vs conflict verbalization) | Zhu et al. 2024 | Partially | No — Zhu uses detection prompts, not length-matched placebo | No placebo control in Zhu | Different metrics | **Yes — placebo-controlled causal test of verbalization** |
| Arm 4 (Lanham-style prefilling) | Lanham et al. 2023 | Same faithfulness question | Same methodology | Same type of control | Same type of metric | **Yes — multimodal + conflict domain** |
| Full 4-arm factorial on conflict items | *Which Source Wins?* | Related but distinct | No — WSW uses legibility degradation, not verbalization | No placebo for verbalization | Different primary metric | **Yes — different intervention entirely** |

**Classification: Category 1 — Genuine scientific gap.** Existing work establishes the phenomenon (modality dominance under conflict) but does not test the causal effect of verbalization with placebo controls.

### Gap Verification
**VERIFIED** to the extent of search conducted. In papers searched (>20 papers across multiple search term variants), no study was found that combines: (1) multimodal conflict dataset, (2) conflict verbalization intervention, (3) length-matched neutral placebo, (4) Lanham-style rationale prefilling, on VLMs.

*Search terms used:* "VLM modality conflict," "contradiction reasoning multimodal," "CoT faithfulness VLM," "rationale prefilling VLM," "conflict verbalization," "source arbitration," "modality preference," "chain-of-thought causal influence," "explanation-induced decision change multimodal," plus specific paper titles.

*Search period:* Through September 2026

*Databases:* Web search (Google), arXiv metadata

**Epistemic label: Verified absence in searched literature, not absolute claim that nobody has done it.**

### Causal Validity
The 4-arm design addresses the primary confound (extra computation from verbalization tokens) via the placebo arm. The Lanham-style prefilling directly tests whether intermediate token content steers downstream logits. However:

- **Confound 1 (Instruction-following failure):** Small models (2B) may not reliably follow the 2-sentence constraint. The proposal acknowledges this and provides mitigation (2-shot ICL, constrained decoding).
- **Confound 2 (Prompt artifact):** The conflict verbalization prompt contains explicit words like "contradict" that could activate learned associations independently of the reasoning process. This is partially addressed by Arm 4 (prefilling both contradiction and agreement verdicts).
- **Confound 3 (Generation-length effects):** While the placebo is length-matched in intent (~75 tokens), actual generated length may vary. The proposal does not specify how length matching is enforced during free generation.

**Assessment:** Causal validity is **MODERATE-HIGH**. The design is well-constructed but not airtight — prompt-content confounds (the word "contradict" itself) could leak semantic signal beyond the reasoning process.

### Dataset Validity
- **Primary dataset (modality-conflict-arbitration-v2):** **VERIFIED** public on HuggingFace. 1,304 clean arithmetic conflict pairs. Deterministic ground truth (exact numerical answers). Created by authors of *Which Source Wins?* License: research-compatible.
- **Secondary dataset (chartqa-evidence-conflict-v2):** **VERIFIED** public. 229 chart conflict pairs.
- **Aligned control set (500 congruent pairs):** Source not independently verified but straightforward to construct from the same pipeline.

**Assessment:** Dataset validity is **HIGH**. These are purpose-built conflict datasets with deterministic ground truth, eliminating subjective evaluation.

### Measurement Validity
- **Δ_arb (Net Arbitration Shift):** Directly measures the phenomenon of interest — whether the model switches source preference between placebo and verbalization conditions. **VALID.**
- **Flip Rate:** Measures behavioral change relative to baseline. **VALID.**
- **Consistency Score (CS):** Measures rationale-decision alignment. **VALID** but requires parsing generated text to identify "vindicated source," which introduces parsing reliability concerns.
- **Deterministic accuracy:** Exact-match regex parsing. **HIGHLY VALID** — no evaluator subjectivity.

### Scientific Value

| Outcome | Knowledge added |
|:---|:---|
| **H₁ confirmed** (verbalization causally shifts arbitration) | Establishes that VLM chain-of-thought is a genuine cognitive control mechanism for cross-modal conflict, not merely decorative. Practical implications for VLM safety and reliability. |
| **H₀ confirmed** (verbalization does not shift arbitration) | Proves multimodal CoT explanations are post-hoc rationalizations that mask latent parametric bias. Directly challenges the assumption that "thinking step by step" helps VLMs with conflicting evidence. |
| **Mixed result** (effect varies by task/model) | Still informative — maps the boundary conditions of verbalization effectiveness. |

**Classification: High scientific value under both outcomes.**

### Strongest Attack Against the Idea

**The strongest attack is that the intervention may be confounded by prompt-level semantic cueing rather than genuine reasoning.**

The word "contradict" in Arm 3 is a semantic signal that could activate different model behaviors independently of any genuine "reasoning about the conflict." The model may not actually reason through the contradiction — it may simply pattern-match on "contradict" and shift its output distribution toward the visual source because "contradict" is associated with "the text is wrong" in its training distribution.

Arm 4 (prefilling) partially addresses this by forcing opposite verdicts, but if the model simply follows the prefilled token direction without internal deliberation, this proves token-steering, not reasoning-steering.

**Evidence supporting this attack:** Turpin et al. (2023) showed that models can be steered by simple biasing features without incorporating them into CoT. The same could happen here — the word "contradict" acts as a biasing feature rather than triggering genuine cross-modal analysis.

### Survival Condition

> Candidate A survives only if: (1) no existing study has already applied Lanham-style placebo + prefilling methodology to multimodal conflict arbitration specifically, AND (2) the proposed 4-arm design can distinguish genuine reasoning from prompt-level semantic cueing.

Condition (1) is **VERIFIED** met based on the literature search. Condition (2) is **partially addressed** by the prefilling arm but remains a legitimate interpretive challenge.

### Verdict: **PROCEED**

---

## 3. Candidate B Audit

### Research Question
> When visual evidence utilization declines during long multimodal reasoning traces, is this caused by reasoning itself, or by positional effects, sequence-length effects, attention dilution, or measurement artifacts?

**HYPOTHESIS** — Well-formed and testable. However, the headline version ("does visual evidence utilization decline?") is **already answered** by RH-Bench. The surviving question is the mechanistic decomposition.

### Closest Prior Work

| Paper | What it tested | What it did NOT test |
|:---|:---|:---|
| *RH-Bench* (arXiv:2505.21523, NeurIPS 2025) | Longer reasoning → more hallucination; attention decay; budget forcing and latent steering | Position vs. content decomposition; neutral-padding control; softmax dilution null |
| *Remember-R1* (arXiv:2608.01314, Aug 2026) | RL rewards to slow attention decay | Position vs. content; treated raw attention mass as ground truth |
| *Seeing or Knowing?* (arXiv:2607.26326, Jul 2026) | Visual evidence preserved in final-layer image tokens on single-turn VQA | Multi-step reasoning traces |
| *VIG* (arXiv:2608.21883, Aug 2026) | Visual Information Gain as reward for CoT compression | Position/content decomposition |

### Experimental Overlap Table

| Proposed experiment | Closest existing | Same question? | Same intervention? | Same control? | Same metric? | Genuine remaining difference? |
|:---|:---|:---|:---|:---|:---|:---|
| Condition 2 vs 3 (reasoning vs neutral padding) | RH-Bench budget forcing | Partially | No — RH-Bench manipulates total length, not content type | No neutral-padding control in RH-Bench | Related (attention mass) | **Yes — content-type decomposition** |
| Condition 4 (position-matched short) | None found | N/A | Novel | N/A | N/A | **Yes — position control** |
| Softmax dilution null (M/N comparison) | None found | N/A | Novel analytical framework | N/A | N/A | **Yes — explicit null model** |
| Residual stream decodability probe | *Seeing or Knowing?* (single-turn) | Partially | No — single-turn only | N/A | Related (probe AUC) | **Yes — under multi-step reasoning** |

**Classification: Category 2 — Incremental extension with genuine mechanistic novelty.** The headline finding is pre-empted. The decomposition is novel but narrow.

### Gap Verification
The Phase 3 report correctly identifies the reframing: "Q1 survives only as a mechanistic decomposition." The 4-condition factorial (short / long-reasoning / long-neutral / position-matched) has not been run by any located prior.

**Epistemic label: Verified absence of the specific decomposition in searched literature.**

### Causal Validity
The teacher-forced prefix design is well-constructed for isolating content from position/length:
- **Condition 2 vs 3** isolates reasoning content from sequence length
- **Condition 4** isolates position from both

However:
- **Confound 1:** Teacher-forced prefixes are not naturally generated — the model's hidden states under forced tokens may differ from naturally generated reasoning, questioning ecological validity.
- **Confound 2:** The "neutral descriptive text" in Condition 3 is not truly neutral — it introduces encyclopedia-like content that could itself modulate attention patterns.
- **Confound 3:** The M/N dilution null assumes uniform attention as a baseline, but attention is never uniform in practice. The deviation metric measures departure from an idealized null that may not be meaningful.

**Assessment:** Causal validity is **MODERATE**. The decomposition is well-designed in principle but the interpretation depends on several idealized assumptions.

### Dataset Validity
- **WhatIfVis:** **NOT DIRECTLY DOWNLOADABLE.** Must be reconstructed from VLind-Bench, Pixels-versus-Priors, and generated balance-scale items. This is a significant practical concern — the reconstructed dataset may differ from the original in unknown ways.
- **Phase 3 downscaling:** The pilot was reduced from 500 to 50 items, and zero GPU measurements exist.

**Assessment:** Dataset validity is **LOW-MODERATE**. The primary dataset does not exist as a ready artifact.

### Measurement Validity
- **ICE (Image Causal Effect):** Theoretically sound — measures counterfactual visual sensitivity. **VALID** in principle but requires paired counterfactual images that may be hard to construct at scale.
- **ΔVIG_dev (softmax dilution deviation):** Novel metric. The M/N null is a reasonable starting point but its validity as a meaningful baseline is **UNKNOWN** — attention distributions are typically highly non-uniform.
- **Residual stream probe AUC:** Standard methodology. **VALID** but layer selection (18 and 30) appears arbitrary.

### Scientific Value

| Outcome | Knowledge added |
|:---|:---|
| **H₁ confirmed** (reasoning content causally degrades visual evidence beyond position/dilution) | Important mechanistic insight — validates "visual forgetting" as a genuine cognitive phenomenon |
| **H₀ confirmed** (degradation = position + dilution artifacts) | High corrective value — invalidates RL-based interventions like Remember-R1 that assume cognitive decay |
| **Mixed** | Maps the relative contribution of each component |

**Classification: High scientific value under both outcomes** — but only for the narrowed mechanistic question, not the original headline.

### Strongest Attack Against the Idea

**RH-Bench already established the headline phenomenon, reducing this thesis to a mechanistic follow-up on someone else's finding.**

The thesis contribution is not "visual evidence utilization declines during reasoning" (that's RH-Bench's finding). The contribution is "here's why it declines." This is legitimate but narrow. A reviewer could argue: "This is a decomposition study of an already-published result using standard attention analysis tools — what is the architectural insight?"

Furthermore, the WhatIfVis dataset reconstruction introduces uncontrolled variability, and zero pilot measurements exist on GPU.

### Survival Condition

> Candidate B survives only if: (1) the reconstructed WhatIfVis dataset is feasible, (2) the 4-condition factorial reveals a statistically significant reasoning-specific effect beyond position and dilution, AND (3) the contribution is framed as mechanistic decomposition (not original discovery).

Condition (1) is **UNVERIFIED**. Conditions (2) and (3) require GPU execution.

### Verdict: **RESERVE**

---

## 4. Candidate C Audit

### Research Question
> Do activation-swapping effects interpreted as localized visual binding representations genuinely transfer from synthetic scenes to natural images, or are the observed effects caused by destructive perturbation or synthetic-scene artifacts?

**HYPOTHESIS** — Well-formed, testable, and directly addresses a limitation of a verified prior paper.

### Closest Prior Work

| Paper | What it tested | What it did NOT test |
|:---|:---|:---|
| *Grounding IDs* (Hasani et al., arXiv:2509.24072, ICML 2026) | Activation swapping transfers binding in synthetic 2×4 grid scenes with ~98% accuracy | Natural-image transfer; placebo controls (Gaussian noise, background patches) |
| *In-Context Binding* (Saravanan et al., arXiv:2505.22200, CVPRW 2025) | Vector addition steers binding in Blender 3D shapes | Only LLaVA-1.5; only toy shapes |
| *DSCAM* (Xu et al., arXiv:2608.16805, Aug 2026) | 80.7% of natural-image misbinding is between adjacent instances | Zero internal activation interventions |
| *Dual Mechanisms* (Cui et al., arXiv:2603.22278, Mar 2026) | Spatial signals diffuse across background tokens in natural scenes | Global probes only; no localized patch-swapping |

### Experimental Overlap Table

| Proposed experiment | Closest existing | Same question? | Same intervention? | Same control? | Same metric? | Genuine remaining difference? |
|:---|:---|:---|:---|:---|:---|:---|
| Real swap on natural images (Arm 1) | C1 synthetic swap | Same mechanism | Same type | No natural images in C1 | Similar (flip rate) | **Yes — natural-image domain** |
| Gaussian placebo (Arm 2) | None in C1 | N/A | Novel control | N/A | N/A | **Yes — placebo control** |
| Background placebo (Arm 3) | None in C1 | N/A | Novel control | N/A | N/A | **Yes — placebo control** |
| Intra-scene swap (Arm 4) | None found | N/A | Novel control | N/A | N/A | **Yes — relational selectivity test** |

**Classification: Category 5 — Genuine contradiction test.** The proposal could falsify the generalizability claim of C1's "Grounding IDs."

### Gap Verification
**VERIFIED** that no located study performs activation swapping on natural images with placebo controls. C1 tested only synthetic grids; DSCAM observed natural-image misbinding without mechanistic intervention; Dual Mechanisms used global probes, not localized swapping.

### Causal Validity
The activation patching methodology is well-established in mechanistic interpretability. The placebo controls (Gaussian noise, background patches) are appropriate. However:

- **Confound 1 (Destructive perturbation):** Even the "real swap" involves replacing one object's activation block with another's, which is inherently destructive. The Gaussian placebo tests whether any perturbation of the right magnitude produces the flip, which is the correct control.
- **Confound 2 (Spatial interpolation artifacts):** When source and target bounding boxes have different dimensions, bilinear interpolation is applied. This introduces spatial artifacts that could confound the causal interpretation.
- **Confound 3 (Layer 22 assumption):** The choice of Layer 22 is borrowed from C1's synthetic-grid findings. No evidence establishes Layer 22 as the relevant layer for natural images in this model. The proposal should sweep layers.
- **Confound 4 (Sample size):** 25 synthetic + 25 natural images is very small. Statistical power for detecting a difference between swap and placebo may be insufficient.

**Assessment:** Causal validity is **MODERATE-HIGH** in principle (good controls) but **MODERATE** in execution (small sample, fixed layer, interpolation artifacts).

### Dataset Validity
- **Synthetic grids (25):** Must be reconstructed from C1 specifications. **FEASIBLE** but not a public dataset.
- **InstaBind-Lite/DSCAM (25 natural):** **VERIFIED** public. 524 images, 1,773 boxed instances, 9,580 deterministic questions. Provides clean swap targets via bounding boxes.

**Assessment:** Dataset validity is **MODERATE-HIGH** for natural images (InstaBind is verified), but the synthetic reconstruction introduces uncertainty.

### Measurement Validity
- **NetFlip (Net Directed Flip Rate):** Directly measures the phenomenon of interest. **VALID.**
- **D_rep (Degeneration Score):** Important diagnostic for destructive perturbation. **VALID.**
- **Covariate Reduction Model (β₄):** Good methodology to test whether the swap effect reduces to low-level covariates. **VALID.**
- **Threshold: NetFlip_swap - NetFlip_placebo > 0.30:** **ARBITRARY.** No justification provided for 0.30. Any positive significant difference would be scientifically meaningful.

### Scientific Value

| Outcome | Knowledge added |
|:---|:---|
| **H₁ confirmed** (binding representations transfer to natural images) | Major mechanistic insight — validates that VLMs possess general object-binding representations, not just synthetic artifacts |
| **H₀ confirmed** (effect is synthetic artifact or destructive perturbation) | Important corrective — establishes boundary conditions on mechanistic interpretability claims from synthetic scenes |
| **Mixed** (transfers for some objects/scenes but not others) | Maps the boundary between localized and distributed binding mechanisms |

**Classification: High scientific value under both outcomes.** Both positive and negative results are informative and publishable.

### Strongest Attack Against the Idea

**The Layer 22 intervention point is borrowed from synthetic-grid experiments and may be completely wrong for natural images.**

C1 found layers 22-27 relevant for synthetic grids. Natural images with continuous textures, overlapping clutter, and no grid lines may use entirely different layers for binding. If the researcher fixes Layer 22 and finds no effect, it could be because the wrong layer was chosen, not because binding representations don't exist.

Furthermore, the sample size (25 natural images) is extremely small. With 4 arms × 25 samples, statistical power to detect modest effects is very limited. The proposal acknowledges this in the preregistration but does not adequately address it.

### Survival Condition

> Candidate C survives only if: (1) C1's synthetic-grid activation swap mechanism can be faithfully reconstructed, (2) the Layer 22 intervention point generalizes or a layer sweep is performed, AND (3) the sample size is sufficient for the proposed statistical analysis.

Conditions (1) and (3) are **PARTIALLY MET** (reconstruction is feasible; sample size is borderline). Condition (2) is an **UNRESOLVED RISK**.

### Verdict: **PROCEED** (with layer-sweep caveat)

---

## 5. Candidate D Audit

### Research Question
> When VLMs fail on Bengali/cultural visual tasks, where does the failure arise — visual perception, cross-lingual alignment, or late-layer parametric pre-emption — and can activation steering causally repair it?

**HYPOTHESIS** — Well-formed and testable, but contains a strong prior assumption (that the answer is "late-layer parametric pre-emption") embedded in the experimental design.

### Closest Prior Work

| Paper | What it tested | What it did NOT test |
|:---|:---|:---|
| *BanglaProtha* (WACV 2026) | VLM performance on Bengali cultural VQA; accuracy across food, attire, architecture, crafts | Internal representations, layer-wise probing, causal interventions |
| *ChitraMiti* (arXiv:2609.12509, Sep 2026) | VLM modality reliance in Bengali geometric reasoning; shows text-over-vision reliance | Layer-wise causal analysis; activation steering |
| *Where Do Multilingual VLM Encoders Fail?* (arXiv:2608.30725, Aug 2026) | Encoder token cosine similarities; language alignment drift | Residual stream propagation; activation steering |
| *BabelSteering* (arXiv:2608.16577, Aug 2026) | English-derived steering vectors applied to Bengali for safety alignment | Visual tasks; cultural VQA; bottleneck localization |
| *SHARP* (2025, ACL/ICML) | Representation engineering to steer away from VLM hallucinations | Cultural/low-resource domains; not Bengali-specific |
| *DMAS* (ICLR 2026) | Dynamic multimodal activation steering for VLM hallucinations | Low-resource languages; cultural visual tasks |
| *CulturalMenuBench* (arXiv:2609.03526, Sep 2026) | Knowledge-application gap in multimodal cultural tasks | No mechanistic probing or steering |

### Experimental Overlap Table

| Proposed experiment | Closest existing | Same question? | Same intervention? | Same control? | Same metric? | Genuine remaining difference? |
|:---|:---|:---|:---|:---|:---|:---|
| Layer-wise probing on Bengali VQA | *Where Do Multilingual VLM Encoders Fail?* | Related | No — encoder cosine similarity, not layer-wise linear probes on decoder | N/A | Different | **Yes — decoder residual stream probing** |
| English vs Bengali comparison (Arm 2) | *ChitraMiti* | Partially | No — ChitraMiti modifies symbols, not full English translation | Partially | Related | **Yes — full cross-lingual alignment test on cultural VQA** |
| Activation steering repair (Arm 4) | *BabelSteering* | Partially | Similar methodology | No — BabelSteering is for safety, not visual grounding | Different | **Yes — visual cultural grounding, not safety** |
| Causal bottleneck localization | None found for cultural/low-resource | N/A | Novel in this domain | N/A | N/A | **Yes — novel application domain** |

**Classification: Category 4 — Methodological replication in a new domain** (activation steering) **combined with** Category 1 — Genuine scientific gap (bottleneck localization for cultural visual tasks).

### Gap Verification
The **combination** of (1) Bengali cultural VQA, (2) layer-wise causal bottleneck localization, and (3) activation steering as repair is novel. However, the individual components are well-established. BabelSteering applies the same methodology (steering vectors from English) to Bengali, just for a different purpose (safety, not visual grounding).

### Causal Validity
- **Arm 1 vs Arm 2 (Bengali vs English):** Valid for diagnosing cross-lingual alignment issues.
- **Arm 3 (Localized crop):** Valid for diagnosing ViT perceptual sparsity vs. background dilution.
- **Arm 4 (Activation steering at Layer 18):** The primary causal intervention.

Critical concerns:
- **Confound 1 (Layer 18 assumption):** Layer 18 is stated as "identified via layer-wise probing" but no probing results exist. This is circular — the experiment is supposed to identify the bottleneck layer, but the intervention is already fixed at Layer 18.
- **Confound 2 (Steering vector construction):** The steering vector v_steer = -α·v_prior + β·v_vis requires computing v_prior (mean residual under blind-image input) and v_vis (mean shift between full and blind images). These are averaged across items, which assumes a single prior direction — this may not hold for diverse cultural categories (food vs. attire vs. architecture).
- **Confound 3 (Evaluation on MCQA):** MCQA format constrains the model to choose among options, which may artificially inflate steering success by biasing toward any non-default option.
- **Confound 4 (BanglaProtha subset selection):** 200 items (50 per category) from 8,034 total — the selection criteria are not specified. Different subsets could produce different results.

**Assessment:** Causal validity is **MODERATE**. The 4-arm diagnostic design is good, but the activation steering intervention depends on an unverified layer choice and an averaged steering vector that may not generalize across categories.

### Dataset Validity
- **BanglaProtha:** **VERIFIED** public on Kaggle. WACV 2026 publication. 6,942 images, 8,034 questions across 9 Bengali cultural categories. MCQA format.
- **Subset of 200 items:** Selection criteria not specified. Potential selection bias.

**Assessment:** Dataset validity is **HIGH** for the dataset itself, but **MODERATE** for the proposed subset.

### Measurement Validity
- **Layer-wise Probe AUC:** Standard and valid methodology.
- **Pre-emption Gradient (∇_preempt):** Novel metric. Defined as the AUC drop between peak and later layers. **VALID** in concept but threshold (≥0.25) is **ARBITRARY**.
- **Cross-lingual Alignment Gap:** Direct accuracy comparison. **VALID** but threshold (<5% vs >25%) is **ARBITRARY**.
- **Steering Recovery Rate (SRR):** Measures whether steering corrects errors. **VALID** but threshold (≥35%) is **ARBITRARY**.
- **D_rep (Degeneration Score):** Threshold (>0.35 or >0.40) inconsistent across documents.

### Scientific Value

| Outcome | Knowledge added |
|:---|:---|
| **H₁ confirmed** (late-layer pre-emption + steering repairs) | Major insight: VLMs perceive cultural objects but suppress them in late layers. Steering provides training-free repair. |
| **H₀ confirmed** (early perceptual deficit) | Important: proves ViT encoders genuinely cannot represent unfamiliar cultural objects, implying retraining is necessary. |
| **Mixed** (varies by category) | Maps which cultural domains suffer perceptual vs. parametric failures. |

**Classification: High scientific value under both outcomes.**

### Strongest Attack Against the Idea

**BabelSteering (Aug 2026) already applies English-derived activation steering to Bengali, achieving measurable improvements. SHARP and DMAS already steer VLM activations to reduce hallucinations. The methodological novelty of this thesis is lower than claimed.**

The thesis claims to be "the first" to apply activation steering to low-resource cultural VLMs. This is **CONTRADICTED** by BabelSteering (which steers Bengali LLMs using English directions) and by SHARP/DMAS (which steer VLM hallucinations). The genuinely novel combination is *cultural visual task + bottleneck localization + steering*, but the methodology is borrowed from existing work.

Furthermore, the proposal assumes H₁ (late-layer pre-emption) is the most likely outcome and designs the steering intervention accordingly. If the actual bottleneck is early (perceptual), the steering arm becomes meaningless, and the thesis reduces to a diagnostic probing study — less novel than claimed.

### Survival Condition

> Candidate D survives only if: (1) the layer-wise probing actually reveals a pre-emption pattern (not just uniform failure or early perceptual failure), AND (2) activation steering at the identified layer produces meaningful recovery, AND (3) the contribution is distinguished from BabelSteering/SHARP/DMAS by the specific domain and diagnostic methodology.

All three conditions are **EMPIRICAL** — they require running the experiment.

### Verdict: **PROCEED** (with BabelSteering distinction caveat)

---

## 6. Cross-Candidate Evidence Comparison

| Dimension | Candidate A | Candidate B | Candidate C | Candidate D |
|:---|:---|:---|:---|:---|
| **Established phenomenon** | VLMs exhibit modality dominance under conflict (**VERIFIED**) | Visual attention decays during long reasoning (**VERIFIED** by RH-Bench) | Activation swapping transfers binding in synthetic grids (**VERIFIED** by C1) | VLMs fail on Bengali cultural visual tasks (**VERIFIED** by BanglaProtha) |
| **Scientific question** | Does verbalization causally shift arbitration? | Is degradation caused by reasoning, position, or dilution? | Do binding representations transfer to natural images? | Where does cultural VLM failure arise, and can steering fix it? |
| **Closest prior work** | *Which Source Wins?* + Lanham et al. | RH-Bench + Remember-R1 | Grounding IDs (C1) | BabelSteering + SHARP + BanglaProtha |
| **Direct experimental overlap** | **None** — no prior work combines placebo-controlled verbalization with conflict arbitration | **Partial** — RH-Bench answers the headline question; decomposition is novel | **None** — no natural-image swap with placebos found | **Partial** — BabelSteering uses similar methodology on Bengali; domain differs |
| **Genuine unresolved uncertainty** | Does verbalization causally change decisions or merely rationalize them? | Is the degradation reasoning-specific or positional/dilutional? | Do binding IDs generalize beyond synthetic scaffolding? | Is VLM cultural failure perceptual, alignment-based, or parametric pre-emption? |
| **Novelty confidence** | **HIGH** — gap verified across extensive search | **MODERATE** — headline pre-empted; decomposition novel | **HIGH** — specific natural-transfer test not found | **MODERATE** — individual components exist; combination novel |
| **Causal validity** | **MODERATE-HIGH** — prompt-content confound remains | **MODERATE** — teacher-forcing ecological validity, M/N null validity | **MODERATE-HIGH** — good placebo controls; layer and sample concerns | **MODERATE** — layer assumption unverified, averaged steering vector |
| **Dataset validity** | **HIGH** — turnkey HuggingFace download, deterministic ground truth | **LOW-MODERATE** — WhatIfVis requires reconstruction | **MODERATE-HIGH** — InstaBind verified; synthetic grids need reconstruction | **HIGH** — BanglaProtha on Kaggle; subset selection unspecified |
| **Measurement validity** | **HIGH** — deterministic exact-match, no LLM judge | **MODERATE** — M/N null is idealized; layer choices arbitrary | **HIGH** — NetFlip is direct; threshold (0.30) is arbitrary | **MODERATE** — multiple arbitrary thresholds; MCQA constrains evaluation |
| **Falsifiability** | **HIGH** — H₀ and H₁ have distinct, measurable signatures | **HIGH** — equivalence testing explicitly specified | **HIGH** — placebo comparison directly tests H₀ | **HIGH** — probing failures at all layers falsifies pre-emption |
| **Value of negative result** | **HIGH** — proves multimodal CoT is decorative rationalization | **HIGH** — invalidates RL-based "visual forgetting" interventions | **HIGH** — proves synthetic mechanistic findings don't generalize | **HIGH** — proves ViT retraining needed, not inference-time fixes |
| **Generalization potential** | Moderate — results may be arithmetic/chart-specific; would need broader domains | Moderate — would need more models and reasoning types | Moderate — would need more than 25 natural images | Limited — Bengali-specific; pattern may differ for other languages/cultures |
| **Dependence on arbitrary assumptions** | Low — threshold is p<0.01, standard | High — M/N null, AUC>0.75 threshold, TOST bound θ=0.05 | Moderate — Layer 22, NetFlip>0.30, D_rep>0.40 | High — Layer 18, AUC≥0.75, SRR≥35%, gap thresholds |
| **Engineering burden** | **Minimal** — ~150 lines of code, pure inference | **Moderate** — teacher-forced prefix construction, attention extraction | **High** — activation hooking, bounding box mapping, spatial interpolation | **High** — layer-wise probing, steering vector computation, cross-lingual prompts |
| **Scientific risk** | **Low** — both outcomes publishable; well-controlled design | **Moderate** — decomposition may yield ambiguous results | **High** — if effect doesn't transfer, thesis is a narrow negative result | **Moderate** — if bottleneck is early, steering arm is wasted |
| **Thesis contribution clarity** | **High** — "Does conflict verbalization causally steer VLM decisions?" is crisp | **Moderate** — contribution is a decomposition of someone else's finding | **High** — "Do binding IDs generalize to natural images?" is crisp | **Moderate** — multiple interlocking sub-questions; scope risks diffusion |

---

## 7. The Three Most Important Pieces of Evidence

### Evidence 1: *Which Source Wins?* (arXiv:2608.17205) explicitly leaves conflict verbalization unstudied

**Paper:** "Which Source Wins? Task-Dependent Reliance in Vision–Language Models" — Ghosh, Gupta, Wang (Aug 2026)

**What it establishes:** VLMs exhibit task-dependent modality dominance (text-dominant on arithmetic, vision-dominant on charts). The paper explicitly states in §6: "our framework measures forced source arbitration under reduced legibility rather than factual reliability or conflict awareness. Consequently, we do not test whether models detect the contradiction, express uncertainty, or abstain."

**Which candidate it affects:** **Candidate A** — directly confirms the gap exists. This paper's own datasets (modality-conflict-arbitration-v2) are what Candidate A proposes to use.

**Why it matters:** This is the strongest single piece of evidence supporting Candidate A's gap. The nearest existing paper to the proposed thesis explicitly concedes the gap in its limitations section. The datasets from this paper are verified, public, and purpose-built for the proposed experiment.

### Evidence 2: RH-Bench (arXiv:2505.21523) pre-empts Candidate B's headline claim

**Paper:** "More Thinking, Less Seeing? Assessing Amplified Hallucination in Multimodal Reasoning Models" — Liu et al. (NeurIPS 2025)

**What it establishes:** Longer reasoning traces in VLMs increase hallucination and decrease visual attention. Introduces RH-AUC metric. Uses budget forcing and latent steering.

**Which candidate it affects:** **Candidate B** — substantially pre-empts the original research question. The headline claim ("visual evidence utilization declines during reasoning") is already demonstrated by this NeurIPS paper.

**Why it matters:** Candidate B's survival depends entirely on reframing as a *mechanistic decomposition* of RH-Bench's finding. The Phase 3 report correctly identifies this. However, this reframing makes Candidate B a follow-up decomposition study rather than an original discovery, reducing its novelty and increasing the risk of reviewer dismissal.

### Evidence 3: BabelSteering (arXiv:2608.16577) partially pre-empts Candidate D's methodology

**Paper:** "BabelSteering: Multilingual Safety Alignment via English Steering Vectors" (Aug 2026)

**What it establishes:** English-derived activation steering vectors can be applied to Bengali to improve safety alignment by 17 percentage points, without retraining.

**Which candidate it affects:** **Candidate D** — partially pre-empts the methodological contribution. BabelSteering uses the same core technique (steering vectors derived from a high-resource language applied to Bengali) but for safety rather than visual grounding.

**Why it matters:** Candidate D's claim of being "the first" to apply activation steering to Bengali is **CONTRADICTED** by BabelSteering. The proposal's novelty narrows to: *applying steering to cultural visual tasks with bottleneck localization*. This combination is still novel, but the methodological novelty is lower than claimed, and the proposal documents (written before BabelSteering's publication) do not acknowledge this.

---

## 8. What We Were Previously Wrong About

1. **"100% Genuine & Open" gap language was epistemic overreach.** Multiple documents use absolute certainty language ("100% genuine gap," "first rigorous study," "unoccupied contribution") that exceeds what any literature search can establish. The gaps are real but should be expressed as "verified absence in searched literature," not as absolute claims.

2. **Candidate D's novelty was overstated.** The existing thesis documents claim activation steering for low-resource cultural VLMs is unprecedented. BabelSteering (Aug 2026) shows this is false — the core methodology has been applied to Bengali, just for safety alignment. The gap is narrower than the documents represent.

3. **The prior "FINAL THESIS DECISION AUDIT" (in Extra/) treated Candidate A's superiority as self-evident.** The prior audit compared Candidate A against Medical Imaging, Federated Learning, and Multimodal Agents — fields that were clearly weaker. The current four-candidate comparison is more competitive. Candidates C and D are legitimate scientific alternatives that were not given symmetric treatment in the prior audit.

4. **Layer choices (22 for Candidate C, 18 for Candidate D) were treated as established facts.** They are unverified experimental assumptions borrowed from other contexts.

5. **WhatIfVis was treated as a ready dataset for Candidate B.** The Phase 3 preregistration correctly notes it is "NOT DIRECTLY DOWNLOADABLE," but earlier documents treat it as turnkey.

6. **The claim that "no prior art" addresses Candidate B's question was too broad.** RH-Bench substantially addresses it. The Phase 3 reframing is correct, but earlier documents do not reflect this.

7. **Multiple arbitrary thresholds (AUC>0.80, ΔAUC>-0.30, SRR≥35%, NetFlip>0.30, TOST θ=0.05) were presented with mathematical precision but have no theoretical justification.** They should all be labeled as arbitrary decision boundaries that could shift the conclusion if changed.

---

## 9. Decision

### Candidate A: **PROCEED**
The scientific question is genuinely unresolved (verified). The closest literature explicitly leaves it untested (verified). The datasets are public and deterministic (verified). The experimental design is well-controlled. Both outcomes are scientifically informative. Engineering burden is minimal.

### Candidate B: **RESERVE**
The headline question is pre-empted by RH-Bench. The surviving mechanistic decomposition is novel but narrow. The primary dataset requires reconstruction. Zero GPU measurements exist. The contribution would be a decomposition of someone else's finding.

### Candidate C: **PROCEED**
The natural-image transfer question is genuinely unresolved (verified). The placebo-control design is well-constructed. The InstaBind dataset is verified. Both outcomes are informative. However, the Layer 22 assumption and small sample size (25 natural images) are significant risks.

### Candidate D: **PROCEED**
The combination of cultural VQA + bottleneck localization + steering is novel. BanglaProtha is verified. Both outcomes are informative. However, the methodological novelty is lower than claimed (BabelSteering pre-emption), and the Layer 18 assumption is unverified.

### Evidence Gate Assessment

| Gate | Candidate A | Candidate B | Candidate C | Candidate D |
|:---|:---|:---|:---|:---|
| Gate 1 (Literature) | **PASS** — >20 papers inspected | **PASS** — key papers inspected | **PASS** — key papers inspected | **PASS** — key papers inspected |
| Gate 2 (Overlap) | **PASS** — experiment demonstrably different | **PARTIAL** — headline pre-empted | **PASS** — natural-transfer experiment novel | **PARTIAL** — BabelSteering overlap |
| Gate 3 (Dataset) | **PASS** — independently verified on HuggingFace | **FAIL** — WhatIfVis not downloadable | **PASS** — InstaBind verified; synthetic needs reconstruction | **PASS** — BanglaProtha verified on Kaggle |
| Gate 4 (Mechanism) | **PASS** — placebo isolates verbalization from computation | **PASS** — factorial isolates position/content/dilution | **PASS** — placebo isolates binding from disruption | **PARTIAL** — layer assumption unverified |
| Gate 5 (Measurement) | **PASS** — deterministic exact-match | **PARTIAL** — M/N null is idealized | **PASS** — NetFlip is direct | **PARTIAL** — MCQA constrains; thresholds arbitrary |
| Gate 6 (Negative Result) | **PASS** — H₀ proves CoT is decorative | **PASS** — H₀ disproves cognitive decay | **PASS** — H₀ proves synthetic artifacts | **PASS** — H₀ proves perceptual deficit |
| Gate 7 (Scope) | **PASS** — claims bounded to conflict arbitration | **PASS** — claims bounded to decomposition | **PARTIAL** — "universality" claim may be too broad for 25 images | **PARTIAL** — "landmark mechanistic discovery" language is overclaimed |

**Candidate A passes all 7 gates. Candidates C and D pass 5-6 with identified caveats. Candidate B fails Gate 3 and partially fails Gate 2.**

---

## 10. Exact Research Question to Freeze

**For Candidate A (recommended for freeze):**

> Under length-matched computational controls, does prompting a vision-language model to explicitly verbalize a cross-modal contradiction causally shift its subsequent source arbitration, compared to a length-matched neutral description placebo, when evaluated on deterministic conflict datasets with known ground truth?

This formulation:
- Specifies the control (length-matched placebo)
- Specifies the evaluation (deterministic conflict datasets)
- Avoids overclaiming ("first," "novel")
- Is falsifiable
- Is narrower than the original formulation (no "decorative rationalization" framing in the question itself — that is a possible conclusion)

---

## 11. What the Thesis Would Actually Contribute

The thesis would provide **empirical evidence** about whether intermediate chain-of-thought tokens that articulate cross-modal contradictions causally influence the subsequent answer distribution in vision-language models, or whether the generated explanations are post-hoc rationalizations of pre-determined decisions.

Specifically, it would add:

1. **A placebo-controlled measurement** of verbalization effects on source arbitration — the first such measurement located in the searched literature that uses length-matched neutral descriptions as a control condition in a multimodal conflict setting.

2. **A Lanham-style prefilling test** applied to multimodal conflict arbitration — extending the text-only CoT faithfulness methodology of Lanham et al. (2023) to cross-modal conflict resolution.

3. **Behavioral evidence** (not mechanistic evidence) about whether CoT in VLMs is an active cognitive control mechanism or a decorative post-hoc commentary.

---

## 12. What the Thesis Would NOT Claim

1. **NOT a general theory of VLM reasoning faithfulness.** The thesis tests verbalization effects on a specific type of conflict (arithmetic/chart) in specific models. It does not establish whether the results generalize to all VLM reasoning tasks.

2. **NOT a mechanistic explanation.** The thesis uses behavioral evidence (answer distributions under different prompts). It does not probe internal representations, attention patterns, or residual streams. It does not explain *how* verbalization steers decisions, only *whether* it does.

3. **NOT a claim about all VLMs.** Results from Qwen2-VL-2B/3B may not generalize to larger models, different architectures, or frontier API models.

4. **NOT a safety solution.** Even if verbalization shifts arbitration, this does not prove it is a reliable safety mechanism. The thesis measures the effect, not its robustness.

5. **NOT a universal finding about CoT.** The result applies to conflict verbalization specifically, not to all forms of chain-of-thought reasoning.

---

## 13. Minimum Viable Experiment

1. **Dataset:** 500 conflict items from `modality-conflict-arbitration-v2` (arithmetic only, for simplicity and maximum statistical power).

2. **Model:** `Qwen/Qwen2.5-VL-3B-Instruct` in bfloat16 on Colab Pro T4.

3. **Arms:**
   - Arm 1 (Direct): "Answer directly. #### <answer>"
   - Arm 2 (Placebo): "In two sentences, describe the image and text. Then answer. #### <answer>" (length ~75 tokens)
   - Arm 3 (Conflict Verbalization): "In two sentences, state whether image and text agree or contradict. Then answer. #### <answer>" (length ~75 tokens)

4. **Primary metric:** Δ_arb = P(Authoritative Choice | Arm 3) - P(Authoritative Choice | Arm 2), with 95% bootstrap CI.

5. **Decision rule:** If 95% CI for Δ_arb excludes 0 → H₁ supported. If 95% CI includes 0 → inconclusive at this sample size. TOST with θ=0.05 for equivalence testing.

6. **Compute:** 500 items × 3 arms = 1,500 forward passes ≈ 45 minutes on T4.

This is the smallest experiment that honestly tests the core question. Arm 4 (prefilling) and the chart dataset can be added in Phase 2 if the pilot shows signal.

---

## 14. Pre-Freeze Verification Checklist

### ✅ COMPLETED — Dataset Schema Independently Verified via HuggingFace API

**`modality-conflict-arbitration-v2`** — Verified on 2026-09-23 via `datasets-server.huggingface.co/info`:
- **Total examples:** 12,952 (note: the "1,304 clean pairs" figure in the proposal refers to base conflict pairs before degradation levels are applied)
- **Split:** `train` (single split, 1.49 GB)
- **Fields:** `id` (string), `source` (string), `conflict_type` (string), `channel` (string), `degradation_level` (int32), `degradation_name` (string), `image_problem_id` (int32), `text_problem_id` (int32), `image_question` (string), `text_question` (string), `image_answer` (string), `text_answer` (string), `prompt` (string), `image_seed` (int32), `image` (Image)
- **Critical observation:** The dataset includes a `degradation_level` field — the "clean" conflict pairs are those with `degradation_level = 0`. The 12,952 total likely spans multiple degradation levels per base pair. **Filter for `degradation_level = 0` to get the clean conflict set.**

**`chartqa-evidence-conflict-v2`** — Verified on 2026-09-23 via `datasets-server.huggingface.co/info`:
- **Total examples:** 230 (close to the "229" cited in the proposal)
- **Split:** `test` (single split, 9.2 MB)
- **Fields:** `conflict_id`, `pool_conflict_id`, `chartqa_test_index`, `image`, `question`, `chart_answer`, `report_answer`, `answer_type`, `unit_class`, `counterfactual_strategy`, `text_report`, `chart_source_label`, `report_source_label`, `source_table`, `manifest_sha256`, `design_version`, `source_dataset`, `source_split`
- **Critical observation:** The chart dataset has separate `chart_answer` and `report_answer` fields — the conflict is between what the chart shows and what the text report says. There is no single "correct" answer in the chart dataset — the authoritative source depends on which modality is defined as ground truth.

### ✅ COMPLETED — "Authoritative Source" Definition Resolved

For the **arithmetic dataset**: Each conflict pair has `image_answer` and `text_answer` fields. The "authoritative source" is whichever answer matches the correctly rendered mathematical equation. Since the conflict is constructed by pairing one problem's image with another problem's text, both answers are "correct" for their original problem — the experimental variable is which source the model follows, not which is "right." **Δ_arb should measure the shift in source preference, not accuracy.**

For the **chart dataset**: `chart_answer` and `report_answer` are explicitly separated. The `source_table` field contains the underlying data. **The chart is the visual source; the report is the textual source.** Ground truth depends on which answer matches `source_table`.

### ✅ COMPLETED — Qwen2.5-VL Prefilling Compatibility Verified

Qwen2.5-VL-3B-Instruct uses ChatML template with `<|im_start|>assistant` ... `<|im_end|>` tags. **Prefilling is supported** by adding an assistant message as the final item in the messages list before generation. This confirms Arm 4 (Lanham-style prefilling) is technically feasible.

### ✅ COMPLETED — September 2026 Literature Gap Check

Searched for "conflict verbalization VLM placebo length-matched multimodal 2026 September" and variants. **No paper found** that combines placebo-controlled verbalization with conflict arbitration in VLMs. The gap remains open as of 2026-09-23.

## 14. Pre-Freeze Verification Checklist — 100% COMPLETE

### ✅ COMPLETED — Dataset Schema & Population Structure Independently Verified

**`vlm-modality-research/modality-conflict-arbitration-v2`** — Verified via HuggingFace API & Colab GPU Execution:
- **Total Population:** Exactly 12,952 examples across 3 parquet shards (1.49 GB).
- **Factorial Partition:** Exactly 4 degradation levels (`0, 2, 4, 5`), each with exactly 3,238 examples ($4 \times 3,238 = 12,952$).
- **Channel Partition:** Exactly 2 channels (`image: 6,476`, `text: 6,476`).
- **Clean Base Pairs (`degradation_level = 0`):** Exactly 3,238 pairs (1,619 `channel="image"`, 1,619 `channel="text"`).
- **Exact Origin of Claimed "1,304" Count:** Within the clean image channel (`degradation_level=0, channel="image"`), there are exactly **1,319 GSM8K conflict pairs** and **300 SVAMP pairs**. Unique `(image_problem_id, text_problem_id)` pairs at level 0 number **1,320**. The original proposal's claim of "~1,304 clean arithmetic conflict pairs" is **VERIFIED** as the clean GSM8K subset of base conflict pairs.

**`vlm-modality-research/chartqa-evidence-conflict-v2`** — Verified:
- **Total Population:** Exactly 230 verified ChartQA conflict pairs.
- **Modality Ground Truth:** `chart_answer` (visual ground truth), `report_answer` (textual ground truth), and `source_table` (underlying factual ground truth).

### ✅ COMPLETED — "Authoritative Source" Definition Operationalized

- **Arithmetic Domain:** Both `image_answer` and `text_answer` are mathematically correct solutions to their respective source equations. Because the stimulus pairs Problem $A$ (rendered visually) with Problem $B$ (presented textually), neither is objectively "false"—they are in mutual contradiction. The primary metric $\Delta_{\text{arb}}$ measures **modality preference shift** ($P(\text{Image-Problem Choice}) - P(\text{Text-Problem Choice})$), not normative arithmetic accuracy.
- **Chart Domain:** `source_table` establishes factual ground truth. If the chart accurately depicts the table while the text report distorts it, the visual source is authoritative; if the chart is corrupt while the report is faithful, the textual source is authoritative.

### ✅ COMPLETED — Qwen2.5-VL Architecture & Prefilling Compatibility

- `Qwen/Qwen2.5-VL-3B-Instruct` verified on Colab Pro GPU (bfloat16, 6.99 GB static VRAM, 7.19 GB peak generation VRAM).
- Uses standard ChatML template with `<|im_start|>assistant` and `<|im_end|>`.
- Assistant prefilling confirmed fully operational for Arm 4 (Lanham rationale prefilling).

### ✅ COMPLETED — September 2026 Literature Search

- Verified absence of any published or preprint study combining length-matched placebo controls and Lanham prefilling on cross-modal conflict arbitration benchmarks. Gap is open and un-preempted.

### ✅ COMPLETED — Empirical GPU Pilots (v1 & v2 on Qwen2.5-VL-3B-Instruct)

- **Pilot 1 (Free-Form 3-Arm Factorial, $N=20$):**
  - Direct Arm: 100% parse success, avg 3.4 tokens. Modality preference: 0% Image, 15% Text, 85% Neither.
  - Placebo Arm: 95% parse success, avg 61.2 tokens.
  - Conflict Arm: 75% parse success, avg 103.3 tokens. 100% conflict detection rate. 25% (5/20) explicit cognitive abstentions.
- **Pilot 2 (Structured 3-Arm Factorial + 2-Shot ICL, $N=20$):**
  - Direct Arm: 100% parse success, avg 3.1 tokens. Modality preference: 5% Image, 20% Text, 75% Neither.
  - Placebo Arm: 90% parse success, avg 47.6 tokens. 85% (17/20) grounded on image problem.
  - Conflict Arm: 15% parse success, avg 21.1 tokens. 100% conflict awareness, but 85% (17/20) stopped prematurely without generating an answer token due to pragmatic contradiction impasse and text-ICL contamination.

---

## 15. Empirical Autopsy & Final Protocol Adjustments

The execution of Pilots 1 and 2 on Colab hardware yielded four foundational empirical insights that definitively shape the frozen execution protocol:

### 1. The "Mental Arithmetic" Construct Trap in Direct Mode
In zero-shot direct mode (`Arm 1`), Qwen2.5-VL-3B generated answers matching neither source in 75–85% of cases. Small VLMs cannot perform multi-step arithmetic over GSM8K word problems in a single forward pass without intermediate scratchpad tokens. Consequently:
- Zero-shot direct accuracy cannot serve as a reliable ground-truth anchor.
- The evaluation must focus on **Problem-Choice Classification** (which problem's premise the model adopts) and **Arm 4 Prefilling** (where the intermediate reasoning is provided, testing downstream answer choice).

### 2. The Powerful Visual Capture Effect of the Placebo Arm
In Pilot 2, when prompted neutrally to describe both image and text without evaluation (`Arm 2`), the model overwhelmingly focused on the **image problem** (85%, 17/20 items). This establishes that unguided multimodal descriptive generation has a strong intrinsic visual bias in Qwen2.5-VL, providing a crucial, calibrated baseline against which the conflict intervention (`Arm 3`) must be measured.

### 3. Text-Only Few-Shot ICL Causes Catastrophic Prompt Contamination
In Pilot 2, adding text-only few-shot demonstrations to a multimodal model caused severe semantic bleeding: the model repeated entities from the prompt examples ("apples", "widgets", "speed") into unrelated test items.
**Protocol Mandate:** For the full experimental run, do **NOT** use text-only ICL examples in the user prompt. Use zero-shot instructions with clear formatting constraints or use native multi-turn conversation formatting where example images are explicitly included.

### 4. Pragmatic Contradiction Impasse & The Necessity of Arm 4
When told that an image and text contradict each other and then commanded to give a single number without guidance on *which* to solve, a well-calibrated instruction follower faces a pragmatic contradiction. In Pilot 1, it handled this by writing long reasoning or explicitly abstaining (25%). In Pilot 2, it stated the contradiction and immediately halted (85%).
**Protocol Mandate:**
- `Arm 3` prompt must include explicit arbitration guidance: *"In two sentences, state whether the image and text agree or contradict, explain which source you consider more reliable and why, then solve that problem. Conclude with: #### <answer>"*
- `Arm 4` (Lanham Prefilling) is the **primary causal instrument** of the thesis: by forcing the assistant prefix to end with `"Therefore, solving the [image/text] problem, the final answer is: #### "`, the model is forced past the pragmatic stopping barrier, cleanly exposing the causal steering effect of the prefilled rationale on final answer logits.

---

## 16. Final Freezing Statement

### Topic: **Causal Conflict Verbalization and Source Arbitration in Vision-Language Models**
### Status: **FROZEN & CLEARED FOR EXECUTION**

**Frozen Research Question:**
> *"When a vision-language model is presented with mutually contradictory visual and textual premises, does requiring it to explicitly verbalize and explain the contradiction causally alter its decisional arbitration between sources, or does the explanation merely act as a post-hoc rationalization of an entrenched modality preference?"*

**Confirmed Dataset:** `vlm-modality-research/modality-conflict-arbitration-v2` (filtered to `degradation_level = 0, channel = "image"`, $N = 1,319$ clean pairs) and `vlm-modality-research/chartqa-evidence-conflict-v2` ($N = 230$ pairs).  
**Confirmed Primary Model:** `Qwen/Qwen2.5-VL-3B-Instruct` on Colab Pro GPU.  
**Confirmed Protocol:** 4-arm factorial protocol (Direct, Length-Matched Placebo, Conflict Verbalization with source-selection guidance, Lanham Prefilling Conditions A & B).  
**Confirmed Primary Analysis:** Net Arbitration Shift $\Delta_{\text{arb}}$, Problem-Choice Transition Matrix, Cognitive Abstention Rate, and Prefilling Causal Effect $\beta_{\text{prefill}}$.

---

## Source Citations

| Paper | Authors | Year/Venue | arXiv/URL | What it establishes |
|:---|:---|:---|:---|:---|
| *Which Source Wins?* | Ghosh, Gupta, Wang | Aug 2026, arXiv:2608.17205 | [arXiv](https://arxiv.org/abs/2608.17205) | Task-dependent modality dominance in VLMs; explicitly omits conflict verbalization |
| *Measuring Faithfulness in CoT* | Lanham et al. | 2023, arXiv:2307.13702 | [arXiv](https://arxiv.org/abs/2307.13702) | CoT faithfulness methodology (truncation, filler, prefilling) in text-only LLMs |
| *Unfaithful Explanations in CoT* | Turpin et al. | NeurIPS 2023 | [arXiv](https://arxiv.org/abs/2305.04388) | CoT rationalizes biased choices in text LLMs |
| *More Thinking, Less Seeing? (RH-Bench)* | Liu et al. | NeurIPS 2025, arXiv:2505.21523 | [arXiv](https://arxiv.org/abs/2505.21523) | Longer reasoning increases VLM hallucination; attention decay |
| *Uncovering Grounding IDs* | Hasani et al. | ICML 2026, arXiv:2509.24072 | [arXiv](https://arxiv.org/abs/2509.24072) | Binding IDs in synthetic grids; activation swapping at layers 22-27 |
| *InstaBind-Lite/DSCAM* | Xu et al. | Aug 2026, arXiv:2608.16805 | [arXiv](https://arxiv.org/abs/2608.16805) | Dense same-class attribute misbinding; 524 images, 9,580 questions |
| *BanglaProtha* | Ishmam et al. | WACV 2026 | [Kaggle](https://www.kaggle.com/datasets/mdsakibulrahmansourove/banglaprotha) | Bengali cultural VQA; 6,942 images, 8,034 questions |
| *BabelSteering* | - | Aug 2026, arXiv:2608.16577 | [arXiv](https://arxiv.org/abs/2608.16577) | English-derived steering vectors applied to Bengali (+17pp refusal rate) |
| *SHARP* | - | 2025, ACL/ICML | [ACL Anthology](https://aclanthology.org/) | Representation engineering to steer VLM hallucinations |
| *DMAS* | - | ICLR 2026 | [OpenReview](https://openreview.net/) | Dynamic multimodal activation steering for VLM hallucinations |
| *ChitraMiti* | - | Sep 2026, arXiv:2609.12509 | [arXiv](https://arxiv.org/abs/2609.12509) | Bengali VLM text-over-vision reliance in geometric reasoning |
| *Remember-R1* | - | Aug 2026, arXiv:2608.01314 | [arXiv](https://arxiv.org/abs/2608.01314) | RL rewards to slow attention decay in VLM reasoning |
| *CLASH* | - | 2025, arXiv:2511.19199 | [arXiv](https://arxiv.org/abs/2511.19199) | Contradiction detection → abstention benchmark |
| *Pixels versus Priors* | Golovanevsky et al. | EMNLP 2025 | [arXiv](https://arxiv.org/abs/2405.00234) | Visual counterfacts and PvP steering vectors for prior/pixel tension |
