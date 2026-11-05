
Listed directory Cross%20Modal
Listed directory Context
Listed directory Medical%20Imaging%20&%20FL
Listed directory Multimodal%20Agent
Searched for "Trustworthy"
Viewed Cross_Modal_Discovery_Synthesis_and_Handover.md:1-167
Viewed Medical%20Imaging%20&%20FL.md:1-250
Viewed Medical%20Imaging%20&%20FL.md:250-331
Viewed Multimodal%20Agent.md:1-142
Viewed Canonical_Cross_Modal_Thesis_Synthesis.md:1-150
Viewed Canonical_Cross_Modal_Thesis_Synthesis.md:151-300

# FINAL THESIS DECISION AUDIT: 4-FIELD ADVERSARIAL COMPARISON

---

## 1. Deep Field-by-Field Adversarial Audits

### Field 1: Multimodal Agents (Active Perception & Tool Utility)

#### 1. Research Question Reality vs. Application

* **The Claimed Question:** *"Can a multimodal agent learn/predict whether an active perception action (crop, zoom, retrieve) will improve task accuracy before incurring the computational or token cost of executing it?"*
* **The Reality:** The broad question is **not an open research gap; it is an occupied engineering domain.**
* **Apparent Novelty Diagnosis:** Apparent novelty in discovery reports was manufactured by **terminology substitution and weak literature search**. What was described as "action-value prediction" has already been published across late 2024–2026 under different names:
  * *AdaTooler-V* (`arXiv:2512.16918`) explicitly defines and optimizes the sample-level **Tool Benefit Score** $\Delta S(q) = S^+(q) - S^-(q)$ to suppress unhelpful tool calls via reinforcement learning (RL).
  * *ToolGate* (`arXiv:2606.03054`) trains a pre-call controller to gate visual operations, cutting unneeded calls by 36–69%.
  * *CAM-DF* (`arXiv:2607.27083`) formalizes decision-focused stopping when marginal information gain falls below execution cost ($\max_a \mathbb{E}[\Delta U(a)] \le \lambda \cdot \text{Cost}(a)$).
  * *MED* (`arXiv:2602.01334`) and *Spurious Tool Use* (`arXiv:2609.16268`) already proved that $>70\%$ of RL crop-agent gains stem from intrinsic model capabilities rather than tool execution.
