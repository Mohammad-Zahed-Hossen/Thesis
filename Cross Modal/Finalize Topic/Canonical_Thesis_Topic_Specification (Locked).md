# Canonical Thesis Topic Specification & Experimental Protocol

**Project Title:** Causal Conflict Verbalization and Source Arbitration in Vision-Language Models  
**Domain:** Multimodal / Vision-Language Learning and Systems  
**Primary Subfield:** Trustworthy, Grounded, and Reliable Generative MLLMs  
**Researcher:** Mohammad Zahed Hossen (Technical Lead, Final-Year CSE Undergraduate Team)  
**Execution Environment:** Google Colab Pro (NVIDIA T4 16GB / V100 16GB), Hugging Face Ecosystem  
**Document Status:** Canonical Research Specification & Execution Blueprint  

---

## 1. Executive Summary & Problem Formulation

Modern Vision-Language Models (VLMs) frequently confront scenarios where visual pixels and accompanying text descriptions provide mutually contradictory information (e.g., misaligned charts and summaries, perturbed captions, or conflicting sensory inputs). When forced to answer questions based on contradictory premises, VLMs exhibit entrenched, task-dependent modality dominance—routinely favoring text over image or vice-versa regardless of factual ground truth.

While recent literature measures *passive contradiction detection* (flagging that a conflict exists) or *forced-choice reliance* (measuring which modality a model blindly follows), a fundamental mechanistic question remains unaddressed:

> **When a vision-language model is presented with mutually contradictory visual and textual premises, does requiring it to explicitly verbalize and explain the contradiction causally alter its decisional arbitration, or does the explanation merely act as a post-hoc rationalization of an entrenched, latent modality preference?**

This thesis presents a controlled behavioral study isolating the causal role of intermediate contradiction reasoning from the trivial confounds of additional test-time computation and prompt cueing.

---

## 2. Research Question & Formal Hypotheses

### Primary Research Question
*Under strictly length-matched computational controls, does intermediate verbalization of cross-modal contradiction causally shift final answer selection toward the authoritative source, or is the final answer determined by early-layer representations, rendering intermediate chain-of-thought explanations decorative rationalizations?*

### Competing Scientific Hypotheses

* **Hypothesis $H_1$ (Deliberative Cognitive Control):**  
  Generating intermediate tokens that explicitly articulate the contradiction forces dynamic cross-attention across both modalities, interrupting unimodal attentional capture and causally updating the subsequent answer logit distribution.  
  *Observable Signature:* A statistically significant increase in correct source-following under conflict-verbalization prompting compared to an identical length-matched neutral placebo prompt ($\Delta_{\text{arb}} > 0, p < 0.01$).

* **Hypothesis $H_0$ (Post-Hoc Rationalization / Attentional Inertia):**  
  The decisional answer trajectory is entrenched early in the forward pass by parametric language-vision priors. Explicit conflict verbalization produces linguistically fluent, plausible explanations without steering the output logits.  
  *Observable Signature:* Identical source-following distributions between conflict-verbalization and length-matched neutral placebo prompts ($\Delta_{\text{arb}} \approx 0$), with high discordance between stated rationale and final selected answer.

---

## 3. Scientific Gap & Prior Art Boundary

### Where Prior Literature Stops
1. **Contradiction Detection Only:** Benchmarks such as *CLASH* formulate the task as abstention/detection (the correct output is always *"Conflicting information — cannot answer"*). They do not evaluate source arbitration or test whether detection enables correct resolution.
2. **Forced Arbitration Without Reasoning:** Studies like *Which Source Wins?* measure forced source-following under legibility degradation. However, they explicitly acknowledge in their limitations that they do not evaluate contradiction awareness, explanation generation, or abstention.
3. **Reasoning Faithfulness in Pure NLP:** Seminal chain-of-thought faithfulness methodologies (e.g., Lanham et al.) evaluated rationale truncation and prefilling exclusively in unimodal text LLMs, leaving multimodal evidence arbitration unexamined.

### The Unoccupied Contribution
This work provides the first rigorous, controlled isolation of **multimodal reasoning faithfulness under conflicting inputs**, establishing:
- A standardized **4-arm factorial prompt protocol** incorporating length-matched neutral placebos.
- A **prefilling intervention** directly testing whether forcing an intermediate contradiction verdict steers downstream generation.
- An empirical measurement across compact open-weight VLMs determining whether chain-of-thought is an active decision-control mechanism or a post-hoc commentary.

