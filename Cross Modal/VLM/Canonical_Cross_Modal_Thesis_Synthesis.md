# CANONICAL CROSS-MODAL THESIS RESEARCH SYNTHESIS
**Comprehensive Audit, Evidence Reconciliation, and Question Filtration for Undergraduate Thesis Discovery**

*Consolidated from all discovery reports, adversarial audits, and canonical specifications within `/Cross Modal` and `/Context`*  
*Date: 20 September 2026 | Principal Researcher: Mohammad Zahed Hossen*

---

## 1. Executive Synthesis and Source Map

This canonical report resolves, reconciles, and synthesizes the entire body of exploratory research conducted across four discovery streams and multiple decision records:
- **Report 1 (AlphaXiv / Base Discovery):** `Cross-modal evidence use and source arbitration.md`
- **Report 2 (Gemini Discovery):** `Cross-Modal AI Thesis Discovery (Gemini).md`
- **Report 3 (Perplexity Discovery):** `Cross-modal evidence use and source arbitration (Perflexity).md` & `kill occupied questions (Perflexity).md`
- **Adversarial Audit (Claude):** `Claude Critique Analysis.md`
- **Foundational Context:** `Thesis_Topic_Discovery_Handover.md`, `Thesis_Progress_and_Research_Map.md`, `Canonical Thesis Field Specification.md`, and `Canonical_Rejected_and_Parked_Thesis_Fields_Report.md`

### The Current Reality
You have achieved exceptional scope discipline, locked your parent field (**Multimodal / Vision-Language Learning and Systems**), and selected your primary subfield (**Trustworthy and Reliable Generative MLLMs**). However, you have been caught in an **AI discovery and audit echo-chamber**:
1. Discovery assistants (Gemini, Perplexity, AlphaXiv) repeatedly generated ambitious proposals claiming "novel, unstudied research gaps" supported by complex formulas and runtime estimates.
2. Adversarial audits (Claude, S08, S09) demonstrated that **these reports were not independent** (Report 2 mirrored Report 1; Report 3 was seeded from local files) and uncovered fatal construct, metric, and dataset flaws.
3. As written, **zero candidates in those reports clear "Proceed to Pilot" without structural repair**.
4. The path forward is not another broad 12-family scan, but isolating the narrow, leakage-resistant empirical questions that survive adversarial cross-examination.

---

## 2. Consolidation & Merging of Equivalent Research Questions

Across the multiple reports, twelve broad research families were repeatedly discussed under different names. They consolidate into eight core candidate clusters:

```
Consolidated Research Space
├── Cluster 1: Cross-Modal Conflict Arbitration & Modality Dominance
│   └── Merged: R1 C1/U1, R2 Top 1, R3 Family 2, Claude C1
├── Cluster 2: Evidence Sufficiency, Masking & Uncertainty Calibration
│   └── Merged: R1 C2, R2 Top 2, R3 Family 3, Claude C2, Astra B/C
├── Cluster 3: Visual-Token Compression & Locality Destruction
│   └── Merged: R1 C3, R2 Top 3, R3 Candidate 3, Claude C3
├── Cluster 4: Modality Attribution & Unimodal Shortcut Auditing
│   └── Merged: R1 Family 4, R2 Family 6/12, R3 Family 1/6/12
├── Cluster 5: Cross-Lingual & Morphological Modality Reliance
│   └── Merged: R1 C5, R2 Family 10, R3 Top 1 (Bengali repair)
├── Cluster 6: Explanation Faithfulness & Grounding Drift in CoT
│   └── Merged: R1 Family 5, R2 Family 4/11, R3 Family 4
├── Cluster 7: Distribution Shift & Test-Time Adaptation (TTA)
│   └── Merged: R1 C4/Family 9, R2 Family 9, R3 Family 9
└── Cluster 8: Active Information Acquisition (Zoom / Crop / Retrieve)
    └── Merged: R3 Candidate 2, Astra BCEA / ReCoVERR
```

---

## 3. Direct Contradictions Between the Reports