* **The Only Surviving Sub-Question:** A pure diagnostic confound audit: *"In multimodal active perception benchmarks (e.g., ActiView), what proportion of reported accuracy gains is driven by spatial resolution recovery versus an uncalibrated confound of auxiliary test-time reasoning compute (extra forward passes and extended reasoning tokens)?"*
* **Baseline and Leakage:** Direct zero-shot vs. compute-matched multi-step chain-of-thought (CoT) on [ActiView](https://github.com/THUNLP-MT/ActiView). While deterministic exact-match prevents evaluator leakage, the question is fragile: if ActiView’s targets are so physically degraded that extra thinking tokens cannot infer the answer without sub-pixel data, the baseline yields a zero delta, collapsing the study into an unpublishable benchmark replication.
* **Engineering Burden & Collapse Risk:**
  * *Constructive agent build (RL/environment):* **Automatic failure.** Training 7B+ policies on Colab Pro triggers GPU out-of-memory (OOM) errors, and tool-agent environments (e.g., Playwright, Docker, live APIs) suffer from software drift and non-deterministic timeouts.
  * *Diagnostic audit:* Manageable in code, but high risk of viva dismissal: *"Everyone knows test-time thinking tokens improve reasoning; showing it on an image benchmark is an incremental empirical check, not a thesis-defining discovery."*

---

### Field 2: Medical Imaging (Selective Classification & Sensor Shift)

#### 2. Research Question Reality vs. Application

* **The Claimed Question:** *"Under physical sensor shift (dermatoscope $\to$ clinical smartphone camera: ISIC 2020 $\to$ PAD-UFES-20 / DDI), does post-hoc confidence calibration preserve sample-level risk-coverage ordering (AUGRC), or does selective triage fail where automated referral is most needed?"*
* **The Reality:** This fails the **"Medical Imaging Is Not Enough" test**. It is an applied computer vision benchmark evaluation using medical images as an arbitrary substrate.
* **Apparent Novelty Diagnosis:** Apparent novelty stemmed from **coupling an existing metric with a known domain shift**:
  * *Traub et al. (NeurIPS 2024, `arXiv:2407.01032`)* already mathematically proved the flaw in standard AURC, formalized AUGRC, and established selective classification bounds.
  * *Kozachok et al. (`arXiv:2607.26765`, July 2026)* already mapped cross-dataset dermoscopy domain shifts across 6 sources (25,903 images) under contamination-controlled protocols.
  * *Kina & Petersen (`arXiv:2609.07922`, 2025)* already showed that post-hoc logit recalibration adjusts for demographic and acquisition shifts.
* **Data Integrity & Hidden Collapse Hazards:**
  * Public dermatological archives suffer from **catastrophic nesting and leakage**: ISIC 2019 fully subsumes HAM10000; ISIC 2020 contains an official list of 425 duplicate images across patients; PAD-UFES-20 and DDI have distinct biopsy-verification standards and diagnostic taxonomy misalignments.
  * An undergraduate team will spend 6–8 weeks writing deduplication scripts, verifying patient IDs, and resolving label ontologies.
* **Contribution Value & Viva Vulnerability:** In a Computer Science defense, examiners will challenge the clinical validity: *"Did you consult a dermatologist? How do you account for biopsy biopsy-selection bias?"* If answered with *"This is an evaluation of Traub's metric,"* the examiners will retort: *"Then why wasn't this evaluated on clean, standardized computer vision benchmarks without clinical confounders?"* It creates maximum data-cleaning friction for minimal algorithmic insight.

---

### Field 3: Federated Learning (Conformal Risk Control & Client Drift)

#### 3. Research Question Reality vs. Application

* **The Claimed Question:**
  * *Non-VLM:* *"How resilient is site-conditional federated conformal risk control (risk-curve shrinkage) to partial client participation and severe local sample-size imbalances ($n_k < 15$)?"*
  * *VLM Variant:* *"Does federated LoRA aggregation cause worst-client calibration disparity in medical vision-language models?"*
* **The Reality:** Fails the **"Why FL?" test** and suffers from **core gap pre-emption**.
* **Apparent Novelty Diagnosis:**
  * *Non-VLM:* The core discovery was published by *Shahid (`arXiv:2606.20115`, June 2026, Fed-CRC-Seg)* on FeTS-2022. Shahid established that pooled conformal calibration violates coverage at 40% of institutions and that empirical Bayes risk-curve shrinkage ($n_0=19$) guarantees bounded institutional risk. Extending this to partial client participation is an **operational parameter sweep**, not an algorithmic thesis.
  * *VLM Variant:* A **manufactured intersection**. Centralized medical VLMs already exhibit zero positive calibration transfer across distribution shift (*MVC-Bench, `arXiv:2608.27004`*). Claiming that federated parameter aggregation causes calibration disparity is an unproven assumption; centralized shift already explains the observed variance.
* **Dataset & Infrastructure Kill Gates:**
  * Authentic multi-institution data exists **only** in FeTS-2022 (23–33 real clinical silos). FeTS-2022 is access-gated behind manual administrative approval on Synapse (`syn28546456`), with documented multi-week approval delays.
  * Training 3D U-Nets on multi-parametric MRI exceeds Colab Pro GPU limits.
  * Splitting 2D public datasets via synthetic Dirichlet distributions ($\alpha = 0.1$) was explicitly discredited by *Neurocomputing 2026 (`doi:10.1016/j.neucom.2026.135005`)*, which proved synthetic label skew produces ranking artifacts that do not replicate on authentic multi-center clinical cohorts.
* **Collapse Risk:** A team waiting on Synapse credentials or debugging asynchronous Flower/Ray distributed runtime memory leaks on Colab will see their 3–4 month timeline evaporate before running a single valid calibration round.

---

### Field 4: Trustworthy VLM / MLLM (Causal Conflict Verbalization)

#### 4. Research Question Reality vs. Application

* **The Claimed Question:** *"When a vision-language model is presented with mutually contradictory visual and textual premises, does requiring it to explicitly verbalize and explain the contradiction causally alter its decisional arbitration, or does the explanation merely act as a post-hoc rationalization of an entrenched, early-layer modality preference?"*
* **The Reality:** This is a **pure, foundational artificial intelligence and cognitive-mechanisms research question**. It probes the structural limits of multimodal autoregressive reasoning: does intermediate chain-of-thought generate causal computational steering, or is it decorative text generated downstream of fixed cross-modal attention projections?
* **Gap Evidence & Primary Literature Audit:** The gap is **100% verified, open, and explicitly conceded in primary literature**:
  * *Which Source Wins? Task-Dependent Reliance in VLMs (`arXiv:2608.17205`, August 2026)* mapped modality dominance across 1,500+ items. In §6 (Limitations), the authors explicitly state:
    > *"our framework measures forced source arbitration under reduced legibility rather than factual reliability or conflict awareness. Consequently, we do not test whether models detect the contradiction, express uncertainty, or abstain."*
    >
  * *Zhu et al. (2024)* tested prompting for conflict mitigation, and *Lanham et al. (2023)* tested rationale faithfulness in text LLMs, but **neither isolated intermediate conflict verbalization via counterfactual rationale prefilling and length-matched placebo controls**.
* **Dataset Readiness:**
  * Turnkey, verified, and completely public on Hugging Face: [`vlm-modality-research/modality-conflict-arbitration-v2`](https://huggingface.co/datasets/vlm-modality-research/modality-conflict-arbitration-v2). Contains 1,304 clean, mathematically distinct arithmetic conflict pairs, plus 229 verified chart conflict items.
  * Includes fully aligned control items to evaluate and penalize false-conflict hallucinations.
* **Compute & Engineering Feasibility:**
  * Model: `Qwen/Qwen2-VL-2B-Instruct` or `Qwen/Qwen2.5-VL-3B-Instruct` in `bfloat16`.
  * Footprint: 4.5 GB VRAM. Zero-shot 4-arm factorial inference on 500 items takes **~90 minutes on a single Colab Pro T4/V100 GPU** and costs $<\$1.00$.
  * Zero browser drivers, zero distributed networking, zero manual medical credentialing.
* **Negative-Result Value:** **Outstanding and publication-grade under either outcome:**
  * *If $H_1$ holds (Deliberative Control):* Verbalizing contradiction breaks unimodal capture and causally flips decisions toward the authoritative source, establishing an inference-time reasoning intervention for multimodal reliability.
  * *If $H_0$ holds (Post-Hoc Rationalization):* Decision flip rates are identical between the conflict prompt and a length-matched neutral placebo prompt, proving that multimodal chain-of-thought explanations are causally unfaithful rationalizations that mask latent parametric bias.

---

## 2. Final Adversarial Comparison Table

| Criterion                              | Multimodal Agent                                                                                                                                     | Medical Imaging                                                                                                                  | Federated Learning                                                                                                                   | Trustworthy VLM (Held Direction)                                                                                                          |
| :------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------- |
| **Real research gap**            | **Narrow / Fragile.** Algorithmic tool gating is occupied (*AdaTooler-V*, *ToolGate*); only the test-time compute confound audit survives. | **Benchmark application.** Evaluating Traub's AUGRC metric across camera shifts. No new learning mechanism.                | **Occupied.** Conformal calibration failure already solved by Shahid (*Fed-CRC-Seg*). VLM FL is a manufactured intersection. | **100% Genuine & Open.** Causal role of conflict verbalization explicitly left unstudied by *Which Source Wins?* (§6).           |
| **Closest-work saturation**      | **Heavily saturated.** RL tool invocation, cost-aware stopping, and efficiency pruning are crowded 2025–2026 areas.                           | **Saturated.** Dermoscopy classification, HAM10000 splits, and demographic recalibration (*Kina & Petersen*) are closed. | **Pre-empted.** Shahid (June 2026) published the headline FeTS-2022 conformal result.                                          | **Unoccupied gap.** Closest works (*Which Source Wins?*, *CLASH*) forced choice without testing causal awareness or abstention. |
| **Dataset/baseline readiness**   | **Moderate.** ActiView is public, but agent tool harnesses require parsing custom sub-view formats.                                            | **Deceptive.** ISIC 2020/PAD-UFES are public, but require purging 425 duplicates and resolving taxonomy mismatches.        | **Fatal Gate.** FeTS-2022 is locked behind Synapse manual approval. Synthetic Dirichlet splits are discredited.                | **100% Turnkey.** Hugging Face repo (`modality-conflict-arbitration-v2`) is verified, clean, and instant-download.                |
| **Experimental controllability** | **Moderate.** Prompting agent to reason can trigger text degeneration; difficult to perfectly match token budgets.                             | **Low-Moderate.** Confounded by acquisition artifacts (gel bubbles, hair, lighting) and biopsy-selection bias.             | **Low.** Confounded by stochastic client selection, communication latency, and non-IID partition parameters.                   | **Exceptional.** 4-way factorial prompt design with length-matched neutral placebos and Lanham prefilling.                          |
| **Compute feasibility**          | **High (Audit only).** ~75 mins on Colab T4. (Constructive RL training fails automatically on Colab).                                          | **High.** 2D DenseNet-121 trains in ~5 hours on Colab T4.                                                                  | **Conditional/Fails.** FeTS 3D MRI training exceeds 16GB VRAM. Tensor-only evaluation requires pre-computed features.          | **Flawless.** Pure inference on 2B–3B open VLMs. ~90 mins on Colab T4; $<\$1.00$ API budget.                                     |
| **Engineering burden**           | **Moderate-High.** Even diagnostic audits require PIL spatial cropping and view-stitching pipelines.                                           | **High.** Extensive data cleaning, duplicate cross-matching, and patient-stratified split verification.                    | **Extreme.** Distributed simulation frameworks (Flower/Ray), inter-process communication, and seed synchronization.            | **Near Zero.** ~150 lines of clean PyTorch/HuggingFace Python code. Zero third-party platform scaffolding.                          |
| **Evaluation strength**          | **Moderate.** Multiple-choice exact match, but vulnerable to reasoning-token length confounds.                                                 | **Weak in CS Viva.** Vulnerable to clinical validity critiques and lack of clinician-in-the-loop evaluation.               | **Fragile.** Synthetic Dirichlet results are scientifically invalid; FeTS evaluation is tied to one proprietary metric.        | **Rock-Solid.** Deterministic arithmetic/chart exact match. Completely eliminates LLM-as-a-judge subjectivity.                      |
| **Novelty confidence**           | **Moderate-Low.** Reviewers may dismiss compute matching as an obvious application of known LLM scaling properties.                            | **Low.** Evaluates someone else's metric (Traub 2024) on existing benchmark transitions.                                   | **Low.** Minor parameter variation (partial participation) on someone else's framework (Shahid 2026).                          | **High.** First causal isolation of intermediate conflict reasoning vs. post-hoc rationalization in multimodal systems.             |
| **Negative-result value**        | **Moderate.** If compute doesn't help, the benchmark simply requires sub-pixel cropping—an unexciting confirmation.                           | **Moderate.** Confirms that post-hoc scaling doesn't fix camera shifts, replicating standard OOD findings.                 | **Low.** If shrinkage resists dropout, it merely confirms that Shahid’s prior was sufficiently conservative.                  | **Outstanding.** Proving that verbalized conflict does *not* alter decisions definitively exposes multimodal CoT as decorative.   |
| **3–4 month thesis risk**       | **Moderate.** High risk of reviewer pushback regarding benchmark artificiality.                                                                | **High.** Sunk time in medical data cleaning; potential rejection by examiners for lacking clinical grounding.             | **Critical.** High probability of schedule collapse due to Synapse access delays or FL simulation bugs.                        | **Minimal.** Zero administrative gates, zero training instability, fully reproducible, defensible within 8–10 weeks.               |

---

## 3. FINAL DECISION

# **FREEZE: Trustworthy VLM / MLLM**

### *(Causal Conflict Verbalization and Source Arbitration in Vision-Language Models)*

---

### 1. The Exact Research Question

> **"When a vision-language model is presented with mutually contradictory visual and textual premises, does requiring it to explicitly verbalize and explain the contradiction causally change its decisional arbitration, or does the explanation merely act as a post-hoc rationalization of an entrenched modality preference?"**

---

### 2. Why This Question Survives the Strongest Attacks

1. **It avoids the "Arbitration Accuracy" Construct Trap:** Earlier flawed proposals attempted to measure "arbitration accuracy" on symmetric datasets where neither source had ground truth. This question operates on mathematically verifiable items (arithmetic equations where one modality contains a corrupted digit, or chart QA with known tabular truth) and isolates **causal mediation**, not subjective source preference.
2. **It isolates reasoning from token length via Placebo Controls:** Reviewers often dismiss prompt interventions by claiming that extra intermediate tokens merely act as computational buffer. By incorporating a **length-matched neutral placebo condition** (describing both sources neutrally before answering), any observed shift in decision cannot be attributed to generic compute expansion.
3. **It definitively proves or disproves Multimodal CoT Faithfulness:** If forced conflict verbalization shifts the answer, the thesis proves that multimodal CoT provides genuine cognitive control. If the model articulates the contradiction but still follows its default modality prior, the thesis proves that multimodal explanations are decorative, post-hoc rationalizations. Both outcomes are publication-grade contributions.
4. **Complete Independence from Infrastructure Gates:** It requires no private medical approvals, no live web browser daemons, and no multi-node distributed simulations.

---

### 3. Closest Existing Work & What Remains Untested

* **Closest Paper 1:** *Which Source Wins? Task-Dependent Reliance in VLMs (`arXiv:2608.17205`, August 2026)*.
  * *What it did:* Evaluated forced-choice modality reliance across arithmetic, chart, and text tasks under visual legibility degradation.
  * *What remains untested:* The authors explicitly conceded in §6 that they did not evaluate conflict detection, awareness, or whether verbalizing the contradiction alters the decision.
* **Closest Paper 2:** *Lanham et al. (2023) — Measuring Faithfulness in Chain-of-Thought Reasoning (`arXiv:2305.04388`)*.
  * *What it did:* Formalized rationale truncation, filler tokens, and prefilling in text-only LLMs.
  * *What remains untested:* Has never been applied to cross-modal contradiction arbitration in modern vision-language models.

---

### 4. Minimum Viable Experimental Design

* **Dataset:** 500 clean arithmetic conflict items + 200 chart conflict items from [`vlm-modality-research/modality-conflict-arbitration-v2`](https://huggingface.co/datasets/vlm-modality-research/modality-conflict-arbitration-v2), interleaved with 500 aligned control pairs (to penalize false conflict hallucination).
* **Models:** `Qwen/Qwen2-VL-2B-Instruct` and `Qwen/Qwen2.5-VL-3B-Instruct` (evaluated locally in `bfloat16` on Colab Pro), with optional API validation on `Gemini 1.5 Flash`.
* **The 4-Arm Factorial Protocol (Pure Inference):**
  1. **Arm 1 (Direct Zero-Shot Baseline):** Model outputs final answer directly without intermediate reasoning ($T \approx 10$ tokens).
  2. **Arm 2 (Length-Matched Placebo Control):** Model is prompted to neutrally describe both the image and the text premise in 2 sentences before answering ($T \approx 80$ tokens). *Controls for compute expansion.*
  3. **Arm 3 (Conflict Verbalization Intervention):** Model is prompted to explicitly detect and articulate whether the visual and textual premises agree or contradict before answering ($T \approx 80$ tokens).
  4. **Arm 4 (Lanham-Style Prefilling Intervention):** Prefilling the assistant output with an explicit contradiction verdict vs. an agreement verdict to measure the direct causal impact of the rationale on the subsequent answer logits.
* **Execution Footprint:** $1,200 \text{ items} \times 4 \text{ arms} = 4,800$ forward passes. Total compute: **$\approx 2.5$ hours on a single Colab Pro T4/V100 instance**. Cost: $<\$1.00$.

---

### 5. The Biggest Risk & Its Mitigation

* **The Biggest Risk:** **Instruction-Following Failure in Small Open Models.***A 2B or 3B parameter model might ignore the prompt structure, failing to generate the 2-sentence neutral description in Arm 2 or failing to output a cleanly parseable final answer.*
* **Mitigation:**
  1. Use 2-shot in-context demonstration examples showing the required output format.
  2. Apply constrained logit masking or structured generation (e.g., via `outlines` or regex guidance) for the final answer token.
  3. If small open models exhibit format drift, run the exact same prompt suite across `Gemini 1.5 Flash` via API ($<\$0.50$ total cost) as an authoritative frontier baseline.

---

### 6. Why the Other Three Fields Must NOT Be Selected at This Stage

1. **Medical Imaging:** Sinks 6–8 weeks into patient-ID deduplication, image leak auditing, and resolving taxonomy differences across ISIC and PAD-UFES, only to produce an incremental evaluation of an existing metric (Traub’s AUGRC) that invites sharp clinical validity challenges in a Computer Science viva.
2. **Federated Learning:** Suffers from a fatal infrastructure gate (FeTS-2022 Synapse registration delays) or forces the use of artificial Dirichlet label skews that the 2026 literature has proven produce invalid findings. The core statistical problem of conformal shrinkage under FL was already solved by Shahid in June 2026.
3. **Multimodal Agents:** Constructive RL agent building is computationally unfeasible on Colab Pro. The surviving diagnostic question (ActiView compute-matching) is narrow, fragile to target-resolution confounds, and risks reviewer dismissal as an obvious demonstration that thinking tokens help.

---

### 7. What Evidence Would Falsify This Decision?

This decision should be reconsidered **only** if:

* A paper published in the last 30 days is uncovered that has **already implemented length-matched neutral placebo prompts and Lanham-style rationale prefilling specifically on cross-modal conflict arbitration datasets**, demonstrating the exact causal transition.
  *(Note: As verified in our alphaXiv autopsy of `arXiv:2608.17205` and `arXiv:2511.19199`, no such study exists.)*

---

### 8. The Single Concrete Action to Take Next

> **Open Google Colab, connect a standard T4 GPU instance, install `transformers` and `datasets`, load 50 samples from [`vlm-modality-research/modality-conflict-arbitration-v2`](https://huggingface.co/datasets/vlm-modality-research/modality-conflict-arbitration-v2), and run the 4 prompt conditions on `Qwen2-VL-2B-Instruct` to verify prompt formatting and establish your baseline output logit parser.**