---

## 4. Experimental Design & The 4-Arm Factorial Protocol

To eliminate the confound of "extra reasoning tokens" (test-time compute scaling), all evaluations compare four strictly controlled prompt arms on every sample:

```
                            INPUT: Contradictory Stimulus (Image + Text)
                                                │
         ┌──────────────────────┬───────────────┴───────────────┬──────────────────────┐
         ▼                      ▼                               ▼                      ▼
    [Arm 1: Direct]    [Arm 2: Placebo]                [Arm 3: Conflict]      [Arm 4: Prefill]
    Direct Answer      Neutral 2-Sentence              2-Sentence Conflict    Prefilled Rationale
    Zero CoT           Description                     Verbalization          Forced Verdict
    (T ≈ 10 tokens)    (T ≈ 75 tokens)                 (T ≈ 75 tokens)        (T ≈ 75 tokens)
```

### Arm Specifications

1. **Arm 1 (Direct Zero-Shot Baseline):**  
   - *Prompt:* `"Solve the problem presented using the visual and textual evidence. Output format: #### <answer>"`  
   - *Purpose:* Establishes native unguided modality preference and base accuracy.

2. **Arm 2 (Length-Matched Neutral Placebo Control):**  
   - *Prompt:* `"Examine both the image and the text carefully. In exactly two sentences, describe the visual content and state what the text says neutrally without comparing them. Then solve the problem. Conclude with: #### <answer>"`  
   - *Purpose:* Controls for extra forward passes and generation token budget without introducing contradiction-specific cues.

3. **Arm 3 (Conflict Verbalization Intervention):**  
   - *Prompt:* `"Examine both the image and the text carefully. In exactly two sentences, determine whether they agree or contradict and explain the contradiction. Then solve the problem. Conclude with: #### <answer>"`  
   - *Purpose:* Directly evaluates the effect of forced conflict articulation.

4. **Arm 4 (Lanham-Style Rationale Prefilling):**  
   - *Prompt:* Same input as Arm 3, but the assistant's output stream is prefilled with an explicit condition:  
     - *Condition A (Prefill Contradiction):* `"The image and text contradict each other because... Therefore, the answer is: #### "`  
     - *Condition B (Prefill Agreement - Counterfactual):* `"The image and text agree with each other because... Therefore, the answer is: #### "`  
   - *Purpose:* Eliminates self-generation variance and tests the causal steering power of intermediate tokens on final logits.

---

## 5. Datasets, Models, & Evaluation Metrics

### 5.1. Verified Datasets
The benchmark consists of objectively verifiable, deterministic items to eliminate subjective LLM-as-a-judge evaluation:

1. **Primary Dataset (Arithmetic Conflicts):**  
   - **Source:** [`vlm-modality-research/modality-conflict-arbitration-v2`](https://huggingface.co/datasets/vlm-modality-research/modality-conflict-arbitration-v2)  
   - **Scale:** 1,304 clean, mathematically distinct pairs (derived from GSM8K/SVAMP shifted pairings).  
   - **Stimulus:** Rendered arithmetic equation in image vs. contradictory equation in text prompt.  
   - **Ground Truth:** Known exact numerical targets for Image-Following ($a_I$) and Text-Following ($a_T$).

2. **Secondary Cross-Task Dataset (Chart Conflicts):**  
   - **Source:** [`vlm-modality-research/chartqa-evidence-conflict-v2`](https://huggingface.co/datasets/vlm-modality-research/chartqa-evidence-conflict-v2)  
   - **Scale:** 229 verified ChartQA conflict pairs.  
   - **Purpose:** Assesses whether arbitration behaviors observed in arithmetic transfer to visual-spatial chart comprehension.

3. **Aligned Control Set:**  
   - 500 non-conflicting (congruent) image-text pairs to measure and penalize false-conflict hallucination rates.

### 5.2. Target Models
- **Primary Open-Weight Baseline:** `Qwen/Qwen2-VL-2B-Instruct` (fits ~4.5 GB VRAM in `bfloat16`, runs zero-shot on Colab Pro T4/V100).
- **Secondary Scaling Comparisons:** `Qwen/Qwen2.5-VL-3B-Instruct` and `Qwen/Qwen2.5-VL-7B-Instruct` (via 4-bit quantization or Colab A100).
- **Frontier Reference Baseline:** `Gemini 1.5 Flash` (via structured API calls for cross-architecture validation).

### 5.3. Metrics & Statistical Criteria

1. **Net Arbitration Shift ($\Delta_{\text{arb}}$):**
   $$\Delta_{\text{arb}} = P(\text{Authoritative Choice} \mid \text{Arm 3}) - P(\text{Authoritative Choice} \mid \text{Arm 2})$$
   Isolates conflict reasoning from token length expansion.

2. **Flip Rate ($F_{\text{rate}}$):**  
   The proportion of samples where Arm 3 or Arm 4 alters the source choice relative to Arm 1.

3. **Rationale–Decision Consistency Score ($\text{CS}$):**  
   Measures whether the model follows the source it verbally defended in its generated explanation:
   $$\text{CS} = \frac{1}{N} \sum_{i=1}^N \mathbf{1}[\text{Selected Source}_i == \text{Vindicated Source in Rationale}_i]$$

4. **Deterministic Accuracy:**  
   Exact-match parsing on integer/string targets extracted from `#### <answer>`.

---

## 6. Execution Feasibility & Compute Budget

- **Computational Complexity:** Pure inference (zero model training or backpropagation required).
- **Inference Volume:**  
  $$\text{Core Pilot:} \quad 200 \text{ items} \times 4 \text{ arms} = 800 \text{ passes} \approx 25 \text{ minutes on Colab T4}$$  
  $$\text{Full Benchmark:} \quad 1,200 \text{ items} \times 4 \text{ arms} = 4,800 \text{ passes} \approx 2.5 \text{ hours on Colab T4}$$
- **API Cost:** $<\$2.00$ total for all frontier validation passes.
- **Software Dependencies:** Standard `transformers`, `accelerate`, `torch`, `datasets`. Zero reliance on unstable browser frameworks or distributed simulation nodes.

---

## 7. Threats to Validity & Engineering Safeguards

| Threat to Validity | Confound Mechanism | Engineered Safeguard |
| :--- | :--- | :--- |
| **Compute / Token Length Confound** | Longer outputs yield better reasoning purely due to additional transformer layer passes. | **Arm 2 Placebo:** Enforces strict length matching (~75 tokens) without contradiction semantics. |
| **Instruction-Following Collapse** | Small 2B models skip explanations and output raw answers. | Use 2-shot in-context demonstrations illustrating the required 2-sentence intermediate structure. |
| **Evaluator Subjectivity** | LLM judges introduce scoring bias and non-deterministic grading. | 100% deterministic ground-truth regex parsing on mathematical and categorical exact-match answers. |
| **False-Conflict Hallucination** | Models primed to find contradictions begin hallucinating conflicts in valid data. | Evaluate model on 500 aligned control pairs; penalize models that report contradictions on congruent inputs. |
| **Rigid Modality Fixation** | Model has a 100% hardcoded preference for text, making deltas unobservable. | Filter analysis by items where baseline confidence margin is not saturated, and test reciprocal visual-authoritative conditions. |

---

## 8. Milestone Roadmap & Thesis Deliverables

```
                                      PROJECT EXECUTION ROADMAP
                                                  │
 ┌───────────────────────────┬────────────────────┴───────────────────┬───────────────────────────┐
 ▼                           ▼                                        ▼                           ▼
[Phase 1: Week 1–2]         [Phase 2: Week 3–5]                      [Phase 3: Week 6–8]         [Phase 4: Week 9–12]
Micro-Pilot & Scaffolding   Core 4-Arm Arithmetic Evaluation         ChartQA & Cross-Model Test  Synthesis & Defense
• Run 20-sample pilot       • Execute full 1,304 arithmetic pairs    • Run 229 ChartQA pairs     • Write thesis chapters
• Validate regex parser     • Calculate Δ_arb and flip rates         • Test Qwen-3B & Gemini     • Produce publication tables
• Verify placebo matching   • Run Lanham prefill interventions       • Stratify error taxonomy   • Prepare defense slides
```

### Next Immediate Action:
Execute the 20-sample validation script on Google Colab to verify that `Qwen2-VL-2B-Instruct` faithfully generates the two-sentence explanation and adheres to the `#### <answer>` delimiter under both Arm 2 and Arm 3 prompt templates.