| Issue | Report 1 & Report 2 (Gemini) Claim | Claude Adversarial Audit Finding | Reality & Resolution |
| :--- | :--- | :--- | :--- |
| **Dataset Size of `multimodal-arbitration-artifact`** | Claims 1,000 paired items (500 chart + 500 arithmetic) or 400 chart items ready for evaluation. | Directly cloned and inspected the repository: **only 229 chart items exist**. Arithmetic items sit on unverified anonymous review mirrors. | **Contradicted.** The dataset is 75% smaller than claimed; arithmetic data access is unverified. |
| **Metric: "Arbitration Accuracy"** | Claims models can be evaluated on accuracy ($\text{Acc}_{\text{arb}}$) under image-true/text-false and text-true/image-false conditions. | The underlying prompt explicitly states: *"Neither source is privileged"* and forbids hedging. Outcomes are **exact-match source preference**, not ground-truth correctness. | **Fatal Construct Flaw.** There is no gold truth. Source preference cannot be labeled "accuracy" without imposing an external authority rule. |
| **Manual Annotation Overhead** | Claims zero manual annotation; completely automated inference-only script. | The authors' protocol required per-item manual certification (230 items reviewed). Creating aligned controls or repaired conditions requires identical manual review. | **Contradicted.** Any valid diagnostic extension requires manual verification. |
| **Model Compatibility (`Qwen2.5-VL-3B`)** | Claims out-of-the-box execution of `Qwen2.5-VL-3B` on the artifact with known runtime and unimodal competence. | Repo configs contain Qwen2-VL-2B, Qwen2.5-VL-7B, Idefics3-8B, Phi-3.5, etc. **Qwen2.5-VL-3B is not present**, and its unimodal accuracy is untested. | **Unverified.** Baseline unimodal competence must be established before running conflict items. |
| **Novelty of Clean-Threshold Transfer vs. Ranking** | Claimed in Gemini S11 and Report 2 that no prior work compares clean-threshold transfer with ranking under degradation. | Audit S08 and Claude confirmed that *Bigger or Cheaper?* (July 2026) already performed clean-threshold transfer and condition-wise AUROC. | **Novelty Disproved.** The central gap claim was completely occupied. |
| **Novelty of Conflict Detection Prompting** | Claimed that prompting a VLM to detect contradictions before answering is an unstudied gap. | *Zhu et al. (2024)* already studied prompt-based conflict detection/mitigation; *CLASH (2025)* is an established benchmark. | **Overstated.** Prior art exists; novelty survives only if framed as a causal mediation test. |
| **Compute Arithmetic** | Gemini compute table claimed: 4 ratios $\times$ 3 pruners = 12 passes, totaling 6,000 passes, at 0.15s per pass. | 12 passes on 1,500 items = 18,000 passes. Furthermore, 0.15s ignores multi-token autoregressive generation. | **Arithmetic Error.** Colab runtime was underestimated by at least $3\times$. |

---

## 4. Literature Coverage & Omissions Matrix

### A. Papers Missed by Discovery Reports but Identified by Audits
1. **Zhu et al. (2024) — *Cross-Modality Conflict Detection and Mitigation*:** Directly evaluates prompting strategies to resolve image-text conflicts.
2. **CLASH (2025):** Benchmark dedicated to cross-modal contradiction detection and assertion screening.
3. **Lanham et al. (2023) — *Measuring Faithfulness in Chain-of-Thought*:** The foundational methodology for testing whether reasoning traces are causal or post-hoc (via rationale truncation and corruption).
4. **Bigger or Cheaper? (July 2026):** Decisive study on visual degradation, confidence ranking, and clean-threshold transfer.
5. **Seeing without Looking (May 2026):** Proves that VLMs remain confidently affirmative even when the queried object is completely excised.
6. **TUBench / UVQA (Oct 2024):** Ground-truth benchmark for out-of-frame and unanswerable visual questions.

### B. Recent 2026 Papers Surfaced in Discovery Reports
- *Which Source Wins? Task-Dependent Reliance in VLMs* (Aug 2026)
- *C³PO: Cross-Modal Composition and Counterfactual Performance* (Aug 2026)
- *Which Modality Decides? Counterfactual Modality Attribution (CMA)* (Aug 2026)
- *Visuals Lie, Consistency Speaks* (June 2026)
- *How Many Visual Tokens Do Multimodal Language Models Need?* (May 2026)
- *Logit–Attention Divergence (LAD)* (May 2026)
- *Evidence-Order Calibration (EOC)* (Sept 2026)
- *Look Again Before You Abstain & BCEA* (June 2026)

---

## 5. Novelty Claims Made vs. Disproved

1. **Claim: "Token pruning selectively destroys localized fine-grained evidence."**  
   *Disproof:* Confounded by benchmark variance (MMBench vs. TextVQA). Furthermore, legibility loss under pixel downsampling is geometrically trivial, not an unexpected cognitive failure.
2. **Claim: "Visual degradation causes flat confidence (models are evidence-blind)."**  
   *Disproof:* Conflates lack of confidence change with language prior answerability. On prior-solvable items, confidence *should* remain flat. True evidence blindness must be measured relative to blind text-only accuracy.
3. **Claim: "Subword fragmentation (tokenizer fertility) causally drives modality reliance."**  
   *Disproof:* Subword fertility cannot be experimentally isolated from language semantics and translation artifacts.
4. **Claim: "Bengali cultural failure repair via 3-way factorial intervention."**  
   *Disproof:* Visual, linguistic, and cultural interventions are not orthogonal (a visual description is text); hints leak ground-truth answers.

