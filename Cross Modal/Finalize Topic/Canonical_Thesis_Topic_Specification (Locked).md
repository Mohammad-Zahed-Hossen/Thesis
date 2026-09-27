# Canonical Thesis Topic Specification & Experimental Protocol (Locked)

**Project Title:** Causal Conflict Verbalization and Source Arbitration in Vision-Language Models  
**Domain:** Multimodal / Vision-Language Learning and Systems  
**Primary Subfield:** Trustworthy, Grounded, and Reliable Generative Multimodal LLMs  
**Principal Researcher:** Mohammad Zahed Hossen (Technical Lead, Final-Year BSc CSE)  
**Reference Model:** `Qwen/Qwen2.5-VL-3B-Instruct` (36 Layers, Hidden Size 2048, 16 Heads)  
**Primary Benchmark:** `vlm-modality-research/modality-conflict-arbitration-v2` ($N = 1,619$ pristine conflict pairs)  
**Execution Environment:** Google Colab Pro (NVIDIA T4 / V100 16GB VRAM, CUDA 13.0, PyTorch 2.x SDPA, FP16 Tensor Cores)  
**Status:** **FROZEN & EMPIRICALLY CONFIRMED ACROSS FULL POPULATION CENSUS ($N = 1,619$)**  

---

## 1. Executive Summary & Problem Formulation

Modern Vision-Language Models (VLMs) routinely process multimodal inputs where information presented across modalities is mutually contradictory. When a model is confronted with conflicting premises, its output choice reflects source arbitration: deciding which input channel to follow, synthesize, or reject.

Prior literature has investigated *passive contradiction detection* (classifying whether a conflict exists, e.g., *CLASH*) or *forced-choice reliance under sensory degradation* (measuring which modality dominates when visual clarity is corrupted, e.g., *Which Source Wins?*). However, prior benchmarks explicitly leave open whether requiring a model to detect and reason about a contradiction causally alters its subsequent decision arbitration or merely rationalizes an entrenched modality bias.

In this thesis, we investigate this question through a controlled, 4-arm causal factorial intervention on the open-weight vision-language model `Qwen2.5-VL-3B-Instruct`. Evaluating across the complete census of $N = 1,619$ clean conflict pairs in `vlm-modality-research/modality-conflict-arbitration-v2`, we observe that source arbitration is governed by a **Prompt-Arbitration Triad**:

1. **Direct Zero-Shot Prompting (Arm 1):** Produces overwhelming reliance on the text modality (**85.5%** follows text, **13.8%** follows image).
2. **Neutral Placebo Description (Arm 2):** Prompting the model to neutrally describe both the image and text in two sentences induces dramatic **visual capture** (**89.5%** follows image, **9.0%** follows text).
3. **Conflict Verbalization & Reliability Directive (Arm 3):** Requiring the model to explicitly evaluate contradiction and source reliability breaks visual capture (**25.8%** follows image, **58.9%** follows text, and **13.7%** deliberatively abstains).

