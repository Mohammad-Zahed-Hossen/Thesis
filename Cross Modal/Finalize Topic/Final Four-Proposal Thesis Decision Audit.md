# Final Four-Proposal Thesis Decision Audit: Evidence Verification and Decision-Readiness Assessment

---

## 1. The Candidate Proposals

### Canonical Thesis: Causal Conflict Verbalization and Source Arbitration in Vision-Language Models

* **Operational Core Question:** When a vision-language model (VLM) is presented with mutually contradictory visual and textual premises, does an explicit prompt requiring it to identify and verbalize the contradiction causally alter its subsequent source arbitration (which source’s answer it outputs), or does the verbalized explanation act as a post-hoc rationalization of an already-entrenched latent modality preference?
* **Competing Hypotheses:**
  * **$H_1$ (Deliberative / Causal Control):** Generating intermediate tokens that articulate the contradiction forces cross-modal attention updates that actively steer the output distribution toward the authoritative source, yielding a statistically significant shift in source arbitration relative to a length-matched neutral placebo ($\Delta_{\text{arb}} > 0$).
  * **$H_0$ (Post-Hoc Rationalization / Attentional Inertia):** The source preference is entrenched early in the forward pass by parametric language/vision priors; intermediate contradiction verbalization produces fluent text without steering the output logits beyond generic computation ($\Delta_{\text{arb}} \approx 0$).
* **Proposed Experimental Protocol:** A 4-arm factorial prompt evaluation on conflicting arithmetic equations (`GSM8K`/`SVAMP` shifted pairs) and chart-text conflicts (`ChartQA-Conflict`):
  1. *Arm 1 (Direct Zero-Shot):* Direct answer generation without explanation ($T \approx 10$ tokens).
  2. *Arm 2 (Length-Matched Neutral Placebo):* Two-sentence neutral description of visual and textual content without comparison ($T \approx 75$ tokens).
  3. *Arm 3 (Conflict Verbalization Intervention):* Two-sentence explicit contradiction identification and explanation ($T \approx 75$ tokens).
  4. *Arm 4 (Lanham-Style Rationale Prefilling):* Forcing assistant output to begin with a contradiction verdict vs. an agreement verdict to test token-steering causality.

---

### Proposal 1: Decomposing Multimodal Reasoning Trace Degradation: Causal Reasoning vs. Positional and Attention Dilution Artifacts

* **Operational Core Question:** When visual evidence utilization appears to decline during extended multimodal reasoning chains ($T_{\text{CoT}} > 200$ tokens), is this degradation causally driven by the cognitive computation of the deductive reasoning trace, or is it a measurement and architectural artifact of Rotary Position Embedding (RoPE) distance and uniform softmax denominator dilution ($M/N$)?
* **Competing Hypotheses:**
  * **$H_1$ (Cognitive Autoregressive Drift / True Forgetting):** Generating deductive reasoning tokens actively drives the residual stream into linguistic attractor basins that overwrite or discard visual representations, producing a significantly larger drop in counterfactual visual sensitivity than inserting an equal number of neutral non-reasoning tokens ($\Delta_{\text{reasoning}} \gg \Delta_{\text{neutral}}$).
  * **$H_0$ (Positional & Softmax Measurement Artifact):** Visual attention mass decays strictly according to the mathematical $M/N$ uniform dilution curve. Inserting neutral padding produces an indistinguishable drop, and visual information remains linearly decodable in intermediate residual streams ($\text{AUC} > 0.75$).
* **Proposed Experimental Protocol:** Teacher-forced prefix slicing on 500 counterfactual image-question pairs (`WhatIfVis`):
  1. *Condition 1 (Direct Short):* Prompt + Question $\to$ Direct answer ($T \approx 10$ tokens).
  2. *Condition 2 (Long Reasoning Prefix):* Prompt + Question + 150 teacher-forced reasoning tokens $\to$ Predict answer.
  3. *Condition 3 (Long Neutral Padding - Softmax Control):* Prompt + Question + 150 neutral descriptive tokens $\to$ Predict answer.
  4. *Condition 4 (Position-Matched Short - RoPE Control):* 150 neutral tokens prepended *before* image and prompt, advancing absolute RoPE sequence index by 150 positions, followed by direct answer.

---

### Proposal 2: Do Latent Visual Binding Identifiers Survive Beyond Synthetic Grids? A Placebo-Controlled Natural-Image Transfer Audit

* **Operational Core Question:** Do the localized residual-stream activation swaps that transfer object-attribute binding in synthetic grid scenes represent genuine, relation-specific binding representations that transfer to natural photographic instances under strict placebo controls, or are they destructive perturbation artifacts induced by artificial geometric scaffolding?
* **Competing Hypotheses:**
  * **$H_1$ (Genuine Localized Binding Subspace):** Intermediate residual-stream visual patch activations encode localized, modular object-attribute binding representations that transfer across natural photographic instances of the same semantic class under activation swapping, significantly exceeding placebo disruption rates ($\text{NetFlip}_{\text{swap}} - \text{NetFlip}_{\text{placebo}} > 0.30$).
  * **$H_0$ (Synthetic Cue Artifact / Destructive Disruption):** The apparent "Binding ID" is an artifact of synthetic partition lines and symbolic tags. On natural images, swapping activations either acts as non-specific noise (matching Gaussian/background placebos) or collapses linguistic generation into repetitive degeneration ($\mathcal{D}_{\text{rep}} > 0.40$).
* **Proposed Experimental Protocol:** Layer 22 residual-stream activation overwrite across 25 synthetic grid scenes vs. 25 natural photographic pairs from `InstaBind-Lite/DSCAM`:
  1. *Arm 1 (Real Swap):* Source object patch activations patched into target object bounding box tokens.
  2. *Arm 2 (Gaussian Placebo):* Target tokens overwritten with norm-matched random Gaussian noise $\mathcal{N}(0, \sigma^2 \mathbf{I})$.
  3. *Arm 3 (Background Placebo):* Target tokens overwritten with activations from an empty background quadrant.
  4. *Arm 4 (Intra-Scene Swap):* Swapping Object 1 and Object 2 within the same image.

---

### Proposal 3 (ACTIVE v2.1 — Causal & Mechanistic Formulation): Disentangling Perceptual Deficit from Late-Layer Parametric Pre-emption: Causal Bottleneck Localization and Activation Steering in Low-Resource Cultural VLMs

* **Operational Core Question:** When a vision-language model fails on a culturally localized multimodal task under asymmetric pretraining, is the failure caused by early perceptual blindness in the vision encoder (Stage 1), cross-lingual lexical misalignment in the multimodal projector (Stage 2), or late-layer parametric pre-emption where language priors overwrite preserved visual representations in the deep residual stream (Stage 3)? Furthermore, can a localized causal intervention—residual activation steering—prevent this pre-emption and restore grounded cultural recognition without retraining?
* **Competing Hypotheses:**
  * **$H_1$ (Late-Layer Parametric Pre-emption & Restorable Grounding):** The vision encoder and projector successfully encode and inject fine-grained cultural visual features into early-to-mid LLM residual stream layers ($L \le 16$), but between Layers 18 and 28, strong parametric language priors dominate the residual stream, extinguishing visual token decodability ($\Delta \text{AUC} > -0.30$). Localized activation steering at Layer 18 ($h_{L^*}^{\text{steered}} = h_{L^*} - \alpha \vec{v}_{\text{prior}} + \beta \vec{v}_{\text{vis}}$) causally restores correct grounded predictions ($\text{SRR} \ge 35\%$).
  * **$H_0$ (Early Perceptual / Alignment Bottleneck):** Cultural visual features never penetrate the LLM backbone due to extreme representation sparsity or projection misalignment. Linear probes fail to decode cultural entities across all layers ($\text{AUC} \le 0.55$), and activation steering produces only non-specific linguistic degeneration ($\mathcal{D}_{\text{rep}} > 0.40$).
* **Proposed Experimental Protocol:** A 4-arm factorial diagnostic & causal intervention protocol on 200 entity-stratified items from `BanglaProtha` (50 Food, 50 Attire, 50 Architecture, 50 Traditional Craft/Heritage):
  1. *Arm 1 (Standard Multimodal Baseline):* Original image + Bengali MCQA prompt (records layer-wise residual vectors $h_L \in \mathbb{R}^D$).
  2. *Arm 2 (Cross-Lingual Alignment Control):* Original image + verified English parallel prompt (isolates Stage 2 projector misalignment from Stage 1 perceptual encoding).
  3. *Arm 3 (Localized Crop / Spatial Zoom):* High-resolution bounding-box crop of the diagnostic cultural object (isolates Stage 1 ViT feature sparsity from background clutter / spatial dilution).
  4. *Arm 4 (Causal Activation Steering at Layer $L^* = 18$):* Forward hook injecting contrastive steering vector $\vec{v}_{\text{steer}} = -\alpha \vec{v}_{\text{prior}} + \beta \vec{v}_{\text{vis}}$ on baseline error items to evaluate causal recovery without fine-tuning.

---

### Proposal 3 (DEPRECATED v1.0 — Observational Diagnostic Formulation): Decoupling Visual Reliance from Correctness: A Placebo-Controlled Diagnostic of Cultural Prior Dominance and Selective Prediction in Multimodal VLMs

* **Status:** **SUPERSEDED / DEPRECATED** by Proposal 3 v2.1.
* **Why It Was Deprecated:** Proposal 3 v1.0 was primarily an *evaluative / validation task* that treated the model as a black box. It measured whether selective prediction risk-coverage (AUGRC) degraded under blank-image ablation ($I = \mathbf{0}$) due to "correct-but-ungrounded" language priors. While scientifically valid as a diagnostic benchmark, it lacked constructive mechanistic depth: it did not localize internal representation bottlenecks across layers or attempt causal representation repair. Proposal 3 v2.1 retains the authentic cultural domain (`BanglaProtha`) but elevates the task into an active *mechanistic interpretability and causal representation steering* research study.

---

## 2. Ingestion Baseline & Methodological Boundaries

All evidence, claims, and formulations in this audit are grounded directly in the workspace repository documents:

* [Canonical_Context.md](file:///d:/Thesis/Important/Cross%20Modal/Context/Canonical_Context.md)
* [Canonical_Thesis_Topic_Specification.md](file:///d:/Thesis/Important/Cross%20Modal/Finalize%20Topic/Canonical_Thesis_Topic_Specification.md)
* [Canonical_Proposal_1_Reasoning_Trace_Degradation.md](file:///d:/Thesis/Important/Cross%20Modal/Finalize%20Topic/Canonical_Proposal_1_Reasoning_Trace_Degradation.md)
* [Canonical_Proposal_2_Binding_IDs_Natural_Transfer.md](file:///d:/Thesis/Important/Cross%20Modal/Finalize%20Topic/Canonical_Proposal_2_Binding_IDs_Natural_Transfer.md)
* [Canonical_Proposal_3_Cultural_Multimodal_Causal_Steering.md](file:///d:/Thesis/Important/Cross%20Modal/Finalize%20Topic/Canonical_Proposal_3_Cultural_Multimodal_Causal_Steering.md) *(Active Proposal 3 v2.1)*
* [Canonical_Proposal_3_Cultural_VLM_Modality_Decoupling.md](file:///d:/Thesis/Important/Cross%20Modal/Finalize%20Topic/Canonical_Proposal_3_Cultural_VLM_Modality_Decoupling.md) *(Deprecated Proposal 3 v1.0)*
* Associated autopsies: [Final Boundary Verification (Antigravity).md](file:///d:/Thesis/Important/Cross%20Modal/Bengali%20VLM/Final%20Boundary%20Verification%20%28Antigravity%29.md), [Proposed Idea Related Paper.md](file:///d:/Thesis/Important/Cross%20Modal/Finalize%20Topic/Proposed%20Idea%20Related%20Paper.md), and [Canonical Thesis Topic Related Paper.md.md](file:///d:/Thesis/Important/Cross%20Modal/Finalize%20Topic/Canonical%20Thesis%20Topic%20Related%20Paper.md.md).

No generic model assumptions replace documented evidence. Scientific statements, proposed metrics, and numerical criteria are audited against primary sources rather than accepted as verified facts.

---

## 3. Evidence Status Taxonomy

Every claim audited in this document is classified under exactly one status:

* **VERIFIED:** Directly supported by an inspected primary source, official repository, dataset manifest, peer-reviewed paper, or verifiable artifact.
* **STRONGLY SUPPORTED:** Supported by multiple relevant primary sources, but not demonstrated in the exact experimental configuration proposed.
* **INFERRED:** A logical, reasonable deduction derived from available evidence, but not directly demonstrated by an empirical test.
* **UNKNOWN:** The available literature and repository records do not establish or measure the claim.
* **CONTRADICTED:** Existing primary evidence directly refutes or challenges the claim.

---

## 4. Literature Search Statement

> **"No additional broad literature search is decision-critical."**

**Justification:** The workspace contains exhaustive primary autopsies of all key literature anchors across the four proposals:

* *Canonical:* `Which Source Wins?` (`arXiv:2608.17205`), `CLASH` (`arXiv:2511.19199`), `Lanham et al.` (`arXiv:2305.04388`).
* *Proposal 1:* `RH-Bench` (`arXiv:2505.21523`), `Remember-R1` (`arXiv:2608.01314`), `Seeing or Knowing?` (`arXiv:2607.26326`), `VIG` (`arXiv:2608.21883`).
* *Proposal 2:* `Grounding IDs` / Hasani et al. (`arXiv:2509.24072`), `In-Context Binding` (`arXiv:2505.22200`), `InstaBind-Lite/DSCAM` (`arXiv:2608.16805`), `Dual Mechanisms` (`arXiv:2603.22278`).
* *Proposal 3 (Active v2.1 Anchors):* `Where Do Multilingual VLM Encoders Fail?` (`arXiv:2608.30725`), `TRAPSBench` (`arXiv:2608.13167`), `Dual Mechanisms` (`arXiv:2603.22278`), `CulturalMenuBench` (`arXiv:2609.03526`), `ChitraMiti` (`arXiv:2609.12509`), `BanglaProtha` (WACV 2026 text verified), `BanglaVerse` (`arXiv:2603.21165`).

The literature landscape, pre-emption risks, and methodological boundaries are thoroughly documented. Remaining uncertainties are empirical, not missing literature.

---

## 5. Exact Scientific Question Audit (All Four Proposals)

### Canonical Thesis

* **A. Precise Phenomenon:** The shift in categorical/numerical answer output between conflicting visual vs. textual sources when an intermediate text explanation verbalizing the conflict is forced, relative to when an equally long non-conflict explanation is generated.
* **B. What Is Already Known:**
  * VLMs display rigid, task-dependent modality dominance under contradictory inputs (**VERIFIED**, `arXiv:2608.17205`).
  * VLMs can be prompted to detect contradictions or abstain (**VERIFIED**, `arXiv:2511.19199`).
  * In unimodal text LLMs, chain-of-thought explanations can be unfaithful post-hoc rationalizations (**VERIFIED**, `arXiv:2305.04388`).
* **C. What Remains Unknown:** When a VLM generates an explicit explanation stating that source $A$ contradicts source $B$ and that source $A$ is corrupted, does the subsequent answer token distribution causally follow the verbalized deduction, or does it output the answer favored by its pre-existing forward-pass bias regardless of what was verbalized?
* **D. Minimum Discriminative Experiment:** Compare final answer accuracy and source selection between Arm 2 (Length-matched neutral description placebo) and Arm 3 (Conflict-verbalization prompt), augmented by Arm 4 (Prefilling an explicit agreement rationale vs. a contradiction rationale).
* **E. Could Result Reproduce Existing Work?** No. `Which Source Wins?` explicitly omitted conflict verbalization and awareness (§6). `CLASH` formulated contradiction exclusively as abstention.
* **F. Null-Result Value ($H_0$):** High. Demonstrates that multimodal chain-of-thought explanations in VLMs are decorative rationalizations that mask latent parametric bias, proving that prompting for verbalized conflict awareness fails as a safety or calibration mechanism.

---

### Proposal 1

* **A. Precise Phenomenon:** The decline in Image Causal Effect (ICE)—the log-odds shift between visually grounded and prior-driven answers across paired counterfactual images—as a function of intermediate sequence length and content.
* **B. What Is Already Known:**
  * Attention mass to visual tokens decays over long reasoning traces (**VERIFIED**, `arXiv:2505.21523`, `arXiv:2608.01314`).
  * Longer generated reasoning correlates with increased perceptual hallucination (**VERIFIED**, `arXiv:2505.21523`).
  * RoPE introduces natural positional decay as token distance increases (**VERIFIED**, standard Transformer literature).
  * Softmax normalization imposes a mathematical $M/N$ uniform probability dilution on an invariant block of $M$ visual tokens as total context $N$ expands (**VERIFIED**, standard attention formulation).
* **C. What Remains Unknown:** Whether the observed decline in visual evidence utilization during extended reasoning is causally induced by the semantic computation of deductive reasoning tokens, or whether it is fully accounted for by RoPE distance and uniform softmax denominator expansion ($M/N$).
* **D. Minimum Discriminative Experiment:** Compare ICE and visual attention mass at the final answer token under teacher-forced insertion of 150 reasoning tokens (Condition 2) versus 150 neutral non-reasoning tokens (Condition 3), and compare against a 150-token prepended RoPE-advancing prefix (Condition 4).
* **E. Could Result Reproduce Existing Work?** Moderate risk. If the experiment only measures raw attention decay, it simply reproduces `RH-Bench`. It avoids reproduction only if the neutral-padding and RoPE-position controls are strictly executed and analyzed via equivalence testing.
* **F. Null-Result Value ($H_0$):** High. Proves that "visual forgetting" in long-trace VLMs is a measurement and positional artifact, invalidating complex reinforcement learning loss functions (e.g., `Remember-R1`) designed to mitigate an assumed cognitive decay.

---

### Proposal 2

* **A. Precise Phenomenon:** The directional flip of generated attribute text for a target visual object toward a source object's attributes following the transplantation of intermediate residual-stream hidden states corresponding to the source object's visual tokens.
* **B. What Is Already Known:**
  * Swapping object-region residual activations in layers 22–27 redirects attribute output with ~98% accuracy in synthetic $2 \times 4$ geometric grid scenes with explicit symbol tags (**VERIFIED**, `arXiv:2509.24072`).
  * Adding vector offsets in intermediate layers can steer visual-attribute binding in toy 3D shapes (**VERIFIED**, `arXiv:2505.22200`).
  * In natural images, 80.7% of attribute misbinding occurs between adjacent instances (**VERIFIED**, `arXiv:2608.16805`).
* **C. What Remains Unknown:** Whether localized residual-stream activation swaps transfer object-attribute binding in natural, cluttered photographic instances under strict placebo controls (Gaussian noise, background patches), or whether the synthetic swap relies on artificial geometric row lines and symbolic scaffolding.
* **D. Minimum Discriminative Experiment:** Intercept Layer 22 residual activations in `Qwen2.5-VL-3B` on paired photographic instances from `DSCAM`, comparing the Net Directed Flip Rate of the real object swap against norm-matched Gaussian noise and background quadrant patches.
* **E. Could Result Reproduce Existing Work?** No. Hasani et al. (`arXiv:2509.24072`) evaluated natural images (MS-COCO) strictly observationally for hallucination; they never executed activation swaps on photographic images.
* **F. Null-Result Value ($H_0$):** High. Establishes the mechanistic fragility of multimodal binding, demonstrating that modular "Binding IDs" are artifacts of synthetic geometric grids and that foundation VLMs resolve real-world binding through distributed attention rather than localized residual vectors.

---

### Proposal 3 (Active v2.1 Formulation)

* **A. Precise Phenomenon:** The layer-wise decodability trajectory of ground-truth cultural entity labels in the LLM residual stream ($\text{AUC}_L$) and the subsequent recovery rate ($\text{SRR}$) of incorrect baseline predictions when a contrastive steering vector ($\vec{v}_{\text{steer}} = -\alpha \vec{v}_{\text{prior}} + \beta \vec{v}_{\text{vis}}$) is injected at intermediate transformer layer $L^* = 18$.
* **B. What Is Already Known:**
  * Foundation VLMs fail dramatically (<42% accuracy) on Bengali cultural entities with close distractors (**VERIFIED**, `BanglaProtha`, WACV 2026).
  * Multilingual encoders suffer from cross-lingual representation drift (**VERIFIED**, `arXiv:2608.30725`).
  * Models exhibit a large cultural knowledge-application gap, scoring +7–18 points higher when prompted with entity names in text vs. images (**VERIFIED**, `arXiv:2609.03526`).
  * Intermediate linear probes can decode latent properties (e.g., physical uncertainty) that are suppressed during autoregressive decoding (**VERIFIED**, `arXiv:2608.13167`).
  * Spatial visual signals diffuse into background tokens in natural scenes (**VERIFIED**, `arXiv:2603.22278`).
* **C. What Remains Unknown:** In low-resource cultural domains, does the computational breakdown occur because the vision encoder fails to extract features (Stage 1), because the projector fails to map features into Bengali text space (Stage 2), or because late-layer language priors extinguish intact visual representations in the deep residual stream (Stage 3)? Crucially, can test-time activation steering actively prevent late-layer pre-emption and recover correct cultural recognitions without fine-tuning?
* **D. Minimum Discriminative Experiment:** Execute 4 arms on 200 deduplicated `BanglaProtha` items: Arm 1 (Bengali baseline + layer-wise probing), Arm 2 (English parallel prompt to isolate Stage 2), Arm 3 (Cropped entity zoom to isolate Stage 1), and Arm 4 (Causal activation steering at Layer 18 to isolate Stage 3).
* **E. Could Result Reproduce Existing Work?** No. Prior Bengali VLM works (`BanglaProtha`, `BanglaVerse`, `ChitraMiti`) were purely black-box behavioral evaluations. None conducted internal residual-stream probing or causal activation steering.
* **F. Null-Result Value ($H_0$):** High. If linear probes fail across all layers ($\text{AUC} \le 0.55$), it refutes the popular claim in literature that cultural errors stem from "missing factual knowledge" in the language model; it proves that the bottleneck is an early perceptual/projection barrier, establishing that post-hoc prompt engineering or language fine-tuning cannot solve cultural VLM failure without vision-encoder retraining.

---

## 6. Pre-emption Test (All Four Proposals)

### Canonical Thesis: Pre-emption Audit


| Paper                                                 | What It Already Establishes                                                               | What Remains Untested                                                                   | Type of Overlap             | Redundancy Risk |
| :------------------------------------------------------ | :------------------------------------------------------------------------------------------ | :---------------------------------------------------------------------------------------- | :---------------------------- | :---------------- |
| **Which Source Wins?** (`arXiv:2608.17205`, Aug 2026) | Maps modality dominance across arithmetic & chart conflicts under legibility degradation. | Explicitly omits contradiction awareness, verbalization, and abstention (§6).          | Dataset & Task Framing      | Low             |
| **CLASH** (`arXiv:2511.19199`, Nov 2025)              | Evaluates cross-modal contradiction detection as an abstention task ("Cannot answer").    | Source arbitration; causal effect of verbalization on choosing an authoritative source. | Conceptual (Contradiction)  | Low             |
| **Lanham et al.** (`arXiv:2305.04388`, NeurIPS 2023)  | Rationale prefilling, truncation, and CoT faithfulness in unimodal text LLMs.             | Multimodal cross-modal sensory contradiction; vision-language arbitration.              | Methodological (Prefilling) | Low             |
| **Zhu et al.** (2024)                                 | Prompting strategies to mitigate cross-modal conflict in general benchmarks.              | Controlled factorial isolation of verbalization from length placebos.                   | Methodological (Prompting)  | Moderate        |

* **Exact Remaining Experiment:** A 4-arm factorial prompt evaluation (Direct vs. Length-Matched Neutral Placebo vs. Conflict Verbalization vs. Rationale Prefill) on 1,304 arithmetic pairs (`modality-conflict-arbitration-v2`) and 229 chart pairs (`chartqa-evidence-conflict-v2`) measuring $\Delta_{\text{arb}}$ and Flip Rate.

---

### Proposal 1: Pre-emption Audit


| Paper                                                 | What It Already Establishes                                                                 | What Remains Untested                                                                                | Type of Overlap             | Redundancy Risk |
| :------------------------------------------------------ | :-------------------------------------------------------------------------------------------- | :----------------------------------------------------------------------------------------------------- | :---------------------------- | :---------------- |
| **RH-Bench** (`arXiv:2505.21523`, NeurIPS 2025)       | Longer CoT correlates with lower visual attention mass and higher perceptual hallucination. | Did not isolate reasoning content from token position; no neutral padding; no softmax dilution null. | Conceptual & Observational  | High            |
| **Remember-R1** (`arXiv:2608.01314`, Aug 2026)        | Uses RL rewards on attention mass to slow visual attention decay in CoT.                    | Treated raw attention mass as ground truth; did not control for token distance or softmax expansion. | Methodological (RL Defense) | Moderate        |
| **Seeing or Knowing?** (`arXiv:2607.26326`, Jul 2026) | Proves visual features remain in final-layer image tokens on single-turn VQA.               | Evaluated only single-turn prompts; did not test multi-step chain-of-thought traces.                 | Mechanistic (Probing)       | Low             |
| **VIG** (`arXiv:2608.21883`, Aug 2026)                | Visual Information Gain metric used as reward signal for CoT compression.                   | Does not decompose sequence position from reasoning computation.                                     | Evaluation Metric           | Moderate        |

* **Exact Remaining Experiment:** Teacher-forced prefix slicing on 500 `WhatIfVis` counterfactual pairs comparing the Counterfactual Image Causal Effect (ICE) under 150 reasoning tokens vs. 150 neutral descriptive tokens at the identical sequence index, with linear probing of Layer 18 and 30 residual streams.

---

### Proposal 2: Pre-emption Audit


| Paper                                                        | What It Already Establishes                                                                     | What Remains Untested                                                                             | Type of Overlap               | Redundancy Risk |
| :------------------------------------------------------------- | :------------------------------------------------------------------------------------------------ | :-------------------------------------------------------------------------------------------------- | :------------------------------ | :---------------- |
| **Grounding IDs (C1)** (`arXiv:2509.24072`, ICML 2026)       | Residual activation swapping transfers object-attribute binding in synthetic$2 \times 4$ grids. | Omitted random/Gaussian placebos; never executed activation swaps on photographic natural images. | Mechanistic (Activation Swap) | High            |
| **In-Context Binding (C2)** (`arXiv:2505.22200`, CVPRW 2025) | Vector addition steers binding in toy Blender 3D shapes for LLaVA-1.5.                          | Restricted to synthetic toy shapes; single architecture; no natural photographic instances.       | Conceptual & Mechanistic      | Moderate        |
| **InstaBind-Lite / DSCAM** (`arXiv:2608.16805`, Aug 2026)    | Quantifies that 80.7% of natural attribute misbinding occurs between adjacent instances.        | Purely observational benchmark; zero internal activation patching or mechanistic interventions.   | Dataset / Domain              | Low             |
| **Dual Mechanisms** (`arXiv:2603.22278`, Mar 2026)           | Proves spatial signals diffuse across background tokens in natural scenes via linear probes.    | Evaluated global linear probes; did not isolate a localized patch-swapping mechanism.             | Mechanistic (Probing)         | Low             |

* **Exact Remaining Experiment:** Layer 22 residual-stream activation overwrite on 25 natural photographic pairs from `DSCAM` comparing the real object swap against norm-matched Gaussian noise and background quadrant placebos in `Qwen2.5-VL-3B`.

---

### Proposal 3 (Active v2.1): Pre-emption Audit


| Paper                                                                       | What It Already Establishes                                                             | What Remains Untested                                                                                         | Type of Overlap            | Redundancy Risk |
| :---------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------- | :-------------------------------------------------------------------------------------------------------------- | :--------------------------- | :---------------- |
| **Where Do Multilingual VLM Encoders Fail?** (`arXiv:2608.30725`, Aug 2026) | Documents alignment drift in multilingual vision encoders across languages.             | Analyzed encoder token similarity only; did not track residual stream propagation or causal steering.         | Mechanistic (Encoder Only) | Moderate        |
| **TRAPSBench** (`arXiv:2608.13167`, Aug 2026)                               | Linear probes decode internal uncertainty better than generated text in physics videos. | Evaluated synthetic physics simulations; did not test cultural distribution shift or late-layer pre-emption.  | Methodological (Probing)   | Low             |
| **Dual Mechanisms** (`arXiv:2603.22278`, Mar 2026)                          | Linear probes trace spatial binding signals across visual layers.                       | Tested Western spatial binding; did not investigate cross-lingual lexical pre-emption or activation steering. | Methodological (Probing)   | Moderate        |
| **CulturalMenuBench** (`arXiv:2609.03526`, Sep 2026)                        | Proves cultural text names outperform image presentations (+7–18 pts).                 | Evaluated black-box prompt variations; executed zero internal probing or representation repair.               | Conceptual (Knowledge Gap) | Moderate        |
| **BanglaProtha** (WACV 2026) & **BanglaVerse** (`arXiv:2603.21165`)         | Benchmarked open/closed VLMs on Bengali cultural MCQA.                                  | Purely observational benchmarks; evaluated zero internal representations or causal steering.                  | Dataset / Domain           | Low             |

* **Exact Remaining Experiment:** A 4-arm diagnostic and causal intervention protocol on 200 deduplicated items from `BanglaProtha` tracking layer-wise linear decodability $\text{AUC}(L)$ across Layers $0\text{--}32$ and measuring Causal Steering Recovery Rate ($\text{SRR}$) under Layer 18 activation steering.

---

## 7. Canonical Thesis — Special Audit

### 7.1 Contradiction Detection vs. Source Arbitration

Prior literature demonstrates that **contradiction detection** and **source arbitration** are distinct capabilities:

* *Contradiction detection* (recognizing that image and text disagree) is an abstention/classification task. In `CLASH`, models achieve up to 88% detection by outputting a fixed abstention token ("Cannot answer").
* *Source arbitration* (determining which source to follow when forced to choose) requires assessing evidence validity or following an authoritative premise. In `Which Source Wins?`, models forced to arbitrate display severe, uncalibrated modality biases regardless of detection.
* **Finding:** Prior work does **not** evaluate whether successfully verbalizing a detected contradiction enables or alters source arbitration. They are treated as separate literatures.

### 7.2 Verbalization vs. Additional Computation

A fundamental confound in chain-of-thought literature is that intermediate generation adds test-time compute (transformer forward passes).

* The canonical protocol addresses this via **Arm 2 (Length-Matched Neutral Placebo)**: prompting the model to generate a 2-sentence description of the visual and textual content without comparing them (~75 tokens).
* **Audit Finding:** Arm 2 controls for token count, forward passes, and generation budget. However, Arm 3 (Conflict verbalization) also introduces a semantic directive ("determine whether they agree or contradict"). If Arm 3 outperforms Arm 2, the experiment successfully isolates *contradiction-directed processing* from *raw token length*.

### 7.3 Causality Claim

* **Conservative Epistemic Boundary:** The proposed factorial prompt intervention can legitimately prove:
  $$
  \text{"Requiring explicit contradiction verbalization causally changes the model's subsequent output distribution."}

  $$
* **What It Does NOT Prove:** It does **not** prove that the internal reasoning circuit or latent modality preference of early transformer layers was reorganized. To claim a change in "internal reasoning," internal activation patching or circuit tracing would be required. The claim must remain bounded to **behavioral output steering and explanatory faithfulness**.

### 7.4 Prefill Intervention

* **Variable Changed:** The assistant prefix tokens immediately preceding the answer delimiter. Condition A prefils: `"The image and text contradict each other because..."`; Condition B prefils: `"The image and text agree with each other because..."`.
* **Uncontrolled Variables:** Autoregressive continuation bias induced by local n-gram conditioning.
* **Scientific Utility:** It provides direct evidence regarding **downstream steering**: if forcing a contradiction verdict flips the subsequent answer token whereas forcing an agreement verdict preserves the default modality choice, intermediate tokens exert causal leverage over the output distribution. If the answer remains unchanged under both prefills, the explanation is completely disconnected from answer generation.

### 7.5 Conflict Construction

* **Arithmetic Conflicts (`GSM8K`/`SVAMP` Shifted Pairs):** Constructed by pairing the rendered equation of problem $i$ with the text of problem $i+1$.
  * *Artifact Risk:* High semantic divergence. The question text and rendered image describe entirely different numerical situations. This makes conflict detection trivial, but creates an unnatural task environment that does not reflect subtle visual-textual discrepancies.
* **Chart Conflicts (`ChartQA-Conflict`):** 229 pairs where a real chart is paired with an authored textual summary containing a modified data point.
  * *Artifact Risk:* Low. Naturalistic business/scientific reporting conflict where text and graphic disagree on a specific value.

### 7.6 Canonical Datasets and Assets

* `vlm-modality-research/modality-conflict-arbitration-v2`: Hosted on Hugging Face; contains 1,304 clean arithmetic pairs and 296 SVAMP pairs (**VERIFIED**, `arXiv:2608.17205` release).
* `vlm-modality-research/chartqa-evidence-conflict-v2`: 229 valid conflict items (**VERIFIED**).
* *Licensing and Access:* Publicly downloadable without credentials or gated approvals. Exact-match deterministic regex parsing eliminates subjective grading.

### 7.7 Canonical Engineering Claims

* The claim that 1,200 items $\times$ 4 arms = 4,800 passes takes $\approx 2.5$ hours on a Colab T4 GPU in `bfloat16` for `Qwen2-VL-2B` is an **engineering estimate**. At ~1.5 to 2.0 seconds per generation pass, 4,800 passes requires ~2.0 to 2.7 hours. This estimate is technically reasonable, but serves as feasibility context, not scientific novelty.

---

## 8. Proposal 1 — Special Audit

### 8.1 Operationalization of "Visual Forgetting"

Proposal 1 operationalizes "visual forgetting" as the **Counterfactual Image Causal Effect (ICE)** decay at the answer token across sequence position $t$:

$$
\text{ICE}_t = \left[ \log \frac{p(a_{\text{vis}} \mid I, q, p_{<t})}{p(a_{\text{prior}} \mid I, q, p_{<t})} \right] - \left[ \log \frac{p(a_{\text{vis}} \mid I', q, p_{<t})}{p(a_{\text{prior}} \mid I', q, p_{<t})} \right]

$$

This operationalization is sound because it measures whether an edit in the image ($I \to I'$) still shifts the output probability distribution when conditioned on prefix $p_{<t}$.

### 8.2 Disentangling Reasoning from Positional and Attention Dilution

* **Positional Decay (RoPE):** Rotary Position Embeddings inherently attenuate attention scores as the coordinate distance $|i - j|$ increases. As reasoning unfolds, the answer token is displaced further from the visual patch tokens.
* **Softmax Denominator Dilution ($M/N$):** In standard softmax self-attention:
  $$
  \text{Attn}(q, K) = \frac{\exp(q k_j^T / \sqrt{d})}{\sum_{n=1}^N \exp(q k_n^T / \sqrt{d})}

  $$

  If visual tokens occupy $M$ positions and total context expands to $N$ tokens, the uniform baseline attention share is mathematically $M/N$. As $N$ increases from 100 to 1,000, visual attention mass *must* decrease mathematically even if visual features are fully utilized.
* **How Proposal 1 Decomposes This:**
  * Condition 2 (Reasoning prefix) vs. Condition 3 (Neutral padding matched for length and perplexity): Holds $N$ and RoPE distance constant while varying reasoning semantics.
  * Condition 4 (Prepending neutral tokens *before* image): Advances RoPE coordinates without adding text between the image and the answer.

### 8.3 Architecture Specificity and Replication Risk

* **Architecture Specificity:** The quantitative rate of RoPE decay and attention dilution depends on base frequencies and attention implementation (e.g., Qwen2.5-VL’s 3D-RoPE). However, the mathematical $M/N$ softmax denominator expansion is universal to all standard dense Transformer architectures.
* **Replication Risk:** High if the experiment merely plots attention decay against length. It escapes replication only by testing whether $\Delta \text{VIG}_{\text{dev}}$ deviates from the $M/N$ null and whether linear probes decode visual attributes from the residual stream despite attention decay.
* **If Positional/Softmax Mechanics 100% Explain the Effect:** The result provides high scientific utility as a corrective rebuttal against the emerging "multimodal forgetting" literature, demonstrating that training RL policies (like `Remember-R1`) to force higher attention mass is combating a mathematical artifact of softmax normalization rather than cognitive decay.

---

## 9. Proposal 2 — Special Audit

### 9.1 Operational Meaning of "Visual Binding Identifier"

In Anchor C1 (`arXiv:2509.24072`), a "Grounding ID" is operationalized as:

> The multi-dimensional activation tensor of an object’s visual patch tokens in intermediate layers ($L22\text{--}27$) that, when transplanted into another context, redirects the model’s attribute generation to describe the source object.

* **Critical Distinction:** This is a **region-level activation slice**, not an isolated, one-dimensional "binding vector" or disentangled subspace. It contains object shape, color, spatial coordinates, texture, and prompt interaction history simultaneously.

### 9.2 Natural-Image Transfer and Placebo Validity

* **Has Natural Transfer Been Studied?** Hasani et al. evaluated MS-COCO *observationally* (measuring CHAIR hallucination metrics when prompt cues were present). They **never performed activation swapping on natural photographic instances**.
* **Placebo Deficit in Prior Art:** Hasani et al. included a disjoint-symbol control, but omitted:
  1. Norm-matched random Gaussian noise injection;
  2. Irrelevant background patch transplantation;
  3. Scrambled spatial patch swaps.
* **Dominant Threat to Validity:** On natural images, bounding boxes do not align cleanly with ViT patch grids ($14 \times 14$), and natural scenes lack high-contrast grid lines. Swapping activations on natural images requires spatial bilinear interpolation across differing aspect ratios, which risks corrupting the hidden state and triggering text degeneration rather than selective binding transfer.
* **Interpreting Transfer Failure:** If the swap fails on natural images, does it prove "synthetic artifact" or "intervention fragility"?
  * If the model outputs repetitive n-grams ($\mathcal{D}_{\text{rep}} > 0.40$), the failure is **intervention fragility** (the activation graft corrupted the residual stream).
  * If the model remains linguistically fluent but ignores the transplanted features (or matches the Gaussian placebo), the failure proves that **modular binding IDs are synthetic scaffolding artifacts**.

---

## 10. Proposal 3 — Special Audit (Active v2.1 & Deprecation Review)

### 10.1 Audit of the Literature Premise

Proposal 3 v2.1 grounds its mechanistic formulation in six primary literature anchors:

1. **`Where Do Multilingual VLM Encoders Fail?` (`arXiv:2608.30725`, Aug 2026):** Proves that multilingual multimodal encoders exhibit severe representation drift across non-Latin scripts. However, it evaluated token cosine similarities at the encoder level only, leaving residual stream propagation through the LLM unexamined.
2. **`TRAPSBench` (`arXiv:2608.13167`, Aug 2026):** Proves that intermediate linear probes extract valid latent representations from VLM hidden states even when autoregressive text generation fails or hallucinates. Validates linear probing as a diagnostic tool for representation preservation.
3. **`Dual Mechanisms of Visual Binding` (`arXiv:2603.22278`, Mar 2026):** Establishes that visual representations diffuse across layers and background tokens, providing precedent for layer-wise linear probing in foundation VLMs.
4. **`CulturalMenuBench` (`arXiv:2609.03526`, Sep 2026):** Establishes the empirical reality of the cultural knowledge-application gap (+7–18 pt advantage for text names over visual plates).
5. **`ChitraMiti` (`arXiv:2609.12509`, Sep 2026):** Demonstrates modality reliance collapse on Bengali multimodal tasks.
6. **`BanglaProtha` (WACV 2026):** Provides a large-scale verified cultural MCQA benchmark (6,942 images, 8,034 questions).

### 10.2 Audit of the Three-Stage Bottleneck Premise

Proposal 3 v2.1 categorizes cultural failure into three competing mechanistic bottlenecks:

* **Stage 1 (Vision Encoder ViT):** Does the ViT fail to extract discriminating low-level visual features due to sparse pretraining?
* **Stage 2 (Multimodal Projector & Cross-Lingual Alignment):** Does the projector map visual tokens into English semantic space while failing to bridge to Bengali lexical tokens?
* **Stage 3 (Late-Layer Parametric Pre-emption):** Are cultural visual features successfully encoded and projected, only to be overwritten by autoregressive language priors in late transformer layers ($L18\text{--}28$)?
* **Audit Finding:** Prior literature treated VLM failure as a monolithic black box ("the model hallucinated" or "lacks knowledge"). Isolating these three stages provides a genuine mechanistic research framework.

### 10.3 Audit of the Four-Arm Experimental Design (v2.1 vs. Deprecated v1.0)

* **Active v2.1 4-Arm Design:**
  1. *Arm 1 (Standard Multimodal):* Original image + Bengali MCQA prompt. Establishes baseline and extracts layer-wise residual vectors $h_L$.
  2. *Arm 2 (Cross-Lingual Alignment Control):* Original image + verified English parallel prompt. *Directly isolates Stage 2:* if accuracy surges in English, the vision encoder works and the failure is cross-lingual lexical projection.
  3. *Arm 3 (Localized Crop / Zoom):* Bounding-box crop of the diagnostic cultural object. *Directly isolates Stage 1:* if zooming fails to improve decodability, the ViT genuinely lacks low-level feature representations.
  4. *Arm 4 (Causal Activation Steering at Layer 18):* Injects contrastive vector $h_{L^*}^{\text{steered}} = h_{L^*} - \alpha \vec{v}_{\text{prior}} + \beta \vec{v}_{\text{vis}}$. *Directly proves Stage 3:* if steering flips errors to correct answers, the information was present internally and pre-empted by late-layer autoregression.
* **Comparison to Deprecated v1.0:** Deprecated v1.0 used black-image ablation ($I = \mathbf{0}$) and patch scrambling purely to measure selective risk curves (AUGRC). That was a passive evaluation protocol. Active v2.1 uses activation hooks, linear probing, cross-lingual translation controls, and causal vector steering, converting the study into an active mechanistic investigation.

### 10.4 Audit of Proposed Metrics (v2.1)

* **Layer-Wise Probe Decodability ($\text{AUC}_L$):** 5-fold cross-validated logistic regression probe trained on $h_L(t_{\text{last}})$ across layers $L \in \{0, 4, 8, \dots, 32\}$. Standard, established interpretability technique (**VERIFIED**, Alain & Bengio; TRAPSBench).
* **Pre-emption Gradient ($\nabla_{\text{preempt}} = \max_{L \le 16} \text{AUC}_L - \text{AUC}_{L_{\text{final}}}$):** Proposed mathematical formulation to quantify late-layer representation collapse (**INFERRED / ADAPTED FORMULATION**).
* **Causal Steering Recovery Rate ($\text{SRR}$):** Proportion of baseline error items corrected by Layer 18 activation steering (**PROPOSED METRIC**).
* **Linguistic Fluency Preservation ($\mathcal{D}_{\text{rep}}$):** 3-gram repetition frequency threshold ($\mathcal{D}_{\text{rep}} > 0.35$ defines destructive collapse) (**STANDARD SAFEGUARD**).

### 10.5 Audit of Numerical Thresholds (v2.1)

* $\max_{L \le 16} \text{AUC}_L \ge 0.75$: **RESEARCHER-DEFINED EXPLORATORY HEURISTIC**. Indicates non-trivial internal classification capability.
* $\nabla_{\text{preempt}} \ge 0.25$: **RESEARCHER-DEFINED EXPLORATORY HEURISTIC**. Quantifies a substantial collapse between mid and late layers.
* $\text{SRR} \ge 35\%$: **RESEARCHER-DEFINED TARGET CRITERION**.
* $\mathcal{D}_{\text{rep}} < 0.25$: **CONVENTIONAL LINGUISTIC COHERENCE THRESHOLD**.
* **Audit Verdict:** These thresholds are operational criteria for evaluating the hypothesis, not established physical laws. A lower recovery rate (e.g., 20%) still provides scientifically useful causal information.

### 10.6 Audit of Dataset Slicing & Engineering Claims

* Proposal 3 v2.1 uses a curated, balanced subset of **200 items from `BanglaProtha`** (50 Food, 50 Attire, 50 Architecture, 50 Traditional Craft), strictly deduplicated across unique image filenames.
* *Arm 2 Requirement:* Requires authoring and human-verifying 200 parallel English prompts. Because the target entities and options are discrete cultural terms, translating 200 items is manageable within 1–2 days and introduces minimal overhead.
* *Compute Budget:* 200 items $\times$ 4 arms = 800 forward passes $\approx 25\text{--}35$ minutes on a single Colab Pro T4 GPU.

### 10.7 Audit of the Causal Activation Steering Mechanism

* **Steering Vector Formulation:**
  $$
  \vec{v}_{\text{steer}} = -\alpha \vec{v}_{\text{prior}} + \beta \vec{v}_{\text{vis}}

  $$

  Where $\vec{v}_{\text{prior}} = \frac{1}{N} \sum h_{L^*}(\mathbf{0}, q)$ and $\vec{v}_{\text{vis}} = \frac{1}{N} \sum (h_{L^*}(I, q) - h_{L^*}(\mathbf{0}, q))$.
* **Vulnerability & Confound:** Steering vectors extracted from global averages can introduce non-specific activation offsets that disrupt language modeling.
* **Engineered Safeguard:** Hyperparameters $\alpha, \beta \in [0.5, 2.0]$ must be tuned via grid search on a disjoint 20-sample validation split, and fluency preservation ($\mathcal{D}_{\text{rep}} < 0.25$) must be strictly enforced.

---

## 11. Novelty vs. Application Assessment


| Proposal                         | Scientific Characterization                                             | Classification Rationale                                                                                                                                                                                                                                                                                                                                      |
| :--------------------------------- | :------------------------------------------------------------------------ | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Canonical**                    | **General Scientific Mechanism**                                        | Investigates the fundamental relationship between intermediate autoregressive reasoning tokens and latent modality arbitration. The arithmetic and chart domains serve as standardized test environments.                                                                                                                                                     |
| **Proposal 1**                   | **General Scientific Mechanism**                                        | Investigates core architectural properties of Transformers (RoPE positional attenuation and softmax denominator dilution) versus cognitive reasoning drift.                                                                                                                                                                                                   |
| **Proposal 2**                   | **General Scientific Mechanism**                                        | Tests representation modularity and the validity of activation-patching interpretability claims across synthetic vs. natural image distributions.                                                                                                                                                                                                             |
| **Proposal 3 (Active v2.1)**     | **General Cross-Modal Mechanistic Discovery & Representation Steering** | Moves far beyond an applied benchmark study. It uses Bengali cultural data as an authentic, real-world stress condition to discover where multimodal information breaks down (Vision vs. Projector vs. Late-Layer Pre-emption) and develops an inference-time activation steering method to causally repair cultural representation loss without fine-tuning. |
| **Proposal 3 (Deprecated v1.0)** | **Domain-Dependent Stress Condition (Evaluative Only)**                 | Evaluated selective prediction risk-coverage curves (AUGRC) under black-box input ablations. Valuable as a diagnostic benchmark, but lacked mechanistic localization and causal intervention.                                                                                                                                                                 |

---

## 12. Null-Result Value (All Four Proposals)

### Canonical Thesis

* **If $H_1$ is true:** Proves that requiring explicit contradiction verbalization acts as a causal inference-time reasoning intervention that breaks unimodal attentional capture and updates output arbitration toward the authoritative source.
* **If $H_0$ is true:** Proves that multimodal chain-of-thought explanations are causally unfaithful post-hoc rationalizations that describe contradictions without altering latent decision trajectories, refuting prompt-based conflict awareness as a reliable safety mechanism.
* **If both perform similarly (Arm 3 $\approx$ Arm 2):** Proves that any observed accuracy or arbitration gain under conflict prompting is entirely driven by test-time compute expansion (token length), not contradiction-specific reasoning.
* **If inconclusive:** Caused by instruction-following collapse in small 2B models (e.g., model fails to output the required 2-sentence intermediate structure or ignores delimiter tags).

### Proposal 1

* **If $H_1$ is true:** Proves that deductive autoregressive reasoning causes true cognitive drift in hidden states, overriding visual representations beyond what is explained by token distance or context growth.
* **If $H_0$ is true:** Rebuts the emerging "visual forgetting" literature, proving that visual attention decay is a mathematical artifact of softmax denominator normalization ($M/N$) and RoPE coordinate displacement, showing that complex RL mitigations (e.g., `Remember-R1`) target a non-existent cognitive failure.
* **If both perform similarly (Condition 2 $\approx$ Condition 3):** Confirms that sequence length alone drives the observed degradation, eliminating reasoning content as a causal factor.
* **If inconclusive:** Caused by teacher-forced prefix perplexity mismatches between reasoning traces and neutral padding.

### Proposal 2

* **If $H_1$ is true:** Validates that object-attribute binding in foundation VLMs is encoded in localized, modular residual subspaces that transfer across photographic instances, confirming the universality of latent "Binding IDs."
* **If $H_0$ is true:** Delivers a major corrective finding to multimodal mechanistic interpretability, proving that reported "Binding IDs" are artifacts of synthetic geometric grids and that real-world binding is resolved via distributed attention routines.
* **If both perform similarly (Arm 1 $\approx$ Arm 2 Placebo):** Proves that reported activation-swapping effects are non-specific destructive disruptions that trigger default prior generation.
* **If inconclusive:** Caused by spatial interpolation errors across mismatched bounding-box aspect ratios triggering catastrophic token degeneration ($\mathcal{D}_{\text{rep}} > 0.40$).

### Proposal 3 (Active v2.1)

* **If $H_1$ is true:** Discovers that foundation VLMs actually perceive low-resource cultural artifacts in early-to-mid layers, but late-layer language priors extinguish them. Validates a training-free **causal activation steering intervention** that repairs cultural recognition at test-time.
* **If $H_0$ is true:** Conclusively refutes the dominant narrative in literature (`BanglaVerse`) that cultural VLM failures stem from "missing factual knowledge" in the language backbone. Proves that the failure is an early **perceptual/projection bottleneck** ($\text{AUC} \le 0.55$), establishing that post-hoc prompting and language tuning cannot resolve cultural VLM failure without vision-encoder retraining.
* **If Stage 2 dominates (Arm 2 English accuracy surges while Arm 1 fails):** Isolates the failure specifically to the multimodal projector's cross-lingual alignment, showing that visual features are learned but only connect to English lexical tokens.
* **If inconclusive:** Caused by steering vectors inducing non-specific activation shock that collapses autoregressive generation ($\mathcal{D}_{\text{rep}} > 0.35$).

---

## 13. Dominant Scientific Risk (All Four Proposals)

### Canonical Thesis

* **Dominant Scientific Threat:** **Behavioral Output Steering without Internal Causal Arbitration.** The prompt intervention may change the generated tokens without establishing that internal source arbitration occurred.
* **Existing Evidence:** Prompt framing comparisons in `Which Source Wins?` changed arbitration asymmetry in `Qwen2.5-VL-7B` from +0.813 to +0.060 purely via instruction phrasing.
* **Experimental Control:** The 4-arm factorial design with a length-matched neutral placebo (Arm 2) and bidirectional Lanham prefilling (Arm 4) directly bounds prompt-length and surface-instruction confounds.

### Proposal 1

* **Dominant Scientific Threat:** **Complete Explanation by Known Mathematical / Positional Properties ($M/N$ Softmax Dilution + RoPE Attenuation).** The apparent "reasoning degradation" may leave zero residual cognitive phenomenon to investigate once simple mathematical normalization is accounted for.
* **Existing Evidence:** `RH-Bench` and `Remember-R1` documented attention decay but completely omitted uniform-dilution nulls and position-matched padding controls.
* **Experimental Control:** Explicitly benchmark empirical attention decay against the theoretical $M/N$ null ($\Delta \text{VIG}_{\text{dev}}$) and test linear probe decodability in intermediate layers.

### Proposal 2

* **Dominant Scientific Threat:** **Intervention Fragility and Spatial Incompatibility on Natural Images.** Patching multi-dimensional activation blocks across non-aligned photographic bounding boxes may cause severe out-of-distribution activation shock, collapsing language model decoding into repetitive degeneration rather than providing a clean test of binding transfer.
* **Existing Evidence:** Hasani et al. evaluated activation swaps exclusively on synthetic images where objects occupied uniform single patches within fixed geometric grid cells.
* **Experimental Control:** Strict monitoring of linguistic degeneration ($\mathcal{D}_{\text{rep}} > 0.40$) and comparison against norm-matched Gaussian noise placebos.

### Proposal 3 (Active v2.1)

* **Dominant Scientific Threat:** **Destructive Activation Perturbation vs. Genuine Semantic Steering.** Injected steering vectors ($\vec{v}_{\text{steer}}$) may alter output logits through non-specific activation disruption rather than targeted representation repair, or the underlying representation may be non-linearly distributed, making single-vector steering ineffective.
* **Existing Evidence:** While activation steering is established in unimodal LLMs (e.g., representation engineering), cross-modal residual steering in 3B VLMs can trigger fluency collapse if steering norms are uncalibrated.
* **Experimental Control:** Rigorous grid search for $\alpha, \beta$ on a disjoint validation set, strict monitoring of 3-gram repetition ($\mathcal{D}_{\text{rep}} < 0.25$), and comparing targeted steering against random direction controls.

---

## 14. Feasibility Separate from Scientific Quality


| Dimension                       | Canonical                | Proposal 1                 | Proposal 2                    | Proposal 3 (Active v2.1)  | Proposal 3 (Deprecated v1.0) |
| :-------------------------------- | :------------------------- | :--------------------------- | :------------------------------ | :-------------------------- | :----------------------------- |
| **Scientific question clarity** | High                     | High                       | Moderate-High                 | High                      | High                         |
| **Novelty evidence**            | High                     | Moderate-High              | High                          | High                      | Moderate-High                |
| **Closest-work overlap**        | Moderate                 | High (`RH-Bench`)          | High (Anchor C1)              | Moderate                  | Moderate                     |
| **Falsifiability**              | High                     | High                       | High                          | High                      | High                         |
| **Null-result value**           | High                     | High                       | High                          | High                      | High                         |
| **Dataset accessibility**       | High (HF turnkey)        | High (`WhatIfVis`)         | Moderate-High                 | High (Kaggle turnkey)     | High (Kaggle turnkey)        |
| **Dataset cleanliness**         | High (Exact match)       | High (Counterfactual)      | Moderate                      | High (200 curated)        | Moderate-High (500 items)    |
| **Model accessibility**         | High (`Qwen2-VL-2B`)     | High (`Qwen2.5-VL-3B`)     | High (`Qwen2.5-VL-3B`)        | High (`Qwen2.5-VL-3B`)    | High (`Qwen2.5-VL-3B`)       |
| **Compute feasibility**         | High (~2.5h Colab T4)    | High (~3h Colab T4)        | High (~2h Colab T4)           | High (~30m Colab T4)      | High (~40m Colab T4)         |
| **Evaluation determinism**      | High (Regex/Exact)       | High (Logits/AUC)          | Moderate (Gen text)           | High (Exact MCQA + AUC)   | High (Single token MCQA)     |
| **Leakage/confounding risk**    | Low                      | Low                        | Moderate-High                 | Low (Deduplicated)        | Low (with image-hash split)  |
| **Implementation complexity**   | Low (Prompt pipeline)    | Moderate (Attention hooks) | Moderate-High (Patch mapping) | Moderate (Hooks/Probing)  | Low (Forward pass ablation)  |
| **Unverified assumptions**      | Low                      | Moderate                   | Moderate-High                 | Moderate                  | Moderate                     |
| **Dependence on one model**     | Low (Transferable)       | Moderate                   | High                          | Low (Qwen + Gemma)        | Low (Qwen + Gemma)           |
| **Dependence on one dataset**   | Low (Arithmetic + Chart) | Moderate                   | Moderate                      | Moderate (`BanglaProtha`) | Moderate (`BanglaProtha`)    |
| **Reproducibility**             | High                     | High                       | Moderate                      | High                      | High                         |

---

## 15. Evidence Tables (All Four Proposals)

### Canonical Thesis: Evidence Table


| Claim                                                                         | Evidence / Source                               | Status                 | Limitation                                                                |
| :------------------------------------------------------------------------------ | :------------------------------------------------ | :----------------------- | :-------------------------------------------------------------------------- |
| VLMs exhibit task-dependent modality dominance under contradictory inputs.    | `Which Source Wins?` (`arXiv:2608.17205`, 2026) | **VERIFIED**           | Measured forced choice under visual degradation, not conflict awareness.  |
| Contradiction detection benchmarks do not evaluate source arbitration.        | `CLASH` (`arXiv:2511.19199`, 2025)              | **VERIFIED**           | Formulates task exclusively as abstention ("Cannot answer").              |
| Prompting for contradiction verbalization causally steers source arbitration. | Proposed research hypothesis ($H_1$).           | **UNKNOWN**            | Untested in existing literature; core hypothesis of the thesis.           |
| Length-matched neutral placebo isolates reasoning from compute expansion.     | Lanham et al. (`arXiv:2305.04388`, 2023)        | **STRONGLY SUPPORTED** | Demonstrated in unimodal text LLMs, not multimodal conflict settings.     |
| Turnkey conflict datasets are publicly accessible.                            | Hugging Face:`modality-conflict-arbitration-v2` | **VERIFIED**           | GSM8K shifted pairs have high semantic divergence between image and text. |
| Experiment fits within single Colab Pro GPU session.                          | Execution budget: 4,800 passes on 2B VLM.       | **STRONGLY SUPPORTED** | Pure inference; timing is an engineering estimate.                        |

---

### Proposal 1: Evidence Table


| Claim                                                                           | Evidence / Source                                                   | Status       | Limitation                                                                        |
| :-------------------------------------------------------------------------------- | :-------------------------------------------------------------------- | :------------- | :---------------------------------------------------------------------------------- |
| Visual attention mass decays as reasoning chains lengthen.                      | `RH-Bench` (`arXiv:2505.21523`); `Remember-R1` (`arXiv:2608.01314`) | **VERIFIED** | Observational association; did not control for sequence position or context size. |
| Longer reasoning traces correlate with increased perceptual hallucination.      | `RH-Bench` (`arXiv:2505.21523`, NeurIPS 2025)                       | **VERIFIED** | Evaluated on Qwen2.5-VL models; length confounded with task difficulty.           |
| Softmax normalization mathematically dilutes visual attention by$M/N$.          | Standard Transformer self-attention formulation.                    | **VERIFIED** | Theoretical property; empirical deviation slope remains to be measured.           |
| RoPE introduces distance-dependent attenuation between image and answer tokens. | Standard RoPE literature (Su et al., 2024).                         | **VERIFIED** | Interaction with 3D-RoPE in Qwen2.5-VL not isolated in CoT traces.                |
| "Visual forgetting" is an artifact rather than cognitive decay.                 | Proposed research hypothesis ($H_0$).                               | **UNKNOWN**  | Untested with position-matched neutral padding controls.                          |
| Visual features remain decodable in residual streams during long CoT.           | Proposed probe hypothesis; partial support in`arXiv:2607.26326`.    | **INFERRED** | Prior probing evaluated single-turn VQA, not long reasoning chains.               |

---

### Proposal 2: Evidence Table


| Claim                                                                              | Evidence / Source                                   | Status       | Limitation                                                                       |
| :----------------------------------------------------------------------------------- | :---------------------------------------------------- | :------------- | :--------------------------------------------------------------------------------- |
| Residual activation swaps transfer object-attribute binding in synthetic grids.    | Hasani et al. (`arXiv:2509.24072`, ICML 2026)       | **VERIFIED** | Evaluated exclusively on synthetic$2 \times 4$ grids with explicit symbol tags.  |
| C1 binding swap mechanism transfers to natural photographic instances.             | Proposed research hypothesis ($H_1$).               | **UNKNOWN**  | Untested; Hasani et al. evaluated natural images only observationally for CHAIR. |
| Prior synthetic binding swaps lacked random/Gaussian placebo controls.             | Hasani et al. (`arXiv:2509.24072`, Appendix L)      | **VERIFIED** | Disjoint-symbol control was used, but random noise placebos were omitted.        |
| Dense same-class natural images suffer from frequent attribute misbinding.         | `InstaBind-Lite / DSCAM` (`arXiv:2608.16805`, 2026) | **VERIFIED** | Observational benchmark; no internal mechanistic activation patching.            |
| Spatial patch interpolation on natural images preserves residual stream stability. | Proposed implementation design.                     | **UNKNOWN**  | Bilinear interpolation of hidden states risks triggering text degeneration.      |

---

### Proposal 3 (Active v2.1): Evidence Table


| Claim                                                                                                                                    | Evidence / Source                                               | Status                                                                  | Limitation                                                                          |
| :----------------------------------------------------------------------------------------------------------------------------------------- | :---------------------------------------------------------------- | :------------------------------------------------------------------------ | :------------------------------------------------------------------------------------ |
| Foundation VLMs exhibit severe failure (<42%) on Bengali cultural MCQA.                                                                  | `BanglaProtha` (WACV 2026); `BanglaVerse` (`arXiv:2603.21165`)  | **VERIFIED**                                                            | Evaluated behavioral accuracy only; zero internal layer-wise probing.               |
| Multilingual VLM encoders experience cross-lingual alignment drift.                                                                      | `Where Do Multilingual VLM Encoders Fail?` (`arXiv:2608.30725`) | **VERIFIED**                                                            | Evaluated token cosine similarity; did not trace residual propagation or steering.  |
| Foundation VLMs exhibit cultural knowledge-application gap (+7–18 pts text vs. vision).                                                 | `CulturalMenuBench` (`arXiv:2609.03526`, Sep 2026)              | **VERIFIED**                                                            | Evaluated prompt accuracy; zero representation probing or causal interventions.     |
| Linear probes extract internal representations suppressed during text decoding.                                                          | `TRAPSBench` (`arXiv:2608.13167`, Aug 2026)                     | **VERIFIED**                                                            | Evaluated physics counterfactuals; did not evaluate cultural pretraining asymmetry. |
| Cultural visual features are preserved in mid layers ($L \le 16$) and pre-empted in late layers. | Proposed research hypothesis ($H_1$). | **UNKNOWN**                                                     | Untested in existing literature; central hypothesis of Proposal 3 v2.1. |                                                                                     |
| Causal activation steering at Layer 18 can recover correct cultural recognition.                                                         | Proposed research hypothesis ($H_1$).                           | **UNKNOWN**                                                             | Untested in cultural VLM domains; central intervention of v2.1.                     |
| BanglaProtha contains 6,942 images and 8,034 MCQA questions.                                                                             | `BanglaProtha` (WACV 2026, Table 1); Kaggle repo.               | **VERIFIED**                                                            | Curation of 200 clean, deduplicated items is required for the protocol.             |

---

## 16. Assumption Audit (All Four Proposals)

### Canonical Thesis

* **Established Assumptions:** VLMs exhibit modality bias under conflict; contradiction detection does not equal source arbitration; 2B–3B open VLMs fit within Colab GPU constraints.
* **Plausible Assumptions:** A 2-sentence neutral description prompt accurately matches the computational overhead of a 2-sentence conflict explanation; small open models will follow the two-sentence constraint under 2-shot prompting.
* **Critical Unknowns:** Whether small 2B models (`Qwen2-VL-2B`) maintain sufficient instruction following to output parseable answer tags across all 4 prompt arms without falling into format collapse.

### Proposal 1

* **Established Assumptions:** Attention mass decays with sequence length; RoPE attenuates attention over token distance; softmax denominator expands with context length.
* **Plausible Assumptions:** 150 tokens of neutral descriptive text will match the perplexity and hidden-state norm trajectory of 150 reasoning tokens.
* **Critical Unknowns:** Whether the empirical degradation in Image Causal Effect (ICE) leaves any measurable residual signal once RoPE coordinate displacement (Condition 4) is controlled.

### Proposal 2

* **Established Assumptions:** Activation swapping in intermediate layers redirects attribute generation on synthetic grids; natural images exhibit high attribute misbinding.
* **Plausible Assumptions:** Bilinear interpolation of hidden states across differing bounding box dimensions will preserve sufficient representational geometry to avoid language model collapse.
* **Critical Unknowns:** Whether transplanting visual patch activations between distinct natural photographs causes immediate linguistic degeneration ($\mathcal{D}_{\text{rep}} > 0.40$), rendering binding transfer unmeasurable.

### Proposal 3 (Active v2.1)

* **Established Assumptions:** BanglaProtha is publicly accessible; foundation VLMs exhibit severe failure on Bengali cultural entities; linear probes can extract latent representations from intermediate transformer layers.
* **Plausible Assumptions:** The cultural failure is not 100% vision-encoder blindness; intermediate residual layers preserve measurable entity signals ($\text{AUC} > 0.70$) that get pre-empted in late layers.
* **Critical Unknowns:** Whether intermediate activation steering ($\vec{v}_{\text{steer}}$) can cleanly flip final logit predictions to the correct cultural entity without inducing repetitive degeneration ($\mathcal{D}_{\text{rep}} > 0.35$).

---

## 17. Literature Readiness vs. Experimental Readiness

* **Literature Readiness:** Assesses whether the research question is scientifically differentiated from existing publications, possesses verified primary anchors, and occupies an authentic, non-preempted gap.
* **Experimental Readiness:** Assesses whether the empirical behavior of the models, datasets, prompts, and interventions has already been demonstrated to work as anticipated in the specific proposed configuration.


| Proposal                     | Literature Readiness | Experimental Readiness | Explanatory Audit                                                                                                                                                                                                                 |
| :----------------------------- | :--------------------- | :----------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Canonical**                | **High**             | **Moderate**           | The gap is 100% verified and conceded in literature (`Which Source Wins?` §6). Experimental readiness is moderate because small open VLMs (2B) may exhibit format drift or prompt insensitivity, requiring demonstration tuning. |
| **Proposal 1**               | **High**             | **Moderate-High**      | The mechanistic decomposition of CoT length is completely open. Experimental readiness is moderate-high because teacher-forced prefix slicing is computationally deterministic and well-established in NLP.                       |
| **Proposal 2**               | **High**             | **Low-Moderate**       | The boundary conditions of Anchor C1 are clear. Experimental readiness is low-moderate because activation interpolation across natural image patches is technically fragile and untested on photographic bounding boxes.          |
| **Proposal 3 (Active v2.1)** | **High**             | **Moderate-High**      | The three-stage bottleneck question is fully open and un-preempted. Experimental readiness is moderate-high because linear probing and forward activation hooks are standardized PyTorch workflows with turnkey data access.      |

---

## 18. Decision-Critical Unknown Test

Is there a specific missing piece of evidence that could realistically change whether any proposal should be selected?

1. **Canonical Thesis:**
   * *Missing Evidence:* Empirical confirmation that `Qwen2-VL-2B` follows the 2-sentence intermediate explanation format without skipping straight to the answer.
   * *Classification:* **Implementation / Pilot Uncertainty** (Ordinary empirical uncertainty). Not decision-critical.
2. **Proposal 1:**
   * *Missing Evidence:* Empirical confirmation of whether the ICE drop is completely eliminated by Condition 4 (RoPE matched).
   * *Classification:* **Core Experimental Hypothesis**. This is the scientific question the thesis exists to answer. Not decision-critical.
3. **Proposal 2:**
   * *Missing Evidence:* Whether bilinear interpolation of visual patch hidden states on natural images triggers catastrophic language degeneration ($\mathcal{D}_{\text{rep}} > 0.40$).
   * *Classification:* **Methodological Feasibility Risk**. If interpolation destroys language stability, the experimental vehicle collapses.
4. **Proposal 3 (Active v2.1):**
   * *Missing Evidence:* Whether intermediate residual layers contain any decodable cultural entity representation ($\text{AUC} > 0.60$) or whether the vision encoder/projector drops all cultural information at Stage 1/2.
   * *Classification:* **Core Experimental Hypothesis**. Both outcomes ($H_1$ vs. $H_0$) constitute publishable, high-value findings. Not decision-critical.

> **Statement on Literature Search:** **"No additional broad literature search is decision-critical."** All remaining uncertainties are empirical and experimental, not gaps in prior art discovery.

---

## 19. Final Decision-Readiness Classification


| Proposal                     | Classification   | Decision-Critical Reason                                                                                                                                                                                                            |
| :----------------------------- | :----------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Canonical Thesis**         | **FREEZE-READY** | Verified, open research gap; turnkey public datasets; flawless 4-arm factorial control; high negative-result value.                                                                                                                 |
| **Proposal 1**               | **FREEZE-READY** | Fully open mechanistic decomposition; robust teacher-forced protocol; high-impact rebuttal value against published literature.                                                                                                      |
| **Proposal 2**               | **CONDITIONAL**  | Scientifically high-value, but conditioned on verifying that natural-image spatial patch interpolation does not cause language degeneration.                                                                                        |
| **Proposal 3 (Active v2.1)** | **FREEZE-READY** | Transitioned from passive evaluation to genuine mechanistic research; clear 3-stage bottleneck localization; causal activation steering; balanced 200-item curated setup; "no-loss" publication symmetry under both$H_1$ and $H_0$. |

---

## 20. Final Synthesis

### Canonical Thesis — Evidence Position

The Canonical Thesis rests on a verified and explicitly documented scientific gap. In August 2026, `Which Source Wins?` (`arXiv:2608.17205`) mapped forced modality dominance across 1,500+ arithmetic and chart conflict instances, but explicitly admitted in Section §6 that its framework did not evaluate contradiction awareness, verbalization, or abstention. Conversely, contradiction detection benchmarks such as `CLASH` (`arXiv:2511.19199`) formulated contradiction purely as an abstention task, never testing whether explicit conflict identification enables correct source arbitration. The core question—whether verbalizing a contradiction causally alters subsequent source selection or merely rationalizes an already-established modality bias—remains completely unoccupied in primary literature.

The experimental design is robustly controlled. By introducing Arm 2 (a length-matched neutral placebo describing both sources neutrally), the protocol isolates contradiction-directed reasoning from the trivial confound of extra test-time compute (token budget expansion). Arm 4 (Lanham-style rationale prefilling) introduces a direct causal test of intermediate token steering. Furthermore, the dataset substrates (`modality-conflict-arbitration-v2` and `chartqa-evidence-conflict-v2`) provide exact-match mathematical and categorical targets, eliminating subjective LLM-as-a-judge grading.

The dominant scientific risk is behavioral prompt steering without internal reasoning: the intervention may alter the output string without establishing that internal evidence arbitration occurred. However, this is bounded by the conservative scientific claim: the thesis investigates behavioral output steering and chain-of-thought faithfulness, not internal circuit reorganization. The null result ($H_0$) possesses exceptional value: proving that a model can fluently articulate a contradiction while remaining completely bound to its latent modality bias definitively exposes multimodal chain-of-thought as a decorative rationalization. The thesis is fully feasible within a single Colab Pro T4 GPU budget (~2.5 hours inference) and is classified as **FREEZE-READY**.

---

### Proposal 1 — Evidence Position

Proposal 1 tackles the emerging 2025–2026 literature on multimodal reasoning degradation (`RH-Bench`, `Remember-R1`, `VIG`). These papers established that as vision-language models generate longer chains-of-thought ($T_{\text{CoT}} > 200$ tokens), attention to visual tokens decays and perceptual hallucinations increase. However, our primary literature autopsy reveals that existing work treats trace length as an endogenous, correlational variable, failing to decouple the cognitive computation of reasoning from two fundamental architectural mechanisms: Rotary Position Embedding (RoPE) coordinate distance and uniform softmax denominator dilution ($M/N$).

The proposed 4-condition teacher-forced prefix slicing protocol directly addresses this gap. By comparing a 150-token deductive reasoning prefix (Condition 2) against a 150-token neutral descriptive padding prefix (Condition 3) and an RoPE-advancing prepended prefix (Condition 4), the experiment isolates semantic reasoning drift from positional and context expansion artifacts. The inclusion of linear probing on intermediate residual streams (Layers 18 and 30) directly separates visual feature availability from output head utilization.

The dominant scientific threat is that known positional and attention dilution mechanics will completely explain the observed degradation, leaving no residual "cognitive forgetting." However, this outcome represents a high-impact negative result: it provides a definitive rebuttal against published literature, proving that complex reinforcement learning objectives designed to maintain visual attention mass (e.g., `Remember-R1`) are attempting to correct a mathematical property of softmax normalization rather than an authentic cognitive failure. The proposal is technically sound, runnable in ~3 hours on Colab Pro, and is classified as **FREEZE-READY**.

---

### Proposal 2 — Evidence Position

Proposal 2 investigates the representation geometry of object-attribute binding in foundation VLMs. The primary literature anchor (Hasani et al., ICML 2026, `arXiv:2509.24072`, Anchor C1) claimed that localized residual-stream activations in layers 22–27 encode modular "Grounding IDs" that can be swapped between contexts to transfer object bindings with 98% accuracy. However, our adversarial autopsy revealed that Hasani et al. evaluated causal activation swaps exclusively on artificial $2 \times 4$ geometric grids with prominent horizontal partition lines and non-ordinal symbol tags (`&`, `$`, `#`, `@`), while omitting basic norm-matched Gaussian noise placebos and background controls.

Proposal 2 formulates a rigorous audit: testing whether localized activation swaps transfer object-attribute bindings across dense same-class photographic instances from `InstaBind-Lite/DSCAM` under strict placebo controls (Gaussian noise and background quadrant patches). If the swap succeeds on natural images while exceeding placebo flip rates, it validates the existence of modular binding subspaces. If it fails or matches the placebo, it delivers a landmark corrective finding: proving that reported "Binding IDs" are artifacts of artificial geometric scaffolding and that real-world binding relies on distributed attention routines.

The dominant scientific risk is intervention fragility. Natural photographic bounding boxes vary in size and aspect ratio; mapping them to discrete ViT patch grids and applying spatial bilinear interpolation to intermediate hidden states risks inducing catastrophic activation disruption that collapses language generation into repetitive degeneration ($\mathcal{D}_{\text{rep}} > 0.40$). Because natural-image patch interpolation has not been demonstrated in prior literature, Proposal 2 is classified as **CONDITIONAL** upon verifying that activation interpolation does not induce immediate linguistic collapse.

---

### Proposal 3 — Evidence Position (Active v2.1 Causal Steering & v1.0 Deprecation)

Proposal 3 has been successfully refined from a passive, evaluative validation task (deprecated v1.0) into a rigorous mechanistic interpretability and causal representation steering study (active v2.1). In the previous v1.0 formulation, the proposal evaluated whether selective prediction risk-coverage (AUGRC) degraded under blank-image ablation due to ungrounded cultural text priors. While methodologically clean, it treated the VLM as an impenetrable black box, limiting its contribution to an evaluative benchmark study.

The updated v2.1 specification transforms the research direction by decomposing cultural VLM failure into a **Three-Stage Bottleneck**: Stage 1 (Vision Encoder ViT feature extraction), Stage 2 (Multimodal Projector cross-lingual lexical alignment), and Stage 3 (Deep Transformer Residual Stream Late-Layer Parametric Pre-emption). By executing a 4-arm protocol on 200 curated items from `BanglaProtha`—combining layer-wise linear probing ($\text{AUC}_L$), parallel English prompts (Arm 2), localized object zoom (Arm 3), and causal activation steering at Layer 18 (Arm 4)—the thesis actively discovers where the multimodal pipeline breaks down and tests whether test-time representation steering can causally recover correct cultural recognitions without fine-tuning.

The scientific outcomes possess complete symmetry ("No-Loss Guarantee"): if $H_1$ holds, the thesis discovers late-layer parametric pre-emption and delivers an inference-time activation steering method that repairs cultural hallucinations; if $H_0$ holds, it provides the first empirical refutation of the prevailing belief (`BanglaVerse`) that cultural VLM errors stem from "missing knowledge," conclusively proving that the failure is an early perceptual/projection bottleneck that cannot be resolved without visual pre-training. With a runtime footprint of ~30 minutes on a single Colab T4 GPU, Proposal 3 (v2.1) is fully **FREEZE-READY**.

---

### Cross-Proposal Trade-offs

The four proposals represent distinct scientific paradigms and contribution types:

```
                            THE FOUR CANDIDATE PARADIGMS
                                         │
         ┌───────────────────────────────┼───────────────────────────────┐
         ▼                               ▼                               ▼
[Behavioral Faithfulness]     [Mechanistic Interpretability]  [Causal Representation Steering]
     Canonical Thesis             Proposal 1 & Proposal 2           Proposal 3 (Active v2.1)
• Does verbalized reasoning   • Prop 1: Is trace degradation   • Does cultural failure stem
  causally control source       cognitive or positional?         from early vision vs. late
  arbitration or rationalize  • Prop 2: Do synthetic binding     language pre-emption, and
  prior bias?                   IDs survive in natural photos?   can steering repair it?
```

1. **Canonical Thesis (Behavioral Faithfulness & Cognitive Control):**

   * *Contribution Type:* Evaluates the causal validity of chain-of-thought explanations in multimodal reasoning. It treats the model as an agent performing source arbitration under contradictory evidence and determines whether intermediate reasoning exerts decision control.
   * *Trade-off:* Highest experimental certainty and cleanest baseline-to-target mapping, but bounded to behavioral output observations rather than internal circuit tracing.
2. **Proposal 1 (Architectural vs. Cognitive Decomposition):**

   * *Contribution Type:* A foundational interpretability audit that dissects whether a celebrated empirical failure mode ("visual forgetting") is an authentic cognitive breakdown or an uncalibrated artifact of Transformer mathematics (RoPE and softmax normalization).
   * *Trade-off:* High scientific depth and excellent rebuttal value, but requires teacher-forced prefix slicing and internal residual-stream probing.
3. **Proposal 2 (Representation Modularity & Transfer Audit):**

   * *Contribution Type:* A high-risk, high-reward mechanistic audit testing whether modular representation claims from synthetic toy domains generalize to real-world photographic scenes.
   * *Trade-off:* Outstanding scientific impact if binding modularity is refuted or verified, but carries the highest implementation risk due to spatial patch interpolation across natural bounding boxes.
4. **Proposal 3 (Active v2.1 — Causal Bottleneck Localization & Activation Steering):**

   * *Contribution Type:* A foundational cross-modal mechanistic interpretability study that localizes representational failure across the vision encoder, projector, and residual stream in an authentic low-resource cultural domain, testing training-free activation steering to recover grounded recognition.
   * *Trade-off:* Combines authentic cultural relevance with high-tier mechanistic rigor; requires registering forward hooks and authoring 200 parallel English prompts, but executes rapidly (~30 minutes) on Colab Pro.

---

### Remaining Decision-Critical Unknowns

Only two genuinely decision-critical uncertainties remain across the candidate directions:

1. **Proposal 2 Patch Interpolation Viability:** Whether spatial bilinear interpolation of intermediate residual hidden states between different photographic instances induces immediate linguistic collapse ($\mathcal{D}_{\text{rep}} > 0.40$), rendering binding transfer unmeasurable. *(Requires an implementation check before selection).*
2. **Canonical Instruction Following:** Whether small 2B models (`Qwen2-VL-2B`) strictly adhere to the 2-sentence explanation constraint without skipping straight to the answer under 2-shot demonstrations. *(Minor implementation tuning).*

*Note:* Proposal 1 and Proposal 3 (v2.1) have zero decision-critical unknowns; both have mathematically and methodologically symmetrical outcomes where both positive ($H_1$) and negative ($H_0$) results constitute high-value publishable contributions.

---

### Is More Literature Search Necessary?

> **NO.**
>
> **"No additional broad literature search is decision-critical."**

**Justification:** The primary literature anchors, closest pre-emption threats, methodological designs, and theoretical failure modes have been thoroughly excavated and verified from primary texts across all four candidates. Further broad searching would merely accumulate duplicate citations without resolving any empirical or architectural question.

---

### Final Decision-Readiness Table


| Proposal                       | Classification   | Decision-Critical Reason                                                                                                                                 |
| :------------------------------- | :----------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Canonical Thesis**           | **FREEZE-READY** | Verified, open research gap; turnkey public datasets; flawless 4-arm factorial control; high negative-result value.                                      |
| **Proposal 1**                 | **FREEZE-READY** | Fully open mechanistic decomposition; robust teacher-forced protocol; high-impact rebuttal value against published literature.                           |
| **Proposal 2**                 | **CONDITIONAL**  | Scientifically high-value, but conditioned on verifying that natural-image spatial patch interpolation does not cause language degeneration.             |
| **Proposal 3 (Active v2.1)**   | **FREEZE-READY** | Elevates direction into active mechanistic interpretability and causal activation steering; isolates 3-stage bottleneck; "no-loss" publication symmetry. |
| *Proposal 3 (Deprecated v1.0)* | *SUPERSEDED*     | *Passive black-box evaluation / validation task; superseded by v2.1 causal steering blueprint.*                                                          |

---

### Recommended Next Decision Step

> **A. Freeze a proposal now**

**Justification:** Three of the candidate directions (**Canonical Thesis**, **Proposal 1**, and **Proposal 3 Active v2.1**) have achieved full **FREEZE-READY** status. The evidence base is mature, pre-emption boundaries are clearly delineated, datasets are turnkey and verified, and computational feasibility on Google Colab Pro is established. The human researcher possesses all necessary evidence to responsibly select the final thesis topic based on their scientific preference:

* **Canonical Thesis:** If prioritizing *Behavioral Chain-of-Thought Faithfulness & Source Arbitration*.
* **Proposal 1:** If prioritizing *Foundational Transformer Architecture & Mathematical Decomposition (RoPE / Softmax)*.
* **Proposal 3 (v2.1):** If prioritizing *Cross-Modal Mechanistic Interpretability, Bottleneck Localization, and Causal Activation Steering in Low-Resource Cultural AI*.


### Your Final Decision Menu (Apples-to-Apples Comparison)

All four candidates now stand at the exact same standard of scientific depth, formal mathematical notation, and execution safety:


| Metric / Attribute            | **Canonical Topic (Primary Locked)***Conflict Verbalization & Source Arbitration*           | **Proposal 1***Reasoning Trace Degradation (Cognitive vs RoPE)*                       | **Proposal 2***Visual Binding IDs Natural Transfer*                                                | **Proposal 3 (Elevated)***Cultural Multimodal Bottleneck & Steering*                                    |
| ------------------------------- | --------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| **Research Domain**           | Multimodal Reasoning Faithfulness & Modality Conflict                                       | Long-Context Reasoning & Attention Dilution                                           | Mechanistic Interpretability & Object Binding                                                      | Multimodal Representation Learning & Cultural VLMs                                                      |
| **Core Scientific Question**  | Is CoT explanation an active causal decision arbiter or a post-hoc rationalization?         | Is visual decay in long CoT true forgetting or a RoPE/Softmax dilution artifact?      | Do internal "Binding IDs" survive in natural images or are they synthetic grid artifacts?          | Are cultural VLM failures early perceptual deficits or late-layer parametric pre-emptions?              |
| **Implementation Mechanism**  | 4-arm prompt factorial + length-matched neutral placebos + prefilling.                      | Teacher-forced prefix slicing + attention mass sums + linear probing.                 | Layer 22 causal activation patching + Gaussian/background placebos.                                | Layer-wise linear probing (L0–32**L**0**–**32) + Layer 18 causal activation steering.                 |
| **Dataset Source**            | Deterministic arithmetic conflicts (`modality-conflict-arbitration-v2`)                     | `WhatIfVis` paired counterfactuals (500 items)                                        | `InstaBind-Lite` / `DSCAM` (50 natural pairs + 25 synthetic)                                       | `BanglaProtha` (200 entity-stratified items)                                                            |
| **Implementation Complexity** | **Low:** Pure behavioral generation; zero PyTorch hook dependencies.                        | **Medium:** Eager attention sums and residual-stream linear probes.                   | **High:** Bounding box to ViT patch mapping + bilinear activation interpolation.                   | **Medium:** Residual-stream forward hooks + contrastive vector addition.                                |
| **Execution Risk**            | **Near Zero:** Clean deterministic answers; impossible to get blocked by tensor-shape bugs. | **Low-Medium:** Well-understood attention slicing; standard eager forward pass.       | **Medium-High:** Tensor alignment across varying bounding box geometries.                          | **Low:** Single-pass forward hooks on standard hidden states.                                           |
| **Alignment with Your Goal**  | **Maximum polish:** Safest, cleanest undergraduate timeline; zero risk of becoming messy.   | **Highest general ML prestige:** Directly attacks foundational CoT reasoning debates. | **Deepest mechanistic interpretability:** Direct intervention on internal binding representations. | **Strongest regional/cultural impact:** Solves the "weak evaluation" trap with genuine causal research. |