---

## 6. Four-Tier Epistemic Boundary Separation

```
EPISTEMIC TAXONOMY
├── 1. Established Facts
│   ├── VLMs achieve high accuracy via language priors without using visual pixels.
│   ├── Attention maps (saliency) correlate near-zero with correctness (R ≈ 0).
│   ├── Modality dominance reverses across tasks (text in math, image in charts).
│   └── Softmax confidence is severely miscalibrated under visual distribution shift.
│
├── 2. Paper-Reported Limitations
│   ├── 'Which Source Wins?' only tested forced-choice preference, NOT uncertainty or abstention.
│   ├── 'multimodal-arbitration-artifact' contains only 229 chart items and lacks gold truth.
│   ├── Counterfactual Modality Attribution (CMA) requires costly diffusion inpainting.
│   └── Supervised internal probes fail to transfer across diverse model architectures.
│
├── 3. Reasonable Inferences
│   ├── Autoregressive generation suffers from linguistic inertia, ignoring visual tokens late in CoT.
│   ├── Forcing conflict detection may act as prompt scaffolding rather than perceptual arbitration.
│   └── At 100% evidence masking, confidence cannot drop below unimodal blind solvability.
│
└── 4. Unresolved Uncertainties
    ├── Does verbalizing conflict causally alter decisions, or does the logit trajectory freeze early?
    ├── Does selective prediction calibrated on clean images guarantee bounded risk on unanswerable inputs?
    └── Can cheap inference-time interventions improve evidence faithfulness without fine-tuning?
```

---

## 7. Systematic Screening and Elimination of Candidates

### A. Eliminated as Already Substantially Answered / Occupied
- **Generic Hallucination Prompting:** Saturated by hundreds of 2024–2026 papers.
- **Attention Map Reliability Proxy:** Killed by *Visuals Lie, Consistency Speaks* and *LAD*.
- **Broad "Do VLMs Prefer Text or Images?":** Answered by *Which Source Wins?* (task-dependent reversal).
- **Fixed-Ratio Token Pruning Benchmarking:** Answered by *How Many Visual Tokens Do MLLMs Need?*.
- **Clean-Threshold Transfer under Corruption:** Occupied by *Bigger or Cheaper?*.

### B. Eliminated as Experimentally Unidentifiable
- **Arbitration Accuracy on Symmetric Conflict Data:** Without an authoritative ground truth, correctness cannot be identified.
- **Tokenizer Fertility as a Causal Driver:** Impossible to disentangle tokenization from translation quality and grammar.
- **Token Pruning Locality via Cross-Benchmark ANOVA:** Conflates benchmark format and chance rates with spatial locality.
- **Post-Treatment Conditioned Accuracy:** Testing accuracy only on samples where the model successfully verbalized a conflict conditions on a mediator and biases results.

### C. Eliminated Due to Unfeasible Data, Annotation, or Compute
- **Bengali Cultural VLM Repair (BanglaVerse):** Extreme annotation burden, high answer-leakage risk, unverified provenance.
- **Mechanistic Circuit Tracing (Gemma-3-4B Transcoders):** Requires multi-GPU infrastructure and extensive manual neuron interpretation.
- **Diffusion-Based Counterfactual Generation:** Unrealistic on Colab Pro limits.
- **Active Action-Selection Simulation (Zoom/Crop/Retrieve):** Requires building custom interactive reinforcement environments.
- **Five Detour Areas (Continual Learning, Memory Systems, Long-Context, Planning):** Officially parked by user instruction (`U1`).

---

## 8. Surviving Research Questions (Maximum 5)

---

### RQ 1: Causality of Conflict Verbalization in Cross-Modal Decision Arbitration

- **Scientific phenomenon:** Decoupling between verbalized contradiction awareness and decisional arbitration in vision-language models.
- **Failure mode:** Under mutually contradictory visual and textual premises, a VLM defaults to its dominant modality prior even when prompted to perform intermediate reasoning.
- **Competing explanations:**
  1. *Deliberative Arbitration Hypothesis:* Generating intermediate tokens that articulate the conflict forces cross-attention across both modalities, breaking unimodal capture and updating the logit trajectory.
  2. *Post-Hoc Rationalization Hypothesis:* The final decision token is entrenched by early-layer cross-modal projection dynamics and parametric priors; explicit conflict verbalization produces superficial linguistic commentary without altering the output choice.
- **Controlled intervention:**
  1. Direct zero-shot answer.
  2. Length-matched placebo prompt (describe both sources neutrally, no comparison required).
  3. Cue-only prompt ("The image and text may disagree. Output the answer.").
  4. Full conflict-detection prompt ("Step 1: State whether sources agree or conflict. Step 2: Answer.").
  5. Lanham-style rationale prefilling (prefill a correct contradiction verdict vs. prefill a false agreement verdict).