This produces a **net causal arbitration shift of $\Delta_{\text{arb}} = +63.74\text{ percentage points}$** ($p = 1.20 \times 10^{-215}, OR = 24.57$, Cohen's $h = 1.42$), mirrored by an exact-match mathematical problem-solving inversion ($35.6\%$ Img / $4.7\%$ Txt in Arm 2 $\rightarrow$ $11.7\%$ Img / $35.8\%$ Txt in Arm 3).

---

## 2. Research Questions & Formal Hypotheses

### Primary Research Question
* **RQ1 (Core):** *When a vision-language model receives contradictory visual and textual problems, does an explicit conflict-verbalization intervention causally change its subsequent source arbitration compared with a neutral verbalization control?*

### Secondary Research Questions
* **RQ2 (Arbitration Magnitude):** How much does conflict verbalization reduce visual capture relative to a length-matched neutral placebo?  
  $$\Delta_{\text{visual}} = P(\text{visual}\mid \text{Arm 2}) - P(\text{visual}\mid \text{Arm 3}) = 89.50\% - 25.76\% = +63.74\text{ pp}$$
* **RQ3 (Source-Execution Validity):** Does the shift in categorical source selection correspond to observable execution of the selected problem's ground-truth mathematical answer, rather than superficial labeling drift?
* **RQ4 (Contradiction-Conditioned Abstention):** Does explicit conflict verbalization prompt the model to spontaneously abstain from answering contradictory premises ($13.65\%$ in Arm 3 vs. $0.25\%$ in Arm 2)?
* **RQ5 (Within-Item Transition Dynamics):** How do individual items migrate across behavioral states (visual-following, text-following, abstention, ambiguity) when transitioning from the neutral control to the conflict intervention?
* **RQ6 (Intervention Resistance & Prefill Steering):** Which items remain resistant to verbalization (the $27.05\%$ persistent visual cases), and how does short rationale prefilling compare with the full conflict-verbalization intervention?

### Formal Competing Hypotheses
* **Hypothesis $H_1$ (Causal Behavioral Steering):**  
  Requiring intermediate contradiction evaluation and source-reliability assessment causally redirects downstream generation, significantly shifting source selection away from the default visual capture state observed under neutral description.  
  *Observable Signature:* A statistically significant within-subject reduction in visual capture ($\Delta_{\text{visual}} > 0$, McNemar $p < 0.001$), accompanied by an inversion in exact-match ground-truth agreement toward the competing text problem.
* **Hypothesis $H_0$ (Post-Hoc Rationalization / Attentional Inertia):**  
  Source selection is entrenched prior to intermediate reasoning. Intermediate verbalization generates fluent commentary without causally altering downstream source selection.  
  *Observable Signature:* Invariant source distributions between neutral placebo and conflict verbalization ($\Delta_{\text{visual}} \approx 0$), with high discordance between stated rationale and final extracted answer.

---

## 3. Scientific Gap & Prior Art Boundary

### Where Prior Literature Stops
1. **Absence of Verbalized Contradiction in Multimodal Arbitration:**  
   *Which Source Wins? Task-Dependent Reliance in Vision-Language Models* (Ghosh, Gupta, & Wang, arXiv:2608.17205, August 2026) systematically mapped source reliance across degradation regimes, but explicitly left open the role of intermediate verbalization in Section 5 (Limitations):  
   > *"Consequently, we do not test whether models detect the contradiction, express uncertainty, or abstain."*
2. **Abstention-Only Formulation Without Source Arbitration:**  
   Benchmarks such as *CLASH* (arXiv:2511.19199) evaluate whether models detect contradiction, but formulate correct behavior exclusively as refusal/abstention (*"Cannot answer due to conflict"*), failing to measure how models arbitrate between competing premises when forced to resolve them.
3. **Unimodal Confinement of CoT Faithfulness Literature:**  
   Foundational chain-of-thought faithfulness methodologies (Lanham et al., arXiv:2307.13702; Turpin et al., arXiv:2305.04388) developed rationale truncation and prefilling exclusively on text-only LLMs. Multimodal source arbitration under cross-modal conflict remained unexamined.

### The Unoccupied Contribution
This work provides the first controlled factorial evaluation of intermediate conflict verbalization on multimodal source arbitration, establishing:
- A standardized **4-arm factorial protocol** with length-matched neutral placebos.
- A **full-population census ($N = 1,619$)** on pristine, uncorrupted conflict pairs.
- Dual-track validation combining **entity-based source tracking** and **deterministic ground-truth integer exact match**.
- Characterization of **contradiction-conditioned abstention** ($13.7\%$) and **persistent visual capture** ($27.1\%$).

---

## 4. Experimental Design & The 4-Arm Factorial Protocol

To eliminate the confound of test-time token budget expansion, all evaluations compare four strictly controlled prompt conditions evaluated on every item:

```
                            INPUT: Contradictory Stimulus
               Image: Rendered Problem A  |  Text: Conflicting Problem B
                                          │
         ┌────────────────────────────────┼────────────────────────────────┐
         ▼                                ▼                                ▼
   [Arm 1: Direct]               [Arm 2: Placebo]                [Arm 3: Conflict]
   Unprompted Solve              Neutral 2-Sentence              2-Sentence Conflict
   No CoT Preamble               Description Preamble            & Reliability Directive
   Budget: 80 tokens             Budget: 200 tokens              Budget: 200 tokens
   Observed: 85.5% Text          Observed: 89.5% Image           Observed: 58.9% Text, 13.7% Abstain
                                          │
                                          ▼
                                 [Arm 4: Prefill Probe]
                         4a: Prefill Contradiction (Forced Image)
                         4b: Prefill Agreement (Forced Text)
                         Budget: 20 tokens | Observed: 58.6% Invariant
```

### Exact Literal Prompt Specifications (Frozen Protocol)

The experimental protocol utilizes the exact prompt strings executed in `Pilot/production_experiment_harness_v3.py`:

```python
# Arm 1: Direct Zero-Shot Baseline
PROMPT_ARM1_DIRECT = (
    "Look at the image and read the text problem below.\n"
    "{text_question}\n\n"
    "Solve the problem. Conclude with: #### <answer>\n"
)

# Arm 2: Length-Matched Neutral Placebo Control
PROMPT_ARM2_PLACEBO = (
    "Look at the image and read the text problem below.\n"
    "{text_question}\n\n"
    "In two sentences, neutrally describe what is presented in the image and what is stated in the text without comparing them. "
    "Then solve the problem. Conclude with: #### <answer>\n"
)

# Arm 3: Conflict Verbalization Intervention
PROMPT_ARM3_CONFLICT = (
    "Look at the image and read the text problem below.\n"
    "{text_question}\n\n"
    "In two sentences, state whether the image and the text agree or contradict each other, and explain which source you consider more reliable. "
    "Then solve that problem. Conclude with: #### <answer>\n"
)

# Arm 4a: Rationale Prefill (Forced Image Direction)
PREFILL_ARM4_CONTRADICTION = (
    "The image and text contradict each other because they present different problems. "
    "Following the image problem, the answer is: #### "
)

# Arm 4b: Rationale Prefill (Forced Text Direction)
PREFILL_ARM4_AGREEMENT = (
    "The image and text describe consistent premises. "
    "Following the text problem, the answer is: #### "
)
```

### Methodological Nature of the Arm 3 Intervention
Arm 3 is a **compound prompt intervention** consisting of two explicit components:
1. Contradiction evaluation (*"state whether the image and the text agree or contradict each other"*).
2. Source-reliability arbitration directive (*"explain which source you consider more reliable. Then solve that problem."*).

The causal contrast between Arm 2 and Arm 3 isolates the effect of this evaluative and directive structure from the general effect of generating a two-sentence descriptive preamble.

---

## 5. Dataset Construct & Reverse-Engineering

### Dataset Specification
* **Repository:** [`vlm-modality-research/modality-conflict-arbitration-v2`](https://huggingface.co/datasets/vlm-modality-research/modality-conflict-arbitration-v2)
* **Underlying Origin:** Clean mathematical word problems from GSM8K ($1,319$ pairs) and SVAMP ($300$ pairs).
* **Target Cohort:** `channel = image`, `degradation_level = 0` ($N = 1,619$ items).

### Experimental Construct & Scope Boundary
* **Image Stimulus:** A 900-pixel rendered PNG screenshot displaying an arithmetic word problem in standard typography (DejaVu Sans).
* **Text Stimulus:** A distinct, syntactically similar but mathematically disjoint arithmetic word problem supplied directly in the prompt text.
* **Ground Truth:** Deterministic, unique ground-truth numerical solutions for the image problem ($a_I$) and text problem ($a_T$), where $a_I \neq a_T$.
* **Construct Scope:** The dataset measures source arbitration between **rendered typographical text** in an image and **direct textual prompt input**. It does not evaluate conflicts between natural photographic scenes and captions.

---

## 6. Empirical Findings ($N = 1,619$ Full Population Census)

### Primary Population Contingency Matrix

| Experimental Condition | Follows Image | Follows Text | Abstains | Ambiguous |
| :--- | :---: | :---: | :---: | :---: |
| **Arm 1: Direct Zero-Shot** | $223$ ($13.77\%$) | $1,385$ ($85.55\%$) | $0$ ($0.00\%$) | $11$ ($0.68\%$) |
| **Arm 2: Placebo (Neutral Control)** | $1,449$ ($89.50\%$) | $145$ ($8.96\%$) | $4$ ($0.25\%$) | $21$ ($1.30\%$) |
| **Arm 3: Conflict Verbalization** | $417$ ($25.76\%$) | $954$ ($58.93\%$) | $221$ ($13.65\%$) | $27$ ($1.67\%$) |

### Primary Statistical Inferences (Arm 2 vs. Arm 3)
* **Net Visual Capture Reduction ($\Delta_{\text{visual}}$):** $+63.74\text{ percentage points}$ ($89.50\% \rightarrow 25.76\%$)
* **McNemar's Paired Within-Item Test:** $\chi^2_{\text{McNemar}} = 982.40$ ($b = 1057, c = 25, p = 1.20 \times 10^{-215}$)
* **Odds Ratio ($OR$):** $24.57$ [$95\%$ CI: $20.24, 29.83$] (Paired Discordant $OR = 42.28$ [$28.46, 62.81$])
* **Cohen's $h$ Effect Size:** $1.417$ ("Very Large" effect; standard threshold $> 0.8$)
* **Relative Risk ($RR$):** $0.2878$ ($71.22\%$ relative reduction in visual capture risk)

### Source-Conditioned Exact-Match Cross-Over
Evaluating agreement between the extracted answer and ground-truth values confirms that the model actually executes the selected problem:
* **Arm 2 (Placebo):** Image Problem Match = **$35.64\%$** ($577 / 1,619$), Text Problem Match = **$4.69\%$** ($76 / 1,619$).
* **Arm 3 (Conflict):** Text Problem Match surges to **$35.76\%$** ($579 / 1,619$), Image Problem Match collapses to **$11.74\%$** ($190 / 1,619$).

### Within-Subject State Transitions of the 1,449 Visual Capture Cases
* **Flipped to Text Problem:** $832$ items ($57.41\%$)
* **Transitioned to Epistemic Abstention:** $201$ items ($13.87\%$)
* **Persisted in Visual Capture (Resistant Cases):** $392$ items ($27.05\%$)
* **Ambiguous / Unresolved:** $24$ items ($1.66\%$)

### Exploratory Rationale Prefill Findings (Arm 4)
* **Response Invariance:** $58.55\%$ of items ($948 / 1,619$) produced identical numerical answers under diametrically opposing prefills.
* **Text Steering Boost:** Arm 4b yielded only a $+5.31\text{ pp}$ increase in text-problem alignment over Arm 4a ($21.12\%$ vs. $15.81\%$).
* **Conclusion:** Short rationale prefilling provides a weak causal lever for complex multi-step reasoning compared with the full conflict-verbalization prompt.

---

## 7. Threats to Validity & Engineered Controls

| Threat to Validity | Confound Mechanism | Engineered Safeguard | Empirical Verification |
| :--- | :--- | :--- | :--- |
| **Test-Time Compute Confound** | Extra reasoning tokens improve accuracy via additional forward passes. | **Arm 2 Placebo:** Enforces length-matched 2-sentence description without evaluative semantics. | Tokens: Arm 2 avg ~86 tok, Arm 3 avg ~90 tok. |
| **Token Budget Truncation** | 200-token ceiling curtails multi-step scratchpads. | **Sensitivity Split:** Stratified analysis across non-truncated vs. truncated cohorts. | Visual reduction is identical: Non-truncated = $-65.0\text{ pp}$, Truncated = $-61.5\text{ pp}$. |
| **Evaluator Scoring Bias** | LLM-as-a-judge introduces non-deterministic bias. | **Deterministic Dual-Track:** Entity keyword regex extraction + integer exact match. | $100\%$ reproducible, zero uncalibrated LLM grading. |
| **Few-Shot Demonstration Bias** | ICL examples steer arbitration toward demonstrated modality. | **Zero-Shot Protocol:** Strict instruction templates without few-shot examples. | Verified in Pilot 2 post-mortem. |

---

## 8. Epistemic & Methodological Boundaries

### Supported Claims
- Explicit conflict verbalization and reliability prompting causally alters observable source-selection behavior in `Qwen2.5-VL-3B-Instruct` ($\Delta = +63.74\text{ pp}, p < 10^{-215}$).
- Source selection corresponds to genuine execution of the selected problem's arithmetic steps (verified by exact-match cross-over).
- Conflict verbalization induces explicit abstention on contradictory inputs in $13.7\%$ of cases.
- The arbitration shift is robust to token truncation.

### Out of Scope & Prohibited Overclaims
- **No Claims of Internal Attention Rerouting:** We did not perform layer-wise attention weight extraction or mechanistic circuit tracing. The finding is behavioral and prompt-conditioned.
- **No Claims of an "Entrenched Visual Prior":** Arm 1 demonstrates that the model defaults to text ($85.5\%$) under unprompted direct conditions. Visual capture is induced by the descriptive preamble (Arm 2, $89.5\%$) and broken by conflict verbalization (Arm 3, $25.8\%$).
- **No Generalization to Natural Photographs:** The dataset consists of rendered typographical word problems. Transfer to natural imagery, chart diagrams, or video inputs is unverified.
- **No Universal Claim of CoT Faithfulness:** Rationale prefilling (Arm 4) demonstrated that short rationales fail to steer the majority of items ($58.6\%$ invariant).

---

## 9. Thesis Manuscript Structure & Defense Alignment

1. **Chapter 1 (Introduction):** Multimodal conflict problem, Prompt-Arbitration Triad, RQ1–RQ6, formal hypotheses, 5 core contributions.
2. **Chapter 2 (Related Work):** Modality reliance benchmarks (*Which Source Wins?*, *CLASH*), unimodal CoT faithfulness (Lanham et al., Turpin et al.), open gap.
3. **Chapter 3 (Methodology):** Dataset provenance ($N = 1,619$), 4-arm factorial design, exact prompt specifications, harness engineering (SDPA, FP16, CUDA 13 fix), evaluation metrics.
4. **Chapter 4 (Results):** Primary $\Delta_{\text{arb}}$ shift, exact-match cross-over, $4 \times 4$ transition matrix, truncation sensitivity analysis, Arm 4 prefill findings.
5. **Chapter 5 (Discussion & Conclusion):** Prompt-conditioned arbitration mechanisms, epistemic abstention, resistant case analysis, explicit limitations, future mechanistic directions.