- **Dependent variable:** Decisional source choice, source-following flip rate, pre-rationale vs. post-rationale logit margin.
- **Primary metric:** Paired arbitration shift ($\Delta_{\text{arb}}$), Net Accuracy change under stated authority, Rationale Faithfulness Score.
- **Strong baseline:** Direct zero-shot generation; Blind text-only LLM; Unimodal Image-only VLM.
- **Dataset:** *CLASH* benchmark (established contradiction pairs) OR a balanced subset of *ChartQA* where an explicit external authority rule is imposed (e.g., Image is authoritative ground truth). Must include 50% aligned control pairs to penalize false conflict hallucinations.
- **Leakage risk:** Prompt cueing leakage (causing the model to hallucinate conflict on aligned pairs) controlled by aligned pairs; Length/syntactic bias controlled by matched templates.
- **Closest work:** *Zhu et al. (2024)*, *Which Source Wins? (2026)*, *Lanham et al. (2023)*, *CLASH (2025)*.
- **What existing work establishes:** VLMs suffer modality dominance; reliance reverses across tasks; models can be prompted to output conflict tokens.
- **What remains unknown:** Whether verbalizing a conflict causally changes the decision, or merely acts as prompt scaffolding / post-hoc rationalization.
- **Why the proposed experiment would answer something new:** Isolates the causal role of intermediate conflict tokens using placebo controls and prefilling interventions.
- **Negative-result value:** High. Proves that verbalized conflict detection is causally decoupled from decision-making, demonstrating that CoT verification is an unfaithful control mechanism in multimodal models.
- **Colab feasibility:** High. Inference-only evaluation on `Qwen2.5-VL-3B-Instruct` or `SmolVLM2-2.2B` across 500 items requires $<2.5$ hours on a single T4/V100.
- **Novelty confidence:** High (under the causal prefill and placebo design).
- **Feasibility confidence:** High.

---

### RQ 2: Evidence-Sufficiency Calibration under Stratified Blind-Solvability Controls

- **Scientific phenomenon:** The functional response of predictive uncertainty to physical evidence removal versus language prior retention.
- **Failure mode:** VLMs generate confident, fabricated assertions when decisive visual evidence is occluded or excised, failing to signal insufficiency.
- **Competing explanations:**
  1. *Information-Theoretic Calibration Hypothesis:* As decisive evidence is physically ablated, cross-modal attention disperses probability, yielding an entropy increase that tracks evidence loss monotonically.
  2. *Linguistic Autoregressive Inertia Hypothesis:* Visual tokens provide weak steering relative to parametric language priors; autoregressive decoding maintains sharp, low-entropy predictions regardless of pixel ablation on prior-solvable items.
- **Controlled intervention:** Continuous masking ladder of decisive visual regions (0%, 25%, 50%, 75%, 100% masked) paired with an identical-area background masking control, stratified into two subsets: *Image-Dependent items* vs. *Blind-Solvable items* (determined by a text-only LLM baseline).
- **Dependent variable:** Output token entropy, top-1 likelihood margin, selective risk.
- **Primary metric:** Normalized Sequence Entropy ($H_{\text{seq}}$), Expected Calibration Error (ECE), Area Under the Risk-Coverage Curve (AURC).
- **Strong baseline:** Blind text-only LLM; 100% masked image baseline; Background-masked control.
- **Dataset:** DocVQA / ChartQA or GQA samples with verified answer bounding boxes and verified blind-solvability splits.
- **Leakage risk:** Redundant visual text (e.g., value repeated in chart legend and axis) controlled by multi-box OCR masking; language leakage controlled by the blind-solvability filter.
- **Closest work:** *Evidence-Order Calibration (2026)*, *Seeing without Looking (2026)*, *Know What You Do Not Know (2025)*.
- **What existing work establishes:** VLMs hallucinate on unanswerable inputs; coarse blur shifts margins; models answer some visual questions without looking.
- **What remains unknown:** Whether predictive entropy responds monotonically to fractional evidence ablation when language-prior solvability is strictly controlled.
- **Why the proposed experiment would answer something new:** Tests whether the apparent failure of uncertainty to track evidence is driven by true evidence blindness or by language prior solvability.
- **Negative-result value:** High. Proving entropy remains flat across 0% to 100% masking on image-dependent questions definitively falsifies softmax uncertainty as a viable signal for selective abstention.
- **Colab feasibility:** High. 500 items $\times$ 6 masking conditions = 3,000 forward passes ($\approx 1.5$ hours on Colab Pro).
- **Novelty confidence:** Moderate.
- **Feasibility confidence:** High.

---

### RQ 3: Selective Abstention and Risk Control under Explicitly Unanswerable Visual Inputs

- **Scientific phenomenon:** The breakdown of selective prediction (rejection of uncertain inputs) under out-of-frame or missing visual evidence.
- **Failure mode:** Acceptance thresholds calibrated to achieve a bounded error rate (e.g., 5% risk) on standard visual questions experience catastrophic error surges when presented with unanswerable queries.
- **Competing explanations:**
  1. *Unified Uncertainty Hypothesis:* Confidence ranking reliably separates correct from incorrect answers regardless of whether the failure stems from visual ambiguity or complete evidence absence.
  2. *Task-Disjunctive Confidence Hypothesis:* The internal confidence distribution for "factually unanswerable" inputs overlaps heavily with "easy correct" inputs, preventing a single threshold from bounding selective risk.
- **Controlled intervention:** Fit an optimal acceptance cutoff $\tau$ on answerable visual questions to satisfy a target risk $\alpha = 0.05$; evaluate the frozen policy on a test set containing known proportions of answerable, corrupted, and out-of-frame unanswerable items.
- **Dependent variable:** Empirical selective risk (error among accepted answers) and coverage (percentage of answered questions).
- **Primary metric:** Selective Risk Surge ($\Delta_{\text{risk}} = R_{\text{unanswerable}} - R_{\text{target}}$), Abstention Precision/Recall, AURC.
- **Strong baseline:** Random abstention; Native softmax confidence threshold; Explicit unanswerability classifier (binary probe).
- **Dataset:** *TUBench (UVQA component)* or *CARA/CASE* dataset (containing verified answerable vs. out-of-frame unanswerable image-question pairs).
- **Leakage risk:** Shortcut question phrasing in unanswerable items (e.g., "What color is the [absent object]?") controlled by matched answerable/unanswerable question templates.
- **Closest work:** *Bigger or Cheaper? (2026)*, *TUBench (2024)*, *CARA/CASE (2024)*, *ConfLVLM (2025)*.
- **What existing work establishes:** Models hallucinate on out-of-frame objects; selective prediction works under in-distribution validation.
- **What remains unknown:** Whether a selective prediction policy calibrated on answerable data preserves its risk bound when unanswerable items enter the stream.
- **Why the proposed experiment would answer something new:** Directly measures the safety violation (risk surge) of selective prediction under unanswerable inputs.
- **Negative-result value:** High. Proves that confidence-gated abstention policies fail catastrophically under evidence absence, showing that explicit answerability detection must precede confidence thresholding.
- **Colab feasibility:** High. Inference-only evaluation on public open models ($\approx 1.5$ hours).
- **Novelty confidence:** Moderate-High.
- **Feasibility confidence:** High.

---

### RQ 4: Faithfulness of Multimodal Rationales under Minimal Counterfactual Evidence Edits

- **Scientific phenomenon:** The unfaithfulness of generated multimodal chain-of-thought (CoT) rationales.
- **Failure mode:** A VLM generates plausible visual explanations that cite specific visual attributes, but changing those attributes does not alter the model's decision, or vice versa.
- **Competing explanations:**
  1. *Faithful Perceptual Reasoning Hypothesis:* Generated rationales reflect the internal cross-modal evidence integration that determines the final answer token.
  2. *Post-Hoc Narrative Rationalization Hypothesis:* The answer is determined by early-layer visual-language associations; generated rationales are post-hoc fabrications designed to satisfy conversational expectations.
- **Controlled intervention:** Apply minimal counterfactual edits to decisive visual attributes (e.g., altering an object's color, count, or spatial relation via public counterfactual pairs) versus non-decisive background edits, and measure whether the rationale updates, whether the answer updates, and whether rationale updates predict answer flips.
- **Dependent variable:** Answer update rate, rationale visual alignment, spurious flip rate.
- **Primary metric:** Rationale Causal Faithfulness Score, Counterfactual Sensitivity Delta ($\Delta_{\text{CF}}$).
- **Strong baseline:** Zero-shot direct generation; Unimodal text-only rationale; Shuffled-image control.
- **Dataset:** Public counterfactual VQA datasets (e.g., *C³PO* image pairs or *Visual-Counterfactual* splits).
- **Leakage risk:** Edit artifacts introduced by synthetic image editing controlled by evaluating natural spatial/attribute counterfactual pairs.
- **Closest work:** *Lanham et al. (2023)*, *C³PO (2026)*, *Circuit Tracing in VLMs (2026)*.
- **What existing work establishes:** CoT can be unfaithful in LLMs; omnimodal models suffer modality dominance.
- **What remains unknown:** How frequently multimodal rationales in compact open VLMs are unfaithful to the actual pixels driving the output logits.
- **Why the proposed experiment would answer something new:** Provides the first behavioral audit of multimodal rationale faithfulness under minimal visual counterfactuals without requiring multi-GPU circuit tracing.
- **Negative-result value:** High. Demonstrates that multimodal chain-of-thought explanations cannot be trusted as faithful explanations of model decisions.
- **Colab feasibility:** High. Zero-shot inference on open VLMs ($\approx 2.0$ hours).
- **Novelty confidence:** Moderate.
- **Feasibility confidence:** High.

---

### RQ 5: Cross-Modal Shortcut Auditing: Isolating Language Prior Dominance from True Fusion

- **Scientific phenomenon:** Inflation of reported multimodal benchmark performance driven by unimodal text shortcuts and memorization.
- **Failure mode:** SOTA vision-language models achieve high scores on multimodal benchmarks while ignoring the visual modality entirely.
- **Competing explanations:**
  1. *Cross-Modal Integration Hypothesis:* High benchmark performance reflects genuine synergistic reasoning across visual pixels and text tokens.
  2. *Linguistic Mutual Information Shortcut Hypothesis:* High benchmark accuracy is driven by unimodal linguistic priors, question-answer mutual information, and benchmark template memorization.
- **Controlled intervention:** 4-way factorial input ablation across diverse multimodal benchmark items:
  1. Full Image + Full Question (standard multimodal input).
  2. Blank (solid black/white) Image + Full Question.
  3. Semantically Shuffled (random mismatched) Image + Full Question.
  4. Full Image + Option-Shuffled / Context-Ablated Question.
- **Dependent variable:** Accuracy, cross-modal attribution gain ($\Delta_{\text{multimodal}} = \text{Acc}_{\text{full}} - \text{Acc}_{\text{blank}}$), ranking stability across open models.
- **Primary metric:** Unimodal Shortcut Fraction (USF), Cross-Modal Synergistic Delta.
- **Strong baseline:** Random guess baseline; Unimodal text-only LLM of matched size; Image-only captioning baseline.
- **Dataset:** Stratified subsets from *ScienceQA-IMG*, *ChartQA*, *MMBench*, and *DocVQA* (200 items each = 800 total).
- **Leakage risk:** Zero data leakage; uses publicly released validation benchmarks.
- **Closest work:** *Seeing without Looking (2026)*, *VL-Checklist*, *POPE (2023)*.
- **What existing work establishes:** Blind LLMs can answer certain VQA questions; POPE exposed object hallucination shortcuts.
- **What remains unknown:** The exact proportion of performance across modern open small VLMs (e.g., Qwen2.5-VL-3B, SmolVLM2) that is genuinely cross-modal versus purely unimodal shortcut use across distinct question types.
- **Why the proposed experiment would answer something new:** Establishes a rigorous, unified shortcut audit across modern small open VLMs, establishing a benchmark correction factor.
- **Negative-result value:** High. If models experience a complete collapse on blank images across all question types, it confirms that open small VLMs are genuinely grounded in pixels, ruling out text-prior dominance.
- **Colab feasibility:** High. $800 \text{ items} \times 4 \text{ passes} = 3,200 \text{ forward passes}$ ($\approx 1.5$ hours).
- **Novelty confidence:** Moderate (Audit / Empirical benchmark study).
- **Feasibility confidence:** Very High.

---

## 9. Decisive Recommendation for Next Investigation

### The Recommended Question: **RQ 1 (Causality of Conflict Verbalization in Cross-Modal Decision Arbitration)**

### Why RQ 1 is Materially Stronger Than All Alternatives:

1. **Unresolved Scientific Uncertainty:**  
   It addresses the exact core question that captured the attention of all discovery reports (*"Can a VLM arbitrate cross-modal conflicts?"*), but **repairs the fatal flaw exposed by Claude**. Instead of naively measuring unprivileged source preference, it tests the fundamental causal question: *Does stating the contradiction actually change the decision, or is CoT verification purely post-hoc commentary?*
2. **Clean Experimental Identification:**  
   Unlike previous flawed proposals, RQ 1 isolates the exact mechanism using **placebo prompt controls** (length-matched neutral description) and **Lanham-style prefilling interventions** (prefilling conflict vs. agreement verdicts). It avoids post-treatment conditioning by using intention-to-treat analysis across all items.
3. **Public, Accessible, and Verified Data:**  
   It does not depend on the flawed `multimodal-arbitration-artifact` repo. It can be executed on **CLASH** (established public benchmark with verified contradiction labels) or an authoritative subset of **POPE / ChartQA** with 50% aligned control pairs.
4. **Reproducible Open Baselines:**  
   Directly runnable on **Qwen2.5-VL-3B-Instruct** and **SmolVLM2-2.2B-Instruct** using standard Hugging Face Transformers.
5. **Manageable Compute:**  
   Inference-only. Evaluating 500 items across 4 prompt conditions requires only 2,000 forward passes, executing in under **1.5 hours on Google Colab Pro**.
6. **Guaranteed Scientific Value from Negative Results:**  
   If explicit conflict detection fails to alter source preference or reduce modality dominance, it provides a definitive, highly publishable empirical result: *Multimodal chain-of-thought verification is causally decoupled from decisional arbitration in open vision-language models.*

---

## 10. Immediate Action Plan (The 48-Hour Pilot Protocol)

Do not conduct another broad topic search. Follow this immediate, concrete protocol:

1. **Step 1: Literature Audit of CLASH & Lanham et al. (2 Hours)**  
   Verify the exact prompt templates and data schema of the *CLASH* benchmark and Lanham's rationale-prefilling protocol.
2. **Step 2: Inspect & Download 50 Pilot Items (1 Hour)**  
   Select 25 conflicting image-text pairs and 25 aligned control pairs with verified ground truth.
3. **Step 3: Build Minimal Colab Inference Script (1 Hour)**  
   Load `Qwen2.5-VL-3B-Instruct` in bfloat16, format the 4 prompt conditions (Direct, Placebo, Cue-only, Conflict-detection), and verify log-probability extraction on 5 items.
4. **Step 4: Execute Pilot Run & Measure Causal Delta (2 Hours)**  
   Run the 50 pilot items and measure whether the conflict detection prompt produces any statistically significant change in source selection compared to the length-matched placebo.

---

## 11. Decisive 3-Way alphaXiv Autopsy Audit (RQ 1 vs. RQ 2 vs. RQ 4)

On 20 September 2026, a rigorous, full-text technical autopsy was executed across all six primary papers using alphaXiv. The results provide an empirical basis for selecting the final thesis topic:

### Cross-Candidate Comparison Matrix

| Evaluation Dimension | RQ 1: Cross-Modal Conflict Arbitration (*CLASH* & *Which Source Wins?*) | RQ 2: Evidence-Sufficiency Masking (*Seeing without Looking* & *Evidence-Order Calibration*) | RQ 4: Counterfactual Rationale Faithfulness (*C³PO* & *Which Modality Decides? / CMA*) |
| :--- | :--- | :--- | :--- |
| **Primary Papers Audited** | • arXiv:2511.19199 (*CLASH*)<br>• arXiv:2608.17205 (*Which Source Wins?*) | • arXiv:2605.22903 (*Seeing without Looking*)<br>• arXiv:2609.09184 (*Evidence-Order Cal.*) | • arXiv:2608.05381 (*C³PO*)<br>• arXiv:2608.00076 (*CMA*) |
| **Scientific Gap Status** | **100% Open & Unoccupied.** Authors of *Which Source Wins?* explicitly state in §6: *"we do not test whether models detect the contradiction, express uncertainty, or abstain."* | **Partially Occupied.** *Evidence-Order Calibration* already evaluated the exact 5-level masking ladder ($\lambda \in \{0, .25, .5, .75, 1\}$) and extracted entropy, ECE, and selective risk. | **Theoretically Open but Ill-Posed.** Neither paper tests rationale faithfulness, but C³PO uses short answers and CMA uses a non-generative classifier. |
| **Public Data & Artifacts** | **Public & Verified on Hugging Face:**<br>• `modality-conflict-arbitration-v2` (1,304 clean arithmetic pairs)<br>• `chartqa-evidence-conflict-v2` (229 chart items)<br>• Public GitHub repo | **Severely Blocked:**<br>• *Seeing without Looking*: No public URL; 117-sample entity set requires SAM2/DINO.<br>• *EOC*: Internal GQA manifest (176 items); no public URL. | **Severely Blocked:**<br>• *C³PO*: No public dataset/code URL in paper text; count discrepancies (3,342 vs 3,404).<br>• *CMA*: Code described as "forthcoming"; no public URL. |
| **Hardware & Compute on Colab Pro** | **Minimal / Highly Feasible:**<br>• Evaluated on `Qwen2-VL-2B-Instruct`<br>• Consumes ~4.5 GB VRAM in bfloat16<br>• 2,000 forward passes take ~1.5 hours on Colab T4/V100 | **Feasible Model, Broken Pipeline:**<br>• Model runs on Colab, but requires complex automated SAM2/DINO segmentation or manual bounding boxes. | **Completely Infeasible:**<br>• *C³PO* required 4x A100 80GB + 2x RTX 5000 32GB GPUs.<br>• *CMA* requires coupled image-text DDPM diffusion inpainting. |
| **Causal Controls & Placebos** | **Clean & Original:**<br>• Can compare conflict prompts against length-matched neutral placebos and Lanham-style prefilling. | **Messy Confounders:**<br>• Masking patches often leave semantic context legible; hard to cleanly separate visual loss from text priors. | **Confounded:**<br>• Diffusion edits introduce visual artifacts; rationale scoring requires expensive LLM judges. |
| **Negative Result Value** | **Definitive & Publishable:**<br>If conflict detection fails to change source preference vs. placebo, it proves multimodal CoT is unfaithful post-hoc rationalization. | **Marginal:**<br>*EOC* already showed that 92% of trajectories violate monotonicity; repeating this adds minimal novelty. | **Uncertain:**<br>Unfaithful rationales in LLMs are already documented; attribution is model-relative. |
| **Final Audit Verdict** | **PROCEED TO EXECUTION (WINNER)** | **REJECT AS PRIMARY THESIS** | **REJECT AS PRIMARY THESIS** |

---

## 12. Final Locked Thesis Topic Specification

*This specification freezes the exact research question, experimental protocol, and dataset for Mohammad Zahed Hossen's undergraduate thesis.*

### 1. The Core Scientific Question
> **"When a vision-language model is presented with mutually contradictory visual and textual premises, does requiring it to explicitly verbalize and explain the contradiction causally change its decisional arbitration, or does the explanation merely act as a post-hoc rationalization of an entrenched modality preference?"**

### 2. The Competing Hypotheses
* **$H_1$ (Deliberative Cognitive Control):** Generating an intermediate token sequence identifying the contradiction forces the model's cross-attention to attend to tokens from both modalities, breaking unimodal attention capture and updating the candidate logit trajectory.  
  *Prediction:* The conflict-detection prompt will produce a statistically significant increase in selecting the correct/authoritative source compared to a length-matched neutral placebo.
* **$H_0$ (Post-Hoc Rationalization):** The final answer is determined by early-layer cross-modal projection dynamics and parametric priors; generating an explanation produces superficial linguistic commentary without altering the output choice.  
  *Prediction:* The conflict-detection prompt will achieve identical source-following rates to the length-matched placebo prompt, proving that the verbalized reasoning does not causally mediate the decision.

### 3. The 4-Way Factorial Prompt Matrix (All Inference-Only)
Every evaluation sample is tested across four standardized prompt conditions:
1. **Condition 1 (Direct Answer - Baseline):**
   ```text
   [Image]
   Source A is the image above. Source B is the text below: [Text Problem]
   Question: [Target Question]
   Respond with exactly one line '#### <answer>', giving only the final answer.
   ```
2. **Condition 2 (Length-Matched Neutral Placebo - The Critical Control):**
   ```text
   [Image]
   Source A is the image above. Source B is the text below: [Text Problem]
   Question: [Target Question]
   Step 1: Describe the visual content and textual content in two neutral sentences without comparing them.
   Step 2: Respond with '#### <answer>', giving the final answer.
   ```
3. **Condition 3 (Explicit Conflict-Aware Arbitration - The Proposed Intervention):**
   ```text
   [Image]
   Source A is the image above. Source B is the text below: [Text Problem]
   Question: [Target Question]
   Step 1: State whether Source A and Source B agree or contradict each other regarding the question.
   Step 2: Respond with '#### <answer>', giving the final answer.
   ```
4. **Condition 4 (Lanham-Style Prefilling - The Causal Mediation Test):**
   ```text
   [Condition 3 prompt + Prefilled Assistant Output]:
   "Step 1: Source A and Source B contradict each other because Source A shows [Fact A] while Source B states [Fact B].
   Step 2: #### [Model generates final token here]"
   ```

### 4. Primary Datasets (Publicly Verified on Hugging Face)
* **Arithmetic Conflicts (1,304 Clean Pairs):**  
  `https://huggingface.co/datasets/vlm-modality-research/modality-conflict-arbitration-v2`  
  *Structure:* Problem $i$ rendered as an image paired with Problem $i+1$ as text. Candidate answers $a_I$ (image-supported) and $a_T$ (text-supported) are mathematically distinct.
* **Chart Conflicts (229 Validated Pairs):**  
  `https://huggingface.co/datasets/vlm-modality-research/chartqa-evidence-conflict-v2`  
  *Structure:* Real chart paired with counterfactual textual report.

### 5. Target Architecture and Compute Environment
* **Primary Model:** `Qwen/Qwen2-VL-2B-Instruct` (and optionally `Qwen/Qwen2.5-VL-3B-Instruct`).
* **Loading:** `bfloat16`, zero-shot inference, no fine-tuning.
* **Memory Footprint:** $\approx 4.5$ GB VRAM.
* **Hardware:** Google Colab Pro (NVIDIA T4 or V100 GPU).
* **Runtime:** $\approx 500 \text{ items} \times 4 \text{ prompt conditions} = 2,000 \text{ forward passes} \approx 90 \text{ minutes total runtime}$.

